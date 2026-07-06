"""
build_docs_db.py
================
One-time script that reads all plant documents from the "RAG docs/" directory,
chunks them by H2 section, embeds each chunk using the BGE-small retrieval model,
and stores everything in a ChromaDB vector database.

Usage:
    python build_docs_db.py             # Incremental upsert (safe to re-run)
    python build_docs_db.py --rebuild   # Wipe and rebuild from scratch

On first run, the BGE model (~130 MB) is downloaded automatically from HuggingFace
and cached locally. No internet needed after that.
"""

import os
import sys
import re
import yaml
import json
import argparse
from pathlib import Path

# ── Paths ────────────────────────────────────────────────────────────────────
PROJECT_DIR = Path(__file__).parent
DOCS_DIR    = PROJECT_DIR / "RAG docs"
DB_DIR      = PROJECT_DIR / "rag_vector_db"
COLLECTION  = "plant_docs"
MODEL_NAME  = "BAAI/bge-small-en-v1.5"

# BGE models perform best when the query is prefixed — we use the same prefix
# at query time (in rag_tools.py) to keep embeddings aligned.
EMBED_PREFIX = "Represent this sentence for searching relevant passages: "

# Chunking thresholds
MIN_CHUNK_TOKENS  = 50    # merge sections shorter than this with the next
MAX_CHUNK_TOKENS  = 800   # split sections longer than this at H3 / paragraph


# ── Front-matter parser ───────────────────────────────────────────────────────

def parse_front_matter(text: str) -> tuple[dict, str]:
    """
    Split a markdown file into (metadata_dict, body_text).
    Returns ({}, full_text) if no YAML front matter block is found.
    """
    if not text.startswith("---"):
        return {}, text
    end = text.find("\n---", 3)
    if end == -1:
        return {}, text
    yaml_block = text[3:end].strip()
    body = text[end + 4:].lstrip("\n")
    try:
        meta = yaml.safe_load(yaml_block) or {}
    except yaml.YAMLError:
        meta = {}
    return meta, body


# ── Tokeniser (approximate) ───────────────────────────────────────────────────

def approx_tokens(text: str) -> int:
    """Rough token count: ~0.75 tokens per word (good enough for chunking decisions)."""
    return int(len(text.split()) * 0.75)


# ── Chunker ───────────────────────────────────────────────────────────────────

def chunk_document(title: str, body: str) -> list[dict]:
    """
    Split a document body into chunks at H2 headings.
    Each chunk gets:
      - section_title: the H2 heading text (or "Introduction" for pre-H2 content)
      - text: the raw section text
      - prefixed_text: title-prefixed version used for embedding
      - chunk_index: position within the document
    """
    # Split at H2 boundaries — keep the heading with its content
    raw_sections = re.split(r"(?=^## )", body, flags=re.MULTILINE)

    sections = []
    for sec in raw_sections:
        sec = sec.strip()
        if not sec:
            continue
        m = re.match(r"^## (.+)", sec)
        heading = m.group(1).strip() if m else "Introduction"
        content = sec[m.end():].strip() if m else sec
        sections.append((heading, content))

    # Merge micro-sections into their successor
    merged: list[tuple[str, str]] = []
    i = 0
    while i < len(sections):
        heading, content = sections[i]
        # If too short and there's a next section to absorb it into, merge forward
        if approx_tokens(content) < MIN_CHUNK_TOKENS and i + 1 < len(sections):
            next_heading, next_content = sections[i + 1]
            sections[i + 1] = (heading + " / " + next_heading, content + "\n\n" + next_content)
            i += 1
            continue
        merged.append((heading, content))
        i += 1

    # Split sections that are too long at H3 boundaries or double-newlines
    final: list[tuple[str, str]] = []
    for heading, content in merged:
        if approx_tokens(content) <= MAX_CHUNK_TOKENS:
            final.append((heading, content))
            continue
        # Try H3 split first
        h3_parts = re.split(r"(?=^### )", content, flags=re.MULTILINE)
        if len(h3_parts) > 1:
            for part in h3_parts:
                part = part.strip()
                if not part:
                    continue
                h3m = re.match(r"^### (.+)", part)
                subheading = (heading + " › " + h3m.group(1).strip()) if h3m else heading
                subcontent = part[h3m.end():].strip() if h3m else part
                final.append((subheading, subcontent))
        else:
            # Fall back to paragraph splits
            paragraphs = [p.strip() for p in content.split("\n\n") if p.strip()]
            current_heading = heading
            buffer: list[str] = []
            part_idx = 0
            for para in paragraphs:
                buffer.append(para)
                if approx_tokens("\n\n".join(buffer)) >= MAX_CHUNK_TOKENS:
                    chunk_heading = current_heading if part_idx == 0 else f"{heading} (cont.)"
                    final.append((chunk_heading, "\n\n".join(buffer)))
                    buffer = []
                    part_idx += 1
            if buffer:
                chunk_heading = current_heading if part_idx == 0 else f"{heading} (cont.)"
                final.append((chunk_heading, "\n\n".join(buffer)))

    # Build output chunk dicts with context prefix for embedding
    chunks = []
    for idx, (sec_title, sec_text) in enumerate(final):
        prefixed = f"{title}: {sec_title} — {sec_text}"
        chunks.append({
            "section_title": sec_title,
            "text": sec_text,
            "prefixed_text": prefixed,
            "chunk_index": idx,
        })
    return chunks


# ── Document loader ───────────────────────────────────────────────────────────

def load_all_documents() -> list[dict]:
    """
    Walk DOCS_DIR, parse every .md file with valid front matter.
    Returns a list of document dicts ready for chunking.
    """
    docs = []
    for md_path in sorted(DOCS_DIR.rglob("*.md")):
        text = md_path.read_text(encoding="utf-8")
        meta, body = parse_front_matter(text)
        if not meta.get("doc_id"):
            print(f"  [SKIP] {md_path.name} — no front matter / doc_id")
            continue
        docs.append({
            "path": md_path,
            "doc_id":   str(meta.get("doc_id", "")),
            "doc_type": str(meta.get("doc_type", "unknown")),
            "title":    str(meta.get("title", md_path.stem)),
            "revision": str(meta.get("revision", "1.0")),
            # equipment and tags are lists in the YAML; store as comma-joined for ChromaDB
            "equipment": ", ".join(str(e) for e in (meta.get("equipment") or [])),
            "tags":      ", ".join(str(t) for t in (meta.get("tags") or [])),
            "body": body,
        })
    return docs


# ── Main build ────────────────────────────────────────────────────────────────

def build(rebuild: bool = False) -> None:
    import chromadb
    from sentence_transformers import SentenceTransformer

    print(f"\n{'='*60}")
    print("Boiler Historian — Plant Document RAG Builder")
    print(f"{'='*60}")
    print(f"Docs dir  : {DOCS_DIR}")
    print(f"DB dir    : {DB_DIR}")
    print(f"Model     : {MODEL_NAME}")
    print(f"Mode      : {'REBUILD (wipe + re-index)' if rebuild else 'UPSERT (incremental)'}")
    print()

    # ── 1. Load documents ─────────────────────────────────────────────────────
    print("Step 1/4 — Loading documents...")
    docs = load_all_documents()
    print(f"  Found {len(docs)} documents with valid front matter")

    # ── 2. Chunk ──────────────────────────────────────────────────────────────
    print("Step 2/4 — Chunking documents...")
    all_chunks: list[dict] = []
    for doc in docs:
        chunks = chunk_document(doc["title"], doc["body"])
        for c in chunks:
            c.update({
                "doc_id":   doc["doc_id"],
                "doc_type": doc["doc_type"],
                "title":    doc["title"],
                "revision": doc["revision"],
                "equipment": doc["equipment"],
                "tags":      doc["tags"],
                "source_path": str(doc["path"].relative_to(PROJECT_DIR)),
            })
        all_chunks.extend(chunks)
        print(f"  {doc['doc_id']}: {len(chunks)} chunks")

    total_chars = sum(len(c["text"]) for c in all_chunks)
    print(f"\n  Total: {len(all_chunks)} chunks across {len(docs)} documents")
    print(f"  Total text: {total_chars:,} characters")

    # ── 3. Embed ──────────────────────────────────────────────────────────────
    print(f"\nStep 3/4 — Loading embedding model ({MODEL_NAME})...")
    print("  (First run downloads ~130MB — subsequent runs use local cache)")
    model = SentenceTransformer(MODEL_NAME)

    texts_to_embed = [c["prefixed_text"] for c in all_chunks]
    print(f"  Embedding {len(texts_to_embed)} chunks...")
    # normalize_embeddings=True is recommended for BGE models (cosine similarity)
    embeddings = model.encode(
        texts_to_embed,
        normalize_embeddings=True,
        show_progress_bar=True,
        batch_size=64,
    )
    print(f"  Embedding shape: {embeddings.shape}")

    # ── 4. Store in ChromaDB ──────────────────────────────────────────────────
    print(f"\nStep 4/4 — Storing in ChromaDB at {DB_DIR}...")
    DB_DIR.mkdir(parents=True, exist_ok=True)
    client = chromadb.PersistentClient(path=str(DB_DIR))

    if rebuild:
        try:
            client.delete_collection(COLLECTION)
            print(f"  Deleted existing collection '{COLLECTION}'")
        except Exception:
            pass

    collection = client.get_or_create_collection(
        name=COLLECTION,
        metadata={"hnsw:space": "cosine"},  # BGE embeddings use cosine distance
    )

    # Upsert in batches of 100 (ChromaDB recommendation)
    batch_size = 100
    total_upserted = 0
    for i in range(0, len(all_chunks), batch_size):
        batch = all_chunks[i : i + batch_size]
        batch_embeddings = embeddings[i : i + batch_size]

        ids        = [f"{c['doc_id']}_chunk_{c['chunk_index']}" for c in batch]
        documents  = [c["prefixed_text"] for c in batch]
        metadatas  = [
            {
                "doc_id":        c["doc_id"],
                "doc_type":      c["doc_type"],
                "title":         c["title"],
                "section_title": c["section_title"],
                "chunk_index":   c["chunk_index"],
                "revision":      c["revision"],
                "equipment":     c["equipment"],
                "tags":          c["tags"],
                "source_path":   c["source_path"],
            }
            for c in batch
        ]

        collection.upsert(
            ids=ids,
            documents=documents,
            embeddings=batch_embeddings.tolist(),
            metadatas=metadatas,
        )
        total_upserted += len(batch)
        print(f"  Upserted {total_upserted}/{len(all_chunks)} chunks", end="\r")

    print(f"\n  Done. Collection '{COLLECTION}' now has {collection.count()} chunks.\n")

    # ── Summary ───────────────────────────────────────────────────────────────
    print(f"{'='*60}")
    print("BUILD COMPLETE")
    print(f"{'='*60}")
    print(f"  Documents indexed : {len(docs)}")
    print(f"  Total chunks      : {collection.count()}")
    print(f"  Vector DB path    : {DB_DIR}")
    print(f"  Embedding model   : {MODEL_NAME}")
    print()
    print("Next steps:")
    print("  1. Restart the MCP server (restart Claude Code)")
    print("  2. Use docs_search(), docs_list_documents(), docs_get_document() tools")
    print()

    # Persist a build manifest for debugging
    manifest = {
        "doc_count": len(docs),
        "chunk_count": collection.count(),
        "model": MODEL_NAME,
        "collection": COLLECTION,
        "docs": [
            {"doc_id": d["doc_id"], "doc_type": d["doc_type"], "title": d["title"]}
            for d in docs
        ],
    }
    (DB_DIR / "build_manifest.json").write_text(
        json.dumps(manifest, indent=2), encoding="utf-8"
    )
    print(f"  Build manifest saved to {DB_DIR / 'build_manifest.json'}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Build the plant documentation RAG index")
    parser.add_argument(
        "--rebuild",
        action="store_true",
        help="Wipe the existing collection and rebuild from scratch",
    )
    args = parser.parse_args()
    build(rebuild=args.rebuild)
