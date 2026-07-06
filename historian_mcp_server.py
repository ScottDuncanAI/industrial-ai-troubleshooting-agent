"""
Boiler Historian MCP Server

Entry point for all tool calls from Claude Code. This file is responsible
for two things only: declaring tools (list_tools) and routing calls to the
right implementation module (call_tool). All query logic lives elsewhere.

  historian_tools.py  —  historian_* tools  (DuckDB process data)
  alarm_tools.py      —  alarm_* tools      (DuckDB alarm log)
  kg_tools.py         —  kg_* tools         (knowledge graph wrappers)
  rag_tools.py        —  docs_* tools       (ChromaDB vector search)

Start automatically via Claude Code's MCP configuration (see CLAUDE.md).
Do NOT run this manually during normal use — Claude Code manages the process.
"""

import os
import json
import logging
import time
import traceback
from datetime import datetime
from typing import Any

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp import types

from historian_tools import (
    tool_list_tags, tool_search_tags, tool_get_data_range,
    tool_get_tag_data, tool_get_statistics, tool_plot_tags,
    PLOTS_DIR,
)
from alarm_tools import (
    tool_alarm_query, tool_alarm_get_statistics, tool_alarm_get_active_at,
    tool_alarm_search_context, tool_alarm_detect_flood,
)
from kg_tools import (
    tool_kg_trace_stream, tool_kg_query_equipment, tool_kg_get_upstream_sensors,
    tool_kg_find_process_path, tool_kg_get_related_sensors, tool_kg_get_system_sensors,
)
from rag_tools import rag_search, rag_list_documents, rag_get_document
import audit_trace

# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))

logging.basicConfig(
    filename=os.path.join(PROJECT_DIR, "historian_mcp.log"),
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
)
logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# MCP Server
# ---------------------------------------------------------------------------
server = Server("boiler-historian")


@server.list_tools()
async def list_tools() -> list[types.Tool]:
    return [
        # ── Historian ────────────────────────────────────────────────────────
        types.Tool(
            name="historian_list_tags",
            description=(
                "List all available historian tags with their descriptions, units, "
                "sensor type, and normal operating range. Use this to discover which "
                "tag names to use for queries."
            ),
            inputSchema={"type": "object", "properties": {}, "required": []},
        ),
        types.Tool(
            name="historian_search_tags",
            description=(
                "Search historian tags by keyword. Matches against tag name, "
                "description, and sensor type. Useful when you know what you're "
                "looking for but not the exact tag name. "
                "Example queries: 'steam temperature', 'pressure', 'fan flow', 'oxygen'."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "Keyword to search for (case-insensitive)"},
                },
                "required": ["query"],
            },
        ),
        types.Tool(
            name="historian_get_data_range",
            description=(
                "Return the earliest and latest timestamp available in the historian "
                "database. ALWAYS call this first when the user asks about a relative "
                "time period (e.g. 'past 12 hours', 'last day') so you can compute "
                "the correct absolute start/end times."
            ),
            inputSchema={"type": "object", "properties": {}, "required": []},
        ),
        types.Tool(
            name="historian_get_tag_data",
            description=(
                "Retrieve time-series data for one or more tags over a time range. "
                "Returns a JSON array of {timestamp, <tag>: value} objects. "
                "Use downsample_minutes to reduce data volume for long time ranges "
                "(e.g. 1 minute averages instead of raw 5-second data)."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "tag_names": {
                        "type": "array", "items": {"type": "string"},
                        "description": "List of tag names to retrieve (e.g. ['TE_8332A', 'PT_8313A'])",
                    },
                    "start_time": {"type": "string", "description": "Start of time range as ISO datetime string"},
                    "end_time":   {"type": "string", "description": "End of time range as ISO datetime string"},
                    "downsample_minutes": {
                        "type": "integer",
                        "description": (
                            "Optional: aggregate raw 5-second data into N-minute averages. "
                            "Recommended for time ranges > 1 hour to avoid large responses."
                        ),
                    },
                },
                "required": ["tag_names", "start_time", "end_time"],
            },
        ),
        types.Tool(
            name="historian_get_statistics",
            description=(
                "Compute summary statistics (min, max, mean, std deviation, count) "
                "for one or more tags over a time range. Useful for answering questions "
                "like 'what was the average steam temperature yesterday?' or "
                "'how much did the furnace pressure vary over the last 6 hours?'."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "tag_names":  {"type": "array", "items": {"type": "string"}, "description": "List of tag names"},
                    "start_time": {"type": "string", "description": "Start of time range as ISO datetime string"},
                    "end_time":   {"type": "string", "description": "End of time range as ISO datetime string"},
                },
                "required": ["tag_names", "start_time", "end_time"],
            },
        ),
        types.Tool(
            name="historian_plot_tags",
            description=(
                "Generate a time-series plot for one or more tags and save it as a PNG "
                "file. Returns the path to the saved image. The user can open it to view "
                "the chart. Use downsample_minutes to keep plots readable for long ranges."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "tag_names":  {"type": "array", "items": {"type": "string"}, "description": "List of tag names to plot"},
                    "start_time": {"type": "string", "description": "Start of time range as ISO datetime string"},
                    "end_time":   {"type": "string", "description": "End of time range as ISO datetime string"},
                    "title":      {"type": "string", "description": "Optional chart title"},
                    "downsample_minutes": {"type": "integer", "description": "Optional: average data into N-minute intervals"},
                    "show_normal_range": {
                        "type": "boolean",
                        "description": "If true, draw a shaded band showing the normal operating range. Default false.",
                    },
                },
                "required": ["tag_names", "start_time", "end_time"],
            },
        ),
        # ── Knowledge Graph ──────────────────────────────────────────────────
        types.Tool(
            name="kg_trace_stream",
            description=(
                "Trace the complete path of a process stream through the boiler. "
                "Returns an ordered list of equipment nodes along the stream with sensors at each step. "
                "Available streams: PrimaryAir, SecondaryAir, ReturnAir, FlueGas, Solids, "
                "FeedWater, Steam, DesuperheatingWater, Coal."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "stream_name": {"type": "string", "description": "Name of the stream to trace (e.g. 'Steam', 'FlueGas')"},
                },
                "required": ["stream_name"],
            },
        ),
        types.Tool(
            name="kg_query_equipment",
            description=(
                "Find equipment nodes in the boiler by natural-language name. "
                "Returns matching equipment with attached sensors, process streams, "
                "and upstream/downstream connections. "
                "Examples: 'furnace', 'induced draft fan', 'economizer', 'left cyclone'."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "Natural-language equipment name or description"},
                },
                "required": ["query"],
            },
        ),
        types.Tool(
            name="kg_get_upstream_sensors",
            description=(
                "Return all sensors on equipment upstream of a given tag or equipment, "
                "ordered by hop distance. Use this to find what to investigate when a "
                "sensor is anomalous — e.g. 'what is upstream of TE_8332A?'."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "node_id": {"type": "string", "description": "A tag name (e.g. 'TE_8332A') or equipment name"},
                },
                "required": ["node_id"],
            },
        ),
        types.Tool(
            name="kg_find_process_path",
            description=(
                "Find the process path between two pieces of equipment. "
                "Returns each hop with its edge type and stream. "
                "Example: from='primary fan', to='steam outlet'."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "from_node": {"type": "string", "description": "Starting equipment (natural language)"},
                    "to_node":   {"type": "string", "description": "Destination equipment (natural language)"},
                },
                "required": ["from_node", "to_node"],
            },
        ),
        types.Tool(
            name="kg_get_related_sensors",
            description=(
                "Return sensors related to a given tag: co-located sensors on the same equipment, "
                "symmetric left/right pair partner, sensors in the same system, "
                "and whether this sensor is part of a control loop."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "tag_name": {"type": "string", "description": "Tag name to find related sensors for"},
                },
                "required": ["tag_name"],
            },
        ),
        types.Tool(
            name="kg_get_system_sensors",
            description=(
                "Return all sensors grouped by equipment within a named system. "
                "Systems: Primary Air, Secondary Air, Combustion, Flue Gas & Heat Recovery, "
                "Draft & Exhaust, Steam Generation & Superheating."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "system_name": {"type": "string", "description": "System name (e.g. 'combustion', 'draft', 'primary air')"},
                },
                "required": ["system_name"],
            },
        ),
        # ── RAG Document Search ──────────────────────────────────────────────
        types.Tool(
            name="docs_search",
            description=(
                "Semantic search across all plant documentation (SOPs, datasheets, "
                "maintenance procedures, troubleshooting guides, control loop descriptions, "
                "safety procedures). Returns the most relevant document sections for a query. "
                "Optionally filter by doc_type, equipment_id, or sensor_tag to narrow the search."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "Natural-language search query"},
                    "doc_type": {
                        "type": "string",
                        "description": "Optional: sop, datasheet, maintenance, troubleshooting, controls, safety",
                        "enum": ["sop", "datasheet", "maintenance", "troubleshooting", "controls", "safety"],
                    },
                    "equipment_id": {
                        "type": "string",
                        "description": "Optional: restrict to documents about a specific equipment node ID",
                    },
                    "sensor_tag": {
                        "type": "string",
                        "description": "Optional: restrict to documents referencing a specific sensor tag",
                    },
                    "top_k": {"type": "integer", "description": "Number of results to return (default 5, max 10)", "default": 5},
                },
                "required": ["query"],
            },
        ),
        types.Tool(
            name="docs_list_documents",
            description=(
                "List all available plant documents in the RAG index. "
                "Returns doc_id, title, doc_type, revision, equipment, and sensor tags for each document. "
                "Use this to browse what documentation is available or to confirm a doc_id."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "doc_type": {
                        "type": "string",
                        "description": "Optional: filter to sop, datasheet, maintenance, troubleshooting, controls, safety",
                        "enum": ["sop", "datasheet", "maintenance", "troubleshooting", "controls", "safety"],
                    },
                },
                "required": [],
            },
        ),
        types.Tool(
            name="docs_get_document",
            description=(
                "Retrieve the complete text of a specific plant document by its doc_id. "
                "Use this when docs_search returns a relevant chunk but you need the full "
                "procedure, datasheet, or guide for complete context. "
                "Always include citation details (title, revision) when presenting content to the user."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "doc_id": {
                        "type": "string",
                        "description": (
                            "The document identifier. Examples: 'trb_high_steam_temperature', "
                            "'ds_induced_draft_fan', 'ctrl_alarm_setpoint_register', 'cold_start_procedure'"
                        ),
                    },
                },
                "required": ["doc_id"],
            },
        ),
        # ── Alarm Log ────────────────────────────────────────────────────────
        types.Tool(
            name="alarm_query",
            description=(
                "Fetch DCS alarm events from the alarm log within a time window. "
                "Returns one row per alarm lifecycle (activation through clearance). "
                "Filter by tag, alarm level, priority, or state. "
                "Use alarm_search_context instead when investigating an anomaly at a known timestamp."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "start_time": {"type": "string", "description": "Start of time window as ISO datetime string"},
                    "end_time":   {"type": "string", "description": "End of time window as ISO datetime string"},
                    "tag_names":  {"type": "array", "items": {"type": "string"}, "description": "Optional: restrict to these tags"},
                    "alarm_level": {"type": "string", "description": "Optional: Lo, Hi, LoLo, HiHi, HiHiHi, Alert, Alarm, Trip"},
                    "priority": {
                        "type": "string",
                        "description": "Optional: Critical, High, Medium, Low",
                        "enum": ["Critical", "High", "Medium", "Low"],
                    },
                    "state": {
                        "type": "string",
                        "description": "ACTIVE, CLEARED, UNACKNOWLEDGED, or ANY (default)",
                        "enum": ["ACTIVE", "CLEARED", "UNACKNOWLEDGED", "ANY"],
                    },
                    "limit": {"type": "integer", "description": "Maximum rows to return (default 100)"},
                },
                "required": ["start_time", "end_time"],
            },
        ),
        types.Tool(
            name="alarm_get_statistics",
            description=(
                "Compute alarm KPIs for a time window: total count, breakdown by tag/level/priority, "
                "average and maximum alarm duration, acknowledgement rate, and top 5 most frequent "
                "tag+level combinations. Use this for shift reports or alarm rationalization."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "start_time": {"type": "string", "description": "Start of time window as ISO datetime string"},
                    "end_time":   {"type": "string", "description": "End of time window as ISO datetime string"},
                    "tag_names":  {"type": "array", "items": {"type": "string"}, "description": "Optional: restrict to these tags"},
                },
                "required": ["start_time", "end_time"],
            },
        ),
        types.Tool(
            name="alarm_get_active_at",
            description=(
                "Return all alarms that were in the ACTIVE state at a specific moment in time. "
                "An alarm is active if it was activated before that moment and not yet cleared. "
                "Essential for building a post-incident timeline — e.g. 'what was in alarm at 09:20?'"
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "timestamp": {"type": "string", "description": "The point in time to check, as ISO datetime string"},
                    "tag_names": {"type": "array", "items": {"type": "string"}, "description": "Optional: restrict to these tags"},
                },
                "required": ["timestamp"],
            },
        ),
        types.Tool(
            name="alarm_search_context",
            description=(
                "Find all alarms within ±window_minutes of a focal timestamp, ordered by "
                "proximity to that moment. This is the primary tool for troubleshooting — "
                "call it immediately after identifying an anomaly timestamp to get the alarm "
                "context. Returns a 'minutes_offset' field (negative = before event, positive = after)."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "timestamp": {"type": "string", "description": "The focal event time as ISO datetime string"},
                    "window_minutes": {"type": "integer", "description": "Search ±this many minutes (default 30)"},
                    "tag_names": {"type": "array", "items": {"type": "string"}, "description": "Optional: restrict to these tags"},
                },
                "required": ["timestamp"],
            },
        ),
        types.Tool(
            name="alarm_detect_flood",
            description=(
                "Detect alarm flood periods within a time window. Per ANSI/ISA-18.2, a flood "
                "is defined as more than threshold_per_10min alarm activations in any 10-minute "
                "window. Returns each flood window with its alarm count and contributing tags."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "start_time": {"type": "string", "description": "Start of time window as ISO datetime string"},
                    "end_time":   {"type": "string", "description": "End of time window as ISO datetime string"},
                    "threshold_per_10min": {
                        "type": "integer",
                        "description": "Alarms per 10-minute window that defines a flood (default 10, per ISA-18.2)",
                    },
                },
                "required": ["start_time", "end_time"],
            },
        ),

        # ── Audit Trail ─────────────────────────────────────────────────────
        types.Tool(
            name="audit_start_session",
            description=(
                "Start a new audit trail session for root cause analysis. "
                "Sets the investigation question text and returns a run_id. "
                "Note: tracing starts automatically on the first tool call even "
                "without this — call it to record the user's question explicitly."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "question": {
                        "type": "string",
                        "description": "The user's original question or investigation prompt",
                    },
                },
                "required": ["question"],
            },
        ),
        types.Tool(
            name="audit_end_session",
            description=(
                "End the active audit trail session and finalize the trace. "
                "Computes a SHA-256 hash of the trace for tamper-evidence. "
                "Note: sessions auto-finalize when a new one starts or when "
                "the report is generated — this is a manual override."
            ),
            inputSchema={"type": "object", "properties": {}, "required": []},
        ),
        types.Tool(
            name="audit_log_reasoning",
            description=(
                "Log a reasoning entry into the active audit trace. "
                "Use this to record hypotheses before investigating, conclusions after, "
                "observations during analysis, and rejections of ruled-out hypotheses. "
                "Each entry can reference evidence_steps (step numbers from prior tool calls). "
                "Essential for the audit report — every hypothesis and conclusion "
                "must be logged here to appear in the final report."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "reasoning_type": {
                        "type": "string",
                        "enum": ["hypothesis", "conclusion", "observation", "rejection", "corrective_action"],
                        "description": "Type of reasoning entry",
                    },
                    "text": {
                        "type": "string",
                        "description": "The reasoning content",
                    },
                    "evidence_steps": {
                        "type": "array",
                        "items": {"type": "integer"},
                        "description": "Step numbers from prior tool calls that support this reasoning",
                    },
                    "confidence": {
                        "type": "number",
                        "description": "Confidence level 0.0-1.0, used for conclusions",
                    },
                },
                "required": ["reasoning_type", "text"],
            },
        ),
    ]


# ---------------------------------------------------------------------------
# Tool call dispatcher
# ---------------------------------------------------------------------------
@server.call_tool()
async def call_tool(name: str, arguments: dict[str, Any]) -> list[types.TextContent]:
    try:
        logger.info("tool=%s args=%s", name, list(arguments.keys()))

        # ── Audit tools (not traced themselves) ──────────────────────────
        if name == "audit_start_session":
            result = audit_trace.start_session(arguments["question"])
            return [types.TextContent(type="text", text=json.dumps(result, indent=2, default=str))]
        elif name == "audit_end_session":
            result = audit_trace.end_session()
            return [types.TextContent(type="text", text=json.dumps(result, indent=2, default=str))]
        elif name == "audit_log_reasoning":
            session = audit_trace.get_active_session()
            if session is None:
                session = audit_trace.ensure_session()
            step = session.record_reasoning(
                arguments["reasoning_type"],
                arguments["text"],
                arguments.get("evidence_steps"),
                arguments.get("confidence"),
            )
            result = {"step": step, "message": "Reasoning recorded."}
            return [types.TextContent(type="text", text=json.dumps(result, indent=2, default=str))]

        # ── Domain tools (always traced) ─────────────────────────────────
        session = audit_trace.ensure_session()
        t0 = time.perf_counter()

        # Historian
        if name == "historian_list_tags":
            result = tool_list_tags()
        elif name == "historian_search_tags":
            result = tool_search_tags(arguments["query"])
        elif name == "historian_get_data_range":
            result = tool_get_data_range()
        elif name == "historian_get_tag_data":
            result = tool_get_tag_data(
                arguments["tag_names"], arguments["start_time"], arguments["end_time"],
                arguments.get("downsample_minutes"),
            )
        elif name == "historian_get_statistics":
            result = tool_get_statistics(
                arguments["tag_names"], arguments["start_time"], arguments["end_time"],
            )
        elif name == "historian_plot_tags":
            result = tool_plot_tags(
                arguments["tag_names"], arguments["start_time"], arguments["end_time"],
                arguments.get("title"), arguments.get("downsample_minutes"),
                arguments.get("show_normal_range", False),
            )

        # Knowledge Graph
        elif name == "kg_trace_stream":
            result = tool_kg_trace_stream(arguments["stream_name"])
        elif name == "kg_query_equipment":
            result = tool_kg_query_equipment(arguments["query"])
        elif name == "kg_get_upstream_sensors":
            result = tool_kg_get_upstream_sensors(arguments["node_id"])
        elif name == "kg_find_process_path":
            result = tool_kg_find_process_path(arguments["from_node"], arguments["to_node"])
        elif name == "kg_get_related_sensors":
            result = tool_kg_get_related_sensors(arguments["tag_name"])
        elif name == "kg_get_system_sensors":
            result = tool_kg_get_system_sensors(arguments["system_name"])

        # RAG Document Search
        elif name == "docs_search":
            result = rag_search(
                arguments["query"],
                doc_type=arguments.get("doc_type"),
                equipment_id=arguments.get("equipment_id"),
                sensor_tag=arguments.get("sensor_tag"),
                top_k=int(arguments.get("top_k", 5)),
            )
        elif name == "docs_list_documents":
            result = rag_list_documents(arguments.get("doc_type"))
        elif name == "docs_get_document":
            result = rag_get_document(arguments["doc_id"])

        # Alarm Log
        elif name == "alarm_query":
            result = tool_alarm_query(
                arguments["start_time"], arguments["end_time"],
                tag_names=arguments.get("tag_names"),
                alarm_level=arguments.get("alarm_level"),
                priority=arguments.get("priority"),
                state=arguments.get("state", "ANY"),
                limit=int(arguments.get("limit", 100)),
            )
        elif name == "alarm_get_statistics":
            result = tool_alarm_get_statistics(
                arguments["start_time"], arguments["end_time"],
                tag_names=arguments.get("tag_names"),
            )
        elif name == "alarm_get_active_at":
            result = tool_alarm_get_active_at(
                arguments["timestamp"],
                tag_names=arguments.get("tag_names"),
            )
        elif name == "alarm_search_context":
            result = tool_alarm_search_context(
                arguments["timestamp"],
                window_minutes=int(arguments.get("window_minutes", 30)),
                tag_names=arguments.get("tag_names"),
            )
        elif name == "alarm_detect_flood":
            result = tool_alarm_detect_flood(
                arguments["start_time"], arguments["end_time"],
                threshold_per_10min=int(arguments.get("threshold_per_10min", 10)),
            )

        else:
            result = {"error": f"Unknown tool: {name}"}

        duration_ms = (time.perf_counter() - t0) * 1000
        session.record_tool_call(
            tool_name=name,
            arguments=arguments,
            result=result,
            duration_ms=duration_ms,
            success=True,
        )

        return [types.TextContent(type="text", text=json.dumps(result, indent=2, default=str))]

    except Exception as exc:
        duration_ms = (time.perf_counter() - t0) * 1000 if "t0" in locals() else 0
        logger.error("tool=%s failed", name, exc_info=True)

        session = audit_trace.get_active_session()
        if session is not None:
            session.record_tool_call(
                tool_name=name,
                arguments=arguments,
                result=None,
                duration_ms=duration_ms,
                success=False,
                error=str(exc),
            )

        error_msg = {"error": str(exc), "traceback": traceback.format_exc()}
        return [types.TextContent(type="text", text=json.dumps(error_msg, indent=2))]


# ---------------------------------------------------------------------------
# Startup helpers
# ---------------------------------------------------------------------------
def _cleanup_old_plots(max_age_days: int = 7) -> None:
    if not os.path.isdir(PLOTS_DIR):
        return
    cutoff = datetime.now().timestamp() - max_age_days * 86400
    for fname in os.listdir(PLOTS_DIR):
        if fname.endswith(".png"):
            fpath = os.path.join(PLOTS_DIR, fname)
            try:
                if os.path.getmtime(fpath) < cutoff:
                    os.remove(fpath)
                    logger.info("Deleted old plot: %s", fname)
            except OSError as e:
                logger.warning("Could not remove old plot %s: %s", fname, e)


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------
async def main():
    logger.info("MCP server starting up")
    _cleanup_old_plots()
    try:
        async with stdio_server() as (read_stream, write_stream):
            logger.info("stdio_server ready, entering run loop")
            await server.run(
                read_stream,
                write_stream,
                server.create_initialization_options(),
            )
    except Exception:
        logger.exception("Unhandled exception in MCP server main loop")


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
