# Experiment Version 2 — Development CV Estimate

Dedicated XGBoost multiclass nested-CV comparison. The earlier single baseline configuration does not establish that the model family is unsuitable.

**Development data only:** outer 4 folds × 10 repeats, inner 3 stratified folds; 1,087 existing development rows. Each arm uses 24 shared randomized hyperparameter configurations, tunes by Macro F1, and refits its inner winner on the current outer training fold.

| Metric | Unweighted | Frequency weighted | Moderated custom |
|---|---:|---:|---:|
| Macro F1 | 0.2809 ± 0.0228 | 0.3059 ± 0.0352 | 0.3102 ± 0.0388 |
| Balanced Accuracy | 0.2815 ± 0.0206 | 0.3397 ± 0.0522 | 0.3210 ± 0.0533 |
| Quadratic Weighted Kappa | 0.5074 ± 0.0442 | 0.5151 ± 0.0446 | 0.5243 ± 0.0416 |
| Macro PR-AUC (average precision, OvR) | 0.3531 ± 0.0335 | 0.3460 ± 0.0333 | 0.3626 ± 0.0341 |
| Macro ROC-AUC (OvR) | 0.7695 ± 0.0472 | 0.7753 ± 0.0345 | 0.7893 ± 0.0297 |
| MAE | 0.4609 ± 0.0306 | 0.5870 ± 0.0604 | 0.4987 ± 0.0311 |
| ±1 accuracy | 0.9580 ± 0.0108 | 0.9157 ± 0.0257 | 0.9428 ± 0.0122 |

SD is population SD across the 40 dependent outer folds, not a standard error or confidence interval. Macro PR-AUC is macro OvR average precision from native class probabilities; ranking scores are not pooled across differently fitted models.

| Quality | Unweighted F1 | Frequency F1 | Moderated F1 | Unweighted recall | Frequency recall | Moderated recall |
|---|---:|---:|---:|---:|---:|---:|
| 3 | 0.0000 ± 0.0000 | 0.1102 ± 0.1531 | 0.0692 ± 0.1420 | 0.0000 ± 0.0000 | 0.1875 ± 0.2421 | 0.1000 ± 0.2000 |
| 4 | 0.0033 ± 0.0208 | 0.0993 ± 0.0631 | 0.0564 ± 0.0693 | 0.0023 ± 0.0142 | 0.1477 ± 0.0947 | 0.0502 ± 0.0635 |
| 5 | 0.6853 ± 0.0280 | 0.6464 ± 0.0279 | 0.6795 ± 0.0277 | 0.7210 ± 0.0423 | 0.6271 ± 0.0445 | 0.7019 ± 0.0460 |
| 6 | 0.5597 ± 0.0321 | 0.4621 ± 0.0533 | 0.5317 ± 0.0368 | 0.5895 ± 0.0470 | 0.4124 ± 0.0726 | 0.5248 ± 0.0585 |
| 7 | 0.4172 ± 0.0593 | 0.4488 ± 0.0418 | 0.4319 ± 0.0588 | 0.3617 ± 0.0837 | 0.5715 ± 0.0808 | 0.4345 ± 0.1047 |
| 8 | 0.0200 ± 0.0872 | 0.0686 ± 0.1025 | 0.0923 ± 0.1405 | 0.0146 ± 0.0642 | 0.0917 ± 0.1341 | 0.1146 ± 0.1794 |

Each outer validation fold has only two quality-3 wines and three or four quality-8 wines. Per-class estimates remain sensitive to individual observations.

| Runtime (seconds) | Unweighted | Frequency weighted | Moderated custom |
|---|---:|---:|---:|
| All inner searches | 232.981 | 253.849 | 257.295 |
| 40 outer refits | 4.173 | 3.950 | 2.841 |
| 40 outer scoring calls | 0.872 | 0.857 | 0.830 |
| Measured search + refit + score | 238.026 | 258.656 | 260.966 |

Total experiment wall time: **760.13 seconds**, excluding kernel startup. All **8,760 fits** completed. These are serial one-thread CPU measurements for the registered procedures, including wrapper/audit overhead; they are not general hardware-independent runtime claims.

| Paired Macro F1 difference | Mean | SD | Positive / negative / tied folds |
|---|---:|---:|---:|
| frequency minus unweighted | +0.0250 | 0.0409 | 31 / 9 / 0 |
| moderated custom minus unweighted | +0.0292 | 0.0377 | 31 / 9 / 0 |
| moderated custom minus frequency | +0.0042 | 0.0457 | 26 / 14 / 0 |

Paired differences compare the complete separately tuned procedures. They are descriptive: overlapping folds are not independent trials, and the moderated arm jointly varies tree settings and class multipliers.

## Search and weighting definitions

| Hyperparameter | Registered choices |
|---|---|
| n_estimators | 80, 150, 250, 400 |
| learning_rate | 0.02, 0.04, 0.07, 0.12 |
| max_depth | 2, 3, 4 |
| min_child_weight | 1, 2, 4, 8 |
| subsample | 0.7, 0.85, 1.0 |
| colsample_bytree | 0.7, 0.85, 1.0 |
| gamma | 0.0, 0.1, 0.5, 1.0 |
| reg_alpha | 0.0, 0.01, 0.1, 1.0 |
| reg_lambda | 1.0, 3.0, 10.0, 30.0 |

The candidate pool is generated before fitting with seed 5242, balanced marginal coverage and randomized joint combinations. The three arms share the same 24 hyperparameter configurations and fold seeds. There is no enormous Cartesian grid, post-result search expansion or candidate retry.

Unweighted fits use unit sample weights. Frequency weights are `n_train / (6 * n_class_train)`. Moderated weights are `clip(sqrt(frequency_weight) * multiplier[class], 0.5, 6)` before normalization. All schemes normalize to mean sample weight one using only the current fitting labels. Multipliers vary independently across all six classes: 0.75/1/1.25/1.5 for classes 3 and 8; 0.75/1/1.25 for classes 4 and 7; 0.9/1/1.1 for classes 5 and 6. The first moderated recipe uses all-one multipliers. The pre-normalization cap bounds the maximum/minimum weight ratio at 12.

The wrapper recomputes weights for every inner fit and outer refit, passes them as `sample_weight`, and maps quality labels 3–8 to 0–5 for `multi:softprob`. Predictions and probability columns map back to the six original labels. All validation metrics are unweighted. No global weights, binary `scale_pos_weight`, calibration or threshold tuning are used.

Trees have depth 2–4. Numeric schema validation precedes histogram XGBoost, with feature binning and trees learned only from training rows. Early stopping is disabled: `n_estimators` is tuned inside inner CV, and no validation `eval_set` enters fitting. The `mlogloss` monitoring default does not select candidates.

See the official [XGBoost parameters](https://xgboost.readthedocs.io/en/stable/parameter.html) and [Python fit API](https://xgboost.readthedocs.io/en/stable/python/python_api.html).

| Quality | Unweighted outer-refit weight | Frequency weight mean (min–max) | Moderated weight mean (min–max) |
|---|---:|---:|---:|
| 3 | 1.000 | 22.646 (22.639–22.667) | 6.300 (4.245–7.575) |
| 4 | 1.000 | 4.315 (4.245–4.387) | 2.745 (1.893–3.318) |
| 5 | 1.000 | 0.393 (0.393–0.394) | 0.770 (0.681–0.834) |
| 6 | 1.000 | 0.423 (0.423–0.424) | 0.767 (0.699–0.877) |
| 7 | 1.000 | 1.352 (1.345–1.358) | 1.272 (1.011–1.760) |
| 8 | 1.000 | 12.970 (12.348–13.583) | 4.832 (3.064–6.689) |

Outer-refit weights are descriptive summaries of separately selected recipes and fold counts, not a new class-weight recipe. Inner-fit weights differ and are retained in the audit table.

## Interpretation and limitations

The observed Macro F1 means were **0.2809** for unweighted XGBoost, **0.3059** for frequency weighting, and **0.3102** for moderated custom weighting. **Moderated custom** had the highest mean among these three registered procedures.

The moderated-minus-frequency paired Macro F1 difference was **+0.0042**, with descriptive paired-fold SD **0.0457**. That small mean gap does not establish a definitive winner. Frequency weighting had higher Balanced Accuracy (**0.3397 versus 0.3210**) and quality-3 F1 (**0.1102 versus 0.0692**); moderated weighting had higher Macro PR-AUC (**0.3626 versus 0.3460**) and quality-8 F1 (**0.0923 versus 0.0686**). Both weighted procedures had higher mean Macro F1 than the unweighted procedure, while performance on the rare classes remained weak and variable. These observations apply to the registered tuning procedures, not to class weighting in isolation.

This comparison re-evaluates XGBoost with multiclass weighting and a controlled conservative search. It neither treats the earlier baseline as a verdict on the family nor establishes that every possible XGBoost configuration has been assessed. The finite 24-candidate budget per arm leaves substantial unexplored parameter space.

The per-arm nested estimates cover their registered inner selection processes. Choosing an arm retrospectively using its outer mean would introduce an additional selection step not evaluated by those per-arm estimates. No arm is automatically promoted, no all-development final model is fitted, and no new independent test claim is made. Previous development exploration remains part of the context.

All new experimentation used the locked development membership. The original final holdout was not accessed or evaluated by the experiment, and all Version 1 results remain preserved. Clean-kernel guards check raw training/validation calls, native sample weights and the absence of early stopping. Saved evidence supports reconstruction of every outer metric, candidate selection and training-weight calculation.

Evidence: [registered plan and candidates](xgboost_20261012/plan.json), [metric comparison](xgboost_20261012/metric_comparison.csv), [per-class table](xgboost_20261012/per_class_comparison.csv), [runtime table](xgboost_20261012/runtime_comparison.csv), [outer selected recipes](xgboost_20261012/outer_fold_metrics.csv), [inner scores](xgboost_20261012/inner_fold_scores.csv), [per-fit weights and training audits](xgboost_20261012/training_audits.csv), and [paired fold differences](xgboost_20261012/paired_fold_differences.csv).
