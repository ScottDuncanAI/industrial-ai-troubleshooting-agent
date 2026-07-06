"""
Deterministic audit trace capture for the boiler historian MCP server.

This module owns all trace state and file I/O. It has no MCP dependency.
The MCP server imports it and calls its functions from the dispatcher.

Every tool call is recorded automatically. The model's reasoning is captured
via audit_log_reasoning calls. The trace is sealed with a SHA-256 hash on
finalization for tamper evidence.
"""

import hashlib
import json
import logging
import os
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)

PROJECT_DIR = Path(os.path.dirname(os.path.abspath(__file__)))
TRACES_DIR = PROJECT_DIR / "traces"
KG_PATH = PROJECT_DIR / "boiler_kg.json"
RAG_DOCS_DIR = PROJECT_DIR / "RAG docs"


# ---------------------------------------------------------------------------
# Result summarization
# ---------------------------------------------------------------------------

def _safe_get(d: Any, *keys: str, default: Any = None) -> Any:
    for k in keys:
        if isinstance(d, dict):
            d = d.get(k, default)
        else:
            return default
    return d


def summarize_result(tool_name: str, result: Any) -> dict:
    """Produce a concise summary for a tool result. Never includes bulk data."""
    try:
        return _SUMMARIZERS.get(tool_name, _summarize_generic)(result)
    except Exception:
        return {"summary_text": "(summarization failed)", "metrics": {}}


def _summarize_generic(result: Any) -> dict:
    if isinstance(result, dict) and "error" in result:
        return {"summary_text": f"Error: {result['error'][:200]}", "metrics": {}}
    if isinstance(result, list):
        return {"summary_text": f"{len(result)} items returned", "metrics": {"count": len(result)}}
    return {"summary_text": str(result)[:200], "metrics": {}}


def _summarize_list_tags(result: Any) -> dict:
    count = len(result) if isinstance(result, list) else 0
    return {"summary_text": f"{count} tags returned", "metrics": {"tag_count": count}}


def _summarize_search_tags(result: Any) -> dict:
    count = len(result) if isinstance(result, list) else 0
    names = [r.get("tag_name", "?") for r in result[:5]] if isinstance(result, list) else []
    return {
        "summary_text": f"{count} tags matched: {', '.join(names)}",
        "metrics": {"match_count": count},
    }


def _summarize_data_range(result: Any) -> dict:
    earliest = _safe_get(result, "earliest_timestamp", default="?")
    latest = _safe_get(result, "latest_timestamp", default="?")
    rows = _safe_get(result, "total_rows", default=0)
    return {
        "summary_text": f"Range: {earliest} to {latest}, {rows} rows",
        "metrics": {"total_rows": rows},
    }


def _summarize_tag_data(result: Any) -> dict:
    row_count = _safe_get(result, "row_count", default=0)
    tags = _safe_get(result, "tag_names", default=[])
    start = _safe_get(result, "start_time", default="?")
    end = _safe_get(result, "end_time", default="?")
    ds = _safe_get(result, "downsample_minutes", default=None)
    ds_str = f", downsample={ds}min" if ds else ""
    return {
        "summary_text": f"{row_count} rows for {len(tags)} tags ({start} to {end}{ds_str})",
        "metrics": {"row_count": row_count, "tag_count": len(tags)},
    }


def _summarize_statistics(result: Any) -> dict:
    stats = _safe_get(result, "statistics", default={})
    tag_names = list(stats.keys())
    lines = []
    for tag in tag_names[:3]:
        s = stats[tag]
        lines.append(f"{tag}: mean={s.get('mean', '?')}, min={s.get('min', '?')}, max={s.get('max', '?')}")
    if len(tag_names) > 3:
        lines.append(f"... and {len(tag_names) - 3} more")
    return {
        "summary_text": f"Stats for {len(tag_names)} tag(s): " + "; ".join(lines),
        "metrics": {"tag_count": len(tag_names)},
    }


def _summarize_plot_tags(result: Any) -> dict:
    path = _safe_get(result, "plot_path", default="?")
    points = _safe_get(result, "data_points", default=0)
    return {
        "summary_text": f"Plot saved: {os.path.basename(str(path))}, {points} data points",
        "metrics": {"data_points": points},
    }


def _summarize_alarm_query(result: Any) -> dict:
    returned = _safe_get(result, "returned", default=0)
    total = _safe_get(result, "total_matching", default=0)
    limit = _safe_get(result, "limit", default=100)
    alarms = _safe_get(result, "alarms", default=[])
    top_tags = list({a.get("tag_name", "?") for a in alarms[:5]})
    return {
        "summary_text": f"{returned}/{total} alarms returned (limit {limit}), tags: {', '.join(top_tags[:3])}",
        "metrics": {"returned": returned, "total_matching": total},
    }


def _summarize_alarm_statistics(result: Any) -> dict:
    total = _safe_get(result, "total_alarms", default=0)
    ack_rate = _safe_get(result, "ack_rate", default="?")
    most_freq = _safe_get(result, "most_frequent", default=[])
    top_tag = most_freq[0].get("tag_name", "?") if most_freq else "none"
    return {
        "summary_text": f"{total} alarms, ack_rate={ack_rate}, top offender: {top_tag}",
        "metrics": {"total_alarms": total},
    }


def _summarize_alarm_active_at(result: Any) -> dict:
    count = _safe_get(result, "active_alarm_count", default=0)
    ts = _safe_get(result, "timestamp", default="?")
    alarms = _safe_get(result, "active_alarms", default=[])
    tags = list({a.get("tag_name", "?") for a in alarms[:5]})
    tag_str = f", tags: {', '.join(tags)}" if count <= 5 else ""
    return {
        "summary_text": f"{count} alarms active at {ts}{tag_str}",
        "metrics": {"active_count": count},
    }


def _summarize_alarm_search_context(result: Any) -> dict:
    count = _safe_get(result, "alarm_count", default=0)
    focal = _safe_get(result, "focal_timestamp", default="?")
    window = _safe_get(result, "window_minutes", default=30)
    alarms = _safe_get(result, "alarms", default=[])
    closest = sorted(alarms, key=lambda a: abs(a.get("minutes_offset", 999)))[:3]
    closest_tags = [f"{a.get('tag_name', '?')}({a.get('alarm_level', '?')})" for a in closest]
    return {
        "summary_text": f"{count} alarms within ±{window}min of {focal}, closest: {', '.join(closest_tags)}",
        "metrics": {"alarm_count": count, "window_minutes": window},
    }


def _summarize_alarm_detect_flood(result: Any) -> dict:
    total = _safe_get(result, "total_flood_windows", default=0)
    return {
        "summary_text": f"{total} flood periods detected",
        "metrics": {"flood_windows": total},
    }


def _summarize_kg_trace_stream(result: Any) -> dict:
    stream = _safe_get(result, "stream_name", default="?")
    steps = _safe_get(result, "path", default=[])
    count = len(steps)
    first = steps[0].get("equipment_name", "?") if steps else "?"
    last = steps[-1].get("equipment_name", "?") if steps else "?"
    return {
        "summary_text": f"Stream '{stream}': {count} steps from {first} to {last}",
        "metrics": {"step_count": count},
    }


def _summarize_kg_query_equipment(result: Any) -> dict:
    query = _safe_get(result, "query", default="?")
    matches = _safe_get(result, "matches", default=[])
    names = [m.get("name", "?") for m in matches[:3]]
    return {
        "summary_text": f"{len(matches)} equipment matched '{query}': {', '.join(names)}",
        "metrics": {"match_count": len(matches)},
    }


def _summarize_kg_upstream_sensors(result: Any) -> dict:
    node = _safe_get(result, "node_id", default="?")
    total = _safe_get(result, "total_upstream_sensors", default=0)
    return {
        "summary_text": f"{total} upstream sensors for '{node}'",
        "metrics": {"upstream_count": total},
    }


def _summarize_kg_find_process_path(result: Any) -> dict:
    from_node = _safe_get(result, "from_node", default="?")
    to_node = _safe_get(result, "to_node", default="?")
    hops = _safe_get(result, "path", default=[])
    return {
        "summary_text": f"Path from {from_node} to {to_node}: {len(hops)} hops",
        "metrics": {"hop_count": len(hops)},
    }


def _summarize_kg_related_sensors(result: Any) -> dict:
    tag = _safe_get(result, "tag_name", default="?")
    co = _safe_get(result, "co_located_sensors", default=[])
    pair = _safe_get(result, "symmetric_pair_sensor", default=None)
    sys = _safe_get(result, "same_system_sensors", default=[])
    pair_str = pair if pair else "none"
    return {
        "summary_text": f"Sensor {tag}: {len(co)} co-located, pair={pair_str}, {len(sys)} same-system",
        "metrics": {"co_located": len(co), "same_system": len(sys)},
    }


def _summarize_kg_system_sensors(result: Any) -> dict:
    system = _safe_get(result, "system_name", default="?")
    equipment = _safe_get(result, "equipment", default=[])
    total_sensors = sum(len(e.get("sensors", [])) for e in equipment)
    return {
        "summary_text": f"System '{system}': {len(equipment)} equipment, {total_sensors} sensors",
        "metrics": {"equipment_count": len(equipment), "total_sensors": total_sensors},
    }


def _summarize_docs_search(result: Any) -> dict:
    if not isinstance(result, list):
        return _summarize_generic(result)
    count = len(result)
    if count > 0:
        top = result[0]
        title = top.get("title", "?")
        section = top.get("section_title", "?")
        score = top.get("relevance_score", "?")
        return {
            "summary_text": f"{count} docs matched, top: {title}, section: {section} (score={score})",
            "metrics": {"match_count": count},
        }
    return {"summary_text": "0 docs matched", "metrics": {"match_count": 0}}


def _summarize_docs_list(result: Any) -> dict:
    count = len(result) if isinstance(result, list) else 0
    return {"summary_text": f"{count} documents listed", "metrics": {"doc_count": count}}


def _summarize_docs_get(result: Any) -> dict:
    title = _safe_get(result, "title", default="?")
    rev = _safe_get(result, "revision", default="?")
    text = _safe_get(result, "full_text", default="")
    return {
        "summary_text": f"Retrieved '{title}' (Rev {rev}), {len(text)} chars",
        "metrics": {"text_length": len(text)},
    }


_SUMMARIZERS = {
    "historian_list_tags": _summarize_list_tags,
    "historian_search_tags": _summarize_search_tags,
    "historian_get_data_range": _summarize_data_range,
    "historian_get_tag_data": _summarize_tag_data,
    "historian_get_statistics": _summarize_statistics,
    "historian_plot_tags": _summarize_plot_tags,
    "alarm_query": _summarize_alarm_query,
    "alarm_get_statistics": _summarize_alarm_statistics,
    "alarm_get_active_at": _summarize_alarm_active_at,
    "alarm_search_context": _summarize_alarm_search_context,
    "alarm_detect_flood": _summarize_alarm_detect_flood,
    "kg_trace_stream": _summarize_kg_trace_stream,
    "kg_query_equipment": _summarize_kg_query_equipment,
    "kg_get_upstream_sensors": _summarize_kg_upstream_sensors,
    "kg_find_process_path": _summarize_kg_find_process_path,
    "kg_get_related_sensors": _summarize_kg_related_sensors,
    "kg_get_system_sensors": _summarize_kg_system_sensors,
    "docs_search": _summarize_docs_search,
    "docs_list_documents": _summarize_docs_list,
    "docs_get_document": _summarize_docs_get,
}


# ---------------------------------------------------------------------------
# Provenance helpers
# ---------------------------------------------------------------------------

def _compute_file_sha256(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


def _capture_provenance(question: str) -> dict:
    """Capture data-source versions at session start."""
    prov: dict[str, Any] = {
        "question": question,
        "start_time": datetime.now(timezone.utc).isoformat(),
    }

    if KG_PATH.exists():
        try:
            prov["kg_file_sha256"] = _compute_file_sha256(KG_PATH)
        except OSError:
            prov["kg_file_sha256"] = "(unreadable)"

    if RAG_DOCS_DIR.exists():
        try:
            files = list(RAG_DOCS_DIR.glob("*.md"))
            prov["doc_set_file_count"] = len(files)
            prov["doc_set_total_bytes"] = sum(f.stat().st_size for f in files)
        except OSError:
            prov["doc_set_file_count"] = "(unreadable)"

    prov["model"] = os.environ.get("CLAUDE_MODEL", "(unknown)")

    return prov


# ---------------------------------------------------------------------------
# TraceSession
# ---------------------------------------------------------------------------

class TraceSession:
    """Manages a single audit trace run."""

    def __init__(self, run_id: str, question: str, trace_dir: Path):
        self.run_id = run_id
        self.question = question
        self.trace_dir = trace_dir
        self.raw_dir = trace_dir / "raw"
        self.trace_file = trace_dir / "trace.jsonl"
        self.step_counter = 0
        self.finalized = False
        self._provenance = _capture_provenance(question)

        self.trace_dir.mkdir(parents=True, exist_ok=True)
        self.raw_dir.mkdir(exist_ok=True)

    def record_tool_call(
        self,
        tool_name: str,
        arguments: dict,
        result: Any,
        duration_ms: float,
        success: bool,
        error: str | None = None,
    ) -> int:
        self.step_counter += 1
        step = self.step_counter

        summary_data = summarize_result(tool_name, result)

        raw_filename = f"step_{step:03d}.json"
        raw_path = self.raw_dir / raw_filename
        raw_json = json.dumps(result, indent=2, default=str)
        raw_path.write_text(raw_json, encoding="utf-8")
        raw_sha256 = hashlib.sha256(raw_json.encode("utf-8")).hexdigest()

        entry = {
            "type": "tool_call",
            "step": step,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "tool_name": tool_name,
            "arguments": arguments,
            "duration_ms": round(duration_ms, 2),
            "success": success,
            "error": error,
            "summary": summary_data["summary_text"],
            "metrics": summary_data["metrics"],
            "raw_result_file": f"raw/{raw_filename}",
            "raw_result_sha256": raw_sha256,
        }

        self._append_entry(entry)
        return step

    def record_reasoning(
        self,
        reasoning_type: str,
        text: str,
        evidence_steps: list[int] | None = None,
        confidence: float | None = None,
    ) -> int:
        self.step_counter += 1
        step = self.step_counter

        entry = {
            "type": "reasoning",
            "step": step,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "reasoning_type": reasoning_type,
            "text": text,
            "evidence_steps": evidence_steps or [],
            "confidence": confidence,
        }

        self._append_entry(entry)
        return step

    def finalize(self) -> dict:
        if self.finalized:
            return self._read_meta()

        trace_hash = hashlib.sha256()

        if self.trace_file.exists():
            with open(self.trace_file, "rb") as f:
                for chunk in iter(lambda: f.read(8192), b""):
                    trace_hash.update(chunk)

        raw_files = sorted(self.raw_dir.glob("step_*.json"))
        for rf in raw_files:
            file_hash = _compute_file_sha256(rf)
            trace_hash.update(file_hash.encode("utf-8"))

        meta = {
            **self._provenance,
            "run_id": self.run_id,
            "end_time": datetime.now(timezone.utc).isoformat(),
            "total_steps": self.step_counter,
            "tool_calls": self._count_entries("tool_call"),
            "reasoning_entries": self._count_entries("reasoning"),
            "trace_sha256": trace_hash.hexdigest(),
            "finalized": True,
        }

        meta_path = self.trace_dir / "session_meta.json"
        meta_path.write_text(json.dumps(meta, indent=2, default=str), encoding="utf-8")

        self.finalized = True
        logger.info("Trace finalized: run_id=%s, steps=%d, hash=%s",
                     self.run_id, self.step_counter, meta["trace_sha256"])
        return meta

    def _append_entry(self, entry: dict) -> None:
        with open(self.trace_file, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry, default=str) + "\n")

    def _count_entries(self, entry_type: str) -> int:
        count = 0
        if self.trace_file.exists():
            with open(self.trace_file, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if line:
                        try:
                            e = json.loads(line)
                            if e.get("type") == entry_type:
                                count += 1
                        except json.JSONDecodeError:
                            pass
        return count

    def _read_meta(self) -> dict:
        meta_path = self.trace_dir / "session_meta.json"
        if meta_path.exists():
            return json.loads(meta_path.read_text(encoding="utf-8"))
        return {}


# ---------------------------------------------------------------------------
# Auto-render report
# ---------------------------------------------------------------------------

def _auto_render_report(trace_dir: Path) -> tuple[str | None, str | None]:
    """Render report.md and summary.md after finalization.

    Returns (report_path, summary_path); either may be None on failure.
    """
    report_path = None
    summary_path = None
    try:
        from render_audit import render_report, render_summary
        report_path = render_report(str(trace_dir))
        summary_path = render_summary(str(trace_dir))
    except Exception as exc:
        logger.warning("Auto-render failed for %s: %s", trace_dir, exc)
    return report_path, summary_path


# ---------------------------------------------------------------------------
# Module-level session management
# ---------------------------------------------------------------------------

_active_session: TraceSession | None = None


def start_session(question: str) -> dict:
    """Start a new trace session. Auto-finalizes any previous session."""
    global _active_session

    if _active_session is not None and not _active_session.finalized:
        _active_session.finalize()
        _auto_render_report(_active_session.trace_dir)
        logger.info("Auto-finalized previous session: %s", _active_session.run_id)

    now = datetime.now(timezone.utc)
    short_uuid = uuid.uuid4().hex[:6]
    run_id = f"{now.strftime('%Y%m%d_%H%M%S')}_{short_uuid}"

    trace_dir = TRACES_DIR / run_id
    _active_session = TraceSession(run_id, question, trace_dir)

    logger.info("Trace session started: run_id=%s, question=%s", run_id, question[:100])

    return {
        "run_id": run_id,
        "trace_dir": str(trace_dir),
        "message": f"Audit session started. Run ID: {run_id}",
    }


def end_session() -> dict:
    """Finalize the active session, seal it, and auto-generate reports."""
    global _active_session

    if _active_session is None:
        return {"error": "No active audit session."}

    meta = _active_session.finalize()
    report_path, summary_path = _auto_render_report(_active_session.trace_dir)

    result = {
        "run_id": _active_session.run_id,
        "trace_sha256": meta.get("trace_sha256", ""),
        "total_steps": meta.get("total_steps", 0),
        "tool_calls": meta.get("tool_calls", 0),
        "reasoning_entries": meta.get("reasoning_entries", 0),
        "trace_dir": str(_active_session.trace_dir),
        "report": report_path,
        "summary": summary_path,
        "message": "Audit session finalized and sealed.",
    }

    _active_session = None
    return result


def get_active_session() -> TraceSession | None:
    return _active_session


def ensure_session() -> TraceSession:
    """Return the active session, auto-starting one if none exists."""
    global _active_session
    if _active_session is None:
        start_session("(auto-started)")
    return _active_session
