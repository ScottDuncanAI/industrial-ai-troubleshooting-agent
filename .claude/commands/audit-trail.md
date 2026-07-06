# Audit Trail Report

Generate a formatted audit report from a completed root cause analysis trace.

ARGUMENTS: $ARGUMENTS

## Steps

### 1. Identify the trace

If the user provided a run_id as the argument, use that.

If no run_id was provided, list available traces:

```
python -c "import os; dirs = sorted(os.listdir('traces'), reverse=True)[:10]; [print(d) for d in dirs]"
```

If there is only one trace or the user just completed an investigation, use the most recent one. Otherwise ask which trace to use.

### 2. Auto-finalize if needed

Check if the session has a `session_meta.json`. If not, call `audit_end_session` to finalize it before rendering.

### 3. Render the reports

```
python render_audit.py traces/{run_id}
```

Capture the output. This generates both `report.md` (detailed) and `summary.md` (executive summary). If the script fails, diagnose and report the error.

### 4. Open the reports

```
start traces/{run_id}/summary.md
start traces/{run_id}/report.md
```

### 5. Summarize

Report to the user:
- Both reports have been generated and opened
- `summary.md` is the executive one-pager (root cause, investigation flow, recommendations)
- `report.md` is the full detailed report with all hypotheses, evidence, and appendices
- The trace SHA-256 hash (read from `traces/{run_id}/session_meta.json`)
- The number of tool calls and reasoning entries
- Any warnings the renderer flagged
- Clickable links to both files, formatted as markdown links using the full `file:///` URL
  with spaces encoded as `%20`. **Derive the project's absolute path at runtime — do not
  hardcode it.** Run `python -c "import os; print(os.path.abspath('.'))"` to get the project
  root, convert backslashes to forward slashes, URL-encode spaces as `%20`, and prepend
  `file:///`. Then build:

  **Audit Trail Files**
  - [summary.md](file:///<project-root>/traces/{run_id}/summary.md) — executive summary
  - [report.md](file:///<project-root>/traces/{run_id}/report.md) — full detailed report

  Substitute the actual project root and the actual `{run_id}` value (e.g.
  `20260623_143206_6ba4aa`) into both URLs.
