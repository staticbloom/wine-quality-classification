# Experiment Version 2 — Development CV Estimate

Dedicated LightGBM multiclass nested-CV comparison. The earlier single baseline configuration does not establish that the model family is unsuitable.

**Development data only:** outer 4 folds × 10 repeats, inner 3 stratified folds; 1,087 existing development rows. Each arm uses 24 shared randomized hyperparameter configurations, tunes by Macro F1, and refits its inner winner on the current outer training fold.

| Metric | Unweighted | Balanced sample weights | Moderated custom |
|---|---:|---:|---:|
| Macro F1 | 0.2827 ± 0.0235 | 0.3067 ± 0.0418 | 0.3120 ± 0.0397 |
| Balanced Accuracy | 0.2821 ± 0.0206 | 0.3477 ± 0.0667 | 0.3266 ± 0.0533 |
| Quadratic Weighted Kappa | 0.5094 ± 0.0417 | 0.5192 ± 0.0407 | 0.5334 ± 0.0412 |
| Macro PR-AUC (average precision, OvR) | 0.3614 ± 0.0347 | 0.3463 ± 0.0329 | 0.3620 ± 0.0330 |
| Macro ROC-AUC (OvR) | 0.7868 ± 0.0305 | 0.7753 ± 0.0329 | 0.7861 ± 0.0323 |
| MAE | 0.4627 ± 0.0313 | 0.5921 ± 0.0512 | 0.5053 ± 0.0279 |
| ±1 accuracy | 0.9575 ± 0.0093 | 0.9120 ± 0.0207 | 0.9425 ± 0.0124 |

SD is population SD across the 40 dependent outer folds, not a standard error or confidence interval. Macro PR-AUC is macro OvR average precision from native, uncalibrated class probabilities; ranking scores are not pooled across differently fitted models.

| Quality | Unweighted F1 | Balanced F1 | Moderated F1 | Unweighted recall | Balanced recall | Moderated recall |
|---|---:|---:|---:|---:|---:|---:|
| 3 | 0.0000 ± 0.0000 | 0.0720 ± 0.1157 | 0.0751 ± 0.1446 | 0.0000 ± 0.0000 | 0.1500 ± 0.2291 | 0.1125 ± 0.2088 |
| 4 | 0.0144 ± 0.0434 | 0.1012 ± 0.0643 | 0.0684 ± 0.0759 | 0.0093 ± 0.0280 | 0.1709 ± 0.1176 | 0.0666 ± 0.0794 |
| 5 | 0.6820 ± 0.0272 | 0.6416 ± 0.0265 | 0.6735 ± 0.0239 | 0.7171 ± 0.0469 | 0.6145 ± 0.0484 | 0.6813 ± 0.0444 |
| 6 | 0.5585 ± 0.0367 | 0.4701 ± 0.0475 | 0.5262 ± 0.0404 | 0.5881 ± 0.0520 | 0.4152 ± 0.0617 | 0.5168 ± 0.0606 |
| 7 | 0.4212 ± 0.0711 | 0.4592 ± 0.0532 | 0.4445 ± 0.0533 | 0.3633 ± 0.0907 | 0.5875 ± 0.1006 | 0.4743 ± 0.0815 |
| 8 | 0.0200 ± 0.0872 | 0.0960 ± 0.1221 | 0.0840 ± 0.1369 | 0.0146 ± 0.0642 | 0.1479 ± 0.1923 | 0.1083 ± 0.1789 |

Each outer validation fold has only two quality-3 wines and three or four quality-8 wines. Per-class estimates remain sensitive to individual observations.

| Runtime (seconds) | Unweighted | Balanced sample weights | Moderated custom |
|---|---:|---:|---:|
| All inner searches | 201.803 | 204.804 | 204.376 |
| 40 outer refits | 3.234 | 3.191 | 2.516 |
| 40 outer scoring calls | 1.244 | 1.232 | 1.160 |
| Measured search + refit + score | 206.281 | 209.227 | 208.052 |

Total experiment wall time: **625.84 seconds**, excluding kernel startup. All **8,760 fits** completed. These are serial one-thread CPU measurements for the registered procedures, including wrapper/audit overhead; they are not general hardware-independent runtime claims.

| Paired Macro F1 difference | Mean | SD | Positive / negative / tied folds |
|---|---:|---:|---:|
| frequency minus unweighted | +0.0240 | 0.0367 | 30 / 10 / 0 |
| moderated custom minus unweighted | +0.0293 | 0.0388 | 27 / 13 / 0 |
| moderated custom minus frequency | +0.0053 | 0.0356 | 24 / 16 / 0 |

Paired differences compare the complete separately tuned procedures. They are descriptive: overlapping folds are not independent trials, and the moderated arm jointly varies tree settings and class multipliers.

## Search and weighting definitions

| Hyperparameter | Registered choices |
|---|---|
| num_leaves | 3, 7, 12, 15 |
| max_depth | 2, 3, 4 |
| learning_rate | 0.02, 0.04, 0.07, 0.12 |
| n_estimators | 80, 150, 250, 400 |
| min_child_samples | 20, 30, 45, 60 |
| subsample | 0.7, 0.85, 1.0 |
| colsample_bytree | 0.7, 0.85, 1.0 |
| reg_alpha | 0.0, 0.01, 0.1, 1.0 |
| reg_lambda | 1.0, 3.0, 10.0, 30.0 |

The candidate pool is generated before fitting with seed 7242, balanced coverage of valid leaves/depth pairs and other parameter marginals and randomized joint combinations. The three arms share the same 24 hyperparameter configurations and fold seeds. There is no enormous Cartesian grid, post-result search expansion or candidate retry.

Unweighted fits use unit sample weights. Frequency weights are `n_train / (6 * n_class_train)`. Moderated weights are `clip(sqrt(frequency_weight) * multiplier[class], 0.5, 6)` before normalization. All schemes normalize to mean sample weight one using only the current fitting labels. Multipliers vary independently across all six classes: 0.75/1/1.25/1.5 for classes 3 and 8; 0.75/1/1.25 for classes 4 and 7; 0.9/1/1.1 for classes 5 and 6. The first moderated recipe uses all-one multipliers. The pre-normalization cap bounds the maximum/minimum weight ratio at 12.

The wrapper recomputes weights for every inner fit and outer refit, passes them as `sample_weight`, with `class_weight=None` to prevent double weighting, and uses the multiclass objective with original quality labels 3–8. Probability columns align explicitly to those labels. All validation metrics are unweighted. No global weights, binary `scale_pos_weight`, calibration or threshold tuning are used.

Trees have depth 2–4 and at most 15 leaves, with `num_leaves <= 2**max_depth`. Valid leaves/depth pairs are (3,2), (3,3), (3,4), (7,3), (7,4), (12,4), (15,4). `min_child_samples` is 20–60; its Hessian-based approximation is not an exact lower bound on every realized leaf count. Numeric schema validation precedes a new LightGBM Dataset for every fit. Feature binning and trees use only training rows. `feature_pre_filter=False` and `subsample_freq=1` ensure the minimum-child and row-subsampling searches are effective. Early stopping is disabled: inner CV selects the requested rounds, and no validation set enters fitting. Native growth may finish earlier if no valid split remains; actual rounds are audited. Fixed CPU execution uses one thread, deterministic column-wise histograms, 63 bins, seed 42 and silent training.

See the official [LightGBM parameters](https://lightgbm.readthedocs.io/en/stable/Parameters.html) and [Python fit API](https://lightgbm.readthedocs.io/en/stable/pythonapi/lightgbm.LGBMClassifier.html).

| Quality | Unweighted outer-refit weight | Balanced weight mean (min–max) | Moderated weight mean (min–max) |
|---|---:|---:|---:|
| 3 | 1.000 | 22.646 (22.639–22.667) | 6.406 (4.106–7.805) |
| 4 | 1.000 | 4.315 (4.245–4.387) | 2.614 (1.809–3.312) |
| 5 | 1.000 | 0.393 (0.393–0.394) | 0.727 (0.670–0.837) |
| 6 | 1.000 | 0.423 (0.423–0.424) | 0.772 (0.707–0.906) |
| 7 | 1.000 | 1.352 (1.345–1.358) | 1.394 (1.054–1.790) |
| 8 | 1.000 | 12.970 (12.348–13.583) | 5.245 (3.235–6.715) |

Outer-refit weights are descriptive summaries of separately selected recipes and fold counts, not a new class-weight recipe. Inner-fit weights differ and are retained in the audit table.

## Interpretation and limitations

The observed Macro F1 means were **0.2827** for unweighted LightGBM, **0.3067** for frequency weighting, and **0.3120** for moderated custom weighting. **Moderated custom** had the highest mean among these three registered procedures.

Moderated custom weighting exceeded balanced weighting by **0.0053 Macro F1** on average, with paired-fold SD **0.0356** and positive differences in 24 of 40 folds. This does not establish a definitive winner. Balanced weighting had higher Balanced Accuracy (**0.3477 versus 0.3266**) and quality-8 F1 (**0.0960 versus 0.0840**); moderated weighting had higher QWK (**0.5334 versus 0.5192**) and Macro PR-AUC (**0.3620 versus 0.3463**). These are tradeoffs between the registered tuning procedures, not isolated effects of class weighting.

Rare-class performance remains weak: quality-3 F1 averaged **0.0000 / 0.0720 / 0.0751**, and quality-8 F1 **0.0200 / 0.0960 / 0.0840**, for unweighted / balanced / moderated procedures. The small validation support and large per-class variation limit the conclusions. All 8,760 native fits reached their requested boosting-round limit; no validation-based stopping occurred.

This comparison re-evaluates LightGBM with multiclass weighting and a controlled conservative search. It neither treats the earlier baseline as a verdict on the family nor establishes that every possible LightGBM configuration has been assessed. The finite 24-candidate budget per arm leaves substantial unexplored parameter space.

The per-arm nested estimates cover their registered inner selection processes. Choosing an arm retrospectively using its outer mean would introduce an additional selection step not evaluated by those per-arm estimates. No arm is automatically promoted, no all-development final model is fitted, and no new independent test claim is made. Previous development exploration remains part of the context.

All new experimentation used the locked development membership. The original final holdout was not accessed or evaluated by the experiment, and all Version 1 results remain preserved. Clean-kernel guards check raw training/validation calls, native sample weights and the absence of early stopping. Saved evidence supports reconstruction of every outer metric, candidate selection and training-weight calculation.

Evidence: [registered plan and candidates](lightgbm_20261013/plan.json), [metric comparison](lightgbm_20261013/metric_comparison.csv), [per-class table](lightgbm_20261013/per_class_comparison.csv), [runtime table](lightgbm_20261013/runtime_comparison.csv), [outer selected recipes](lightgbm_20261013/outer_fold_metrics.csv), [inner scores](lightgbm_20261013/inner_fold_scores.csv), [per-fit weights and training audits](lightgbm_20261013/training_audits.csv), and [paired fold differences](lightgbm_20261013/paired_fold_differences.csv).
