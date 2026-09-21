# Research notes: Quantifying infrastructure noise in agentic coding evals

- **Title:** Quantifying infrastructure noise in agentic coding evals
- **URL:** https://www.anthropic.com/engineering/infrastructure-noise
- **Date:** February 5, 2026
- **Author:** Gian Segato (thanks to Nicholas Carlini, Jeremy Hadfield, Mike Merrill, Alex Shaw)
- **Source status:** full text verified from the anthropic-mirror archive.

## Thesis

Agentic coding benchmarks such as SWE-bench and Terminal-Bench are treated as precise measurements, but the runtime environment is part of the test. Infrastructure configuration alone can swing scores by more than the gap between leaderboard leaders: on Terminal-Bench 2.0 the difference between the most and least resourced setups was 6 percentage points (p < 0.01).

## Findings and numbers

- Anthropic runs Terminal-Bench 2.0 on Google Kubernetes Engine. Treating per-task resource specs as both guaranteed allocation and hard kill limit produced infra error rates up to 6% of tasks (pod errors unrelated to model ability), and scores that did not match the official leaderboard, which uses a more lenient sandbox provider.
- Six configurations were tested, from strict enforcement (1x) to uncapped, with the same model, harness and tasks.
- Infra error rate fell monotonically: 5.8% at 1x, 2.1% at 3x (p < 0.001), 0.5% uncapped.
- Success rates from 1x through 3x stayed within noise (p = 0.40); most tasks crashing at 1x would have failed anyway.
- Above 3x, success rose faster than infra errors fell: 3x to uncapped cut infra errors a further 1.6 points while success rose almost 4 points; total lift over 1x at uncapped was +6 points (p < 0.01). Tasks named: `rstan-to-pystan`, `compile-compcert`, `bn-fit-modify` (installing pandas, networkx, scikit-learn fits under generous limits, out-of-memory under tight ones, while a standard-library implementation exists).
- Replicated across Anthropic models with consistent direction and varying magnitude; not rigorously tested on other providers' models.
- SWE-bench crossover: RAM varied up to 5x across 227 problems with 10 samples each; scores rose monotonically but only 1.54 points higher at 5x than 1x.
- Other variance sources: time limits, cluster health, hardware, concurrency, egress bandwidth, time of day (anecdotal, via API latency).
- Naive binomial confidence intervals already span 1 to 2 points; infrastructure confounders stack on top. Observed spread across moderate configurations was just under 2 points; at the extremes, 6.

## Recommendations

1. Ideal: identical hardware for the scaffold and the inference stack.
2. Specify two parameters per task, a guaranteed allocation and a separate hard kill threshold, never one pinned value.
3. Calibrate the band so scores at floor and ceiling fall within noise (3x worked for Terminal-Bench 2.0: infra errors down about two-thirds with no significant score lift); report the multiplier.
4. Run public benchmarks at multiple times and on multiple days.
5. Treat resource configuration as a first-class experimental variable, documented like prompt format or sampling temperature.
6. Benchmark maintainers should publish recommended specs (as Terminal-Bench 2.0 does) and the enforcement methodology.
7. Consumers should be skeptical of leaderboard differences under 3 percentage points until configurations are documented and matched.

## Implementation checklist

1. Record CPU, memory request, memory limit, time limit, concurrency and date for every eval run.
2. Sweep headroom multipliers (1x, 2x, 3x, 5x, uncapped) once per benchmark; plot infra error rate and success rate; pick the smallest multiplier where scores plateau.
3. Alert when infra error rate exceeds the calibrated baseline.
4. Report the configuration alongside every published score.

## Dependencies

Builds on the evals vocabulary in "Demystifying evals for AI agents" and the Terminal-Bench and SWE-bench material in the SWE-bench Sonnet post; feeds the eval-integrity discussion in the BrowseComp eval-awareness post and the operations lessons in the two postmortems.
