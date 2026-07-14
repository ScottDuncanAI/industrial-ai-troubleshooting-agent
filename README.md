# Agentic AI Industrial Troubleshooting Assistant
By Scott Duncan. Reach me on LinkedIn here: https://www.linkedin.com/in/s-r-duncan/

An agentic AI industrial troubleshooting assistant built on top of a [public coal-fired boiler dataset](https://www.kaggle.com/datasets/nikitamanaenkov/time-series-of-industrial-boiler-operations). The application connects Claude to four plant data sources through an MCP server:

1. **time-series historian** (5 days of sensor data across 30 tags)
2. **DCS alarm log** (6,005 alarm events)
3. **process knowledge graph** (equipment topology)
4. **plant document library** (62 procedures, datasheets, and troubleshooting guides).

Users interact with the troubleshooting assistant through Claude Code using natural language prompts. Ask why steam temperature dropped or what caused an alarm flood, and it walks you through exactly how it reached the answer: every historian query, alarm lookup, knowledge-graph traversal, and plant-document search it ran to drill down to the root cause, in the order it ran them.


https://github.com/user-attachments/assets/19ca5cb0-4407-44f8-ad01-733f0c95c477


> **Scope.** This is a demonstration and reference implementation built on five days of data from a single boiler. It's meant to show what auditable, agentic process troubleshooting looks like and to be a foundation you can extend, not a production monitoring tool. If you want to run it on your own unit, see [Contributing](#contributing-and-extending) below.

## Getting Started

**Roughly 5–10 minutes to a working result.** Most of that is an automated download on first run.

You need two things installed before you begin:

1. **Python 3.11 or newer**, download from [python.org](https://www.python.org/downloads/). On Windows, make sure to check **"Add Python to PATH"** during installation.
2. **Claude Code**, see the [installation guide](https://docs.anthropic.com/en/docs/claude-code/overview). Available as a CLI, desktop app, or IDE extension. This requires a Claude Pro account ($20/month) or higher, so set that up first if you don't have one.

### Setup (3 steps)

**Step 1.** Download this repository and unzip it (or `git clone` it if you're familiar with git).

**Step 2.** Open Claude Code in the project folder:
- **Desktop app**: Open the app and select the project folder
- **CLI**: Open a terminal, navigate to the project folder, and type `claude`

**Step 3.** Once Claude Code is running, type:

```
/setup
```

Claude will install everything automatically: dependencies, document search index, and server configuration. No coding required. The first run downloads a ~130MB embedding model for document search (RAG), which is the bulk of the wait. When it's done, it will ask you to restart Claude Code. After restarting, you're ready to go.

> **Disk space.** The repository download itself is small (~10 MB), but `/setup` installs about 1.5 GB of Python dependencies — most of it PyTorch, which powers the document search — plus the ~130 MB embedding model. Have roughly **2 GB of free disk space** available before you start.

## What can I do with it?

Once setup is complete, just ask questions in plain English:

- "What has flue gas O2 been doing for the past 12 hours?"
- "Why did steam temperature drop below 530 F on March 29?"
- "What alarms were firing on March 29 around 2pm?"
- "Show me a plot of combustion air flow and steam outlet temperature on 3/30."
- "What sensors are upstream of the steam drum?"
- "Show me the troubleshooting guide for high IDF vibration."


### Slash commands

The project includes built-in slash commands you can type directly into Claude Code:

| Command | What it does |
|---------|-------------|
| `/setup` | First-time setup: installs dependencies, builds search index, configures the server |
| `/mspc-analysis` | Runs a PCA-based Multivariate Statistical Process Control analysis. Builds a model from normal operating data, computes T² and SPE monitoring statistics, detects anomalous periods, generates contribution plots for the worst events, and cross-references them with alarms and upstream equipment. |
| `/ml-fault-detection` | Runs an Isolation Forest anomaly detection and XGBoost feature importance analysis on the historian data. Trains on normal operating data to detect fault periods across all 30 sensors simultaneously — including periods where the primary KPI has not yet moved. Ranks the remaining 29 tags by their ability to predict steam temperature excursions, then cross-references the worst events with the alarm log and knowledge graph. |
| `/audit-trail` | Generates a formatted audit report from the most recent root cause investigation (see below) |

### Auditable root cause analysis

This is the part that makes the project different from a chatbot pointed at plant data. When you ask a diagnostic question ("why did steam temperature drop?", "what caused this alarm flood?"), the system doesn't just give you an answer; it builds a traceable chain of evidence you can review and verify.

**Automatic tool call capture.** Every data query the system makes during an investigation (every historian lookup, alarm search, knowledge graph traversal, and document retrieval) is automatically recorded in real time as it executes. The trace captures the full inputs and outputs of each tool call, not a summary written after the fact. This means the audit trail reflects exactly what data was queried and what came back, step by step, as the investigation actually happened.

**Structured reasoning on top.** In addition to the raw tool call record, the system logs structured reasoning at each step:
- **Hypotheses** are stated before data is queried: what the system expects to find and why
- **Observations** are recorded after each data lookup, referencing the specific evidence step
- **Rejections** are logged when a hypothesis is disproven, citing the evidence that disproved it
- **Conclusions** carry a confidence level (HIGH / MEDIUM / LOW) and cite every supporting evidence step
- **Cause vs. symptom** determinations are made explicitly: the system traces upstream until it finds a condition not explained by anything further upstream

**Reports are generated automatically.** When an investigation finishes, two reports are written to the `traces/` directory without any extra step:

- **`summary.md`** — an executive one-pager: the root cause conclusion with confidence level and a numbered investigation flow (one line per tool call or reasoning step). Start here.
- **`report.md`** — the full detailed report: every tool call with its arguments and result summary, the complete hypothesis register showing which theories were confirmed or rejected, and appendices listing all tags queried, alarms analyzed, and documents referenced. Use this when you want to verify the reasoning step by step.

The raw trace is also saved with a SHA-256 hash so you can confirm the record hasn't been modified after the fact. If you want to re-render or revisit the reports from a previous investigation, type `/audit-trail`.

The result: you can check whether the AI's conclusion is actually supported by the data it retrieved, not just trust the answer.

For the full methodology and all available query workflows, see [CLAUDE.md](CLAUDE.md).

## What's in the box

### Data Sources

The system connects Claude to four data sources. The raw sensor data comes from the [Time Series of Industrial Boiler Operations](https://www.kaggle.com/datasets/nikitamanaenkov/time-series-of-industrial-boiler-operations) dataset on Kaggle. The alarm log, knowledge graph, and document library are derived and constructed on top of it.

<img width="1603" height="900" alt="Architecture diagram" src="https://github.com/user-attachments/assets/e1c31aec-7507-482c-932b-9786e0a1b7af" />

#### Time-Series Historian (`boiler_historian.duckdb`)

A DuckDB database of **86,400 sensor readings** across **30 process tags** at 5-second intervals, spanning five days from March 27 to April 1, 2022. Tags cover the full CFB combustion loop: steam temperature and pressure, flue gas oxygen, furnace draft, primary and secondary air flows, cyclone separator differential pressures, and induced draft fan mechanical readings. The primary KPI is `TE_8332A` (boiler outlet steam temperature), which the agent monitors as the main anomaly indicator — approximately 8.6% of the dataset contains anomalous readings.

- 30 tags, 86,400 rows, 5-second resolution
- Values stored in engineering units (°C, MPa, Pa, t/h, m³/h, mm/s, A, %)
- Accessible via the `historian_*` MCP tools

| Tag Name | Variable Name |
|----------|----------------|
| `AIR_8301A` | Upper economizer inlet flue gas oxygen content (left) |
| `AIR_8301B` | Upper economizer inlet flue gas oxygen content (right) |
| `FT_8301` | Primary fan outlet flow rate |
| `FT_8302` | Secondary fan outlet flow rate |
| `FT_8306A` | Return air chamber air flow (left) |
| `FT_8306B` | Return air chamber air flow (right) |
| `PTCA_8322A` | Pot pressure (left side steam drum pressure) |
| `PTCA_8324` | Container outlet vapour pressure |
| `PT_8313A` | Upper furnace pressure (point A) |
| `PT_8313B` | Upper furnace pressure (point B) |
| `PT_8313C` | Upper furnace pressure (point C) |
| `PT_8313D` | Upper furnace pressure (point D) |
| `PT_8313E` | Upper furnace pressure (point E) |
| `PT_8313F` | Upper furnace pressure (point F) |
| `SXLTCYY` | Differential pressure between upper and lower hearth (right) |
| `SXLTCYZ` | Differential pressure between upper and lower hearth (left) |
| `TE_8303` | Primary air preheater outlet air temperature |
| `TE_8304` | Secondary air preheater outlet air temperature |
| `TE_8313B` | Temperature in upper part of furnace chamber (right side) |
| `TE_8319A` | Flue gas temperature at upper economizer outlet (left) |
| `TE_8319B` | Flue gas temperature at upper economizer outlet (right) |
| `TE_8332A` | Boiler outlet steam temperature (primary KPI — normal 530–545°C) |
| `TV_8329ZC` | Primary desuperheater outlet steam temperature regulating valve position |
| `YCLCCY` | Differential pressure in the right layer (cyclone separator) |
| `YFJ3_AI` | Induced draft fan motor current |
| `YFJ3_ZD1` | Vibration of induced draft fan bearing shell (point A) |
| `YFJ3_ZD2` | Vibration of induced draft fan bearing shell (point B) |
| `YJJWSLL` | Primary desuperheating water flow output |
| `ZCLCCY` | Differential pressure in the left layer (cyclone separator) |
| `ZZQBCHLL` | Main steam flow rate after compensation |

#### Alarm Log (`boiler_alarms.duckdb`)

A DuckDB database of **6,005 alarm lifecycle events** derived from the historian data using an ISA-18.2 state machine simulation. Each row represents the complete lifecycle of a single alarm — from activation through acknowledgment to clearance — with 1% deadband hysteresis applied to prevent chattering. Alarm setpoints came from the plant's control & alarm setpoint register (Rev 4.2).

- Each event records: tag, alarm level, activation time and value, acknowledgment time, clearance time, duration, and max deviation from setpoint
- Alarm levels (high): Hi · HiHi · HiHiHi · Alert · Alarm · Trip
- Alarm levels (low): Lo · LoLo
- Priority tiers: Critical (Trip/HiHiHi/LoLo) · High (HiHi/Alarm) · Medium (Hi/Lo) · Low (Alert)
- Accessible via the `alarm_*` MCP tools; regenerate with `python generate_alarms.py`

#### Process Knowledge Graph (`boiler_kg.json`)

A JSON-serialized NetworkX graph representing the physical and process topology of the boiler. Nodes are equipment items and sensors; edges are process connections (air circuits, flue gas paths, steam/water loops, etc.). The graph lets the agent reason about cause-and-effect relationships across the system. When steam temperature drops, it can walk upstream through the steam generation path to identify which equipment or sensor might be responsible.

- Covers 6 major systems: Primary Air, Secondary Air, Combustion, Flue Gas & Heat Recovery, Draft & Exhaust, Steam Generation & Superheating
- Models 8 named process streams: PrimaryAir, SecondaryAir, ReturnAir, FlueGas, Solids, FeedWater, Steam, DesuperheatingWater, Coal
- Lazy-loaded into memory on the first knowledge-graph tool call; accessible via the `kg_*` MCP tools

#### Plant Document Library (`RAG docs/` + `rag_vector_db/`)

A collection of **62 markdown documents** covering the full range of plant technical documentation, indexed in a ChromaDB vector database for semantic search. The agent can surface the right section of the right document in response to natural-language queries without reading every file. The vector index contains 356 searchable chunks built with BGE-small embeddings.

| Category | Count | Examples |
|----------|-------|---------|
| SOPs | 7 | Cold start, emergency shutdown, hot restart procedures |
| Datasheets | 14 | Induced draft fan, steam drum, CFB furnace, high-temp superheater |
| Maintenance | 13 | IDF bearing inspection, cyclone inspection, superheater tube inspection |
| Troubleshooting | 13 | High/low steam temperature, IDF high vibration |
| Controls | 5 | Alarm setpoint register, steam temperature loop, furnace draft loop |
| Safety | 10 | Emergency response, LOTO procedures, confined space entry |

Accessible via the `docs_*` MCP tools; rebuild the index with `python build_docs_db.py --rebuild`.

---

### MCP Server

The MCP server (`historian_mcp_server.py`) is the bridge between Claude and the four data sources. It exposes **23 tools** organized into four groups, plus three audit tools used during root cause investigations. Claude decides which tools to call and in what order based on your question. You never interact with the tools directly.

#### Historian Tools

| Tool | Description |
|------|-------------|
| `historian_list_tags` | Returns all 30 sensor tags with their description, units, and normal operating range. |
| `historian_search_tags` | Keyword search across tag names and descriptions to find the right tag when the name is unknown. |
| `historian_get_data_range` |Returns the earliest and latest timestamps in the historian. Always called first when a question uses relative time (e.g., "past 3 hours"). |
| `historian_get_tag_data` | Retrieves raw or downsampled time-series values for one or more tags over a specified time window. |
| `historian_get_statistics` | Computes min, max, mean, standard deviation, and count for one or more tags over a time window. |
| `historian_plot_tags` | Generates a PNG trend chart of one or more tags and saves it to the `plots/` directory. |

#### Alarm Log Tools

| Tool | Description |
|------|-------------|
| `alarm_query` | Filtered query of alarm events by time window, tag name, alarm level, priority, or lifecycle state. |
| `alarm_get_statistics` | Alarm KPIs for a time window: total count, frequency, average duration, acknowledgment rate, and top-offending tags. |
| `alarm_get_active_at` | Returns the complete list of alarms that were in an active state at a specific timestamp. |
| `alarm_search_context` | The primary troubleshooting tool — finds all alarms within ±N minutes of a focal event, ordered by proximity, to build a timeline around an incident. |
| `alarm_detect_flood` | Identifies periods of alarm flooding (>10 alarms per 10 minutes, per ISA-18.2) within a time window. |

#### Knowledge Graph Tools

| Tool | Description |
|------|-------------|
| `kg_trace_stream` | Returns the end-to-end ordered path of a named process stream (e.g., Steam, FlueGas) with sensors listed at each step. |
| `kg_query_equipment` | Finds equipment items by name and returns their co-located sensors and process connections. |
| `kg_get_upstream_sensors` | Returns all sensors upstream of a given tag, sorted by hop distance — used to identify what could be causing a downstream reading. |
| `kg_find_process_path` | Returns the physical process path between any two equipment nodes in the graph. |
| `kg_get_related_sensors` | Returns sensors that are co-located with, a symmetric counterpart of (e.g., left/right pairs), or in the same system as a given tag. |
| `kg_get_system_sensors` | Returns all sensors grouped by equipment within a named system (e.g., "Steam Generation & Superheating"). |

#### Document Search Tools

| Tool | Description |
|------|-------------|
| `docs_search` | Semantic search across all 356 document chunks, with optional filters for document type, equipment ID, or sensor tag. |
| `docs_list_documents` | Lists all documents in the library, optionally filtered by category (sop, datasheet, maintenance, troubleshooting, controls, safety). |
| `docs_get_document` | Retrieves the full text of a specific document by ID — used after `docs_search` has identified the right document. |

#### Audit Tools

| Tool | Description |
|------|-------------|
| `audit_start_session` | Opens a new audit session and initializes the trace file for a root cause investigation. |
| `audit_log_reasoning` | Records a structured reasoning step (hypothesis, observation, rejection, or conclusion) with optional confidence level and supporting evidence citations. |
| `audit_end_session` | Closes the audit session and finalizes the trace with a SHA-256 hash for tamper detection. |

---

### Code

| File | What it does |
|------|-------------|
| `historian_mcp_server.py` | Server entry point: connects Claude to the data sources |
| `historian_tools.py` | Time-series queries (trends, statistics, plots) |
| `alarm_tools.py` | Alarm log queries (context search, flood detection, statistics) |
| `kg_tools.py` | Knowledge graph queries (upstream sensors, process paths) |
| `rag_tools.py` | Document search (semantic search across plant docs) |
| `knowledge_graph.py` | Graph traversal algorithms |
| `mspc_analysis.py` | PCA-based multivariate statistical process control |
| `ml_fault_detection.py` | Isolation Forest anomaly detection and XGBoost feature importance analysis |
| `generate_alarms.py` | Rebuilds the alarm database from historian data |
| `build_docs_db.py` | Rebuilds the document search index |
| `CLAUDE.md` | System reference for Claude: tag tables, workflows, methodology |

## Contributing and extending

This project is built to be taken apart and rebuilt against your own process. If you run it, improve it, or point it at a different unit, I'd love to hear about it. See the note at the bottom.

The most natural places to extend it:

- **Point it at your own data.** Swap in your own historian tags or a different unit's data and see how the troubleshooting workflow holds up. The historian and alarm schemas are simple DuckDB tables; the tag definitions live in [CLAUDE.md](CLAUDE.md).
- **Extend the knowledge graph.** `boiler_kg.json` is plain topology: what's connected to what. Adding relationships (or correcting ones you'd model differently from your own experience) directly improves the agent's upstream/downstream reasoning.
- **Add to the document library.** Drop SOPs, datasheets, or troubleshooting guides into `RAG docs/` and rebuild the index with `python build_docs_db.py --rebuild`.
- **Add a new tool.** The MCP tool files (`historian_tools.py`, `alarm_tools.py`, `kg_tools.py`, `rag_tools.py`) follow a consistent pattern; a new query type is a self-contained addition.

**Good first contributions** if you want an easy entry point: add your own skills, connect another data source through the MCP server (e.g. shift handover notes, lab sample data, etc.), build on top of a different dataset, or open an issue describing a diagnostic question the agent handled poorly along with what you expected. Pull requests welcome, and contributors get credited.

## For developers

<details>
<summary>Manual setup (if you prefer not to use /setup)</summary>

```bash
# Install dependencies
pip install -r requirements.txt

# Build the document vector index (downloads ~130MB embedding model on first run)
python build_docs_db.py

# Configure the MCP server by creating a .mcp.json file at the project root
# (this is the file Claude Code reads to register project MCP servers):
# {
#   "mcpServers": {
#     "boiler-historian": {
#       "type": "stdio",
#       "command": "/absolute/path/to/python",
#       "args": ["/absolute/path/to/this/folder/historian_mcp_server.py"]
#     }
#   }
# }

# Restart Claude Code to load the MCP server (approve the .mcp.json trust prompt on first run)
```

</details>

<details>
<summary>Regenerating data files</summary>

The alarm database can be regenerated from the historian data and alarm setpoints:

```bash
python generate_alarms.py
```

To rebuild the document search index after editing files in `RAG docs/`:

```bash
python build_docs_db.py --rebuild
```

</details>

## License

Apache 2.0, see [LICENSE](LICENSE).

---

**Built by Scott Duncan.** I write about applied AI in chemical manufacturing on [LinkedIn](https://www.linkedin.com/in/s-r-duncan/) and on [YouTube](https://www.youtube.com/@ScottDuncanAI), where I teach manufacturing engineers how to leverage AI to improve plant operations.

If you run this against your own historian, I want to know what tags, alarms, or equipment relationships it would need to work on your unit. That's the most useful feedback I can get. Open an issue or reach out directly.
