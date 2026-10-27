# Development-only class-imbalance experiment record

Final verification run: `e7399111-e84d-4cc8-b880-bc1ba247daac`. Primary comparison:
[class_imbalance_experiments.csv](class_imbalance_experiments.csv).

The fixed plan evaluated 18 conditions over the same five stratified development
folds (90 fits) and recorded three unsupported class-weight combinations. There
were 1,087 development rows, with exactly one OOF prediction per original row per
condition. The final test set remains locked and was not evaluated; no final
strategy or model has been selected.

## Implementation

The five tuned families retain their selected parameters. Each is compared with
its original training distribution, RandomOverSampler and SMOTE. Logistic
Regression and Random Forest additionally support balanced class weights; the
specialized BalancedRandomForest comparison uses the tuned forest's shared tree
settings. Native class weights are not substituted for unsupported estimators.

All scalers and resamplers are fitted inside CV training folds. ROS and SMOTE use
the same partial target: at most three times the class's original count, capped at
half the largest training class. SMOTE adapts its neighbor count to training
support and explicitly skips targeted singleton classes. Its distance scaling for
trees is inverted before model fitting. Validation rows are never resampled.

The exports retain mean and population SD for every predefined metric, pooled OOF
metrics, all six classes' precision/recall/F1, full classification reports, actual
sampling counts, paired fold deltas, precision review flags, runtime, frozen
parameters and run provenance. Accuracy does not determine the ranking.

## Observed tradeoffs

All entries below are fold means from saved predictions; Macro F1 also shows
population fold SD. Macro AP is One-vs-Rest Average Precision.

| Family / treatment | Macro F1 ± fold SD | Balanced accuracy | QWK | Macro AP | Accuracy |
|---|---:|---:|---:|---:|---:|
| lda / original | 0.3474 ± 0.0476 | 0.3569 | 0.5461 | 0.3767 | 0.5695 |
| lda / smote | 0.3669 ± 0.0355 | 0.3990 | 0.5308 | 0.3761 | 0.5171 |
| gradient_boosting / original | 0.3052 ± 0.0622 | 0.3045 | 0.5099 | 0.3833 | 0.5814 |
| gradient_boosting / random_over | 0.3285 ± 0.0464 | 0.3435 | 0.5290 | 0.3494 | 0.5787 |
| logistic_regression / original | 0.3014 ± 0.0389 | 0.2938 | 0.5034 | 0.3591 | 0.5814 |
| logistic_regression / random_over | 0.3196 ± 0.0365 | 0.3217 | 0.5266 | 0.3539 | 0.5621 |
| logistic_regression / class_weight_balanced | 0.2716 ± 0.0210 | 0.3761 | 0.4536 | 0.3236 | 0.4140 |
| random_forest / original | 0.2856 ± 0.0143 | 0.2879 | 0.5216 | 0.3893 | 0.6062 |
| random_forest / balanced_random_forest | 0.2647 ± 0.0246 | 0.3689 | 0.4724 | 0.3502 | 0.4021 |

LDA with capped SMOTE has the highest mean Macro F1, improving by
0.0196 in 4/5 folds. However,
the paired-difference SD is 0.0510; QWK and accuracy
fall, and Macro AP is slightly lower. Its quality-8 pooled OOF precision is
9.52% (2 correct among 21 predictions), with recall
14.29% (2 of 14 examples). This activates a predeclared
precision review flag. The aggregate gain does not justify automatic adoption.

Random oversampling improves Gradient Boosting and Logistic Regression Macro F1
in four and five folds respectively, without triggering the predeclared precision
flags; their probability-ranking and accuracy tradeoffs still need review.
Balanced Logistic Regression and BalancedRandomForest gain balanced accuracy but
lose Macro F1 and accuracy. Gaussian NB performs worse with either oversampler.
These results do not support assuming oversampling or higher recall is always
beneficial. Flag thresholds are review prompts, not guarantees of adequacy.

## Checks and execution

- Nine synthetic imbalance tests passed, including a complete export integration
  check, adaptive/singleton SMOTE, preserved tree feature names/units, training-only
  scaler/sampler fitting, prediction-time bypass and class-probability alignment.
- Fifty existing evaluation, preprocessing, model-registry, timing, benchmark and
  tuning tests passed (59 distinct relevant tests including the nine above).
  Whole-source data-audit tests were not rerun during this locked-development phase.
- All nine imbalance notebook code cells executed successfully; notebook schema
  validation passed. Earlier audit, EDA, baseline and tuning cells were not rerun.
- An independent audit recomputed all 11 metrics for 90 folds and 18 pooled OOF
  sets plus fold means/SDs: 1,584 metric comparisons and 2,592 per-class report
  comparisons passed at 1e-12. Actual training-fold counts, weights, sampling
  targets, SMOTE neighbors and balanced-forest draw sizes matched all 90 audits.
- Every original-distribution condition reproduced the frozen tuning reference.
- A first run (`a043126a-c279-4efd-a775-80bd9f4c85a8`) emitted 20 feature-name
  warnings for tree SMOTE. Preserving DataFrame column names fixed the issue.
  Verification reran the same 90 fits with no changes to numeric parameters,
  sampling rules or model-selection decisions. All 19,566 OOF rows, including
  predictions and probabilities, are exactly identical; per-class reports,
  sampling audits and predictive metrics are also unchanged. The final run has
  zero captured model warnings. Both runs remain identified in the cumulative
  runtime CSV (36 records, 180 total outer-fold fits across the two runs).
- Final-run total CV wall time summed across the 18 conditions was
  15.224 seconds. This is not a whole-notebook duration.
  Timings vary with hardware, machine load and thread settings; native pools and
  models were limited to one thread/worker here.
- Checksums confirm the dataset, read-only Telco notebook, split manifest, holdout
  lock and all earlier benchmark/tuning/model/visual outputs are unchanged.

For exact reproduction of probability ranking metrics, load saved CSV probabilities
with `pd.read_csv(path, float_precision="round_trip")`. Default float parsing can
perturb nearly tied scores enough to change ROC-AUC/AP slightly.

## Warnings and limitations

Qualities 3 and 8 have only 8 and 14 development observations, respectively,
leaving 6–7 and 11–12 original examples in training folds. SMOTE feasibility is
not evidence of adequate statistical support: synthetic observations can overfit
rare groups or create implausible chemistry. ROS adds no independent observations.
The balanced forest draws only 36–42 examples per tree under the recorded policy.

Previously tuned parameters and reused development folds make these comparisons
selection-biased; they are not nested-CV estimates. Fold SDs and paired differences
are descriptive, not significance tests. Prior changes from resampling can affect
probability calibration. No calibration or threshold search was added.

Jupyter reported its local TCP transport encryption startup warning; experiment
models emitted no warnings in the verified run. Final selection, holdout testing,
interpretation of a final model and packaging remain later, unauthorized phases.

## Files changed

- `README.md`
- `notebook/Wine-Quality-Classification.ipynb`
- `src/wine_quality/imbalance.py`
- `src/wine_quality/timing.py`
- `tables/class_imbalance_classification_reports.json`
- `tables/class_imbalance_experiments.csv`
- `tables/class_imbalance_fold_audits.json`
- `tables/class_imbalance_fold_metrics.csv`
- `tables/class_imbalance_metadata.json`
- `tables/class_imbalance_oof_predictions.csv`
- `tables/class_imbalance_per_class_metrics.csv`
- `tables/class_imbalance_plan.json`
- `tables/class_imbalance_run_report.md`
- `tables/class_imbalance_smote_feasibility.csv`
- `tables/class_imbalance_warnings.csv`
- `tables/model_runtime_comparison.csv`
- `tests/test_imbalance.py`

Local environment only: installed `imbalanced-learn==0.14.2` and its
`sklearn-compat==0.1.6` dependency in `.venv`; requirements already included
imbalanced-learn. No source CSV, Telco notebook, lock, model artifact or figure
was changed.
