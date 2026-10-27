# Experiment Version 2 — Development CV Estimate

Focused Random Forest and Extra Trees imbalance study, with feature-importance stability diagnostics.

**1,087 existing development observations; outer stratified 4-fold × 10 repeats, inner stratified 3-fold CV.** Each of eight procedures selects from 12 registered joint configurations by Macro F1.

| Procedure | Macro F1 mean ± SD | Balanced Accuracy | QWK | Macro PR-AUC |
|---|---:|---:|---:|---:|
| Random Forest — None | 0.2672 ± 0.0198 | 0.2697 | 0.4905 | 0.3854 |
| Random Forest — Balanced | 0.3287 ± 0.0435 | 0.3736 | 0.5343 | 0.3586 |
| Random Forest — Balanced subsample | 0.3350 ± 0.0451 | 0.3767 | 0.5506 | 0.3771 |
| Random Forest — Moderated custom | 0.2967 ± 0.0336 | 0.3056 | 0.5269 | 0.3838 |
| Extra Trees — None | 0.2506 ± 0.0147 | 0.2565 | 0.4590 | 0.4083 |
| Extra Trees — Balanced | 0.3154 ± 0.0273 | 0.4117 | 0.4973 | 0.3758 |
| Extra Trees — Balanced subsample | 0.3183 ± 0.0379 | 0.3867 | 0.5236 | 0.3787 |
| Extra Trees — Moderated custom | 0.2800 ± 0.0241 | 0.2897 | 0.5382 | 0.4033 |

All results are development CV estimates. SD is population SD across overlapping folds, not an independent-sample confidence interval. Full CSVs retain mean, SD, minimum and maximum for all seven metrics, including ROC-AUC, MAE and ±1 accuracy. PR-AUC means macro OvR average precision from native probabilities; probabilities are not claimed to be calibrated.

## Per-class results

| Procedure | F1: 3 | F1: 4 | F1: 5 | F1: 6 | F1: 7 | F1: 8 |
|---|---:|---:|---:|---:|---:|---:|
| Random Forest — None | 0.0000 ± 0.0000 | 0.0000 ± 0.0000 | 0.6865 ± 0.0254 | 0.5674 ± 0.0362 | 0.3494 ± 0.0882 | 0.0000 ± 0.0000 |
| Random Forest — Balanced | 0.1214 ± 0.1659 | 0.1377 ± 0.0748 | 0.6634 ± 0.0324 | 0.4690 ± 0.0450 | 0.4593 ± 0.0499 | 0.1217 ± 0.1581 |
| Random Forest — Balanced subsample | 0.1589 ± 0.1860 | 0.1195 ± 0.0819 | 0.6731 ± 0.0300 | 0.4733 ± 0.0546 | 0.4711 ± 0.0542 | 0.1139 ± 0.1285 |
| Random Forest — Moderated custom | 0.0675 ± 0.1484 | 0.0000 ± 0.0000 | 0.6932 ± 0.0233 | 0.5488 ± 0.0372 | 0.4210 ± 0.0610 | 0.0496 ± 0.1130 |
| Extra Trees — None | 0.0000 ± 0.0000 | 0.0000 ± 0.0000 | 0.7039 ± 0.0218 | 0.5764 ± 0.0329 | 0.2235 ± 0.0676 | 0.0000 ± 0.0000 |
| Extra Trees — Balanced | 0.1542 ± 0.1136 | 0.1484 ± 0.0547 | 0.6591 ± 0.0333 | 0.3481 ± 0.0483 | 0.4501 ± 0.0345 | 0.1322 ± 0.1006 |
| Extra Trees — Balanced subsample | 0.1807 ± 0.1797 | 0.1551 ± 0.0741 | 0.6742 ± 0.0297 | 0.3580 ± 0.0566 | 0.4565 ± 0.0438 | 0.0856 ± 0.1190 |
| Extra Trees — Moderated custom | 0.0000 ± 0.0000 | 0.0000 ± 0.0000 | 0.7069 ± 0.0215 | 0.5173 ± 0.0353 | 0.4432 ± 0.0769 | 0.0125 ± 0.0781 |

| Procedure | Recall: 3 | Recall: 4 | Recall: 5 | Recall: 6 | Recall: 7 | Recall: 8 |
|---|---:|---:|---:|---:|---:|---:|
| Random Forest — None | 0.0000 ± 0.0000 | 0.0000 ± 0.0000 | 0.7199 ± 0.0470 | 0.6201 ± 0.0614 | 0.2780 ± 0.0922 | 0.0000 ± 0.0000 |
| Random Forest — Balanced | 0.2250 ± 0.2487 | 0.1923 ± 0.1018 | 0.6505 ± 0.0515 | 0.4082 ± 0.0564 | 0.5742 ± 0.0675 | 0.1917 ± 0.2358 |
| Random Forest — Balanced subsample | 0.2625 ± 0.2736 | 0.1455 ± 0.1176 | 0.6787 ± 0.0527 | 0.4229 ± 0.0719 | 0.5796 ± 0.0818 | 0.1708 ± 0.1945 |
| Random Forest — Moderated custom | 0.0875 ± 0.1900 | 0.0000 ± 0.0000 | 0.7290 ± 0.0447 | 0.5612 ± 0.0609 | 0.3997 ± 0.0918 | 0.0563 ± 0.1269 |
| Extra Trees — None | 0.0000 ± 0.0000 | 0.0000 ± 0.0000 | 0.7633 ± 0.0364 | 0.6409 ± 0.0552 | 0.1349 ± 0.0468 | 0.0000 ± 0.0000 |
| Extra Trees — Balanced | 0.4000 ± 0.2784 | 0.2525 ± 0.0885 | 0.6611 ± 0.0526 | 0.2540 ± 0.0459 | 0.6526 ± 0.0664 | 0.2500 ± 0.1990 |
| Extra Trees — Balanced subsample | 0.3125 ± 0.2666 | 0.2357 ± 0.1169 | 0.6972 ± 0.0456 | 0.2682 ± 0.0584 | 0.6608 ± 0.0696 | 0.1458 ± 0.1814 |
| Extra Trees — Moderated custom | 0.0000 ± 0.0000 | 0.0000 ± 0.0000 | 0.7776 ± 0.0352 | 0.4953 ± 0.0536 | 0.4567 ± 0.1201 | 0.0083 ± 0.0520 |

Each outer validation fold contains only two quality-3 observations and three or four quality-8 observations; per-class estimates remain sensitive to individual wines.

## Feature-importance stability

Native impurity importance (MDI) and outer-validation permutation importance were collected after each outer refit. Permutation importance is the signed Macro F1 decrease after one feature is shuffled, with five deterministic shuffles per feature. Identical shuffles are shared across procedures on each outer fold. These diagnostics never influence selection, tuning or the feature set.

| Procedure | Importance method | Mean pairwise rank Spearman | Mean top-three Jaccard | Valid rank pairs |
|---|---|---:|---:|---:|
| Extra Trees — Balanced | impurity | 0.9336 | 0.7455 | 780/780 |
| Extra Trees — Balanced | permutation_macro_f1 | 0.3312 | 0.3868 | 780/780 |
| Extra Trees — Balanced subsample | impurity | 0.9250 | 0.7288 | 780/780 |
| Extra Trees — Balanced subsample | permutation_macro_f1 | 0.3117 | 0.3795 | 780/780 |
| Extra Trees — Moderated custom | impurity | 0.9623 | 0.7006 | 780/780 |
| Extra Trees — Moderated custom | permutation_macro_f1 | 0.4744 | 0.5101 | 780/780 |
| Extra Trees — None | impurity | 0.9436 | 0.7045 | 780/780 |
| Extra Trees — None | permutation_macro_f1 | 0.7093 | 0.6341 | 780/780 |
| Random Forest — Balanced | impurity | 0.8209 | 0.9506 | 780/780 |
| Random Forest — Balanced | permutation_macro_f1 | 0.4935 | 0.5968 | 780/780 |
| Random Forest — Balanced subsample | impurity | 0.8866 | 0.9276 | 780/780 |
| Random Forest — Balanced subsample | permutation_macro_f1 | 0.4342 | 0.5076 | 780/780 |
| Random Forest — Moderated custom | impurity | 0.7894 | 0.8878 | 780/780 |
| Random Forest — Moderated custom | permutation_macro_f1 | 0.5828 | 0.7238 | 780/780 |
| Random Forest — None | impurity | 0.8103 | 0.7462 | 780/780 |
| Random Forest — None | permutation_macro_f1 | 0.6725 | 0.8209 | 780/780 |

Each method compares 40 fold vectors (780 overlapping fold pairs). Rank Spearman uses average ranks for ties; top-three ties use configured feature order. Constant rank vectors have undefined correlations and are counted separately. Top-three membership is relative, not proof of predictive signal. These describe the complete tuned procedure across splits, including changes in selected configurations—not isolated estimator-seed variation.

| Procedure | Feature | Permutation Macro F1 drop mean ± SD | Mean rank | Top-three frequency | Positive-fold fraction |
|---|---|---:|---:|---:|---:|
| Random Forest — None | alcohol | 0.0579 ± 0.0130 | 1.10 | 100.0% | 100.0% |
| Random Forest — None | sulphates | 0.0291 ± 0.0124 | 2.42 | 95.0% | 100.0% |
| Random Forest — None | volatile acidity | 0.0271 ± 0.0144 | 2.88 | 85.0% | 97.5% |
| Random Forest — Balanced | alcohol | 0.0628 ± 0.0307 | 1.45 | 97.5% | 100.0% |
| Random Forest — Balanced | sulphates | 0.0443 ± 0.0288 | 2.40 | 85.0% | 100.0% |
| Random Forest — Balanced | volatile acidity | 0.0324 ± 0.0359 | 3.73 | 67.5% | 85.0% |
| Random Forest — Balanced subsample | alcohol | 0.0620 ± 0.0311 | 1.45 | 97.5% | 97.5% |
| Random Forest — Balanced subsample | sulphates | 0.0328 ± 0.0202 | 3.20 | 70.0% | 95.0% |
| Random Forest — Balanced subsample | volatile acidity | 0.0346 ± 0.0362 | 3.70 | 65.0% | 85.0% |
| Random Forest — Moderated custom | alcohol | 0.0764 ± 0.0264 | 1.07 | 100.0% | 100.0% |
| Random Forest — Moderated custom | sulphates | 0.0381 ± 0.0253 | 2.73 | 90.0% | 97.5% |
| Random Forest — Moderated custom | volatile acidity | 0.0353 ± 0.0259 | 2.95 | 77.5% | 97.5% |
| Extra Trees — None | alcohol | 0.0640 ± 0.0147 | 1.00 | 100.0% | 100.0% |
| Extra Trees — None | volatile acidity | 0.0282 ± 0.0110 | 2.75 | 87.5% | 97.5% |
| Extra Trees — None | sulphates | 0.0231 ± 0.0101 | 3.58 | 65.0% | 97.5% |
| Extra Trees — Balanced | alcohol | 0.0528 ± 0.0251 | 1.45 | 92.5% | 100.0% |
| Extra Trees — Balanced | volatile acidity | 0.0245 ± 0.0277 | 3.65 | 65.0% | 72.5% |
| Extra Trees — Balanced | sulphates | 0.0098 ± 0.0203 | 5.47 | 37.5% | 72.5% |
| Extra Trees — Balanced subsample | alcohol | 0.0574 ± 0.0348 | 1.52 | 95.0% | 95.0% |
| Extra Trees — Balanced subsample | volatile acidity | 0.0259 ± 0.0333 | 4.03 | 62.5% | 77.5% |
| Extra Trees — Balanced subsample | sulphates | 0.0161 ± 0.0335 | 5.35 | 37.5% | 65.0% |
| Extra Trees — Moderated custom | alcohol | 0.0675 ± 0.0180 | 1.00 | 100.0% | 100.0% |
| Extra Trees — Moderated custom | sulphates | 0.0144 ± 0.0146 | 3.23 | 70.0% | 90.0% |
| Extra Trees — Moderated custom | volatile acidity | 0.0078 ± 0.0141 | 4.45 | 57.5% | 80.0% |

The full importance table covers all eleven features, both methods, across-fold dispersion, rank dispersion, top-three frequency and within-fold permutation variation. Negative drops are retained. Correlated measurements can share or dilute permutation importance; MDI can favor high-cardinality predictors. Neither method measures causal effects. Outer-validation importance must not be reused to select features while claiming the same outer scores as an unbiased estimate. See [sklearn permutation importance](https://scikit-learn.org/stable/modules/permutation_importance.html).

## Runtime

| Procedure | Inner search (s) | Outer refits (s) | Outer scoring (s) | Importance diagnostics (s) | Total measured (s) |
|---|---:|---:|---:|---:|---:|
| Random Forest — None | 298.37 | 10.99 | 1.36 | 22.59 | 333.31 |
| Random Forest — Balanced | 299.97 | 10.73 | 1.38 | 23.32 | 335.40 |
| Random Forest — Balanced subsample | 370.39 | 11.01 | 1.31 | 21.03 | 403.73 |
| Random Forest — Moderated custom | 315.75 | 11.33 | 1.30 | 20.84 | 349.23 |
| Extra Trees — None | 204.65 | 5.55 | 1.25 | 19.59 | 231.05 |
| Extra Trees — Balanced | 220.98 | 6.85 | 1.45 | 25.06 | 254.34 |
| Extra Trees — Balanced subsample | 295.99 | 9.67 | 1.39 | 23.29 | 330.35 |
| Extra Trees — Moderated custom | 222.63 | 7.33 | 1.41 | 23.66 | 255.02 |

Completed **11,520 inner fits + 320 outer refits = 11,840 fits**, plus **17,600 post-selection permutation predictions**. Total experiment wall time: **2501.89 seconds**. One native CPU thread; timings include wrapper, tree-audit and execution-guard overhead and are not hardware-independent speed claims.

## Registered search and weighting

| Parameter | Choices |
|---|---|
| n_estimators | 80, 150, 250 |
| max_depth | 3, 5, 8 |
| min_samples_split | 8, 16, 24 |
| min_samples_leaf | 4, 8, 12 |
| max_features | sqrt, 0.5, 1.0 |
| bootstrap | False, True |

Seed 8242 generates 12 joint configurations per procedure. Five non-bootstrap settings match across all eight procedures. Balanced coverage is enforced for the valid leaf/split pairs (4,8), (4,16), (4,24), (8,16), (8,24), (12,24) and other marginals. Bootstrap is tuned for unweighted, balanced and custom procedures; balanced_subsample is restricted to True. Thus comparisons include native bootstrap choices and are not isolated causal class-weight ablations.

| Custom dictionary | Quality 3 | Quality 4 | Quality 5 | Quality 6 | Quality 7 | Quality 8 |
|---|---:|---:|---:|---:|---:|---:|
| 0 | 2.0 | 1.25 | 1.0 | 1.0 | 1.25 | 2.0 |
| 1 | 4.0 | 1.5 | 1.0 | 1.0 | 1.5 | 4.0 |
| 2 | 6.0 | 2.0 | 1.0 | 1.0 | 1.5 | 3.0 |
| 3 | 3.0 | 1.5 | 1.0 | 1.0 | 2.0 | 6.0 |

Each explicit dictionary appears in three custom recipes. Tree parameters and weight dictionaries are selected jointly; no enormous Cartesian grid or post-result expansion is used. Native class_weight receives None, balanced, balanced_subsample or the explicit dictionary. There is no additional sample_weight. With sklearn 1.9.1, balanced/custom weights affect bootstrap sampling probabilities when bootstrap=True; otherwise they weight impurity. Balanced_subsample uses uniform bootstrap sampling and per-draw inverse-frequency impurity weighting. All counts and draws are confined to the current training fold. Absent classes in a draw receive zero weight. Both estimator APIs support this policy: [Random Forest](https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.RandomForestClassifier.html), [Extra Trees](https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.ExtraTreesClassifier.html).

Every tree is checked for its actual bootstrap indices, root class mass, depth and minimum unique-row leaf size. The numeric schema and forest are newly fitted inside each training fold. No scaling, external resampling, feature engineering, OOB selection, warm start, calibration or threshold optimization is added. Fixed Gini criterion, seed 42, one CPU thread and silent output. Future sklearn versions require re-auditing native weighting semantics.

| Procedure | Outer trees | Max observed depth | Min observed leaf rows | Trees missing quality 3 | Trees missing quality 8 |
|---|---:|---:|---:|---:|---:|
| Random Forest — None | 6840 | 8 | 4 | 4 | 0 |
| Random Forest — Balanced | 6970 | 8 | 4 | 0 | 0 |
| Random Forest — Balanced subsample | 6320 | 8 | 4 | 18 | 0 |
| Random Forest — Moderated custom | 6470 | 8 | 4 | 0 | 0 |
| Extra Trees — None | 5970 | 8 | 4 | 5 | 0 |
| Extra Trees — Balanced | 8050 | 8 | 4 | 0 | 0 |
| Extra Trees — Balanced subsample | 7500 | 8 | 4 | 21 | 0 |
| Extra Trees — Moderated custom | 7600 | 8 | 4 | 0 | 0 |

Bootstrap absence is a property of the training draws, not a new validation subset. Balanced_subsample cannot create missing rare examples.

## Paired Macro F1 differences

| Comparison | Mean | SD | Positive / negative / tied folds |
|---|---:|---:|---:|
| Random Forest — Balanced minus Random Forest — None | +0.0615 | 0.0491 | 36 / 4 / 0 |
| Random Forest — Balanced subsample minus Random Forest — None | +0.0677 | 0.0483 | 38 / 2 / 0 |
| Random Forest — Moderated custom minus Random Forest — None | +0.0295 | 0.0317 | 35 / 5 / 0 |
| Extra Trees — Balanced minus Extra Trees — None | +0.0647 | 0.0296 | 39 / 1 / 0 |
| Extra Trees — Balanced subsample minus Extra Trees — None | +0.0677 | 0.0430 | 39 / 1 / 0 |
| Extra Trees — Moderated custom minus Extra Trees — None | +0.0293 | 0.0207 | 39 / 1 / 0 |
| Random Forest — Balanced subsample minus Random Forest — Balanced | +0.0062 | 0.0540 | 25 / 15 / 0 |
| Extra Trees — Balanced subsample minus Extra Trees — Balanced | +0.0030 | 0.0363 | 22 / 18 / 0 |
| Extra Trees — None minus Random Forest — None | -0.0166 | 0.0157 | 6 / 34 / 0 |
| Extra Trees — Balanced minus Random Forest — Balanced | -0.0134 | 0.0415 | 14 / 26 / 0 |
| Extra Trees — Balanced subsample minus Random Forest — Balanced subsample | -0.0166 | 0.0468 | 16 / 24 / 0 |
| Extra Trees — Moderated custom minus Random Forest — Moderated custom | -0.0167 | 0.0310 | 13 / 27 / 0 |

## Interpretation

Random Forest Macro F1 means were **0.2672** (None), **0.3287** (Balanced), **0.3350** (Balanced subsample), **0.2967** (Moderated custom). **Balanced subsample** had the highest observed mean within this family.

Extra Trees Macro F1 means were **0.2506** (None), **0.3154** (Balanced), **0.3183** (Balanced subsample), **0.2800** (Moderated custom). **Balanced subsample** had the highest observed mean within this family.

The `balanced_subsample` advantage over `balanced` was **0.0062 Macro F1** for Random Forest (paired-fold SD **0.0540**, 25/40 positive differences) and **0.0030** for Extra Trees (SD **0.0363**, 22/40 positive). These small differences do not establish a definitive weighting winner. Extra Trees with balanced weighting had the highest Balanced Accuracy among the eight procedures (**0.4117**), while Random Forest with balanced_subsample had the highest Macro F1 (**0.3350**). Weighting choices therefore involve precision/recall tradeoffs. Both unweighted procedures had zero F1 for qualities 3, 4 and 8; rare-class performance remained weak and variable even after weighting.

Alcohol was the most consistently high-ranked feature by outer-validation permutation importance, appearing in the top three in **92.5–100%** of folds across the eight procedures. However, impurity rankings were more stable than permutation rankings. For the two balanced_subsample procedures, mean pairwise rank Spearman was **0.8866 MDI versus 0.4342 permutation** for Random Forest and **0.9250 versus 0.3117** for Extra Trees. Their permutation top-three Jaccard overlaps were **0.5076** and **0.3795**. Stable training-based importance is therefore insufficient evidence of stable validation importance; these diagnostics do not justify pruning correlated features or changing the registered models.

These results evaluate the finite registered procedures on previously explored development data. They do not establish statistical superiority using overlapping folds, a causal class-weight benefit, or that all possible configurations of either family have been assessed. Comparing the means is descriptive; choosing the family or weighting arm retrospectively would add a selection step not covered by these per-arm nested estimates.

Feature importance is diagnostic only. No feature set, candidate pool, weighting rule or final model was changed after viewing outer scores or importance values. No all-development model was promoted or fitted. The original holdout was not used, and every prior result remains preserved.

Evidence: [plan](forests_20261013/plan.json), [metrics](forests_20261013/metric_comparison.csv), [per-class results](forests_20261013/per_class_comparison.csv), [runtime](forests_20261013/runtime_comparison.csv), [importance summary](forests_20261013/feature_importance_summary.csv), [importance stability](forests_20261013/feature_importance_stability.csv), [all permutation drops](forests_20261013/feature_importance_raw.csv), [native outer-tree audits](forests_20261013/outer_tree_audits.csv), [selected recipes](forests_20261013/outer_fold_metrics.csv), and [inner candidate scores](forests_20261013/inner_candidate_scores.csv).
