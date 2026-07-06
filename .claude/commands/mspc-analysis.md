# MSPC Analysis

Run Multivariate Statistical Process Control analysis on the boiler historian data using PCA-based monitoring with T-squared and SPE statistics.

## Steps

### 1. Run the analysis

Run the MSPC analysis script:

```
python mspc_analysis.py
```

Capture the JSON output from stdout. The script prints progress to stderr and the JSON summary to stdout.

If the script fails, diagnose the error and report it to the user.

### 2. Open key plots and fault report

All outputs are saved to `plots/MSPC/MSPC_<date>/`. Open the monitoring chart, scree plot, and fault report for the user:

```
start <monitoring_plot_path>
start <scree_plot_path>
start <fault_report_path>
```

### 3. Present model summary

Report to the user:
- Number of PCA components retained and cumulative variance explained
- Training set size (NOC rows vs total rows)
- Control limits (T-squared and SPE at 95% and 99% confidence)

### 4. Present anomaly results

Report:
- Percentage of observations exceeding T-squared and SPE limits
- Number and timing of anomalous periods
- Duration of each anomalous period

### 5. Investigate worst events

For each of the top 3 worst T-squared events from the JSON output:
1. Open the contribution plot: `start <contribution_plot_path>`
2. Call `alarm_search_context` at that timestamp to get alarm context
3. Call `kg_get_upstream_sensors` on the top contributing tag to trace process causality
4. Summarize: what tags drove the anomaly, what alarms were active, what equipment is upstream

Do the same for the top 3 worst SPE events (skip any that overlap with T-squared worst events).

### 6. Present interpretation

Explain the findings using this framework:

- **High T-squared only** (within-model): The process deviated in a direction the model has seen before. This usually means an extreme version of normal variation -- load swings, aggressive control action, or a measurable process shift.

- **High SPE only** (outside-model): A new pattern not captured by the PCA model appeared. This usually means a sensor fault, equipment degradation, a process mode change, or a new correlation structure.

- **Both high**: A major process upset combining known and unknown deviation patterns.

For each worst event, state which category it falls into and what the contribution pattern suggests about root cause.
