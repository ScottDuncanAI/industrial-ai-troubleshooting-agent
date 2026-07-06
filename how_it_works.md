# How the Boiler Historian Application Works

This document explains every piece of the system in plain terms — what each file does,
how all the parts connect, and exactly what happens when you ask Claude a question.

---

## The Big Picture

At its core, this is a **natural-language interface to a coal-fired boiler**. You type a
question in plain English, and Claude figures out which databases to query, runs the
queries, reads the results, cross-references plant documents, and gives you an answer
grounded in real data.

The system has three layers:

```
You (the user)
     ↕  chat messages
Claude Code (the AI)
     ↕  tool calls over stdio
MCP Server (Python, always running in the background)
     ↕  reads data from...
Four data stores: Historian DB · Alarm DB · Knowledge Graph · Document Library
```

---

## What "MCP" Means

MCP stands for **Model Context Protocol** — a standard way for an AI assistant to call
external tools. Think of it like a USB interface: Claude doesn't care what's plugged in,
as long as it speaks the protocol.

When Claude Code starts, it reads `.mcp.json` at the project root, which tells it: "there
is a tool server called `boiler-historian` — launch this Python script to talk to it."
Claude Code starts the Python MCP server as a background process and communicates with
it by sending JSON messages over the command line (stdin/stdout). Every time Claude wants
real data, it sends a message to the server; the server queries the appropriate database
and sends the result back. Claude reads the result and uses it to form its answer.

---

## The Four Data Sources

| Source | File | What It Contains |
|--------|------|-----------------|
| Historian | `boiler_historian.duckdb` | 5 days of sensor readings — 30 tags, one reading every 5 seconds (86,400 rows total) |
| Alarm Log | `boiler_alarms.duckdb` | 6,005 alarm lifecycle records derived from the historian using ISA-18.2 rules |
| Knowledge Graph | `boiler_kg.json` | A map of all equipment, sensors, and how they connect physically and in control logic |
| Document Library | `RAG docs/` + `rag_vector_db/` | 62 plant documents (SOPs, datasheets, troubleshooting guides, etc.) indexed for semantic search |

---

## Runtime Files — What Each One Does

These are the files that must exist and run correctly for the application to work.

---

### `historian_mcp_server.py` — The Front Door

This is the **entry point** — the script that Claude Code launches and keeps running.
It does exactly two things:

1. **Declares all available tools** (`list_tools`): When the server starts, it tells
   Claude the complete menu of tools — their names, what they do, and what parameters
   they accept. Claude reads this menu once at startup.

2. **Routes incoming calls** (`call_tool`): When Claude decides to use a tool, it sends
   a message like `{ "tool": "historian_get_statistics", "args": { ... } }`. This file
   receives that message and calls the right Python function in the right module. It also
   wraps every call in **audit tracing** — every tool call is automatically logged to
   a trace file, including how long it took and whether it succeeded.

This file imports from all four implementation modules but contains no query logic itself.
Everything it does is routing and protocol handling.

---

### `historian_tools.py` — Sensor Data Access

This module handles all six `historian_*` tools. It connects to `boiler_historian.duckdb`
(a DuckDB database file) and runs SQL queries against it.

**What it can do:**
- `historian_list_tags` — returns a list of all 30 sensor tags with their description,
  units, and normal operating range
- `historian_search_tags` — searches tags by keyword (e.g. "steam temperature" → `TE_8332A`)
- `historian_get_data_range` — returns the earliest and latest timestamps in the database.
  **This is always the first call when a relative time is mentioned**, because the data is
  a static 5-day snapshot; "latest" is treated as "now"
- `historian_get_tag_data` — retrieves actual timestamped readings for one or more tags
  over a time range; can downsample into N-minute averages to reduce data volume
- `historian_get_statistics` — computes min, max, mean, and standard deviation for a tag
  over a time window, without returning all the raw rows
- `historian_plot_tags` — generates a PNG chart of one or more tags over time and saves
  it to the `plots/` folder. It uses `hmi_style.py` and `plot_helpers.py` to create a
  dark control-room themed chart with independent Y-axes per tag (like PI ProcessBook)

The module also contains `_validate_tags()` — a safety check that prevents queries for
tag names that don't exist, which would otherwise produce a silent empty result.

---

### `alarm_tools.py` — Alarm Log Access

This module handles all five `alarm_*` tools. It connects to `boiler_alarms.duckdb`,
which stores 6,005 alarm lifecycle records (each record covers one alarm from activation
through clearance).

**What it can do:**
- `alarm_query` — filtered list of alarms in a time window; filter by tag, alarm level
  (Hi/HiHi/Trip etc.), priority (Critical/High/Medium/Low), or state (Active/Cleared)
- `alarm_get_statistics` — KPI summary: total alarm count, acknowledgement rate, most
  frequent offenders, breakdown by level and priority
- `alarm_get_active_at` — snapshot of what alarms were active at a specific moment;
  useful for building post-incident timelines
- `alarm_search_context` — **primary troubleshooting tool**: given an anomaly timestamp,
  finds all alarms within ±30 minutes and sorts them by proximity. Returns a
  `minutes_offset` field so you can build a timeline of what alarmed when
- `alarm_detect_flood` — identifies periods with >10 alarms per 10 minutes (the ISA-18.2
  definition of an alarm flood), which indicates operators were overwhelmed

This module borrows `_parse_time()` from `historian_tools.py` to avoid duplicating the
timestamp parsing logic.

---

### `rag_tools.py` — Document Search

This module handles the three `docs_*` tools and powers the document library search.

**The RAG system explained:** RAG stands for "Retrieval-Augmented Generation." When you
ask about a procedure or specification, the system doesn't read all 62 documents —
instead, it uses a pre-built **vector database** (ChromaDB, stored in `rag_vector_db/`)
that holds every document broken into small chunks, each chunk converted into a list of
numbers (an "embedding") that captures its meaning. When you ask a question, the question
is also converted into numbers, and the database finds the chunks whose numbers are
closest — i.e., the most semantically similar content.

The embedding model is **BGE-small-en-v1.5** (from BAAI), a small but accurate model
that runs locally with no internet connection required. It's loaded once and kept in
memory.

**What it can do:**
- `docs_search` — semantic search across all 356 document chunks; can be filtered by
  document type (sop/troubleshooting/maintenance/etc.), by equipment ID, or by sensor tag
- `docs_list_documents` — lists all 62 documents in the index without running a search;
  useful for browsing available documentation
- `docs_get_document` — retrieves the **full text** of a specific document by its ID,
  by reading the original markdown file from `RAG docs/`. This is used when the search
  returns a relevant chunk but the full procedure context is needed

When `docs_get_document` is called, it first looks up the document's source file path
from the ChromaDB metadata, then reads the markdown file directly. The vector database
is the index; the `RAG docs/` folder is the source of truth.

---

### `kg_tools.py` — Knowledge Graph Access

This module wraps the `BoilerKnowledgeGraph` class (from `knowledge_graph.py`) in a
lazy-loading singleton, so the graph is only loaded from disk when first needed.

**What it can do:**
- `kg_trace_stream` — follows a named stream (e.g. "Steam", "FlueGas") end-to-end
  through all equipment, listing which sensors are at each step
- `kg_query_equipment` — finds equipment by natural-language name (e.g. "induced draft
  fan") and returns its upstream equipment, downstream equipment, attached sensors, and
  which process streams pass through it
- `kg_get_upstream_sensors` — given a sensor tag or equipment name, returns all sensors
  on equipment physically upstream, grouped by how many steps away they are. This is
  the core tool for root cause tracing: "what could have caused this sensor to be off?"
- `kg_find_process_path` — finds the physical route between two pieces of equipment,
  listing each hop with its stream and connection type
- `kg_get_related_sensors` — returns a tag's co-located sensors (same piece of equipment),
  its symmetric left/right pair partner (e.g. left cyclone vs. right cyclone), and other
  sensors in the same system
- `kg_get_system_sensors` — lists all sensors grouped by equipment within a named system
  (e.g. "Steam Generation & Superheating")

---

### `knowledge_graph.py` — The Graph Engine

This is the underlying graph library that `kg_tools.py` uses. It defines the
`BoilerKnowledgeGraph` class, which loads `boiler_kg.json` (a NetworkX node-link export)
into a directed multigraph in memory.

The graph has three types of nodes: **Equipment** (e.g. the furnace, the IDF),
**Sensor** (each tag), and **Boundary** (system boundaries). Edges describe relationships:
`PART_OF` links a sensor to its equipment, `FLOW_TO` links equipment in the process
flow direction, and `CONTROL` links sensors involved in control loops.

The class implements fuzzy name matching (so "induced draft fan" finds `induced_draft_fan`),
upstream traversal using graph shortest-path algorithms, and stream tracing using
pre-built stream path definitions stored in the JSON file.

---

### `audit_trace.py` — The Investigation Recorder

This module is the **audit trail system** — it records every tool call and every piece
of Claude's reasoning into a tamper-evident log.

**How it works:** When any domain tool is called (historian, alarm, knowledge graph, or
document search), the MCP server calls `audit_trace.ensure_session()` first. If no
active session exists, one is auto-started. Every tool call is written as a JSONL entry
to `traces/{run_id}/trace.jsonl`, and the full raw result is saved as a separate JSON
file in `traces/{run_id}/raw/step_NNN.json`. Tool results are summarized (not saved in
full) in the main trace file to keep it compact.

In addition to automatic tool call tracing, Claude can call `audit_log_reasoning` to
explicitly record its thinking — hypotheses before investigating, observations after
seeing data, conclusions with confidence levels, and rejections of ruled-out hypotheses.
This is the mechanism that makes the audit trail meaningful rather than just a list of
database queries.

At the end of an investigation, the trace is finalized with a SHA-256 hash for tamper
evidence, and `render_audit.py` converts the raw trace files into human-readable reports.

---

### `render_audit.py` — Report Generator

This standalone script reads a `traces/{run_id}/` directory and generates two files:

- `report.md` — the full detailed report: all tool calls in chronological order,
  every hypothesis and its outcome, all evidence cited, and appendices
- `summary.md` — a one-page executive summary with the root cause, investigation
  flow, and corrective action recommendations

This script is called automatically by `audit_trace.py` when a session is finalized,
and also invoked directly by the `/audit-trail` skill command.

---

### `hmi_style.py` — Chart Appearance

Defines the dark control-room color theme for all charts. It sets matplotlib's global
style using `rcParams` — dark background, muted grid lines, cyan/amber/green color
palette — to look like a real DCS operator interface. Applied once at server startup via
`historian_tools.py`.

---

### `plot_helpers.py` — Multi-Axis Plotting Engine

Implements the `plot_normalized()` function, which draws multiple sensor tags on a single
chart with independent Y-axes. Each tag gets its own axis scaled to its engineering range,
color-coded to match its legend label — exactly like PI ProcessBook "Multiple Scale" mode.
This makes it possible to overlay `TE_8332A` (°C) and `PTCA_8324` (MPa) on the same
chart without one trace dwarfing the other.

---

## Configuration Files — What Tells Claude How to Behave

### `CLAUDE.md` — The System Instruction Manual

This file is automatically loaded into Claude's context window at the start of every
conversation. Think of it as Claude's standing orders for this project. It contains:

- **Critical rules** (never guess tag names, always resolve relative time first, always
  cite documents, flag steam temperature anomalies proactively)
- **The key tags table** — normal ranges for all major sensors so Claude doesn't have
  to query the database to know if a reading is out of range
- **Query workflows** — step-by-step playbooks for each type of question (time-series,
  statistical, plotting, anomaly investigation, maintenance questions, etc.)
- **The root cause methodology** — the structured investigation protocol that requires
  logging hypotheses, ruling out symptoms vs. causes, and setting confidence levels
- **The data source reference** — schemas, alarm levels, document categories, available
  streams and systems for the knowledge graph
- **The downsampling guide** — when to use 1-min vs. 5-min vs. 15-min averages
- **Full MCP tool reference** — every tool with its parameters

Without `CLAUDE.md`, Claude would have no knowledge of this specific boiler, its sensors,
its normal operating ranges, or how to use the tools correctly. It is the single most
important configuration file in the system.

---

### `.mcp.json` — MCP Server Registration

This file (at the project root) tells Claude Code that the `boiler-historian` MCP server
exists and how to launch it:

```json
{
  "mcpServers": {
    "boiler-historian": {
      "type": "stdio",
      "command": "C:/Python311/python.exe",
      "args": ["C:/path/to/industrial-ai-troubleshooting-agent/historian_mcp_server.py"]
    }
  }
}
```

Claude Code reads this at startup, launches the Python script as a background process,
and keeps it running for the entire session. Without this file, Claude would have no
tools at all and could only answer from its training knowledge.

---

### `.claude/commands/` — Slash Command Skills

These markdown files define custom `/` commands that Claude executes as structured
multi-step workflows.

**`audit-trail.md`** (`/audit-trail`)
Generates the formatted audit report from a completed root cause investigation. Steps:
find the most recent trace folder, call `audit_end_session` if not yet finalized, run
`render_audit.py`, open the output files, and report clickable links to both reports.

**`ml-fault-detection.md`** (`/ml-fault-detection`)
Runs `ml_fault_detection.py` (Isolation Forest + XGBoost), then uses the MCP tools to
enrich the results: alarm context around each detected fault, knowledge graph upstream
tracing for the top feature-importance tags, and documentation cross-referencing.

**`mspc-analysis.md`** (`/mspc-analysis`)
Runs `mspc_analysis.py` (PCA-based Multivariate Statistical Process Control), then
interprets the T-squared and SPE results, opens contribution plots, and cross-references
alarm context for the worst fault events.

**`setup.md`** (`/setup`)
Guides first-time setup: checks Python version, installs requirements, builds the vector
database if missing, and writes the MCP server configuration to `.mcp.json`.

---

## What Enters Claude's Context Window

The context window is the "working memory" Claude has access to during a conversation.
Here is everything that gets loaded into it:

| Source | When Loaded | What It Contributes |
|--------|-------------|---------------------|
| `CLAUDE.md` | Every conversation start | Standing instructions, key tag table, workflows, tool reference |
| `MEMORY.md` | Every conversation start | User preferences and past feedback (stored in `~/.claude/projects/.../memory/`) |
| The conversation history | Accumulates | Your messages and Claude's responses |
| Tool call results | Each tool call | The JSON returned by the MCP server (statistics, alarm lists, chart paths, document chunks, etc.) |
| Skill file contents | When a `/command` is invoked | The step-by-step instructions from the relevant `.claude/commands/*.md` file |

What does **not** go into the context window:
- The raw database files — Claude never reads DuckDB files directly
- The knowledge graph JSON — loaded into the server's process memory, not into Claude's context
- The vector database — queried by the server, only the matching chunks are returned
- Full document text — only retrieved when `docs_get_document` is explicitly called
- The raw trace files in `traces/` — these are written to disk, not read back into context

---

## Step-by-Step Example: "Why Is Steam Temperature Dropping?"

Here is the complete sequence of events when you type that question:

---

**Step 0 — Your message arrives**

Claude receives: *"Why is steam temperature dropping?"*

Already in its context window: the full `CLAUDE.md` (standing orders), your conversation
history so far, and any prior tool results from this session.

---

**Step 1 — Start the audit session**

`audit_start_session("Why is steam temperature dropping?")`

The MCP server creates a new `traces/{run_id}/` folder, initializes `trace.jsonl`, and
records the question text and a SHA-256 fingerprint of the knowledge graph file and
document set. This establishes what version of data was used.

---

**Step 2 — Resolve "now"**

`historian_get_data_range()`

`historian_tools.py` connects to `boiler_historian.duckdb` and runs:
```sql
SELECT MIN(timestamp), MAX(timestamp), COUNT(*) FROM historian_data
```
Result: earliest = `2022-03-27 14:28:54`, latest = `2022-04-01 14:28:49`.

Claude now knows the dataset's "present moment." All relative time references will be
computed from `2022-04-01 14:28:49`.

`audit_trace.py` records this as step 1 in `trace.jsonl`.

---

**Step 3 — Log the first hypothesis**

`audit_log_reasoning(reasoning_type="hypothesis", text="Steam temperature TE_8332A may be below the 530°C floor — checking statistics over the most recent 12 hours to confirm and quantify the deviation.")`

This is recorded as a reasoning entry in the trace. It establishes *why* the next tool
call is being made before the call happens.

---

**Step 4 — Confirm the anomaly**

`historian_get_statistics(["TE_8332A"], "2022-04-01 02:28:49", "2022-04-01 14:28:49")`

`historian_tools.py` runs:
```sql
SELECT MIN(TE_8332A), MAX(TE_8332A), AVG(TE_8332A), STDDEV(TE_8332A), COUNT(TE_8332A)
FROM historian_data WHERE timestamp >= ? AND timestamp <= ?
```
Result: mean = 524.3°C, min = 511.1°C, max = 537.2°C. **This is below the 530°C floor.**
CLAUDE.md's anomaly rule triggers: Claude flags this explicitly even though the user
only asked "why."

The result enters the context window. The audit trace records it as step 2.

---

**Step 5 — Log observation, identify anomaly timestamp**

`audit_log_reasoning(reasoning_type="observation", text="TE_8332A mean is 524.3°C — 5.7°C below the 530°C normal minimum. Min reading was 511.1°C. Anomaly confirmed. Will investigate what changed in the upstream process.", evidence_steps=[2])`

---

**Step 6 — Get alarm context around the anomaly**

`alarm_search_context("2022-04-01 08:00:00", window_minutes=30)`

The approximate onset time of the drop (identified from the statistics trend) is used.
`alarm_tools.py` queries `boiler_alarms.duckdb`:
```sql
SELECT * FROM alarm_events
WHERE activated_at >= ? AND activated_at <= ?
ORDER BY activated_at
```
Result: within ±30 minutes of 08:00, there were 7 alarm events. The two closest to the
onset were `TE_8332A Lo` (at −2 min) and `TV_8329ZC Hi` — the desuperheater spray valve
position alarm (at −8 min).

The alarm list enters the context window. The audit trace records it as step 3.

---

**Step 7 — Check what is active at the anomaly moment**

`alarm_get_active_at("2022-04-01 08:00:00")`

`alarm_tools.py` queries for alarms where `activated_at <= 08:00` AND
`(cleared_at IS NULL OR cleared_at > 08:00)`. Result: 4 active alarms, including the
spray valve and a `YJJWSLL Lo` alarm (desuperheating water flow low).

This confirms: the desuperheater is behaving abnormally around the time the temperature
started dropping.

---

**Step 8 — Trace upstream sensors**

`kg_get_upstream_sensors("TE_8332A")`

`kg_tools.py` loads `boiler_kg.json` into `BoilerKnowledgeGraph` (if not already loaded)
and runs a graph traversal upstream from the steam temperature sensor. Result: hop-1
sensors include `TV_8329ZC` (desuperheater spray valve position) and `YJJWSLL`
(desuperheating water flow); hop-2 includes furnace temperature and air flow sensors.

The knowledge graph result enters the context window. The audit trace records it.

---

**Step 9 — Log hypothesis about the desuperheater**

`audit_log_reasoning(reasoning_type="hypothesis", text="The desuperheater spray valve (TV_8329ZC) alarmed before TE_8332A dropped. Hypothesis: the spray valve stuck open or the water flow unexpectedly increased, over-cooling the steam. Will check spray valve position and water flow statistics.")`

---

**Step 10 — Check desuperheater data**

`historian_get_statistics(["TV_8329ZC", "YJJWSLL"], "2022-04-01 06:00:00", "2022-04-01 10:00:00")`

Result:
- `TV_8329ZC` (spray valve): mean = 72.4%, max = 89.1% — **well above the 20–60% normal range**
- `YJJWSLL` (water flow): mean = 11.2 t/h — **above the 2–8 t/h normal range**

Both sensors confirm the desuperheater was injecting far more water than normal.

---

**Step 11 — Log the cause-vs-symptom determination**

`audit_log_reasoning(reasoning_type="observation", text="TV_8329ZC averaged 72.4% (normal: 20–60%) and YJJWSLL averaged 11.2 t/h (normal: 2–8 t/h). The spray valve was commanding excess water injection. This is either (a) a control loop responding normally to an upstream temperature excursion, or (b) a malfunction/stuck valve. Need to check whether there was a reason for the controller to be demanding this much cooling.", evidence_steps=[4,5,6])`

---

**Step 12 — Search documentation for the troubleshooting guide**

`docs_search("steam temperature dropping desuperheater spray excessive", doc_type="troubleshooting", sensor_tag="TE_8332A")`

`rag_tools.py` embeds the query using the BGE model, queries ChromaDB with the embedding
vector, and filters to `doc_type = "troubleshooting"` and chunks tagged with `TE_8332A`.
Result: top match is `trb_low_steam_temperature` (relevance 0.87), section: "Excess
Desuperheating Water Flow." The chunk text includes steps to check for valve malfunction
vs. control loop response.

The document chunk enters the context window. The audit trace records it.

---

**Step 13 — Retrieve the full document for procedure context**

`docs_get_document("trb_low_steam_temperature")`

`rag_tools.py` looks up the source path from ChromaDB metadata, then reads
`RAG docs/troubleshooting/trb_low_steam_temperature.md` from disk and returns the
full text. Claude now has the complete troubleshooting procedure.

---

**Step 14 — Plot the key sensors**

`historian_plot_tags(["TE_8332A", "TV_8329ZC", "YJJWSLL"], "2022-04-01 06:00:00", "2022-04-01 10:00:00", title="Steam Temp vs Desuperheater — Anomaly Window", show_normal_range=true)`

`historian_tools.py` queries the database, then calls `plot_helpers.plot_normalized()`
with the three tags on independent Y-axes. The chart is saved as a PNG to `plots/`.
The file path is returned to Claude, which passes it to you.

---

**Step 15 — Log the conclusion**

`audit_log_reasoning(reasoning_type="conclusion", text="Root cause: the desuperheater spray valve TV_8329ZC was operating at 72% average open position (normal max 60%), injecting 11.2 t/h of cooling water (normal max 8 t/h). This excess injection over-cooled the main steam, driving TE_8332A from 535°C down to a mean of 524°C and a minimum of 511°C. The Lo alarm on TE_8332A lagged the spray valve alarm by ~6 minutes, consistent with thermal transport delay from desuperheater to the steam outlet sensor. Whether the spray valve malfunctioned (stuck) or the control loop was responding to an actual upstream excursion could not be fully determined from this data alone.", confidence=0.72, evidence_steps=[2,3,4,5,6,7,8])`

Confidence is set to 0.72 (MEDIUM) because the control-loop vs. malfunction distinction
was not resolved from the available data.

---

**Step 16 — Generate the audit report**

The `/audit-trail` skill is invoked. This runs `render_audit.py traces/{run_id}` as a
subprocess, which reads `trace.jsonl` and the raw step files and produces:
- `traces/{run_id}/report.md` — full detailed report with every step, hypothesis, and
  evidence reference
- `traces/{run_id}/summary.md` — executive one-pager with root cause, confidence, and
  recommended corrective actions

---

**Step 17 — Claude's response to you**

Claude assembles its final answer from everything now in its context window:
- The statistics (step 4)
- The alarm timeline (steps 6 and 7)
- The knowledge graph topology (step 8)
- The procedure text from the troubleshooting guide (step 13)
- The chart file path (step 14)

It presents:
- A clear statement that `TE_8332A` is 5.7°C below the 530°C minimum
- The alarm timeline showing the spray valve alarmed 6 minutes before the temperature
  dropped
- The quantified over-injection (spray at 72%, water flow at 11.2 t/h)
- Cited steps from the troubleshooting guide for what to check next
- The chart of all three sensors over the anomaly window
- Links to the audit trail reports
- An explicit confidence level (MEDIUM — 0.72) with a statement of what additional data
  would raise it (e.g. the DCS controller output trend to confirm whether it was
  commanding the valve open vs. the valve acting independently)

---

## Summary of File Roles

| File | Role | Runtime? |
|------|------|----------|
| `historian_mcp_server.py` | MCP protocol handler — launches tools, routes calls, wraps audit | Yes |
| `historian_tools.py` | Historian database queries and chart generation | Yes |
| `alarm_tools.py` | Alarm log queries | Yes |
| `kg_tools.py` | Knowledge graph wrapper with lazy loading | Yes |
| `knowledge_graph.py` | Graph traversal engine — loaded into memory on first KG call | Yes |
| `rag_tools.py` | Document search — embedding model + ChromaDB queries | Yes |
| `audit_trace.py` | Trace recording, session management, SHA-256 sealing | Yes |
| `render_audit.py` | Report generation from trace files | Yes (on demand) |
| `hmi_style.py` | Chart color theme | Yes (imported by historian_tools) |
| `plot_helpers.py` | Multi-axis chart renderer | Yes (imported by historian_tools) |
| `CLAUDE.md` | Standing instructions and workflows for Claude | Yes (in context window) |
| `.mcp.json` | MCP server registration | Yes (read at startup) |
| `.claude/commands/audit-trail.md` | `/audit-trail` skill definition | Yes (when invoked) |
| `.claude/commands/ml-fault-detection.md` | `/ml-fault-detection` skill definition | Yes (when invoked) |
| `.claude/commands/mspc-analysis.md` | `/mspc-analysis` skill definition | Yes (when invoked) |
| `.claude/commands/setup.md` | `/setup` skill definition | Yes (when invoked) |
| `boiler_historian.duckdb` | The 5-day sensor data (raw data, never in context) | Yes (data source) |
| `boiler_alarms.duckdb` | The 6,005 alarm records (raw data, never in context) | Yes (data source) |
| `boiler_kg.json` | The process topology graph (loaded into server memory) | Yes (data source) |
| `rag_vector_db/` | ChromaDB vector index for document search | Yes (data source) |
| `RAG docs/` | Source markdown documents (read only when full text is requested) | Yes (data source) |
