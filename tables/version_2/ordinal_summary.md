# Version 2 — Ordinal Classification Experiments

**Development CV estimates only.** The target order is **3 < 4 < 5 < 6 < 7 < 8**. All 1,087 existing development wines retain their original membership. The Version 1 holdout result remains locked and unchanged; the experiment never evaluates or tunes against it.

## Models and reconstruction

- **Exact cumulative-link / proportional-odds logistic:** one shared linear score and five strictly increasing cutpoints. Optimize the exact categorical likelihood, with L2-regularized slopes and unpenalized cutpoints. There is no additional intercept. A notebook-local implementation uses the existing SciPy optimizer; independent finite-difference checks validate its analytic gradient. This is a true ordinal model, not an all-threshold binary-loss surrogate.
- **Ordered binary thresholds:** five logistic classifiers learn `Y>3`, `Y>4`, `Y>5`, `Y>6`, `Y>7`. Their slopes may differ. Project each sample's exceedance vector to the nearest nonincreasing vector with equal-weight PAVA, preserving threshold meanings. The repair uses no validation labels and is not fitted calibration.
- **Nominal multinomial logistic:** a matched ordinary multiclass control. Giving it integer labels and reporting QWK does not make its objective ordinal. Its native softmax probabilities and decoder remain unchanged; derived tails are only diagnostic.
- **Inner-selected ordinal procedure:** inner Macro F1 chooses among the two ordinal families, then reuses the chosen family's outer refit and predictions. The nominal control is not eligible for this derived procedure.

For exceedance probabilities `q3≥q4≥q5≥q6≥q7`, class masses are `[1−q3, q3−q4, q4−q5, q5−q6, q6−q7, q7]`. Validate finiteness, nonnegativity and a unit sum. All metrics use the same **argmax** class prediction, with exact ties assigned to the lower quality. No posterior-median, rounded expected-value or QWK-specific decoder is substituted. Sorting threshold outputs is not a valid repair because it swaps threshold identities.

Neural CORAL/CORN are **deferred**, not shown unsuitable: architecture/optimization/epoch choices would add complexity with very little genuine tail support; conditional CORN tasks further reduce later-head samples. The compact linear study is the initial ordinal comparison. Primary references: [McCullagh's cumulative-link model](https://doi.org/10.1111/j.2517-6161.1980.tb01109.x), [Frank–Hall threshold decomposition](https://researchcommons.waikato.ac.nz/bitstreams/66ed9342-a2ca-4edb-b27b-962bb6eed025/download), [ordered-model identification](https://www.statsmodels.org/stable/examples/notebooks/generated/ordinal_regression.html), [CORAL](https://arxiv.org/abs/1901.07884), [CORN](https://arxiv.org/abs/2111.08851).

## Registered experiment

- Outer: **stratified 4-fold × 10 repeats**, seed 42. Inner: **stratified 3-fold**, seed 1042 + outer-split index. Exact memberships and class supports are saved.
- Eight candidates per family: **C = 0.1, 1, 10, 100** × **none / square-root frequency weights**. Same candidate budget, scaling and decision rule. The regularization strength's practical effect differs across model objectives and parameter counts.
- Weights derive from the six genuine class frequencies in the actual training fold: `sqrt(n/(6*n_class))`, normalized to mean one. The same row weights enter every binary head; there is no binary-specific balancing. Weighted model outputs are not claimed to be calibrated under the original class prior.
- **Schema → training-only StandardScaler → classifier**. No resampling, feature engineering, early stopping, calibration or decision-threshold tuning. Selection maximizes mean inner **six-class Macro F1**; exact ties follow registered order. QWK and the other supporting metrics do not select candidates.
- **2,880 inner fits + 120 outer refits = 3,000 model fits**, consisting of 6,000 native binary/multinomial fits and 1,000 cumulative-link optimizations. Forty derived joint evaluations add no fits. Every candidate converged; no failed candidate/fold was dropped.

## Development CV results

| Procedure | Macro F1 mean ± SD | Balanced Accuracy mean ± SD | QWK mean ± SD | MAE mean ± SD | ±1 accuracy mean ± SD |
| --- | --- | --- | --- | --- | --- |
| Cumulative logit (ordinal) | 0.3127 ± 0.0591 | 0.3166 ± 0.0584 | 0.5224 ± 0.0373 | 0.5064 ± 0.0259 | 0.9524 ± 0.0090 |
| Ordered thresholds + PAVA (ordinal) | 0.3485 ± 0.0622 | 0.3645 ± 0.0739 | 0.5238 ± 0.0446 | 0.5185 ± 0.0438 | 0.9359 ± 0.0175 |
| Nominal logistic (control) | 0.3318 ± 0.0467 | 0.3612 ± 0.0645 | 0.5036 ± 0.0425 | 0.5325 ± 0.0387 | 0.9271 ± 0.0190 |
| Inner-selected ordinal procedure | 0.3481 ± 0.0626 | 0.3620 ± 0.0720 | 0.5243 ± 0.0447 | 0.5164 ± 0.0442 | 0.9367 ± 0.0183 |

SD is population SD across **40 dependent outer folds**, not a standard error. The CSV includes min/max, PR-AUC and ROC-AUC as supplementary metrics. Macro PR-AUC uses per-fold OvR average precision; scores from different fitted folds are never pooled for ranking metrics.

| Compared with nominal logistic | Mean Δ Macro F1 | SD of paired differences | Min Δ | Max Δ |
| --- | --- | --- | --- | --- |
| Cumulative logit (ordinal) | -0.0191 | 0.0548 | -0.1212 | +0.1266 |
| Ordered thresholds + PAVA (ordinal) | +0.0167 | 0.0408 | -0.0900 | +0.1006 |
| Inner-selected ordinal procedure | +0.0164 | 0.0409 | -0.0900 | +0.1006 |

## Six-class performance

| Procedure | Quality 3 F1 | Quality 4 F1 | Quality 5 F1 | Quality 6 F1 | Quality 7 F1 | Quality 8 F1 |
| --- | --- | --- | --- | --- | --- | --- |
| Cumulative logit (ordinal) | 0.1958 | 0.0366 | 0.6634 | 0.4980 | 0.4166 | 0.0658 |
| Ordered thresholds + PAVA (ordinal) | 0.2655 | 0.1121 | 0.6772 | 0.5028 | 0.4368 | 0.0968 |
| Nominal logistic (control) | 0.2184 | 0.0848 | 0.6831 | 0.4986 | 0.4259 | 0.0799 |
| Inner-selected ordinal procedure | 0.2668 | 0.1051 | 0.6774 | 0.5043 | 0.4383 | 0.0968 |

Minority-class precision and recall remain important even when MAE or QWK improves:

| Procedure | Quality | Precision | Recall | F1 | Zero-prediction folds |
| --- | --- | --- | --- | --- | --- |
| Cumulative logit (ordinal) | 3 | 0.2292 | 0.1875 | 0.1958 | 12/40 |
| Cumulative logit (ordinal) | 4 | 0.0503 | 0.0293 | 0.0366 | 1/40 |
| Cumulative logit (ordinal) | 7 | 0.4127 | 0.4295 | 0.4166 | 0/40 |
| Cumulative logit (ordinal) | 8 | 0.0667 | 0.0688 | 0.0658 | 3/40 |
| Ordered thresholds + PAVA (ordinal) | 3 | 0.2730 | 0.3375 | 0.2655 | 4/40 |
| Ordered thresholds + PAVA (ordinal) | 4 | 0.1599 | 0.0966 | 0.1121 | 2/40 |
| Ordered thresholds + PAVA (ordinal) | 7 | 0.4243 | 0.4608 | 0.4368 | 0/40 |
| Ordered thresholds + PAVA (ordinal) | 8 | 0.1012 | 0.1104 | 0.0968 | 1/40 |
| Nominal logistic (control) | 3 | 0.1968 | 0.3500 | 0.2184 | 4/40 |
| Nominal logistic (control) | 4 | 0.1177 | 0.0741 | 0.0848 | 3/40 |
| Nominal logistic (control) | 7 | 0.4203 | 0.4435 | 0.4259 | 0/40 |
| Nominal logistic (control) | 8 | 0.0664 | 0.1167 | 0.0799 | 1/40 |
| Inner-selected ordinal procedure | 3 | 0.2784 | 0.3250 | 0.2668 | 4/40 |
| Inner-selected ordinal procedure | 4 | 0.1529 | 0.0895 | 0.1051 | 2/40 |
| Inner-selected ordinal procedure | 7 | 0.4258 | 0.4623 | 0.4383 | 0/40 |
| Inner-selected ordinal procedure | 8 | 0.1012 | 0.1104 | 0.0968 | 2/40 |

All six classes' precision/recall/F1, support and confusion counts are available in `per_class_comparison.csv`, `outer_per_class.csv`, and `repeat_per_class.csv`. Zero-prediction precision is reported as zero and its undefined status is recorded separately.

## Reconstruction and stability

| Procedure | Crossing rows | Fraction | Mean absolute correction | Maximum correction | Remaining crossings |
| --- | --- | --- | --- | --- | --- |
| Cumulative logit (ordinal) | 0 | 0.00% | 0.000000 | 0.000000 | 0 |
| Ordered thresholds + PAVA (ordinal) | 361 | 3.32% | 0.000405 | 0.376867 | 0 |
| Nominal logistic (control) | 0 | 0.00% | 0.000000 | 0.000000 | 0 |
| Inner-selected ordinal procedure | 346 | 3.18% | 0.000395 | 0.376867 | 0 |

Counts refer to repeated outer predictions, not unique independent wines. Maximum raw threshold-order violation was 0.7537. PAVA's largest adjustment was 0.3769. Cumulative-link cutpoints stayed ordered; the smallest fitted adjacent gap was 1.4254. All 1,000 cumulative-link optimizations converged in 29–63 iterations; maximum free-parameter gradient magnitude was 1.40e-6 (registered acceptance bound 1e-4), and maximum original-cutpoint gradient magnitude was 8.04e-7.

| Procedure | Chosen family | C | Weight policy | Outer folds |
| --- | --- | --- | --- | --- |
| Cumulative logit (ordinal) | cumulative_logit | 0.1 | sqrt_frequency | 10 |
| Cumulative logit (ordinal) | cumulative_logit | 1 | sqrt_frequency | 13 |
| Cumulative logit (ordinal) | cumulative_logit | 10 | sqrt_frequency | 14 |
| Cumulative logit (ordinal) | cumulative_logit | 100 | sqrt_frequency | 3 |
| Nominal logistic (control) | nominal_logit | 0.1 | sqrt_frequency | 14 |
| Nominal logistic (control) | nominal_logit | 1 | sqrt_frequency | 9 |
| Nominal logistic (control) | nominal_logit | 10 | none | 3 |
| Nominal logistic (control) | nominal_logit | 10 | sqrt_frequency | 7 |
| Nominal logistic (control) | nominal_logit | 100 | sqrt_frequency | 7 |
| Ordered thresholds + PAVA (ordinal) | ordered_thresholds | 0.1 | sqrt_frequency | 21 |
| Ordered thresholds + PAVA (ordinal) | ordered_thresholds | 1 | none | 2 |
| Ordered thresholds + PAVA (ordinal) | ordered_thresholds | 1 | sqrt_frequency | 10 |
| Ordered thresholds + PAVA (ordinal) | ordered_thresholds | 10 | sqrt_frequency | 4 |
| Ordered thresholds + PAVA (ordinal) | ordered_thresholds | 100 | none | 1 |
| Ordered thresholds + PAVA (ordinal) | ordered_thresholds | 100 | sqrt_frequency | 2 |
| Inner-selected ordinal procedure | cumulative_logit | 0.1 | sqrt_frequency | 1 |
| Inner-selected ordinal procedure | cumulative_logit | 10 | sqrt_frequency | 1 |
| Inner-selected ordinal procedure | ordered_thresholds | 0.1 | sqrt_frequency | 20 |
| Inner-selected ordinal procedure | ordered_thresholds | 1 | none | 2 |
| Inner-selected ordinal procedure | ordered_thresholds | 1 | sqrt_frequency | 9 |
| Inner-selected ordinal procedure | ordered_thresholds | 10 | sqrt_frequency | 4 |
| Inner-selected ordinal procedure | ordered_thresholds | 100 | none | 1 |
| Inner-selected ordinal procedure | ordered_thresholds | 100 | sqrt_frequency | 2 |

## Runtime

| Family | Inner search seconds | Outer refit seconds | Outer scoring seconds |
| --- | --- | --- | --- |
| Cumulative logit (ordinal) | 11.85 | 0.42 | 0.88 |
| Nominal logistic (control) | 37.11 | 1.11 | 0.73 |
| Ordered thresholds + PAVA (ordinal) | 20.31 | 0.84 | 0.74 |

Total measured experiment time was **78.05 seconds**, including audit/aggregation overhead, on serial one-thread CPU execution. Derived joint estimates reuse fits and are not counted twice. `warnings.json` retains 120 existing pandas reporting FutureWarnings; there were no convergence warnings. No dependency installation or existing utility change was required.

## Interpretation

**Ordered binary thresholds were the stronger ordinal approach in this bounded study.** Their development Macro F1 was **0.3485 ± 0.0622**, versus **0.3318 ± 0.0467** for the equally tuned nominal logistic control. The mean paired difference was **+0.0167**, with fold differences ranging from **−0.0900 to +0.1006**. This is a descriptive development comparison, not a significance claim or independent-test improvement. The threshold procedure also had higher fold variability.

**Cumulative logit illustrates why QWK alone is insufficient.** It improved MAE (**0.5064 vs 0.5325**) and ±1 accuracy (**0.9524 vs 0.9271**) relative to the nominal control, but its Macro F1 fell to **0.3127**. Quality-4 F1 was only **0.0366** and quality-8 F1 **0.0658**. More near-correct predictions do not establish satisfactory six-class discrimination.

The fully inner-selected ordinal procedure chose ordered thresholds in **38/40** outer training splits and cumulative logit in **2/40**. Its Macro F1 was **0.3481 ± 0.0626**. This estimates the registered choice between those two ordinal procedures; it does not estimate retrospectively choosing among every model previously studied in the project.

Even the stronger threshold procedure had low quality-4/8 F1 (**0.1121 / 0.0968**). Only **two quality-3** and **three–four quality-8** genuine examples occur in each outer validation fold. Repeated CV reuses those wines; it does not create more independent rare-class evidence.

Threshold outputs crossed on **361/10,870 repeated outer prediction rows (3.32%)**. PAVA eliminated every crossing. Average absolute correction was small (**0.000405**), but an individual threshold probability changed by as much as **0.3769**; raw independent outputs therefore cannot be blindly differenced. Cumulative-link and nominal-derived tails had no crossings in this run.

Some inner selections reached the registered C boundaries. The search was not expanded after viewing outer results. No final family, new feature, threshold, or model was selected using the old holdout, and no all-development deployment model was fitted.

## Verification and evidence

- 16 synthetic framework check groups: exact NLL/gradient, extreme logits, PAVA vs sorting, probability reconstruction, ties, class-aligned nominal outputs, cloning, fold-local weights/scaling, invalid inputs, forced optimizer failure, and outer-validation perturbation invariance. These use 48 successful synthetic model fits and one deliberately failed fit.
- A complete synthetic end-to-end fixture validated all 40 outer plans and training guards before the wine run, with filesystem guards forbidding wine-data reads.
- Actual wine execution guards checked exact training/validation membership and feature values, scaler inputs, binary labels, six-class weights and cumulative optimizer inputs. Historical model/result access, holdout evaluation, and resampling were blocked during the experiment.
- Saved-evidence validation reconstructs exact splits, all 3,000 training audits, inner winners, the joint procedure, probabilities, metrics and every per-class report. Five deliberately corrupted evidence copies were rejected.
- Fresh-kernel study replay and full-notebook replay records are stored separately under `ordinal_verification`. Earlier notebook cells and result files are preserved exactly. Ordinary Run All replays evidence; new experiment execution requires a new unique run ID.

All raw tables, predictions, training audits and file hashes are under `tables/version_2/ordinal_20261015/`. Main files: `metric_comparison.csv`, `per_class_comparison.csv`, `paired_nominal_differences.csv`, `outer_fold_metrics.csv`, `outer_oof_predictions.csv`, `reconstruction_diagnostics.csv`, `inner_candidate_scores.csv`, `training_audits.json`, `plan.json`, and `manifest.json`.
