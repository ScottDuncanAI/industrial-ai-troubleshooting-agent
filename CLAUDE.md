# Boiler Historian — System Reference

This system connects an LLM to four data sources for a coal-fired CFB boiler at a
chemical plant in Zhejiang, China: a **time-series historian** (5 days of sensor data),
a **DCS alarm log** (6,005 alarm events derived from the historian), a **process knowledge
graph** (equipment topology and relationships), and a **plant document library**
(62 procedures, datasheets, and guides). Together they enable natural-language operations
queries grounded in real data and real documentation.

---

## Critical Rules — Read First

These apply to every response, no exceptions:

1. **Never read files directly.** Do not use `Read`, `Grep`, or `Glob` on the `RAG docs/`
   folder or any project file. All document access must go through the MCP tools
   (`docs_search`, `docs_list_documents`, `docs_get_document`).

2. **Always resolve relative time before any historian query.** If the user says "past
   3 hours", "last day", or "this morning", call `historian_get_data_range` first to get
   the latest timestamp, then compute the absolute start time. Never guess a time window.

3. **Always cite sources when quoting procedures or limits.** Format:
   *"Per [Document Title], Rev [X.X]: ..."* — include document title and revision for
   every piece of procedural or specification information you present.

4. **Do not invent tag names.** Only use tags confirmed by `historian_list_tags` or
   `historian_search_tags`. If a tag name is uncertain, search first.

5. **Flag anomalies proactively.** Whenever `TE_8332A` is in scope and its value is
   outside 530–545°C, call it out explicitly as outside the normal operating range,
   even if the user didn't ask about it directly.

---

## The Four Data Sources

### 1. Historian (DuckDB)
- **File:** `boiler_historian.duckdb`
- **Data:** 86,400 rows × 30 tags at 5-second intervals
- **Time range:** `2022-03-27 14:28:54` → `2022-04-01 14:28:49` (5 days)
- **This is a static snapshot.** There is no live feed. "Now" = the latest timestamp.

### 2. Alarm Log (DuckDB)
- **File:** `boiler_alarms.duckdb`
- **Table:** `alarm_events` — 6,005 rows, one per alarm lifecycle
- **Generated from:** historian data + setpoints in `ctrl_alarm_setpoint_register` (Rev 4.2)
  using an ISA-18.2 state machine with 1% deadband hysteresis
- **Schema:** `alarm_id, tag_name, alarm_level, priority, message, setpoint,
  activated_at, activated_value, acknowledged_at, cleared_at, duration_sec, max_deviation`
- **Alarm levels (high direction):** Hi · HiHi · HiHiHi · Alert · Alarm · Trip
- **Alarm levels (low direction):** Lo · LoLo
- **Priority tiers:** Critical (Trip/HiHiHi/LoLo) · High (HiHi/Alarm) · Medium (Hi/Lo) · Low (Alert)
- **Note:** PTCA_8322A and PTCA_8324 are stored in **MPa** in the historian (not kPa as
  quoted in the alarm register). Alarm setpoints in the DB are already converted to MPa.
- **To regenerate:** `python generate_alarms.py`

### 3. Knowledge Graph
- **File:** `boiler_kg.json` (loaded into memory on first KG tool call)
- **Contains:** All equipment, sensors, process streams, control loops, and the
  connections between them. Use it to answer topology questions and to identify
  which sensors to investigate when diagnosing an anomaly.

### 4. Plant Document Library (RAG)
- **Source:** `RAG docs/` — 62 markdown documents
- **Index:** `rag_vector_db/` — ChromaDB vector database (356 chunks, BGE embeddings)
- **Access via MCP tools only.** `docs_search` queries the vector database — it does
  not read the markdown files directly. `docs_get_document` reads the source file only
  when full document text is needed after a search has already identified the document.

---

## Key Tags Quick Reference

| Tag | Description | Units | Normal Range |
|-----|-------------|-------|-------------|
| `TE_8332A` | **Boiler outlet steam temperature — PRIMARY KPI** | °C | **530–545** |
| `PTCA_8324` | Main steam outlet pressure | MPa* | 9.4–10.0 |
| `PTCA_8322A` | Steam drum pressure | MPa* | 9.4–10.0 |
| `ZZQBCHLL` | Main steam flow (compensated) | t/h | 120–135 (full load) |
| `AIR_8301A` | Flue gas O2 at economizer inlet (left) | % | 3.5–5.5 |
| `AIR_8301B` | Flue gas O2 at economizer inlet (right) | % | 3.5–5.5 |
| `PT_8313A–F` | Upper furnace pressure (6 points) | Pa | −80 to −160 |
| `YFJ3_ZD1` | IDF bearing vibration — drive end | mm/s | < 2.5 (alert 3.5, alarm 4.5, trip 11.0) |
| `YFJ3_ZD2` | IDF bearing vibration — non-drive end | mm/s | < 2.5 (alert 3.5, alarm 4.5, trip 11.0) |
| `YFJ3_AI` | IDF motor current | A | 180–250 (full load) |
| `FT_8301` | Primary fan outlet flow | m³/h | 90,000–135,000 |
| `FT_8302` | Secondary fan outlet flow | m³/h | 55,000–80,000 |
| `FT_8306A/B` | Return air chamber flow (left/right) | m³/h | 8,000–15,000 |
| `TE_8303` | Primary air preheater outlet air temp | °C | 180–220 |
| `TE_8304` | Secondary air preheater outlet air temp | °C | 175–215 |
| `TE_8313B` | Upper furnace temperature (right side) | °C | 850–950 |
| `TE_8319A/B` | Economizer flue gas outlet temp (left/right) | °C | 135–160 |
| `SXLTCYZ` | Hearth differential pressure (left) | Pa | 1,500–3,000 |
| `SXLTCYY` | Hearth differential pressure (right) | Pa | 1,500–3,000 |
| `ZCLCCY` | Cyclone separator ΔP (left) | Pa | 600–1,200 |
| `YCLCCY` | Cyclone separator ΔP (right) | Pa | 600–1,200 |
| `TV_8329ZC` | Desuperheater spray valve position | % | 20–60 (full load) |
| `YJJWSLL` | Desuperheating water flow | t/h | 2–8 |

Use `historian_search_tags` to find additional tags by keyword.

*\*Pressure unit note:* `PTCA_8324` and `PTCA_8322A` are stored in **MPa** in the historian
(engineering range 0–12 MPa). The alarm register quotes kPa; alarm setpoints have been
converted to MPa in `boiler_alarms.duckdb`. Normal range 9.4–10.0 MPa = 9,400–10,000 kPa.

---

## Anomaly Context

The dataset contains ~8.6% anomalous readings. **The primary anomaly indicator is
`TE_8332A` outside 530–545°C.** When investigating anomalies:
- Below 530°C = undertempering (insufficient heat, excess desuperheating, bed problems)
- Above 545°C = overtempering (excess firing, desuperheater fault, low steam flow)

The `TE_8319A/B` trend (economizer outlet flue gas temperature) is the best early
indicator of backpass fouling — a rising trend over days signals reduced heat transfer.

---

## Query Workflows

### Time-series questions ("what has X been doing for the past Y hours?")
1. `historian_get_data_range` → get latest timestamp ("now")
2. Compute absolute `start_time = latest_timestamp − duration`
3. `historian_search_tags` if tag name is uncertain
4. `historian_get_tag_data` with computed time range + appropriate `downsample_minutes`
5. Summarize: direction (rising/falling/stable), magnitude, any exceedances of normal range

### Statistical questions ("what was the average/min/max of X?")
1. `historian_get_data_range` if relative time
2. `historian_get_statistics` → min, max, mean, std, count
3. Compare explicitly to normal range values in the Key Tags table above

### Plot requests ("plot X", "show me a chart of Y")
1. `historian_get_data_range` if relative time
2. `historian_plot_tags` → saves PNG to `plots/` subdirectory
3. Return the file path; user opens with their system's default image viewer
4. Use `show_normal_range=true` when plotting `TE_8332A`

### Tag discovery ("what tags are available?", "what measures steam?")
- `historian_list_tags` — all 30 tags with metadata
- `historian_search_tags(query)` — keyword search

### Process topology questions ("what is upstream of X?", "trace the steam path")
1. `kg_trace_stream` — ordered path of a process stream end-to-end
2. `kg_query_equipment` — find equipment by name; returns sensors + connections
3. `kg_get_upstream_sensors` — all sensors upstream of a tag, ordered by hop distance
4. `kg_find_process_path` — physical path between two equipment nodes
5. `kg_get_system_sensors` — all sensors grouped by equipment within a system
6. `kg_get_related_sensors` — co-located, symmetric pair, and same-system sensors

### Documentation questions ("what are the steps to...", "what is the alarm limit for...", "how do I...")
1. `docs_search(query)` — semantic search; returns the most relevant document sections
   - Narrow with `doc_type` if the category is clear (e.g., `doc_type="troubleshooting"`)
   - Narrow with `sensor_tag` to find docs referencing a specific tag (e.g., `sensor_tag="YFJ3_ZD1"`)
   - Narrow with `equipment_id` if the equipment node ID is known — use `kg_query_equipment`
     first if uncertain (e.g., search "induced draft fan" to confirm node ID = `induced_draft_fan`)
2. Present the relevant chunk with full citation (title + revision)
3. If the chunk is incomplete: `docs_get_document(doc_id)` → retrieve full document text

### Anomaly investigation ("why is steam temp dropping?", "what could be causing this?")
This is the primary combined workflow — historian + alarm log + knowledge graph + RAG together:
1. `historian_get_data_range` — resolve "now"
2. `historian_get_statistics` for `TE_8332A` — confirm anomaly and severity; note the anomaly timestamp
3. `alarm_search_context(anomaly_timestamp, window_minutes=30)` — get alarm context around the event
4. `alarm_get_active_at(anomaly_timestamp)` — full list of active alarms at that moment
5. `kg_get_upstream_sensors("TE_8332A")` — get all upstream sensors by hop distance
6. `historian_get_statistics` for upstream tags over the same window — find what else is off
7. `historian_plot_tags` — plot `TE_8332A` alongside the suspect tags
8. `docs_search(query, sensor_tag="TE_8332A", doc_type="troubleshooting")` — surface the
   relevant troubleshooting guide and cite it

### Maintenance questions ("the IDF vibration is high — what should I do?")
1. `historian_get_statistics` for the relevant sensor (e.g., `YFJ3_ZD1`, `YFJ3_ZD2`)
   to confirm the reading and its severity
2. `kg_query_equipment("induced draft fan")` — confirm equipment context and co-located sensors
3. `docs_search(query, equipment_id="induced_draft_fan", doc_type="troubleshooting")`
   — surface the troubleshooting guide
4. If full procedure needed: `docs_get_document(doc_id)` for the maintenance procedure
5. Cite document title and revision in your response

### Alarm investigation ("what alarms were firing when X happened?", "how many times did Y alarm today?")
1. `alarm_search_context(timestamp, window_minutes=30)` — primary tool; finds all alarms within
   ±30 min of the event, ordered by proximity. Use the `minutes_offset` field to build a timeline.
2. `alarm_get_active_at(timestamp)` — if you need the complete list of *everything* active at that moment
3. `alarm_get_statistics(start_time, end_time)` — for shift-level summaries or alarm rationalization
4. `alarm_query(start_time, end_time, tag_names=[...])` — for filtered lists (e.g., "all Critical alarms yesterday")
5. `alarm_detect_flood(start_time, end_time)` — identify periods of >10 alarms/10 min (ISA-18.2 flood threshold)

### Setpoint / limit questions ("what is the alarm limit for X?", "what is the normal range for Y?")
1. Check Key Tags Quick Reference above — covers the most common tags
2. If not in the table: `docs_search(query, sensor_tag="<tag>")` — the alarm setpoint
   register (`ctrl_alarm_setpoint_register`) contains all 30 tags with Hi/HiHi/Lo/LoLo values
3. Alternatively: `docs_get_document("ctrl_alarm_setpoint_register")` for the full register

---

## Root Cause Analysis Methodology (Audited)

This methodology applies to diagnostic and root-cause questions. For simple lookups,
answer normally — the factual trace captures automatically regardless.

### Investigation Protocol

For every tool call during a diagnostic investigation:

1. **Before the call:** log the hypothesis you are testing via `audit_log_reasoning`
   with `reasoning_type="hypothesis"` — state what you expect to find and why you
   are making this call.
2. **Make the call.**
3. **After the result:** log an observation or conclusion via `audit_log_reasoning`
   with `reasoning_type="observation"` or `"conclusion"`, referencing the
   `evidence_steps` it is based on.
4. **If a hypothesis is disproven:** log a rejection with `reasoning_type="rejection"`
   and the evidence steps that disprove it.

### Evidence Rules

- Every factual claim must cite a step number.
- Every conclusion must include `evidence_steps`.
- Distinguish data from interpretation: tool results are facts, your analysis
  connecting them is interpretation.

### Hypothesis Tracking

Every hypothesis must end as confirmed, rejected, or inconclusive. Each outcome
must be logged via `audit_log_reasoning`.

### Distinguish Cause from Symptom

An abnormal or correlated variable is a starting point, not a root cause. Before
declaring any variable to be the root cause, investigate WHY it is behaving
abnormally and determine whether it is a true cause or a downstream symptom.

- A **true cause** is a condition that, if corrected, resolves the problem (e.g.,
  a failing IDF bearing causing vibration that destabilizes draft control).
- A **symptom** is a downstream effect of another condition (e.g., elevated
  desuperheater spray because the controller is responding to an upstream
  temperature excursion).

For the implicated variable, explicitly test and rule in or out:
1. Is a control loop driving it in response to something upstream?
2. Is the underlying sensor suspect or out of calibration?
3. Is there an upstream disturbance (feed, load, ambient, equipment) that explains it?

Continue tracing upstream until you reach a condition whose abnormality is not
explained by anything further upstream in the available data. That is the candidate
root cause. Log the cause-versus-symptom determination explicitly. Do not finalize
until at least one cause-versus-symptom check has been logged for the implicated
variable.

### Confidence Levels

Every final conclusion must carry a confidence level (0.0–1.0) set on the
concluding `audit_log_reasoning` entry:

- **HIGH (0.8–1.0):** multiple independent data sources agree, the causal mechanism
  is identified and consistent with process knowledge or a documented failure mode,
  and plausible alternatives were checked and ruled out.
- **MEDIUM (0.5–0.79):** evidence points to this cause but is partly circumstantial,
  some confirming data is missing, or one or more alternatives could not be fully
  excluded.
- **LOW (below 0.5):** evidence is limited or conflicting, there are key data gaps,
  or the conclusion rests mainly on correlation without a confirmed mechanism.

Never present a root cause as definitive while credible alternatives remain open;
lower the confidence instead. Whenever confidence is not HIGH, end the conclusion
by stating exactly what additional data, test, or check would raise it.

### Closing the Investigation

**MANDATORY — do not skip any step. A root cause response is not complete until
all three are done.**

1. Log the final root cause conclusion with `audit_log_reasoning` including
   `confidence` and all supporting `evidence_steps`.
2. Log at least one corrective action with `audit_log_reasoning` using
   `reasoning_type="corrective_action"`. Each corrective action must:
   - be grounded in the confirmed root cause and cite its supporting `evidence_steps`;
   - be based on the relevant troubleshooting guide, SOP, or maintenance procedure
     (use `docs_search` if not already retrieved) and cite the document title and revision;
   - be specific and actionable (what to do, on which equipment/tag), not generic advice.
   The investigation is not complete until at least one corrective action is logged, so
   the "Recommended Corrective Actions" section of `summary.md` is never empty.
3. **Immediately invoke `/audit-trail`** to generate `report.md` and `summary.md`.
   - Do not present a written summary and stop — the skill must run.
   - After the skill completes, include the clickable file links in your response
     exactly as the skill outputs them (full `file:///` URLs with spaces as `%20`).
   - The links must appear in every root cause response, without exception.

---

## Knowledge Graph Reference

### Available Streams (use with `kg_trace_stream`)
`PrimaryAir`, `SecondaryAir`, `ReturnAir`, `FlueGas`, `Solids`, `FeedWater`, `Steam`,
`DesuperheatingWater`, `Coal`

### Available Systems (use with `kg_get_system_sensors`)
`Primary Air`, `Secondary Air`, `Combustion`, `Flue Gas & Heat Recovery`,
`Draft & Exhaust`, `Steam Generation & Superheating`

---

## Downsampling Guide

Raw data is at 5-second intervals. Keep responses manageable:

| Time range | `downsample_minutes` |
|------------|----------------------|
| < 30 min | None (raw) |
| 30 min – 2 hr | 1 |
| 2 hr – 12 hr | 5 |
| 12 hr – 5 days | 15 or 30 |

---

## MCP Tools — Full Reference

### Historian tools
| Tool | Parameters | Purpose |
|------|-----------|---------|
| `historian_list_tags` | — | All 30 tags with metadata |
| `historian_search_tags` | `query` | Find tags by keyword |
| `historian_get_data_range` | — | Earliest/latest timestamps — call this first for relative time |
| `historian_get_tag_data` | `tag_names, start_time, end_time, [downsample_minutes]` | Time-series retrieval |
| `historian_get_statistics` | `tag_names, start_time, end_time` | Min/max/mean/std/count |
| `historian_plot_tags` | `tag_names, start_time, end_time, [title, downsample_minutes, show_normal_range]` | PNG chart |

All timestamps: ISO format `YYYY-MM-DD HH:MM:SS`

### Knowledge graph tools
| Tool | Parameters | Purpose |
|------|-----------|---------|
| `kg_trace_stream` | `stream_name` | End-to-end stream path with sensors at each step |
| `kg_query_equipment` | `query` | Find equipment by name; returns sensors + connections |
| `kg_get_upstream_sensors` | `node_id` | All upstream sensors, ordered by hop distance |
| `kg_find_process_path` | `from_node, to_node` | Physical path between two equipment nodes |
| `kg_get_related_sensors` | `tag_name` | Co-located, symmetric pair, same-system sensors |
| `kg_get_system_sensors` | `system_name` | All sensors grouped by equipment within a system |

### RAG document search tools
| Tool | Parameters | Purpose |
|------|-----------|---------|
| `docs_search` | `query, [doc_type], [equipment_id], [sensor_tag], [top_k]` | Semantic search — returns ranked sections with citation metadata |
| `docs_list_documents` | `[doc_type]` | Browse document index; confirm doc_id before retrieving |
| `docs_get_document` | `doc_id` | Full document text — use after search identifies the right document |

### Alarm log tools
| Tool | Parameters | Purpose |
|------|-----------|---------|
| `alarm_query` | `start_time, end_time, [tag_names], [alarm_level], [priority], [state], [limit]` | Filtered list of alarm events in a time window |
| `alarm_get_statistics` | `start_time, end_time, [tag_names]` | KPIs: count, freq, avg duration, ack rate, top alarms |
| `alarm_get_active_at` | `timestamp, [tag_names]` | All alarms active at a specific moment |
| `alarm_search_context` | `timestamp, [window_minutes=30], [tag_names]` | Alarms ±N min around a focal event — **primary troubleshooting tool** |
| `alarm_detect_flood` | `start_time, end_time, [threshold_per_10min=10]` | ISA-18.2 flood detection |

`state` filter values: `ACTIVE` · `CLEARED` · `UNACKNOWLEDGED` · `ANY` (default)

**`doc_type` values:** `sop` · `datasheet` · `maintenance` · `troubleshooting` · `controls` · `safety`

**Document library contents:**
| Category | Count | Key documents |
|----------|-------|---------------|
| SOPs | 7 | cold_start_procedure, emergency_shutdown_procedure, hot_restart_procedure |
| Datasheets | 14 | ds_induced_draft_fan, ds_steam_drum, ds_cfb_furnace, ds_high_temp_superheater |
| Maintenance | 13 | mnt_idf_bearing_inspection, mnt_cyclone_inspection, mnt_superheater_tube_inspection |
| Troubleshooting | 13 | trb_high_steam_temperature, trb_low_steam_temperature, trb_idf_high_vibration |
| Controls | 5 | ctrl_alarm_setpoint_register, ctrl_steam_temp_loop, ctrl_furnace_draft_loop |
| Safety | 10 | safe_emergency_response, safe_loto_induced_draft_fan, safe_confined_space_steam_drum |

**To re-index after editing documents:**
```
python build_docs_db.py            # incremental update
python build_docs_db.py --rebuild  # wipe and rebuild from scratch
```
Restart Claude Code after re-indexing to reload the MCP server.

---

## Codebase Structure

### Runtime modules (loaded by the MCP server on startup)

| File | Role |
|------|------|
| `historian_mcp_server.py` | Entry point — tool declarations (`list_tools`) and call routing (`call_tool`) only; no query logic |
| `historian_tools.py` | `historian_*` tool implementations; owns connection to `boiler_historian.duckdb` |
| `alarm_tools.py` | `alarm_*` tool implementations; owns connection to `boiler_alarms.duckdb` |
| `kg_tools.py` | `kg_*` tool implementations; lazy-loads `BoilerKnowledgeGraph` from `boiler_kg.json` |
| `rag_tools.py` | `docs_*` tool implementations; lazy-loads ChromaDB client and embedding model |
| `knowledge_graph.py` | `BoilerKnowledgeGraph` class and graph traversal algorithms — no MCP awareness |

### Setup / generation scripts (run once, not at runtime)

| File | Purpose |
|------|---------|
| `generate_alarms.py` | Generates `boiler_alarms.duckdb` from historian data + alarm setpoints |
| `alarm_metadata.py` | Alarm setpoint definitions for all 30 tags (source: `ctrl_alarm_setpoint_register` Rev 4.2) |
| `tag_metadata.py` | Tag definitions used when building the historian database |
| `build_docs_db.py` | Rebuilds `rag_vector_db/` from markdown files in `RAG docs/` |

### Data files

| File | Contents |
|------|---------|
| `boiler_historian.duckdb` | 86,400 rows × 30 tags (5-sec intervals) + `tags` metadata table |
| `boiler_alarms.duckdb` | 6,005 alarm lifecycle rows in `alarm_events` |
| `boiler_kg.json` | NetworkX node-link export of the process knowledge graph |
| `rag_vector_db/` | ChromaDB store — 356 chunks, BGE-small embeddings |
| `RAG docs/` | 62 source markdown documents (read only by `docs_get_document`) |
