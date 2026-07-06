"""
Audit report renderer — reads a trace directory and produces report.md.

Usage:
    python render_audit.py traces/{run_id}

Reads trace.jsonl, session_meta.json, and raw/ results. Produces report.md
in the same directory. Standalone — no MCP dependency.

Can also be imported and called programmatically:
    from render_audit import render_report
    render_report("traces/20260622_014208_c8a662")
"""

import json
import sys
from pathlib import Path


# ---------------------------------------------------------------------------
# Loading
# ---------------------------------------------------------------------------

def load_trace(trace_dir: Path) -> tuple[dict | None, list[dict]]:
    meta = None
    meta_path = trace_dir / "session_meta.json"
    if meta_path.exists():
        meta = json.loads(meta_path.read_text(encoding="utf-8"))

    entries = []
    trace_path = trace_dir / "trace.jsonl"
    if trace_path.exists():
        with open(trace_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line:
                    try:
                        entries.append(json.loads(line))
                    except json.JSONDecodeError:
                        pass
    return meta, entries


# ---------------------------------------------------------------------------
# Classification
# ---------------------------------------------------------------------------

def classify_entries(entries: list[dict]) -> dict:
    classified = {
        "tool_calls": [],
        "hypotheses": [],
        "conclusions": [],
        "observations": [],
        "rejections": [],
        "corrective_actions": [],
    }
    for e in entries:
        if e.get("type") == "tool_call":
            classified["tool_calls"].append(e)
        elif e.get("type") == "reasoning":
            rt = e.get("reasoning_type", "")
            if rt == "hypothesis":
                classified["hypotheses"].append(e)
            elif rt == "conclusion":
                classified["conclusions"].append(e)
            elif rt == "observation":
                classified["observations"].append(e)
            elif rt == "rejection":
                classified["rejections"].append(e)
            elif rt == "corrective_action":
                classified["corrective_actions"].append(e)
    return classified


# ---------------------------------------------------------------------------
# Evidence mapping
# ---------------------------------------------------------------------------

def build_evidence_map(entries: list[dict]) -> dict[int, list[dict]]:
    """Map step number -> reasoning entries that reference it."""
    emap: dict[int, list[dict]] = {}
    for e in entries:
        if e.get("type") == "reasoning":
            for step_ref in e.get("evidence_steps", []):
                emap.setdefault(step_ref, []).append(e)
    return emap


# ---------------------------------------------------------------------------
# Investigation sections
# ---------------------------------------------------------------------------

def extract_investigation_sections(entries: list[dict]) -> dict:
    sections: dict[str, list] = {
        "tags_queried": [],
        "alarms_analyzed": [],
        "kg_paths": [],
        "docs_referenced": [],
    }

    seen_tags: set[str] = set()
    seen_docs: set[str] = set()

    for e in entries:
        if e.get("type") != "tool_call":
            continue

        tool = e.get("tool_name", "")
        args = e.get("arguments", {})
        step = e.get("step", 0)

        if tool.startswith("historian_"):
            for tag in args.get("tag_names", []):
                if tag not in seen_tags:
                    seen_tags.add(tag)
                    sections["tags_queried"].append({
                        "tag": tag,
                        "first_seen_step": step,
                        "time_window": f"{args.get('start_time', '?')} to {args.get('end_time', '?')}",
                    })

        elif tool.startswith("alarm_"):
            sections["alarms_analyzed"].append({
                "tool": tool,
                "step": step,
                "summary": e.get("summary", ""),
                "timestamp": args.get("timestamp", args.get("start_time", "?")),
            })

        elif tool.startswith("kg_"):
            sections["kg_paths"].append({
                "tool": tool,
                "step": step,
                "summary": e.get("summary", ""),
                "key_arg": _kg_key_arg(tool, args),
            })

        elif tool.startswith("docs_"):
            doc_key = args.get("query", args.get("doc_id", "?"))
            if doc_key not in seen_docs:
                seen_docs.add(doc_key)
                sections["docs_referenced"].append({
                    "tool": tool,
                    "step": step,
                    "summary": e.get("summary", ""),
                    "query_or_id": doc_key,
                })

    return sections


def _kg_key_arg(tool: str, args: dict) -> str:
    if tool == "kg_trace_stream":
        return args.get("stream_name", "?")
    if tool == "kg_query_equipment":
        return args.get("query", "?")
    if tool == "kg_get_upstream_sensors":
        return args.get("node_id", "?")
    if tool == "kg_find_process_path":
        return f"{args.get('from_node', '?')} -> {args.get('to_node', '?')}"
    if tool == "kg_get_related_sensors":
        return args.get("tag_name", "?")
    if tool == "kg_get_system_sensors":
        return args.get("system_name", "?")
    return "?"


# ---------------------------------------------------------------------------
# Self-checks
# ---------------------------------------------------------------------------

def run_self_checks(entries: list[dict], meta: dict | None) -> list[str]:
    warnings = []
    all_steps = {e["step"] for e in entries}
    classified = classify_entries(entries)

    for c in classified["conclusions"]:
        ev = c.get("evidence_steps", [])
        if not ev:
            warnings.append(
                f"Step {c['step']}: conclusion has NO evidence steps referenced."
            )
        else:
            dangling = [s for s in ev if s not in all_steps]
            if dangling:
                warnings.append(
                    f"Step {c['step']}: conclusion references non-existent steps: {dangling}"
                )

    tool_count = len(classified["tool_calls"])
    reasoning_count = (len(classified["hypotheses"]) + len(classified["conclusions"])
                       + len(classified["observations"]) + len(classified["rejections"]))
    if tool_count > 3 and reasoning_count == 0:
        warnings.append(
            f"Thin trace: {tool_count} tool calls but NO reasoning entries logged. "
            "The audit report will lack hypothesis tracking."
        )
    elif tool_count > 5 and reasoning_count < tool_count // 3:
        warnings.append(
            f"Sparse reasoning: {tool_count} tool calls but only {reasoning_count} reasoning entries. "
            "Some investigative steps may lack documented rationale."
        )

    if meta is None or not meta.get("finalized", False):
        warnings.append("Trace was NOT finalized — integrity hash may be missing or incomplete.")

    return warnings


# ---------------------------------------------------------------------------
# Tool call formatting
# ---------------------------------------------------------------------------

_TOOL_LABELS = {
    "historian_get_statistics": "Retrieved statistics",
    "historian_get_tag_data": "Retrieved time-series data",
    "historian_get_data_range": "Checked available data range",
    "historian_list_tags": "Listed all available tags",
    "historian_search_tags": "Searched for tags",
    "historian_plot_tags": "Generated plot",
    "alarm_query": "Queried alarm events",
    "alarm_search_context": "Searched alarms around event",
    "alarm_get_active_at": "Checked active alarms at timestamp",
    "alarm_get_statistics": "Retrieved alarm statistics",
    "alarm_detect_flood": "Ran alarm flood detection",
    "kg_trace_stream": "Traced process stream",
    "kg_query_equipment": "Queried equipment",
    "kg_get_upstream_sensors": "Found upstream sensors",
    "kg_find_process_path": "Found process path",
    "kg_get_related_sensors": "Found related sensors",
    "kg_get_system_sensors": "Listed system sensors",
    "docs_search": "Searched plant documents",
    "docs_list_documents": "Listed available documents",
    "docs_get_document": "Retrieved full document",
}


def _format_tool_args(tool: str, args: dict) -> str:
    """Format tool arguments as a human-readable line."""
    parts = []

    tag_names = args.get("tag_names", [])
    if tag_names:
        if len(tag_names) <= 5:
            tags_str = ", ".join(f"`{t}`" for t in tag_names)
        else:
            tags_str = ", ".join(f"`{t}`" for t in tag_names[:4]) + f" + {len(tag_names) - 4} more"
        parts.append(f"Tags: {tags_str}")

    start = args.get("start_time")
    end = args.get("end_time")
    if start and end:
        parts.append(f"Window: {start} to {end}")

    timestamp = args.get("timestamp")
    if timestamp and not start:
        parts.append(f"At: {timestamp}")

    window_min = args.get("window_minutes")
    if window_min:
        parts.append(f"±{window_min} min")

    downsample = args.get("downsample_minutes")
    if downsample:
        parts.append(f"Downsample: {downsample} min")

    node_id = args.get("node_id")
    if node_id:
        parts.append(f"Node: `{node_id}`")

    tag_name = args.get("tag_name")
    if tag_name and not tag_names:
        parts.append(f"Tag: `{tag_name}`")

    query = args.get("query")
    if query:
        parts.append(f"Query: \"{query}\"")

    doc_id = args.get("doc_id")
    if doc_id:
        parts.append(f"Document: `{doc_id}`")

    doc_type = args.get("doc_type")
    if doc_type:
        parts.append(f"Type: {doc_type}")

    equipment_id = args.get("equipment_id")
    if equipment_id:
        parts.append(f"Equipment: `{equipment_id}`")

    stream_name = args.get("stream_name")
    if stream_name:
        parts.append(f"Stream: `{stream_name}`")

    system_name = args.get("system_name")
    if system_name:
        parts.append(f"System: `{system_name}`")

    title = args.get("title")
    if title:
        parts.append(f"Title: \"{title}\"")

    if not parts:
        return ""

    return " | ".join(parts)


# ---------------------------------------------------------------------------
# Markdown rendering
# ---------------------------------------------------------------------------

def render_markdown(
    meta: dict | None,
    entries: list[dict],
    classified: dict,
    evidence_map: dict[int, list[dict]],
    sections: dict,
    warnings: list[str],
) -> str:
    lines: list[str] = []

    lines.append("# Root Cause Analysis Report")
    lines.append("")

    # Warnings (only if present)
    if warnings:
        for w in warnings:
            lines.append(f"> **WARNING:** {w}")
        lines.append("")

    # ----- ROOT CAUSE (first thing a reader sees) -----
    lines.append("## Root Cause")
    lines.append("")

    final_conclusions = [c for c in classified["conclusions"]
                         if c.get("confidence") is not None]
    if final_conclusions:
        fc = final_conclusions[-1]
        conf = fc.get("confidence", 0)
        if conf >= 0.8:
            label = "HIGH"
        elif conf >= 0.5:
            label = "MEDIUM"
        else:
            label = "LOW"
        lines.append(f"**Confidence:** {label} ({conf})")
        lines.append("")
        lines.append(fc["text"])
        lines.append("")
        ev = fc.get("evidence_steps", [])
        if ev:
            lines.append(f"*Supporting evidence: steps {', '.join(str(s) for s in ev)}*")
        lines.append("")
    else:
        non_conf = classified["conclusions"]
        if non_conf:
            lines.append(non_conf[-1]["text"])
            lines.append("")
            lines.append("*(No confidence level was set on the conclusion.)*")
        else:
            lines.append("*(No root cause conclusion was logged in this session.)*")
    lines.append("")

    # ----- INVESTIGATION SUMMARY -----
    lines.append("## Investigation Summary")
    lines.append("")
    if meta:
        question = meta.get("question", "?")
        start = meta.get("start_time", "?")
        end = meta.get("end_time", "?")
        total = meta.get("total_steps", "?")
        tc = meta.get("tool_calls", "?")
        rc = meta.get("reasoning_entries", "?")

        duration_str = ""
        try:
            from datetime import datetime, timezone
            t0 = datetime.fromisoformat(start)
            t1 = datetime.fromisoformat(end)
            dur_sec = (t1 - t0).total_seconds()
            if dur_sec < 120:
                duration_str = f" ({dur_sec:.0f} seconds)"
            else:
                duration_str = f" ({dur_sec / 60:.1f} minutes)"
        except Exception:
            pass

        lines.append(f"**Question:** {question}")
        lines.append("")
        lines.append(f"The investigation comprised {total} steps ({tc} tool calls, "
                      f"{rc} reasoning entries){duration_str}.")
    else:
        lines.append("*(No session metadata available — trace may be incomplete.)*")
    lines.append("")

    # ----- INVESTIGATION STEPS -----
    lines.append("## Investigation Steps")
    lines.append("")
    for e in entries:
        step = e.get("step", "?")
        ts = e.get("timestamp", "?")
        if isinstance(ts, str) and len(ts) > 19:
            ts = ts[:19]

        if e.get("type") == "tool_call":
            tool = e.get("tool_name", "?")
            dur = e.get("duration_ms", 0)
            summary = e.get("summary", "")
            success = e.get("success", True)
            label = _TOOL_LABELS.get(tool, tool)
            status = "" if success else " **FAILED**"

            lines.append(f"### Step {step} — {label}{status}")
            lines.append(f"*{ts} | `{tool}` | {dur:.0f}ms*")
            lines.append("")

            args = e.get("arguments", {})
            args_formatted = _format_tool_args(tool, args)
            if args_formatted:
                lines.append(args_formatted)
                lines.append("")

            lines.append(f"> {summary}")
            lines.append("")

            if e.get("error"):
                lines.append(f"**Error:** {e['error']}")
                lines.append("")

        elif e.get("type") == "reasoning":
            rt = e.get("reasoning_type", "?").upper()
            text = e.get("text", "")
            ev = e.get("evidence_steps", [])
            conf = e.get("confidence")

            lines.append(f"### Step {step} — {rt}")
            lines.append(f"*{ts}*")
            lines.append("")
            lines.append(_numbered_to_bullets(text))
            lines.append("")

            if ev:
                lines.append(f"*Evidence: steps {', '.join(str(s) for s in ev)}*")
                lines.append("")
            if conf is not None:
                lines.append(f"*Confidence: {conf}*")
                lines.append("")

    # ----- APPENDIX -----
    lines.append("---")
    lines.append("")
    lines.append("# Appendix")
    lines.append("")

    # Hypothesis Register
    lines.append("## Hypothesis Register")
    lines.append("")
    all_hyp = classified["hypotheses"]
    if all_hyp:
        lines.append("| Step | Hypothesis | Status | Evidence | Resolution |")
        lines.append("|------|-----------|--------|----------|------------|")
        for h in all_hyp:
            h_step = h["step"]
            text = h["text"][:80]
            if len(h["text"]) > 80:
                text += "..."
            status, resolution = _resolve_hypothesis(h, classified)
            ev = ", ".join(str(s) for s in h.get("evidence_steps", []))
            lines.append(f"| {h_step} | {text} | {status} | {ev} | {resolution} |")
    else:
        lines.append("*(No hypotheses were logged.)*")
    lines.append("")

    # Tags Queried
    lines.append("## Tags Queried")
    lines.append("")
    if sections["tags_queried"]:
        lines.append("| Tag | First Seen (Step) | Time Window |")
        lines.append("|-----|-------------------|-------------|")
        for t in sections["tags_queried"]:
            lines.append(f"| `{t['tag']}` | {t['first_seen_step']} | {t['time_window']} |")
    else:
        lines.append("*(No historian tags were queried.)*")
    lines.append("")

    # Alarms Analyzed
    lines.append("## Alarms Analyzed")
    lines.append("")
    if sections["alarms_analyzed"]:
        for a in sections["alarms_analyzed"]:
            lines.append(f"- **Step {a['step']}** (`{a['tool']}`): {a['summary']}")
    else:
        lines.append("*(No alarm queries were made.)*")
    lines.append("")

    # Knowledge Graph Paths
    if sections["kg_paths"]:
        lines.append("## Knowledge Graph Paths")
        lines.append("")
        for k in sections["kg_paths"]:
            lines.append(f"- **Step {k['step']}** (`{k['tool']}` — {k['key_arg']}): {k['summary']}")
        lines.append("")

    # Documents Referenced
    if sections["docs_referenced"]:
        lines.append("## Documents Referenced")
        lines.append("")
        for d in sections["docs_referenced"]:
            lines.append(f"- **Step {d['step']}** (`{d['tool']}`): {d['summary']}")
        lines.append("")

    # Provenance (moved to end)
    lines.append("## Provenance")
    lines.append("")
    if meta:
        lines.append(f"- **Run ID:** `{meta.get('run_id', '?')}`")
        lines.append(f"- **Start:** {meta.get('start_time', '?')}")
        lines.append(f"- **End:** {meta.get('end_time', '?')}")
        lines.append(f"- **SHA-256:** `{meta.get('trace_sha256', '?')}`")
        lines.append(f"- **Model:** {meta.get('model', '?')}")
        if meta.get("kg_file_sha256"):
            lines.append(f"- **KG version:** `{meta['kg_file_sha256'][:12]}...`")
        if meta.get("doc_set_file_count"):
            lines.append(f"- **Doc set:** {meta['doc_set_file_count']} files, "
                          f"{meta.get('doc_set_total_bytes', '?')} bytes")
    else:
        lines.append("- *(No session metadata available.)*")
    lines.append("")

    return "\n".join(lines)


def _numbered_to_bullets(text: str) -> str:
    """Convert lines starting with '1. ', '2. ' etc. to bullet list lines."""
    import re
    return re.sub(r"(?m)^\d+\.\s+", "- ", text)


def _truncate(text: str, max_len: int = 120) -> str:
    """Truncate to first meaningful sentence or max_len, whichever is shorter."""
    first_line = text.split("\n")[0].strip()
    if not first_line:
        for line in text.split("\n"):
            line = line.strip()
            if line:
                first_line = line
                break
    if len(first_line) <= max_len:
        return first_line
    period = first_line.find(". ")
    if 20 < period < max_len:
        return first_line[: period + 1]
    return first_line[: max_len - 3].rstrip() + "..."


def _strip_rejected_hypotheses(text: str) -> str:
    """Remove the REJECTED HYPOTHESES paragraph from a conclusion for summary display."""
    paragraphs = text.split("\n\n")
    kept = [p for p in paragraphs if not p.strip().startswith("REJECTED HYPOTHESES:")]
    return "\n\n".join(kept)


def _extract_root_cause_and_chain(text: str) -> tuple[str, list[str]]:
    """Extract root cause (first sentence) and causal chain steps (numbered items)."""
    import re

    cleaned = text.strip()
    for prefix in (
        "ROOT CAUSE CONCLUSION: ",
        "ROOT CAUSE CONFIRMED: ",
        "CAUSE VS. SYMPTOM DETERMINATION: ",
    ):
        if cleaned.startswith(prefix):
            cleaned = cleaned[len(prefix):]

    # Root cause = first non-list sentence. Stop at the first ". " that is NOT
    # immediately followed by a digit+dot (which would be a numbered list continuation).
    root_cause = cleaned
    search_start = 0
    while True:
        idx = cleaned.find(". ", search_start)
        if idx < 1 or idx >= len(cleaned) - 2:
            break
        after = cleaned[idx + 2:]
        # Skip if the next non-space chars look like "1. " (continuation of numbered list)
        if re.match(r"\d+\.", after.lstrip()):
            search_start = idx + 2
            continue
        root_cause = cleaned[: idx + 1].strip()
        break

    chain_items: list[str] = []

    # Strategy 1: (1), (2) style — pure-integer parens
    split_parts = re.split(r"\s*\(\d+\)\s+", cleaned)
    if len(split_parts) > 1:
        for part in split_parts[1:]:
            item = part.strip()
            if item:
                chain_items.append(item)

    # Strategy 2: "1. ", "2. " style items on their own lines
    if not chain_items:
        numbered = re.split(r"\n\d+\.\s+", "\n" + cleaned)
        if len(numbered) > 1:
            for part in numbered[1:]:
                # Keep only up to the next blank line (don't bleed into CAUSE vs SYMPTOM etc.)
                item = part.split("\n\n")[0].strip()
                # Strip any stray leading "N. " prefix
                item = re.sub(r"^\d+\.\s+", "", item)
                if item:
                    chain_items.append(item)

    # Fallback: split remainder into sentences
    if not chain_items:
        remainder = cleaned[len(root_cause):].strip()
        for intro in ("The failure sequence:", "The sequence:", "Failure sequence:",
                      "CAUSAL CHAIN:", "Causal chain:"):
            low = remainder.lower()
            if intro.lower() in low:
                remainder = remainder[low.find(intro.lower()) + len(intro):].strip()
        if remainder:
            sentences = [s.strip() for s in remainder.split(". ") if s.strip()]
            chain_items = [s if s.endswith(".") else s + "." for s in sentences[:10]]

    return root_cause, chain_items


def render_summary_markdown(meta: dict | None, entries: list[dict], classified: dict) -> str:
    lines: list[str] = []
    lines.append("# Executive Summary")
    lines.append("")

    question = meta.get("question", "?") if meta else "?"
    lines.append(f"**Question:** {question}")
    lines.append("")

    if meta:
        tc = meta.get("tool_calls", "?")
        rc = meta.get("reasoning_entries", "?")
        duration_str = ""
        try:
            from datetime import datetime, timezone
            t0 = datetime.fromisoformat(meta.get("start_time", ""))
            t1 = datetime.fromisoformat(meta.get("end_time", ""))
            dur_sec = (t1 - t0).total_seconds()
            if dur_sec < 120:
                duration_str = f"{dur_sec:.0f}s"
            else:
                duration_str = f"{dur_sec / 60:.1f}min"
        except Exception:
            pass
        parts = []
        if duration_str:
            parts.append(duration_str)
        parts.append(f"{tc} tool calls")
        parts.append(f"{rc} reasoning entries")
        lines.append(" | ".join(parts))
        lines.append("")

    # --- Root Cause ---
    lines.append("## Root Cause")
    lines.append("")

    final_conclusions = [c for c in classified["conclusions"]
                         if c.get("confidence") is not None]
    all_conclusions = final_conclusions or classified["conclusions"]

    chain_items: list[str] = []
    if all_conclusions:
        conclusion_text = _strip_rejected_hypotheses(all_conclusions[-1]["text"])
        root_cause_sentence, chain_items = _extract_root_cause_and_chain(conclusion_text)
        lines.append(root_cause_sentence)
        lines.append("")
        if final_conclusions:
            fc = final_conclusions[-1]
            conf = fc.get("confidence", 0)
            label = "HIGH" if conf >= 0.8 else ("MEDIUM" if conf >= 0.5 else "LOW")
            lines.append(f"Confidence: {label} ({conf}).")
        lines.append("")
    else:
        lines.append("*(No root cause conclusion was logged.)*")
        lines.append("")

    # --- Causal Chain ---
    lines.append("## Causal Chain")
    lines.append("")
    if chain_items:
        for item in chain_items:
            lines.append(f"- {item}")
    else:
        lines.append("*(No causal chain steps were identified.)*")
    lines.append("")

    # --- Recommended Corrective Actions ---
    lines.append("## Recommended Corrective Actions")
    lines.append("")
    corrective_actions = classified.get("corrective_actions", [])
    if corrective_actions:
        for ca in corrective_actions:
            # Split multi-paragraph blocks so each logical action gets its own bullet
            paragraphs = [p.strip() for p in ca['text'].split('\n\n') if p.strip()]
            if not paragraphs:
                paragraphs = [ca['text'].strip()]
            for para in paragraphs:
                lines.append(f"- {para}")
    else:
        lines.append("*(No corrective actions were logged for this investigation.)*")
    lines.append("")

    # --- Tool Calls ---
    lines.append("## Tool Calls")
    lines.append("")
    tool_calls = classified["tool_calls"]
    if tool_calls:
        lines.append("| Step | Tool | Details | Outcome |")
        lines.append("|------|------|---------|---------|")
        for tc_entry in tool_calls:
            step = tc_entry.get("step", "?")
            tool = tc_entry.get("tool_name", "?")
            args = tc_entry.get("arguments", {})
            args_str = _format_tool_args(tool, args) or "—"
            success = tc_entry.get("success", True)
            outcome = "OK" if success else "**FAILED**"
            lines.append(f"| {step} | `{tool}` | {args_str} | {outcome} |")
    else:
        lines.append("*(No tool calls were recorded.)*")
    lines.append("")

    # --- Reference footer ---
    lines.append("---")
    lines.append("")
    lines.append("Full detailed report: `report.md`")
    if meta:
        run_id = meta.get("run_id", "?")
        sha = meta.get("trace_sha256", "?")
        lines.append(f"Run ID: `{run_id}` | SHA-256: `{sha[:16]}...`")
    lines.append("")

    return "\n".join(lines)


def render_summary(trace_dir_str: str) -> str:
    """Render summary.md for a trace directory. Returns the summary file path."""
    trace_dir = Path(trace_dir_str)

    if not trace_dir.exists():
        raise FileNotFoundError(f"Trace directory not found: {trace_dir}")

    trace_path = trace_dir / "trace.jsonl"
    if not trace_path.exists():
        raise FileNotFoundError(f"No trace.jsonl in {trace_dir}")

    meta, entries = load_trace(trace_dir)
    classified = classify_entries(entries)
    summary = render_summary_markdown(meta, entries, classified)

    summary_path = trace_dir / "summary.md"
    summary_path.write_text(summary, encoding="utf-8")
    return str(summary_path)


def _resolve_hypothesis(hypothesis: dict, classified: dict) -> tuple[str, str]:
    """Check if a hypothesis was later confirmed, rejected, or left open."""
    h_step = hypothesis["step"]

    for c in classified["conclusions"]:
        if c["step"] > h_step:
            if any(s in c.get("evidence_steps", []) for s in hypothesis.get("evidence_steps", [])):
                return "Confirmed", c["text"][:60]

    for r in classified["rejections"]:
        if r["step"] > h_step:
            return "Rejected", r["text"][:60]

    return "Open", "(not resolved)"


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def render_report(trace_dir_str: str) -> str:
    """Render report.md for a trace directory. Returns the report file path."""
    trace_dir = Path(trace_dir_str)

    if not trace_dir.exists():
        raise FileNotFoundError(f"Trace directory not found: {trace_dir}")

    trace_path = trace_dir / "trace.jsonl"
    if not trace_path.exists():
        raise FileNotFoundError(f"No trace.jsonl in {trace_dir}")

    meta, entries = load_trace(trace_dir)
    classified = classify_entries(entries)
    evidence_map = build_evidence_map(entries)
    sections = extract_investigation_sections(entries)
    warnings = run_self_checks(entries, meta)

    report = render_markdown(meta, entries, classified, evidence_map,
                             sections, warnings)

    report_path = trace_dir / "report.md"
    report_path.write_text(report, encoding="utf-8")
    return str(report_path)


# ---------------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------------

_JUNCTION = r"C:\boiler"
_PROJECT_ROOT = str(Path(__file__).resolve().parent)


def _file_url(path_str: str) -> str:
    """Convert an absolute Windows path to a correctly-encoded file:/// URL.

    If the C:\\boiler junction exists, substitutes it for the long project root
    so URLs stay short (file:///C:/boiler/... instead of the full OneDrive path).
    """
    from urllib.parse import quote
    abs_path = str(Path(path_str).resolve())
    if Path(_JUNCTION).exists() and abs_path.startswith(_PROJECT_ROOT):
        abs_path = _JUNCTION + abs_path[len(_PROJECT_ROOT):]
    forward = abs_path.replace("\\", "/")
    encoded = quote(forward, safe="/:@")
    return f"file:///{encoded}"


def main(trace_dir_str: str) -> None:
    try:
        report_path = render_report(trace_dir_str)
        summary_path = render_summary(trace_dir_str)
        print(f"Report generated: {report_path}")
        print(f"Summary generated: {summary_path}")
        report_url = _file_url(str(Path(report_path).resolve()))
        summary_url = _file_url(str(Path(summary_path).resolve()))
        print(f"REPORT_URL: {report_url}")
        print(f"SUMMARY_URL: {summary_url}")
        print(f"REPORT_LINK: [report.md](<{report_url}>)")
        print(f"SUMMARY_LINK: [summary.md](<{summary_url}>)")
    except FileNotFoundError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python render_audit.py traces/{run_id}", file=sys.stderr)
        sys.exit(1)
    main(sys.argv[1])
