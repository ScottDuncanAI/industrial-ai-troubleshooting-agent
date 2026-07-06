"""
rag_tools.py
============
Query layer for the plant documentation RAG system.
Exposes three functions that are called by historian_mcp_server.py:

    rag_search(query, ...)      — semantic search, returns ranked chunks
    rag_list_documents(...)     — list available documents by type
    rag_get_document(doc_id)    — retrieve full document text

The ChromaDB client and embedding model are lazy-loaded on first call
(same singleton pattern as the knowledge graph).
"""

import os

# Must be set before sentence_transformers / huggingface_hub are imported.
# huggingface_hub evaluates HF_HUB_OFFLINE as a module-level constant at import time;
# setting it after the import has no effect and causes a network check that fails offline.
os.environ.setdefault("HF_HUB_OFFLINE", "1")
os.environ.setdefault("TRANSFORMERS_OFFLINE", "1")

import json
from pathlib import Path
from typing import Optional

# ── Paths (same as build_docs_db.py) ─────────────────────────────────────────
PROJECT_DIR = Path(__file__).parent
DOCS_DIR    = PROJECT_DIR / "RAG docs"
DB_DIR      = PROJECT_DIR / "rag_vector_db"
COLLECTION  = "plant_docs"
MODEL_NAME  = "BAAI/bge-small-en-v1.5"

# BGE query prefix — must match what was used during indexing in build_docs_db.py
QUERY_PREFIX = "Represent this sentence for searching relevant passages: "

# ── Lazy singleton ─────────────────────────────────────────────────────────────

# Tuple is (chroma_client, chroma_collection, SentenceTransformer).
# The client must be kept here — if it goes out of scope after _get_rag() returns,
# Python GCs it, its __del__ closes the underlying httpx connection, and every
# subsequent collection.get() / collection.query() raises "client has been closed".
_RAG_INSTANCE: Optional[tuple] = None


def _get_rag() -> tuple:
    """
    Return (chroma_collection, embed_model), loading on first call.
    Subsequent calls return the cached instance immediately.
    Raises RuntimeError with actionable instructions if the DB hasn't been built.
    """
    global _RAG_INSTANCE
    if _RAG_INSTANCE is not None:
        _, collection, model = _RAG_INSTANCE
        return collection, model

    if not DB_DIR.exists():
        raise RuntimeError(
            f"RAG vector database not found at {DB_DIR}. "
            "Run 'python build_docs_db.py' first to build the index."
        )

    try:
        import chromadb
        from sentence_transformers import SentenceTransformer
    except ImportError as e:
        raise RuntimeError(
            f"Missing dependency: {e}. "
            "Run 'pip install chromadb sentence-transformers' to install."
        ) from e

    client = chromadb.PersistentClient(path=str(DB_DIR))
    try:
        collection = client.get_collection(COLLECTION)
    except Exception:
        raise RuntimeError(
            f"Collection '{COLLECTION}' not found in the RAG database. "
            "Run 'python build_docs_db.py --rebuild' to re-build the index."
        )

    model = SentenceTransformer(MODEL_NAME)
    _RAG_INSTANCE = (client, collection, model)
    return collection, model


# ── Public API ─────────────────────────────────────────────────────────────────

def rag_search(
    query: str,
    doc_type: Optional[str] = None,
    equipment_id: Optional[str] = None,
    sensor_tag: Optional[str] = None,
    top_k: int = 5,
) -> list[dict]:
    """
    Semantic search across all indexed plant documents.

    Parameters
    ----------
    query        : Natural-language search query
    doc_type     : Optional filter — one of: sop, datasheet, maintenance,
                   troubleshooting, controls, safety
    equipment_id : Optional filter — knowledge graph equipment node ID
                   (e.g. 'induced_draft_fan', 'steam_drum')
    sensor_tag   : Optional filter — historian sensor tag
                   (e.g. 'TE_8332A', 'YFJ3_ZD1')
    top_k        : Number of results to return (default 5)

    Returns
    -------
    List of result dicts, each containing:
        doc_id, doc_type, title, section_title, chunk_text,
        relevance_score (0–1, higher = more relevant), revision
    """
    collection, model = _get_rag()

    # Embed query — BGE requires the query prefix for best retrieval quality
    query_vector = model.encode(
        QUERY_PREFIX + query,
        normalize_embeddings=True,
    ).tolist()

    # Build optional metadata pre-filter.
    # NOTE: ChromaDB 1.x $contains does NOT do substring matching on string fields —
    # it only works for exact list-element matching. We therefore apply doc_type as
    # a where clause (exact match, reliable) and handle equipment_id / sensor_tag
    # as post-retrieval Python filters on the comma-joined metadata strings.
    where: Optional[dict] = None
    if doc_type:
        where = {"doc_type": {"$eq": doc_type}}

    # Fetch more results than top_k so post-filtering still leaves enough
    fetch_n = min(top_k * 6, collection.count())
    if fetch_n == 0:
        return [{"error": "Vector database is empty. Run build_docs_db.py first."}]

    query_kwargs: dict = {
        "query_embeddings": [query_vector],
        "n_results": fetch_n,
        "include": ["documents", "metadatas", "distances"],
    }
    if where:
        query_kwargs["where"] = where

    try:
        results = collection.query(**query_kwargs)
    except Exception as e:
        if "no documents" in str(e).lower() or "n_results" in str(e).lower():
            return []
        raise

    documents = results["documents"][0]
    metadatas = results["metadatas"][0]
    distances = results["distances"][0]  # cosine distance (0 = identical, 2 = opposite)

    # Post-filter by equipment_id and sensor_tag (substring check on comma-joined string)
    def passes_filter(meta: dict) -> bool:
        if equipment_id and equipment_id not in meta.get("equipment", ""):
            return False
        if sensor_tag and sensor_tag not in meta.get("tags", ""):
            return False
        return True

    # Deduplicate by doc_id — keep only the best-scoring chunk per document
    seen_docs: set[str] = set()
    output: list[dict] = []

    for doc_text, meta, dist in zip(documents, metadatas, distances):
        if not passes_filter(meta):
            continue
        doc_id = meta["doc_id"]
        if doc_id in seen_docs:
            continue
        seen_docs.add(doc_id)

        # Convert cosine distance to a 0-1 relevance score
        # distance=0 → score=1.0 (identical), distance=2 → score=0.0 (opposite)
        relevance = round(max(0.0, 1.0 - dist / 2.0), 4)

        # Strip the context prefix from the returned chunk text before displaying
        chunk_text = doc_text
        if " — " in chunk_text:
            # Format was "{title}: {section} — {content}", strip the prefix
            prefix_end = chunk_text.index(" — ") + 3
            chunk_text = chunk_text[prefix_end:]

        output.append({
            "doc_id":        doc_id,
            "doc_type":      meta.get("doc_type", ""),
            "title":         meta.get("title", ""),
            "section_title": meta.get("section_title", ""),
            "revision":      meta.get("revision", ""),
            "chunk_text":    chunk_text.strip(),
            "relevance_score": relevance,
            "equipment":     [e.strip() for e in meta.get("equipment", "").split(",") if e.strip()],
            "tags":          [t.strip() for t in meta.get("tags", "").split(",") if t.strip()],
        })

        if len(output) >= top_k:
            break

    return output


def rag_list_documents(doc_type: Optional[str] = None) -> list[dict]:
    """
    List all documents in the RAG index, optionally filtered by type.

    Parameters
    ----------
    doc_type : Optional filter — sop, datasheet, maintenance, troubleshooting,
               controls, safety

    Returns
    -------
    List of document summary dicts (one per unique doc_id), sorted by doc_type
    then title. Each dict contains: doc_id, doc_type, title, revision,
    equipment[], tags[], chunk_count.
    """
    collection, _ = _get_rag()

    # Query metadata-only — no vector search needed
    where = {"doc_type": {"$eq": doc_type}} if doc_type else None
    get_kwargs: dict = {"include": ["metadatas"]}
    if where:
        get_kwargs["where"] = where

    results = collection.get(**get_kwargs)
    metadatas = results.get("metadatas") or []

    # Collapse chunks → one entry per doc_id
    docs: dict[str, dict] = {}
    for meta in metadatas:
        did = meta["doc_id"]
        if did not in docs:
            docs[did] = {
                "doc_id":    did,
                "doc_type":  meta.get("doc_type", ""),
                "title":     meta.get("title", ""),
                "revision":  meta.get("revision", ""),
                "equipment": [e.strip() for e in meta.get("equipment", "").split(",") if e.strip()],
                "tags":      [t.strip() for t in meta.get("tags", "").split(",") if t.strip()],
                "chunk_count": 0,
            }
        docs[did]["chunk_count"] += 1

    return sorted(docs.values(), key=lambda d: (d["doc_type"], d["title"]))


def rag_get_document(doc_id: str) -> dict:
    """
    Retrieve the full text and metadata of a specific document.

    Reads from the original markdown file (not from ChromaDB) — the flat file
    is always the authoritative source. Use this when a search result is relevant
    but you need the full procedure context, not just one chunk.

    Parameters
    ----------
    doc_id : The document identifier (e.g. 'trb_high_steam_temperature')

    Returns
    -------
    Dict with keys: doc_id, doc_type, title, revision, equipment[], tags[],
    full_text, source_path. Returns {"error": "..."} if not found.
    """
    collection, _ = _get_rag()

    # Find source_path from the index (most reliable way to locate the file)
    results = collection.get(
        where={"doc_id": {"$eq": doc_id}},
        include=["metadatas"],
        limit=1,
    )
    metadatas = results.get("metadatas") or []
    if not metadatas:
        return {"error": f"Document '{doc_id}' not found in the RAG index. "
                         "Use docs_list_documents() to see available doc_ids."}

    meta = metadatas[0]
    source_path = PROJECT_DIR / meta.get("source_path", "")

    if not source_path.exists():
        # Fallback: search DOCS_DIR for a file whose stem matches doc_id
        matches = list(DOCS_DIR.rglob(f"{doc_id}.md"))
        if not matches:
            return {"error": f"Source file for '{doc_id}' not found on disk at {source_path}."}
        source_path = matches[0]

    full_text = source_path.read_text(encoding="utf-8")

    return {
        "doc_id":      doc_id,
        "doc_type":    meta.get("doc_type", ""),
        "title":       meta.get("title", ""),
        "revision":    meta.get("revision", ""),
        "equipment":   [e.strip() for e in meta.get("equipment", "").split(",") if e.strip()],
        "tags":        [t.strip() for t in meta.get("tags", "").split(",") if t.strip()],
        "source_path": str(source_path.relative_to(PROJECT_DIR)),
        "full_text":   full_text,
    }
