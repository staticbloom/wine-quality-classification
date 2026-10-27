# Experiment Version 2 — Development CV Estimate

Controlled oversampling study on **1,087 existing development wines**. Outer stratified 4-fold ×10 repeats; inner stratified 3-fold. All 25 sampling candidates and fixed model settings were registered before training. The Version 1 holdout was not evaluated; earlier results remain unchanged.

## Comparison

| Fixed model / sampling procedure | Macro F1 mean ± SD | Balanced Accuracy | QWK | Macro PR-AUC |
|---|---:|---:|---:|---:|
| LDA / No resampling | 0.3558 ± 0.0675 | 0.3506 | 0.5269 | 0.3933 |
| LDA / Inner-selected ROS | 0.3493 ± 0.0531 | 0.3675 | 0.5238 | 0.3878 |
| LDA / Inner-selected SMOTE | 0.3611 ± 0.0556 | 0.3776 | 0.5307 | 0.3935 |
| LDA / Inner-selected sampler | 0.3590 ± 0.0554 | 0.3758 | 0.5304 | 0.3921 |
| Logistic Regression / No resampling | 0.2975 ± 0.0467 | 0.2943 | 0.4999 | 0.3923 |
| Logistic Regression / Inner-selected ROS | 0.3355 ± 0.0586 | 0.3388 | 0.5139 | 0.3866 |
| Logistic Regression / Inner-selected SMOTE | 0.3400 ± 0.0586 | 0.3414 | 0.5155 | 0.3887 |
| Logistic Regression / Inner-selected sampler | 0.3393 ± 0.0620 | 0.3399 | 0.5161 | 0.3878 |
| RBF SVM / No resampling | 0.2965 ± 0.0362 | 0.2953 | 0.4824 | 0.3592 |
| RBF SVM / Inner-selected ROS | 0.3074 ± 0.0468 | 0.3058 | 0.4960 | 0.3588 |
| RBF SVM / Inner-selected SMOTE | 0.3097 ± 0.0432 | 0.3095 | 0.4909 | 0.3527 |
| RBF SVM / Inner-selected sampler | 0.3070 ± 0.0384 | 0.3073 | 0.4899 | 0.3527 |
| LightGBM / No resampling | 0.2786 ± 0.0202 | 0.2803 | 0.5085 | 0.3556 |
| LightGBM / Inner-selected ROS | 0.2937 ± 0.0386 | 0.2929 | 0.5202 | 0.3601 |
| LightGBM / Inner-selected SMOTE | 0.2949 ± 0.0360 | 0.2964 | 0.5214 | 0.3559 |
| LightGBM / Inner-selected sampler | 0.2955 ± 0.0356 | 0.2966 | 0.5200 | 0.3565 |

Population SD describes 40 overlapping outer folds, not an independent-sample uncertainty interval. Macro PR-AUC is macro OvR average precision: SVM uses native decision scores; other models use probabilities. Ranking metrics are calculated within each fitted fold, never from pooled cross-model scores. All six classes contribute equally to the optimization metric.

## Precision and recall of the extremely rare classes

Each outer fold contains two quality-3 wines and three or four quality-8 wines. Fold-average precision uses zero_division=0; the zero-prediction column identifies undefined precision explicitly. Counts are observations per validation fold, not synthetic training samples.

| Procedure | Quality | Precision | Recall | F1 | Mean TP / FP | No-positive-prediction folds |
|---|---:|---:|---:|---:|---:|---:|
| LDA / No resampling | 3 | 0.4487 | 0.3500 | 0.3671 | 0.70 / 1.18 | 2/40 |
| LDA / No resampling | 8 | 0.1237 | 0.0646 | 0.0789 | 0.23 / 2.25 | 8/40 |
| LDA / Inner-selected ROS | 3 | 0.2946 | 0.3750 | 0.3007 | 0.75 / 1.85 | 3/40 |
| LDA / Inner-selected ROS | 8 | 0.0809 | 0.0750 | 0.0667 | 0.25 / 3.38 | 4/40 |
| LDA / Inner-selected SMOTE | 3 | 0.3386 | 0.3750 | 0.3180 | 0.75 / 1.90 | 0/40 |
| LDA / Inner-selected SMOTE | 8 | 0.1008 | 0.1250 | 0.1054 | 0.42 / 4.08 | 2/40 |
| LDA / Inner-selected sampler | 3 | 0.3411 | 0.3750 | 0.3204 | 0.75 / 1.88 | 0/40 |
| LDA / Inner-selected sampler | 8 | 0.0883 | 0.1167 | 0.0954 | 0.40 / 3.95 | 0/40 |
| Logistic Regression / No resampling | 3 | 0.1792 | 0.1250 | 0.1408 | 0.25 / 0.47 | 20/40 |
| Logistic Regression / No resampling | 8 | 0.0000 | 0.0000 | 0.0000 | 0.00 / 0.20 | 33/40 |
| Logistic Regression / Inner-selected ROS | 3 | 0.2621 | 0.2875 | 0.2585 | 0.57 / 1.15 | 10/40 |
| Logistic Regression / Inner-selected ROS | 8 | 0.0858 | 0.0667 | 0.0692 | 0.23 / 2.42 | 9/40 |
| Logistic Regression / Inner-selected SMOTE | 3 | 0.2904 | 0.2750 | 0.2655 | 0.55 / 1.05 | 9/40 |
| Logistic Regression / Inner-selected SMOTE | 8 | 0.0802 | 0.0854 | 0.0817 | 0.30 / 2.40 | 3/40 |
| Logistic Regression / Inner-selected sampler | 3 | 0.2904 | 0.2750 | 0.2655 | 0.55 / 1.05 | 9/40 |
| Logistic Regression / Inner-selected sampler | 8 | 0.0873 | 0.0771 | 0.0768 | 0.28 / 2.33 | 4/40 |
| RBF SVM / No resampling | 3 | 0.0896 | 0.0875 | 0.0850 | 0.17 / 0.60 | 20/40 |
| RBF SVM / No resampling | 8 | 0.0000 | 0.0000 | 0.0000 | 0.00 / 0.97 | 17/40 |
| RBF SVM / Inner-selected ROS | 3 | 0.1396 | 0.1000 | 0.1100 | 0.20 / 0.75 | 16/40 |
| RBF SVM / Inner-selected ROS | 8 | 0.0163 | 0.0208 | 0.0183 | 0.07 / 1.60 | 7/40 |
| RBF SVM / Inner-selected SMOTE | 3 | 0.1271 | 0.1125 | 0.1096 | 0.23 / 1.05 | 14/40 |
| RBF SVM / Inner-selected SMOTE | 8 | 0.0446 | 0.0479 | 0.0453 | 0.15 / 1.70 | 6/40 |
| RBF SVM / Inner-selected sampler | 3 | 0.1062 | 0.1000 | 0.0967 | 0.20 / 1.02 | 13/40 |
| RBF SVM / Inner-selected sampler | 8 | 0.0362 | 0.0396 | 0.0370 | 0.12 / 1.68 | 5/40 |
| LightGBM / No resampling | 3 | 0.0000 | 0.0000 | 0.0000 | 0.00 / 0.12 | 36/40 |
| LightGBM / No resampling | 8 | 0.0125 | 0.0083 | 0.0100 | 0.03 / 0.60 | 28/40 |
| LightGBM / Inner-selected ROS | 3 | 0.0750 | 0.0375 | 0.0500 | 0.07 / 0.33 | 27/40 |
| LightGBM / Inner-selected ROS | 8 | 0.0467 | 0.0271 | 0.0323 | 0.10 / 1.57 | 13/40 |
| LightGBM / Inner-selected SMOTE | 3 | 0.0542 | 0.0500 | 0.0492 | 0.10 / 0.62 | 21/40 |
| LightGBM / Inner-selected SMOTE | 8 | 0.0492 | 0.0354 | 0.0356 | 0.12 / 1.93 | 9/40 |
| LightGBM / Inner-selected sampler | 3 | 0.0542 | 0.0500 | 0.0492 | 0.10 / 0.62 | 21/40 |
| LightGBM / Inner-selected sampler | 8 | 0.0492 | 0.0354 | 0.0356 | 0.12 / 1.93 | 8/40 |

## Recall–precision tradeoffs

Each row compares the same fixed model on the same outer fold against no resampling. The first flag requires increased recall and precision below .10 with at least one positive prediction. The second requires increased recall, precision at most half a positive baseline precision, and more false positives. These predeclared flags are descriptive; they never alter inner selection.

| Procedure | Quality | Mean Δ recall | Mean Δ precision | Mean Δ F1 | Mean Δ FP | Low-precision flags | Halved-precision flags |
|---|---:|---:|---:|---:|---:|---:|---:|
| LDA / Inner-selected sampler | 3 | +0.0250 | -0.1076 | -0.0467 | +0.70 | 0/40 | 1/40 |
| LDA / Inner-selected sampler | 8 | +0.0521 | -0.0355 | +0.0165 | +1.70 | 1/40 | 0/40 |
| LDA / Inner-selected ROS | 3 | +0.0250 | -0.1542 | -0.0664 | +0.68 | 0/40 | 1/40 |
| LDA / Inner-selected ROS | 8 | +0.0104 | -0.0429 | -0.0123 | +1.12 | 1/40 | 0/40 |
| LDA / Inner-selected SMOTE | 3 | +0.0250 | -0.1101 | -0.0491 | +0.72 | 0/40 | 1/40 |
| LDA / Inner-selected SMOTE | 8 | +0.0604 | -0.0230 | +0.0265 | +1.82 | 1/40 | 0/40 |
| LightGBM / Inner-selected sampler | 3 | +0.0500 | +0.0542 | +0.0492 | +0.50 | 0/40 | 0/40 |
| LightGBM / Inner-selected sampler | 8 | +0.0271 | +0.0367 | +0.0256 | +1.32 | 0/40 | 0/40 |
| LightGBM / Inner-selected ROS | 3 | +0.0375 | +0.0750 | +0.0500 | +0.20 | 0/40 | 0/40 |
| LightGBM / Inner-selected ROS | 8 | +0.0187 | +0.0342 | +0.0223 | +0.97 | 0/40 | 0/40 |
| LightGBM / Inner-selected SMOTE | 3 | +0.0500 | +0.0542 | +0.0492 | +0.50 | 0/40 | 0/40 |
| LightGBM / Inner-selected SMOTE | 8 | +0.0271 | +0.0367 | +0.0256 | +1.32 | 0/40 | 0/40 |
| Logistic Regression / Inner-selected sampler | 3 | +0.1500 | +0.1113 | +0.1246 | +0.57 | 0/40 | 0/40 |
| Logistic Regression / Inner-selected sampler | 8 | +0.0771 | +0.0873 | +0.0768 | +2.12 | 0/40 | 0/40 |
| Logistic Regression / Inner-selected ROS | 3 | +0.1625 | +0.0829 | +0.1176 | +0.68 | 0/40 | 1/40 |
| Logistic Regression / Inner-selected ROS | 8 | +0.0667 | +0.0858 | +0.0692 | +2.23 | 0/40 | 0/40 |
| Logistic Regression / Inner-selected SMOTE | 3 | +0.1500 | +0.1113 | +0.1246 | +0.57 | 0/40 | 0/40 |
| Logistic Regression / Inner-selected SMOTE | 8 | +0.0854 | +0.0802 | +0.0817 | +2.20 | 0/40 | 0/40 |
| RBF SVM / Inner-selected sampler | 3 | +0.0125 | +0.0167 | +0.0117 | +0.42 | 0/40 | 0/40 |
| RBF SVM / Inner-selected sampler | 8 | +0.0396 | +0.0362 | +0.0370 | +0.70 | 0/40 | 0/40 |
| RBF SVM / Inner-selected ROS | 3 | +0.0125 | +0.0500 | +0.0250 | +0.15 | 0/40 | 0/40 |
| RBF SVM / Inner-selected ROS | 8 | +0.0208 | +0.0163 | +0.0183 | +0.62 | 0/40 | 0/40 |
| RBF SVM / Inner-selected SMOTE | 3 | +0.0250 | +0.0375 | +0.0246 | +0.45 | 0/40 | 0/40 |
| RBF SVM / Inner-selected SMOTE | 8 | +0.0479 | +0.0446 | +0.0453 | +0.72 | 0/40 | 0/40 |

Within-repeat pooled label metrics and complete six-class precision/recall/F1 are retained in the CSV evidence. Each repeat predicts the same 1,087 real wines exactly once; repeating the split does not create ten independent datasets.

## Genuine and added training observations

The following ranges cover all registered inner training fits. Targets depend only on genuine current-fold labels. ROS additions are exact duplicates; SMOTE additions are generated vectors and are not guaranteed unique. Classes 5 and 6 are unchanged. Both methods use identical target rules.

| Profile | Quality | Genuine count | Desired final count | Added duplicates (ROS) or generated vectors (SMOTE) |
|---|---:|---:|---:|---:|
| emphasize_3 | 3 | 4 | 12 | 8 |
| emphasize_3 | 4 | 20–22 | 30–33 | 10–11 |
| emphasize_3 | 7 | 66–68 | 81 | 13–15 |
| emphasize_3 | 8 | 6–8 | 12 | 4–6 |
| emphasize_8 | 3 | 4 | 7 | 3 |
| emphasize_8 | 4 | 20–22 | 30–33 | 10–11 |
| emphasize_8 | 7 | 66–68 | 81 | 13–15 |
| emphasize_8 | 8 | 6–8 | 18–19 | 11–12 |
| gentle | 3 | 4 | 7 | 3 |
| gentle | 4 | 20–22 | 30–33 | 10–11 |
| gentle | 7 | 66–68 | 81 | 13–15 |
| gentle | 8 | 6–8 | 12 | 4–6 |
| middle_only | 3 | 4 | 4 | 0 |
| middle_only | 4 | 20–22 | 40–44 | 20–22 |
| middle_only | 7 | 66–68 | 99–102 | 33–34 |
| middle_only | 8 | 6–8 | 6–8 | 0 |
| moderate | 3 | 4 | 12 | 8 |
| moderate | 4 | 20–22 | 40–44 | 20–22 |
| moderate | 7 | 66–68 | 99–102 | 33–34 |
| moderate | 8 | 6–8 | 18–19 | 11–12 |
| rare_only | 3 | 4 | 12 | 8 |
| rare_only | 4 | 20–22 | 20–22 | 0 |
| rare_only | 7 | 66–68 | 66–68 | 0 |
| rare_only | 8 | 6–8 | 18–19 | 11–12 |

All outer refits obey the same fold-local ratio/multiplier rule and absolute rare-class caps. Their actual selected-method count ranges are:

| Method | Quality | Genuine count | Duplicate additions | Generated additions | Final count |
|---|---:|---:|---:|---:|---:|
| No resampling | 3 | 6 | 0 | 0 | 6 |
| No resampling | 4 | 31–32 | 0 | 0 | 31–32 |
| No resampling | 5 | 345–346 | 0 | 0 | 345–346 |
| No resampling | 6 | 321 | 0 | 0 | 321 |
| No resampling | 7 | 100–101 | 0 | 0 | 100–101 |
| No resampling | 8 | 10–11 | 0 | 0 | 10–11 |
| Inner-selected ROS | 3 | 6 | 0–12 | 0 | 6–18 |
| Inner-selected ROS | 4 | 31–32 | 0–32 | 0 | 31–64 |
| Inner-selected ROS | 5 | 345–346 | 0 | 0 | 345–346 |
| Inner-selected ROS | 6 | 321 | 0 | 0 | 321 |
| Inner-selected ROS | 7 | 100–101 | 0–50 | 0 | 100–151 |
| Inner-selected ROS | 8 | 10–11 | 0–18 | 0 | 10–28 |
| Inner-selected SMOTE | 3 | 6 | 0 | 0–12 | 6–18 |
| Inner-selected SMOTE | 4 | 31–32 | 0 | 0–32 | 31–64 |
| Inner-selected SMOTE | 5 | 345–346 | 0 | 0 | 345–346 |
| Inner-selected SMOTE | 6 | 321 | 0 | 0 | 321 |
| Inner-selected SMOTE | 7 | 100–101 | 0 | 0–50 | 100–151 |
| Inner-selected SMOTE | 8 | 10–11 | 0 | 0–18 | 10–28 |

Counts describe one fitted fold at a time. Summing additions across reused rows, models, candidates or repeats would not measure independent observations.

## Inner selection and runtime

Exact ties in inner Macro F1 prefer fewer additions, then registered candidate order. The joint sampler procedure chooses the method/profile/k inside inner CV. Its predictions reuse an already fitted method winner; it is not an extra fit and is not a choice based on outer scores.

| Fixed model | Joint selections: none | ROS | SMOTE | Inner search seconds | Three outer refits seconds | Outer scoring seconds |
|---|---:|---:|---:|---:|---:|---:|
| LDA | 0 | 4 | 36 | 30.28 | 0.80 | 2.19 |
| Logistic Regression | 0 | 6 | 34 | 45.83 | 1.63 | 2.19 |
| RBF SVM | 0 | 11 | 29 | 67.39 | 2.68 | 4.05 |
| LightGBM | 0 | 3 | 37 | 202.18 | 8.81 | 3.09 |

Executed **12,000 inner fits + 480 outer refits = 12,480 fits** in 378.61 seconds (6.3 minutes), including audit/report overhead. Runtime is specific to this machine and serial one-thread execution. No final model was fitted on all development data.

## Interpretation and limits

The complete **inner-selected sampler** procedures produced Macro F1 **0.3590 ± 0.0554 for LDA, 0.3393 ± 0.0620 for Logistic Regression, 0.3070 ± 0.0384 for RBF SVM and 0.2955 ± 0.0356 for LightGBM**. Their matched no-resampling baselines were 0.3558, 0.2975, 0.2965 and 0.2786. These comparisons describe the fixed model recipes and registered sampler search; they do not establish a final winning model or an optimal SMOTE configuration.

Logistic Regression showed the largest descriptive improvement in Macro F1 (+0.0418). Its quality-3 fold-average precision/recall/F1 increased from **0.1792 / 0.1250 / 0.1408** to **0.2904 / 0.2750 / 0.2655**. However, its quality-8 fold-average precision remained only **0.0873**, with about **2.33 false positives per outer fold**. Improving Macro F1 did not resolve the rarest-class prediction problem.

LDA illustrates the precision cost clearly. Its joint sampler increased quality-3 recall from **0.3500 to 0.3750**, while precision fell from **0.4488 to 0.3411** and F1 fell from **0.3671 to 0.3204**. Quality-8 recall rose from **0.0646 to 0.1167**, while precision fell from **0.1238 to 0.0883** and mean false positives rose from **2.25 to 3.95 per fold**. The quality-8 F1 gain was modest (0.0789 to 0.0954). The registered diagnostics flagged one LDA fold with recall gain and quality-8 precision below .10, and one quality-3 fold with recall gain, at least halved precision and increased false positives.

A small flag count is not evidence that precision is acceptable: the flags require a *paired recall gain*, so they exclude folds with no correct rare-class predictions. Pooling labels within each repeat, the joint procedures' mean quality-8 precision was only **0.0898 for LDA, 0.1103 for Logistic Regression, 0.0450 for SVM and 0.0724 for LightGBM**. False positives therefore remain a material limitation, even where resampling improves recall. Zero-positive-prediction folds are separately reported and must not be confused with predictions that are all wrong.

Inner selection chose SMOTE in **36/40 LDA, 34/40 Logistic Regression, 29/40 SVM and 37/40 LightGBM** outer training sets; remaining choices used ROS. It did not choose the no-resampling candidate, but this does not make no resampling an invalid baseline. The joint procedures selected the moderate profile in only **11, 18, 14 and 14 of 40 folds**, respectively. Other profiles—including those leaving qualities 3 and 8 untouched—were often selected. Neither the most aggressive target profile nor one k value is automatically adopted.

Actual quality-3 inner training sets contained **4 real wines plus 0–8 additions** (4–12 final rows); quality-8 inner sets contained **6–8 real wines plus 0–12 additions** (6–19 final rows). Outer refits contained **6 genuine quality-3 wines**, capped at 18 final rows, and **10–11 genuine quality-8 wines**, with at most 28 final rows in this run. Added rows remain duplicates or interpolations of those few genuine observations. The study supports cautious, fold-local sampler selection and continued scrutiny of rare-class precision; it does not justify enlarging the sampling caps from these outer results.


Synthetic interpolation among only four genuine inner-training quality-3 wines can amplify mislabeled points and class overlap. ROS can encourage memorization of the same rare wines. Targets at most triple genuine rare support, with absolute q3/q8 caps of 18/30, limit augmentation but do not create independent evidence or prove an optimal sampler. Model settings are fixed; a future joint model/sampling search would be a new preregistered procedure.

## Evidence and checks

All study logic is notebook-local in `notebook/Wine-Quality-Classification.ipynb`. The run directory is `tables/version_2/oversampling_20261014/`. `plan.json` registers the design; `manifest.json` hashes all results. CSVs include outer metrics and predictions, all-class metrics, inner candidate scores, exact fold membership/support, per-fit sampling counts, paired precision diagnostics, and repeat-level label metrics. `training_audits.json` records every fitted training membership, scaler moments, native model recipe and actual native sampler additions.

Runtime guards reject old holdout/result/model access during experimentation, inspect each native fit and scaler/sampler input, and prohibit validation resampling. Evidence validation reconstructs split assignments, selections, counts and reported metrics. Synthetic checks and a fresh-kernel notebook replay verify the notebook works without `/src`. Earlier notebook cells and artifacts are checked for exact preservation.
