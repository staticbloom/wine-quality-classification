# Version 2 — Regression with Learned Ordinal Thresholds

**Development CV estimates only.** The study uses the existing 1,087 development wines and preserves the locked Version 1 holdout and all earlier results. No holdout evaluation, recreated test set, or final all-development model fit is performed.

## Method and registered scope

Six regressors predict continuous quality. This uses order **and an equal-distance numerical assumption**, unlike the preceding cumulative-link and ordered-binary classifiers. Squared-error/RMSE training is followed by a separate six-class decoder; improving QWK does not establish six-class performance.

Outer validation uses the established **stratified 4-fold × 10 repeats**, seed 42; inner validation uses **stratified 3-fold**, seed 1042 + outer-split index. Exact memberships and class supports are retained. Each family has **four predeclared recipes**; the full registry is in notebook Configuration and `plan.json`:

- Ridge: alpha 0.1, 1, 10, 100; training-only StandardScaler; SVD solver.
- Random Forest and Extra Trees: 150–250 trees, depth 4–8, minimum leaf size 3–8, constrained split sizes and feature fractions. RF bootstraps; Extra Trees does not.
- Histogram Gradient Boosting: 150–250 iterations, depth 2–4, 4–15 leaves, minimum leaf size 25–35 and L2 regularization.
- XGBoost: 150–250 shallow trees, depth 2–4, conservative child weight, shrinkage, subsampling and L1/L2 regularization.
- CatBoost: 150–250 iterations, depth 3–5, shrinkage, L2 regularization and Bayesian bagging. Quiet CPU execution.

No weighting, resampling, feature engineering, early stopping or validation set is used. Trees use raw numeric features. Every scaler/native fit is confined to the current training fold. Candidate budgets were fixed before the wine fits and were not expanded after viewing outer results.

## Learning five ordered cutpoints

For each candidate, generate exactly one **inner out-of-fold continuous prediction** per outer-training row. Fit five cutpoints on those scores and their corresponding training labels, maximizing six-class Macro F1. The optimized inner score is a **fitted threshold-training objective**, not an unbiased CV performance estimate.

Macro F1 is the sum of six interval contributions `2 TP / (true class count + predicted interval count)`, divided by six. An exact dynamic program searches every ordered contiguous partition of distinct scores. Ties stay together, empty predicted classes are allowed, and fixed predecessor order resolves equal objectives. The five cutpoints are strictly increasing exact rational numbers placed in score gaps; float summaries are for display only. Equality enters the upper class. Extreme scores map to quality 3/8.

After inner selection, refit each distinct winning configuration on the entire outer-training split. Freeze its cutpoints **before** outer prediction. Learning cutpoints from inner fits and applying them to a larger outer-training refit can shift the score distribution; outer validation captures that practical effect.

| Procedure | Inner selection | Outer decoder |
|---|---|---|
| Learned cuts | Highest fitted threshold-training Macro F1 | Five learned cutpoints. |
| Matched rounding | Same winning regressor and identical continuous predictions as learned cuts | Fixed 3.5, 4.5, 5.5, 6.5, 7.5 cuts. |
| Selected rounding | Independently highest naive-rounding OOF Macro F1 | The same fixed half-integer cuts. |

Fixed cuts implement clipped half-up rounding, not Python's ties-to-even rounding. All classification metrics use the identical decoded labels. Continuous MAE is separately saved. Scalar regression scores do not provide class probabilities; PR-AUC and ROC-AUC are not fabricated.

A derived **joint inner-selected** procedure chooses across all 24 candidates using the respective inner objectives and reuses its chosen family's outer predictions. It adds no model fits. Family tables are descriptive; selecting the largest outer mean after inspection would not yield an unbiased model-selection estimate. [Nested-CV rationale](https://scikit-learn.org/stable/auto_examples/model_selection/plot_nested_cross_validation_iris.html).

## Development CV estimates

| Procedure | Macro F1 mean ± SD | Balanced Accuracy mean ± SD | QWK mean ± SD | decoded MAE mean ± SD | ±1 accuracy mean ± SD |
| --- | --- | --- | --- | --- | --- |
| Ridge — learned cuts | 0.2968 ± 0.0304 | 0.3329 ± 0.0591 | 0.5308 ± 0.0295 | 0.5573 ± 0.0349 | 0.9324 ± 0.0191 |
| Ridge — matched rounding | 0.2440 ± 0.0183 | 0.2499 ± 0.0145 | 0.4627 ± 0.0381 | 0.4666 ± 0.0248 | 0.9616 ± 0.0075 |
| Ridge — selected rounding | 0.2498 ± 0.0200 | 0.2542 ± 0.0161 | 0.4735 ± 0.0424 | 0.4643 ± 0.0272 | 0.9621 ± 0.0081 |
| Random Forest — learned cuts | 0.3352 ± 0.0449 | 0.3682 ± 0.0566 | 0.5692 ± 0.0361 | 0.5103 ± 0.0348 | 0.9474 ± 0.0103 |
| Random Forest — matched rounding | 0.2720 ± 0.0178 | 0.2739 ± 0.0164 | 0.5223 ± 0.0420 | 0.4408 ± 0.0276 | 0.9659 ± 0.0092 |
| Random Forest — selected rounding | 0.2733 ± 0.0174 | 0.2754 ± 0.0159 | 0.5284 ± 0.0387 | 0.4382 ± 0.0248 | 0.9671 ± 0.0090 |
| Extra Trees — learned cuts | 0.3397 ± 0.0527 | 0.3701 ± 0.0731 | 0.5800 ± 0.0425 | 0.4987 ± 0.0418 | 0.9514 ± 0.0153 |
| Extra Trees — matched rounding | 0.2666 ± 0.0207 | 0.2691 ± 0.0167 | 0.5050 ± 0.0444 | 0.4283 ± 0.0285 | 0.9658 ± 0.0075 |
| Extra Trees — selected rounding | 0.2687 ± 0.0184 | 0.2705 ± 0.0155 | 0.5104 ± 0.0415 | 0.4266 ± 0.0281 | 0.9661 ± 0.0080 |
| HistGradientBoosting — learned cuts | 0.3246 ± 0.0437 | 0.3588 ± 0.0623 | 0.5613 ± 0.0345 | 0.5282 ± 0.0442 | 0.9427 ± 0.0186 |
| HistGradientBoosting — matched rounding | 0.2732 ± 0.0168 | 0.2751 ± 0.0159 | 0.5338 ± 0.0351 | 0.4447 ± 0.0283 | 0.9688 ± 0.0076 |
| HistGradientBoosting — selected rounding | 0.2739 ± 0.0154 | 0.2762 ± 0.0143 | 0.5381 ± 0.0363 | 0.4423 ± 0.0271 | 0.9696 ± 0.0084 |
| XGBoost — learned cuts | 0.3252 ± 0.0467 | 0.3596 ± 0.0622 | 0.5661 ± 0.0321 | 0.5191 ± 0.0416 | 0.9473 ± 0.0145 |
| XGBoost — matched rounding | 0.2766 ± 0.0170 | 0.2784 ± 0.0157 | 0.5395 ± 0.0369 | 0.4374 ± 0.0281 | 0.9687 ± 0.0077 |
| XGBoost — selected rounding | 0.2752 ± 0.0158 | 0.2772 ± 0.0145 | 0.5389 ± 0.0354 | 0.4395 ± 0.0266 | 0.9692 ± 0.0074 |
| CatBoost — learned cuts | 0.3151 ± 0.0431 | 0.3514 ± 0.0605 | 0.5695 ± 0.0393 | 0.5225 ± 0.0463 | 0.9440 ± 0.0181 |
| CatBoost — matched rounding | 0.2729 ± 0.0160 | 0.2740 ± 0.0137 | 0.5240 ± 0.0396 | 0.4347 ± 0.0257 | 0.9673 ± 0.0093 |
| CatBoost — selected rounding | 0.2723 ± 0.0160 | 0.2735 ± 0.0138 | 0.5229 ± 0.0362 | 0.4362 ± 0.0245 | 0.9672 ± 0.0090 |
| Joint inner-selected — learned cuts | 0.3308 ± 0.0531 | 0.3562 ± 0.0645 | 0.5683 ± 0.0421 | 0.5118 ± 0.0441 | 0.9504 ± 0.0135 |
| Joint inner-selected — matched rounding | 0.2701 ± 0.0207 | 0.2723 ± 0.0183 | 0.5199 ± 0.0482 | 0.4379 ± 0.0290 | 0.9674 ± 0.0080 |
| Joint inner-selected — selected rounding | 0.2731 ± 0.0160 | 0.2753 ± 0.0146 | 0.5324 ± 0.0414 | 0.4396 ± 0.0262 | 0.9686 ± 0.0083 |

All means and population SDs above summarize 40 **dependent** outer folds. SD is descriptive, not a standard error or confidence interval. Min/max are saved in `metric_comparison.csv`.

| Family | Rounding control | Mean Δ Macro F1 | SD of paired differences | Min Δ | Max Δ |
| --- | --- | --- | --- | --- | --- |
| Ridge | matched rounding | +0.0528 | 0.0373 | -0.0043 | +0.1462 |
| Ridge | selected rounding | +0.0470 | 0.0370 | -0.0092 | +0.1288 |
| Random Forest | matched rounding | +0.0633 | 0.0475 | -0.0254 | +0.1703 |
| Random Forest | selected rounding | +0.0620 | 0.0473 | -0.0209 | +0.1753 |
| Extra Trees | matched rounding | +0.0731 | 0.0544 | -0.0056 | +0.2498 |
| Extra Trees | selected rounding | +0.0710 | 0.0557 | -0.0056 | +0.2498 |
| HistGradientBoosting | matched rounding | +0.0515 | 0.0463 | -0.0283 | +0.1446 |
| HistGradientBoosting | selected rounding | +0.0507 | 0.0469 | -0.0215 | +0.1446 |
| XGBoost | matched rounding | +0.0486 | 0.0505 | -0.0371 | +0.2052 |
| XGBoost | selected rounding | +0.0500 | 0.0496 | -0.0343 | +0.2052 |
| CatBoost | matched rounding | +0.0422 | 0.0464 | -0.0329 | +0.1441 |
| CatBoost | selected rounding | +0.0428 | 0.0456 | -0.0329 | +0.1390 |
| Joint inner-selected | matched rounding | +0.0606 | 0.0574 | -0.0371 | +0.2052 |
| Joint inner-selected | selected rounding | +0.0577 | 0.0567 | -0.0338 | +0.1997 |

## Per-class performance

| Procedure | Quality 3 F1 | Quality 4 F1 | Quality 5 F1 | Quality 6 F1 | Quality 7 F1 | Quality 8 F1 |
| --- | --- | --- | --- | --- | --- | --- |
| Ridge — learned cuts | 0.0608 | 0.0452 | 0.6104 | 0.5252 | 0.4271 | 0.1121 |
| Ridge — matched rounding | 0.0000 | 0.0000 | 0.6779 | 0.5705 | 0.2158 | 0.0000 |
| Ridge — selected rounding | 0.0000 | 0.0000 | 0.6795 | 0.5703 | 0.2492 | 0.0000 |
| Random Forest — learned cuts | 0.2638 | 0.0784 | 0.6561 | 0.5327 | 0.4009 | 0.0796 |
| Random Forest — matched rounding | 0.0000 | 0.0000 | 0.7014 | 0.5695 | 0.3608 | 0.0000 |
| Random Forest — selected rounding | 0.0000 | 0.0000 | 0.7020 | 0.5713 | 0.3664 | 0.0000 |
| Extra Trees — learned cuts | 0.2673 | 0.0715 | 0.6682 | 0.5377 | 0.4053 | 0.0884 |
| Extra Trees — matched rounding | 0.0000 | 0.0000 | 0.7034 | 0.6010 | 0.2953 | 0.0000 |
| Extra Trees — selected rounding | 0.0000 | 0.0000 | 0.7058 | 0.6012 | 0.3051 | 0.0000 |
| HistGradientBoosting — learned cuts | 0.2029 | 0.0776 | 0.6402 | 0.5237 | 0.3943 | 0.1090 |
| HistGradientBoosting — matched rounding | 0.0000 | 0.0000 | 0.6903 | 0.5653 | 0.3833 | 0.0000 |
| HistGradientBoosting — selected rounding | 0.0000 | 0.0000 | 0.6923 | 0.5653 | 0.3859 | 0.0000 |
| XGBoost — learned cuts | 0.2460 | 0.0429 | 0.6508 | 0.5212 | 0.3980 | 0.0923 |
| XGBoost — matched rounding | 0.0000 | 0.0000 | 0.6966 | 0.5740 | 0.3894 | 0.0000 |
| XGBoost — selected rounding | 0.0000 | 0.0000 | 0.6936 | 0.5719 | 0.3858 | 0.0000 |
| CatBoost — learned cuts | 0.1965 | 0.0508 | 0.6508 | 0.5325 | 0.3880 | 0.0720 |
| CatBoost — matched rounding | 0.0000 | 0.0000 | 0.7002 | 0.5809 | 0.3561 | 0.0000 |
| CatBoost — selected rounding | 0.0000 | 0.0000 | 0.6983 | 0.5796 | 0.3560 | 0.0000 |
| Joint inner-selected — learned cuts | 0.2502 | 0.0667 | 0.6517 | 0.5296 | 0.3961 | 0.0904 |
| Joint inner-selected — matched rounding | 0.0000 | 0.0000 | 0.6968 | 0.5791 | 0.3449 | 0.0000 |
| Joint inner-selected — selected rounding | 0.0000 | 0.0000 | 0.6953 | 0.5721 | 0.3713 | 0.0000 |

Learned thresholds can trade false negatives for false positives, so tail-class recall must be read alongside precision:

| Learned-cut procedure | Quality | Precision | Recall | F1 | Zero-prediction folds |
| --- | --- | --- | --- | --- | --- |
| Ridge | 3 | 0.0540 | 0.1375 | 0.0608 | 19/40 |
| Ridge | 4 | 0.0663 | 0.0577 | 0.0452 | 4/40 |
| Ridge | 7 | 0.3870 | 0.4882 | 0.4271 | 0/40 |
| Ridge | 8 | 0.0951 | 0.2167 | 0.1121 | 0/40 |
| Random Forest | 3 | 0.2544 | 0.3375 | 0.2638 | 2/40 |
| Random Forest | 4 | 0.0972 | 0.0766 | 0.0784 | 2/40 |
| Random Forest | 7 | 0.3892 | 0.4396 | 0.4009 | 0/40 |
| Random Forest | 8 | 0.0525 | 0.1792 | 0.0796 | 4/40 |
| Extra Trees | 3 | 0.2643 | 0.3500 | 0.2673 | 6/40 |
| Extra Trees | 4 | 0.1096 | 0.0670 | 0.0715 | 2/40 |
| Extra Trees | 7 | 0.3905 | 0.4368 | 0.4053 | 0/40 |
| Extra Trees | 8 | 0.0623 | 0.1708 | 0.0884 | 3/40 |
| HistGradientBoosting | 3 | 0.1705 | 0.3250 | 0.2029 | 3/40 |
| HistGradientBoosting | 4 | 0.0796 | 0.0900 | 0.0776 | 1/40 |
| HistGradientBoosting | 7 | 0.3871 | 0.4209 | 0.3943 | 0/40 |
| HistGradientBoosting | 8 | 0.0897 | 0.1688 | 0.1090 | 2/40 |
| XGBoost | 3 | 0.2227 | 0.3500 | 0.2460 | 4/40 |
| XGBoost | 4 | 0.0399 | 0.0527 | 0.0429 | 3/40 |
| XGBoost | 7 | 0.3928 | 0.4252 | 0.3980 | 0/40 |
| XGBoost | 8 | 0.0675 | 0.1688 | 0.0923 | 3/40 |
| CatBoost | 3 | 0.1908 | 0.3000 | 0.1965 | 8/40 |
| CatBoost | 4 | 0.0596 | 0.0527 | 0.0508 | 4/40 |
| CatBoost | 7 | 0.3907 | 0.4066 | 0.3880 | 0/40 |
| CatBoost | 8 | 0.0476 | 0.1812 | 0.0720 | 4/40 |
| Joint inner-selected | 3 | 0.2461 | 0.3000 | 0.2502 | 5/40 |
| Joint inner-selected | 4 | 0.0726 | 0.0702 | 0.0667 | 0/40 |
| Joint inner-selected | 7 | 0.3824 | 0.4297 | 0.3961 | 0/40 |
| Joint inner-selected | 8 | 0.0655 | 0.1687 | 0.0904 | 4/40 |

Each outer validation fold contains only **two genuine quality-3 wines** and **three or four quality-8 wines**. Repeated folds reuse those observations; they do not increase independent minority-class evidence. All-class precision/recall/F1, supports and confusion counts are retained in `outer_per_class.csv`, `per_class_comparison.csv` and `repeat_per_class.csv`.

## Fitted inner gains and threshold variability

| Family | Fitted inner threshold objective | Same-candidate OOF rounding | Fitted inner gain | Outer matched gain |
| --- | --- | --- | --- | --- |
| Ridge | 0.3644 | 0.2468 | +0.1176 | +0.0528 |
| Random Forest | 0.3864 | 0.2734 | +0.1131 | +0.0633 |
| Extra Trees | 0.3904 | 0.2617 | +0.1286 | +0.0731 |
| HistGradientBoosting | 0.3824 | 0.2730 | +0.1094 | +0.0515 |
| XGBoost | 0.3854 | 0.2754 | +0.1099 | +0.0486 |
| CatBoost | 0.3780 | 0.2724 | +0.1056 | +0.0422 |

The fitted inner gain includes direct optimization of the same OOF labels, plus candidate selection; it is optimistic by construction. Outer matched gain is the decoder comparison on untouched outer validation. A smaller outer gain warns against treating the fitted inner objective as generalization performance.

| Family | Boundary | Mean cut | SD | Min | Max |
| --- | --- | --- | --- | --- | --- |
| Ridge | 3|4 | 4.6263 | 0.2199 | 4.1221 | 5.0391 |
| Ridge | 4|5 | 4.9167 | 0.1380 | 4.3700 | 5.0912 |
| Ridge | 5|6 | 5.4292 | 0.0313 | 5.3661 | 5.5230 |
| Ridge | 6|7 | 6.1207 | 0.0546 | 6.0198 | 6.2776 |
| Ridge | 7|8 | 6.5799 | 0.1146 | 6.3991 | 6.8164 |
| Random Forest | 3|4 | 4.7795 | 0.0983 | 4.5330 | 4.9441 |
| Random Forest | 4|5 | 4.9648 | 0.0705 | 4.8082 | 5.0810 |
| Random Forest | 5|6 | 5.4416 | 0.0476 | 5.3454 | 5.5930 |
| Random Forest | 6|7 | 6.2007 | 0.0976 | 5.9844 | 6.3731 |
| Random Forest | 7|8 | 6.7888 | 0.2300 | 6.4659 | 7.6075 |
| Extra Trees | 3|4 | 4.9048 | 0.1042 | 4.6858 | 5.1360 |
| Extra Trees | 4|5 | 5.0462 | 0.0634 | 4.8767 | 5.1729 |
| Extra Trees | 5|6 | 5.4692 | 0.0326 | 5.3820 | 5.5500 |
| Extra Trees | 6|7 | 6.1314 | 0.0905 | 5.9311 | 6.3241 |
| Extra Trees | 7|8 | 6.6091 | 0.1871 | 6.4118 | 7.4802 |
| HistGradientBoosting | 3|4 | 4.6900 | 0.1141 | 4.4550 | 5.0085 |
| HistGradientBoosting | 4|5 | 4.9144 | 0.0879 | 4.6911 | 5.0741 |
| HistGradientBoosting | 5|6 | 5.4655 | 0.0500 | 5.3720 | 5.6494 |
| HistGradientBoosting | 6|7 | 6.2557 | 0.1128 | 6.0106 | 6.4908 |
| HistGradientBoosting | 7|8 | 6.8124 | 0.1159 | 6.5692 | 7.0156 |
| XGBoost | 3|4 | 4.6648 | 0.1186 | 4.3337 | 4.8428 |
| XGBoost | 4|5 | 4.9042 | 0.0907 | 4.6663 | 5.0834 |
| XGBoost | 5|6 | 5.4768 | 0.0663 | 5.3580 | 5.5993 |
| XGBoost | 6|7 | 6.2492 | 0.1089 | 6.0259 | 6.4284 |
| XGBoost | 7|8 | 6.8135 | 0.1373 | 6.5206 | 7.0767 |
| CatBoost | 3|4 | 4.8015 | 0.1292 | 4.4757 | 5.0588 |
| CatBoost | 4|5 | 4.9857 | 0.0631 | 4.8138 | 5.0991 |
| CatBoost | 5|6 | 5.4523 | 0.0441 | 5.3665 | 5.5423 |
| CatBoost | 6|7 | 6.2001 | 0.0982 | 5.9366 | 6.4233 |
| CatBoost | 7|8 | 6.6881 | 0.2076 | 6.3697 | 7.4758 |

These are descriptive cutpoint summaries for each family's inner-selected model; recipes may differ across folds. They are not a final set of deployment thresholds. The exact cutpoints for all 960 candidate/split combinations and their OOF objectives are retained in `threshold_training.json`; corresponding continuous OOF arrays are stored without pickle in `inner_oof_predictions.npz`.

| Joint procedure | Selected family | Outer folds |
| --- | --- | --- |
| matched rounding | CatBoost | 2 |
| matched rounding | Extra Trees | 15 |
| matched rounding | HistGradientBoosting | 9 |
| matched rounding | Random Forest | 6 |
| matched rounding | Ridge | 2 |
| matched rounding | XGBoost | 6 |
| learned cuts | CatBoost | 2 |
| learned cuts | Extra Trees | 15 |
| learned cuts | HistGradientBoosting | 9 |
| learned cuts | Random Forest | 6 |
| learned cuts | Ridge | 2 |
| learned cuts | XGBoost | 6 |
| selected rounding | CatBoost | 8 |
| selected rounding | Extra Trees | 2 |
| selected rounding | HistGradientBoosting | 13 |
| selected rounding | Random Forest | 7 |
| selected rounding | XGBoost | 10 |

## Comparison with frozen classifier results

Reference predictions are existing **development CV** outputs, loaded for comparison after the new fits. Every `(repeat, outer fold, source row, actual quality)` matches exactly. The historical search budgets differ, so this is not a controlled equal-budget comparison of all algorithms or evidence of universal superiority.

| Procedure | Macro F1 mean ± SD | Balanced Accuracy mean ± SD | QWK mean ± SD | decoded MAE mean ± SD | ±1 accuracy mean ± SD |
| --- | --- | --- | --- | --- | --- |
| Joint inner-selected — learned cuts | 0.3308 ± 0.0531 | 0.3562 ± 0.0645 | 0.5683 ± 0.0421 | 0.5118 ± 0.0441 | 0.9504 ± 0.0135 |
| Joint inner-selected — matched rounding | 0.2701 ± 0.0207 | 0.2723 ± 0.0183 | 0.5199 ± 0.0482 | 0.4379 ± 0.0290 | 0.9674 ± 0.0080 |
| Joint inner-selected — selected rounding | 0.2731 ± 0.0160 | 0.2753 ± 0.0146 | 0.5324 ± 0.0414 | 0.4396 ± 0.0262 | 0.9686 ± 0.0083 |
| Nominal logistic classifier | 0.3318 ± 0.0467 | 0.3612 ± 0.0645 | 0.5036 ± 0.0425 | 0.5325 ± 0.0387 | 0.9271 ± 0.0190 |
| Inner-selected ordinal classifier | 0.3481 ± 0.0626 | 0.3620 ± 0.0720 | 0.5243 ± 0.0447 | 0.5164 ± 0.0442 | 0.9367 ± 0.0183 |
| Tuned RBF SVM classifier | 0.3099 ± 0.0376 | 0.3285 ± 0.0525 | 0.4929 ± 0.0472 | 0.5389 ± 0.0342 | 0.9269 ± 0.0167 |
| LDA + SMOTE classifier | 0.3634 ± 0.0533 | 0.3919 ± 0.0618 | 0.5223 ± 0.0435 | 0.5660 ± 0.0384 | 0.9232 ± 0.0161 |

| Joint learned cuts minus classifier | Mean Δ Macro F1 | SD | Min Δ | Max Δ |
| --- | --- | --- | --- | --- |
| Nominal logistic classifier | -0.0010 | 0.0485 | -0.1107 | +0.0956 |
| Inner-selected ordinal classifier | -0.0174 | 0.0609 | -0.1305 | +0.1260 |
| Tuned RBF SVM classifier | +0.0209 | 0.0608 | -0.0920 | +0.1800 |
| LDA + SMOTE classifier | -0.0326 | 0.0536 | -0.2053 | +0.1115 |

## Interpretation

**Learning cutpoints improves six-class performance over rounding in this bounded study.** The joint inner-selected regression procedure achieved Macro F1 **0.3308 ± 0.0531**, versus **0.2701 ± 0.0207** when rounding the identical continuous predictions and **0.2731 ± 0.0160** for independently selected rounding. Mean paired gains were **+0.0606** and **+0.0577**, respectively. The matched gain ranged from **−0.0371 to +0.2052** across folds; improvement was not universal, and learned thresholds increased variability.

**Regression does not establish better six-class classification than the stronger existing references.** On exactly matching outer folds, its Macro F1 was essentially equal to nominal logistic classification (**0.3318**), below the inner-selected true ordinal classifier (**0.3481**) and LDA + SMOTE (**0.3634**), and above the earlier tuned RBF SVM estimate (**0.3099**). Different historical search budgets and dependent development folds preclude a broad superiority claim. Extra Trees had the highest descriptive family mean (**0.3397**), but that post-hoc observation does not replace the joint inner-selected estimate.

**The ordinal error metrics show a useful but incomplete benefit.** Joint learned-cut regression had QWK **0.5683**, decoded MAE **0.5118**, and ±1 accuracy **0.9504**, better on those metrics than these frozen classifier references. Relative to its own matched rounding control, however, learned cuts increased MAE (**0.4379 → 0.5118**) and lowered ±1 accuracy (**0.9674 → 0.9504**) while improving QWK (**0.5199 → 0.5683**). The objectives reward different error patterns; a better QWK is not evidence of better performance on every ordinal criterion.

**Tail discrimination remains poor.** Joint quality-8 recall was **0.1688**, but precision only **0.0655** and F1 **0.0904**. Quality-4 precision/recall/F1 were **0.0726 / 0.0702 / 0.0667**. Quality-3 F1 was **0.2502**, with no quality-3 predictions in **5/40** folds; quality 8 was unpredicted in **4/40**. The apparent recall gain for quality 8 comes with many false positives. Only two genuine quality-3 and three–four quality-8 wines appear in each outer validation fold.

The joint procedure's fitted inner threshold objective averaged **0.4010**, compared with **0.2701** for its same-candidate inner OOF rounding. Its outer Macro F1 was **0.3308**, and the outer matched gain **0.0606** was far smaller than the fitted inner gain **0.1309**. This is consistent with selection/threshold overfitting and score-distribution shifts; the fitted inner objective must not be reported as generalization performance.

Joint threshold selection chose Extra Trees in **15/40** training splits, Histogram Gradient Boosting in **9**, Random Forest in **6**, XGBoost in **6**, Ridge in **2**, and CatBoost in **2**. No single model or cutpoint set is locked for deployment. These findings support learned decoding over naive rounding, but do not show that regression solves the six-class imbalance problem better than the stronger direct/ordinal classification procedures. All conclusions remain exploratory **development CV estimates**; the original Version 1 holdout was not evaluated or used for selection.

## Runtime

| Family | Inner search sec | Outer refit sec | Outer predict sec | Unique outer refits |
| --- | --- | --- | --- | --- |
| Ridge | 6.66 | 0.27 | 0.07 | 68 |
| Random Forest | 116.48 | 20.55 | 0.73 | 65 |
| Extra Trees | 59.79 | 7.22 | 0.59 | 49 |
| HistGradientBoosting | 21.54 | 3.15 | 0.18 | 72 |
| XGBoost | 15.68 | 1.73 | 0.08 | 64 |
| CatBoost | 31.87 | 4.58 | 0.08 | 66 |

The run completed **2,880 inner fits + 384 unique outer refits = 3264 regressor fits**, and **960 cutpoint optimizations**, in **307.02 seconds**. Shared decoder/joint predictions are counted once. Runtime includes auditing and result assembly on serial one-thread CPU execution. Recorded warning categories: `{'FutureWarning': 720}`. There were no failed candidates or silently dropped folds.

## Validation and evidence

- Eight synthetic cutpoint check groups cover exhaustive global optimality, ties, empty bins, adjacent floating-point scores, extreme scores, serialization and boundary decoding. A separate reviewer checked 30 additional cases against exhaustive partition enumeration.
- Six synthetic framework groups use 72 genuine synthetic model fits to check all native configurations, cloning, training-only preprocessing, outer-validation perturbation invariance and refit reuse.
- A complete 40-fold synthetic assembly fixture uses 24 genuine synthetic native fits followed by 3,294 deterministic stub fit calls; it validates evidence assembly, not wine performance. A separate native runtime-guard fixture checks 83 genuine synthetic fits across all six families.
- Actual wine execution guards verify exact model/scaler training rows, native targets/parameters, inner validation predictions and the OOF vectors entering threshold fitting. Holdout evaluation, historical model loading, resampling and unregistered artifact access are blocked.
- Saved-evidence checks reconstruct exact CV memberships, every training audit, candidate and joint selection, all 960 fitted cutpoint objectives, all outer decodings/metrics/class reports and paired references. Five deliberately corrupted evidence copies are rejected. Replay does not rerun the threshold optimizer.
- A fresh-kernel experiment and full-notebook replay are recorded under `regression_ordinal_verification/`. Full replay blocks wine fitting, regression prediction, threshold optimization and raw dataset parsing after synthetic self-tests; existing checksum-only source reads are allowed for historical evidence integrity. Every prior notebook cell/output and all prior artifact hashes are checked for preservation; `/src` remains absent.

Ordinary **Run All** displays saved evidence. Explicit new execution requires `run_version_2_regression(run_id="a_new_unique_id")`; existing or partial directories cannot be overwritten. All new helper logic and self-tests remain notebook-local.

Raw results and hashes: `tables/version_2/regression_ordinal_20261015/`. Main tables: `metric_comparison.csv`, `per_class_comparison.csv`, `paired_rounding_differences.csv`, `reference_comparison.csv`, `reference_paired_differences.csv`, `outer_fold_metrics.csv`, `outer_oof_predictions.csv`, `inner_candidate_scores.csv`, `training_audits.json`, `plan.json` and `manifest.json`.
