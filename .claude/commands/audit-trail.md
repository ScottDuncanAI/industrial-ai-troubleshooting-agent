# Audit Trail Report

Generate a formatted audit report from a completed root cause analysis trace.

ARGUMENTS: $ARGUMENTS

## Conventions

- **Python:** Always use the project's virtual-environment Python, never bare `python`
  (which on macOS may not exist or may point at a dependency-free system Python). Written as
  `<venv-python>` below — substitute `.venv/bin/python` on macOS/Linux or
  `.venv/Scripts/python` on Windows.
- **Opening files:** Use the command for the user's OS, written as `<open>` below —
  `open` on macOS, `xdg-open` on Linux, `start` on Windows.

## Steps

### 1. Identify the trace

If the user provided a run_id as the argument, use that.

If no run_id was provided, list available traces:

```
<venv-python> -c "import os; dirs = sorted(os.listdir('traces'), reverse=True)[:10]; [print(d) for d in dirs]"
```

If there is only one trace or the user just completed an investigation, use the most recent one. Otherwise ask which trace to use.

### 2. Ensure corrective actions are logged

Before finalizing the session, confirm the trace contains at least one `corrective_action`
reasoning entry. If the investigation reached a root-cause conclusion but no corrective
action was logged, log one or more now with `audit_log_reasoning`
(`reasoning_type="corrective_action"`) before proceeding — each grounded in the confirmed
root cause, citing its `evidence_steps` and the relevant troubleshooting guide / SOP (use
`docs_search` if needed, and cite the document title and revision). Do this now, while the
session is still open, so the entries are captured and the "Recommended Corrective Actions"
section of `summary.md` is never empty.

### 3. Auto-finalize if needed

Check if the session has a `session_meta.json`. If not, call `audit_end_session` to finalize it before rendering.

### 4. Render the reports

```
<venv-python> render_audit.py traces/{run_id}
```

Capture the output. This generates both `report.md` (detailed) and `summary.md` (executive summary). If the script fails, diagnose and report the error.

### 5. Open the reports

```
<open> traces/{run_id}/summary.md
<open> traces/{run_id}/report.md
```

### 6. Summarize

Report to the user:
- Both reports have been generated and opened
- `summary.md` is the executive one-pager (root cause, investigation flow, recommendations)
- `report.md` is the full detailed report with all hypotheses, evidence, and appendices
- The trace SHA-256 hash (read from `traces/{run_id}/session_meta.json`)
- The number of tool calls and reasoning entries
- Any warnings the renderer flagged
- Clickable links to both files, formatted as markdown links using the full `file:///` URL
  with spaces encoded as `%20`. **Derive the project's absolute path at runtime — do not
  hardcode it.** Run `<venv-python> -c "import os; print(os.path.abspath('.'))"` to get the project
  root, convert backslashes to forward slashes, URL-encode spaces as `%20`, and prepend
  `file:///`. Then build:

  **Audit Trail Files**
  - [summary.md](file:///<project-root>/traces/{run_id}/summary.md) — executive summary
  - [report.md](file:///<project-root>/traces/{run_id}/report.md) — full detailed report

  Substitute the actual project root and the actual `{run_id}` value (e.g.
  `20260623_143206_6ba4aa`) into both URLs.
