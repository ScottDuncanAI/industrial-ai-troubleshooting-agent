# ML Fault Detection

Run Isolation Forest anomaly detection and XGBoost feature importance analysis on the boiler historian data to identify fault periods and rank early-warning sensors.

## Steps

### 1. Confirm data range

Call `historian_get_data_range` to confirm the dataset's time span and report it to the user before running.

### 2. Run the analysis

Run the ML fault detection script:

```
python ml_fault_detection.py --downsample-minutes 1 --top-n-events 5
```

Capture the JSON output from stdout. The script prints progress to stderr and the JSON summary to stdout. If xgboost is not installed the script automatically falls back to GradientBoostingClassifier — note which model was used from the `feature_importance.model` field.

If the script fails, diagnose the error from stderr and report it to the user.

### 3. Open key plots

All outputs are saved to `plots/MLFault/MLFault_<date>/`. Open the monitoring chart, feature importance chart, and fault report:

```
start <monitoring_plot_path>
start <feature_importance_plot_path>
start <fault_report_path>
```

### 4. Present model summary

Report to the user:
- Total observations and downsample resolution
- NOC training set size (rows where TE_8332A is in [530–545°C] vs total rows)
- Contamination parameter used and resulting anomaly rate
- Number of fault periods detected

### 5. Investigate worst fault events

For each of the top fault events in `worst_events`:
1. Call `alarm_search_context(event.start, window_minutes=30)` — what alarms were firing around this event?
2. Call `alarm_get_active_at(event.start)` — full list of active alarms at the fault peak
3. Note whether `TE_8332A` was outside 530–545°C at that time (cross-reference with monitoring plot)

Summarize for each: timing, duration, alarm context, and whether the Isolation Forest flagged it before TE_8332A left its normal range.

### 6. Feature importance follow-up

For the top 3 tags in `feature_importance.top_features`:
1. Call `kg_get_upstream_sensors(tag)` — what equipment is upstream of this leading indicator?
2. Call `alarm_get_statistics(start_time, end_time, tag_names=[tag])` — how often did this tag alarm across the full dataset?

This answers: which sensors operators should watch as early warnings, and what process equipment drives them.

### 7. Documentation cross-reference

For the top feature importance tag, call:
- `docs_search(query, sensor_tag="<top_tag>", doc_type="troubleshooting")` — surface the relevant diagnostic guide

Cite the result with title and revision: *"Per [Document Title], Rev [X.X]: ..."*

### 8. Present interpretation

Explain the findings using this framework:

- **Isolation Forest anomaly score** reflects how isolated a data point is in the 30-dimensional sensor space — not just TE_8332A deviating, but unusual combinations across all tags simultaneously. A high score during a period when TE_8332A is still in range is particularly significant: it may indicate a developing fault before the primary KPI is affected.

- **XGBoost feature importances** rank the other 29 tags by how well they predict TE_8332A leaving its normal range. High-importance tags are leading indicators — sensors whose abnormality tends to precede or co-occur with steam temperature excursions. These are distinct from PCA loadings: they reflect predictive power, not variance contribution.

- **Comparison to MSPC** (if already run): periods flagged by Isolation Forest but not MSPC (or vice versa) represent anomalies the linear model misses due to non-linear multivariate interactions. Note any such discrepancies for the user.
