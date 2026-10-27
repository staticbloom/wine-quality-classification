# Experiment Version 2 — Development CV Estimate

Dedicated CatBoost multiclass nested-CV study and direct comparison with the existing development benchmarks.

**Outer 4 folds × 10 repeats; inner 3 stratified folds; 1,087 development wines only.** Each CatBoost arm selects by unweighted sklearn Macro F1 from 24 shared randomized tree configurations. Native `Balanced` and `SqrtBalanced` are supported and verified in CatBoost 1.2.10.

| Procedure | Macro F1 mean ± SD | Balanced Accuracy | QWK | Macro PR-AUC |
|---|---:|---:|---:|---:|
| CatBoost — unweighted | 0.2826 ± 0.0155 | 0.2841 | 0.5195 | 0.3810 |
| CatBoost — Balanced | 0.3250 ± 0.0445 | 0.3675 | 0.5429 | 0.3630 |
| CatBoost — SqrtBalanced | 0.3262 ± 0.0497 | 0.3278 | 0.5529 | 0.3772 |
| CatBoost — custom weights | 0.3116 ± 0.0425 | 0.3350 | 0.5356 | 0.3874 |
| LDA + SMOTE (fixed) | 0.3634 ± 0.0533 | 0.3919 | 0.5223 | 0.3881 |
| RBF SVM (tuned) | 0.3099 ± 0.0376 | 0.3285 | 0.4929 | 0.3455 |
| XGBoost — unweighted (tuned) | 0.2809 ± 0.0228 | 0.2815 | 0.5074 | 0.3531 |
| XGBoost — frequency (tuned) | 0.3059 ± 0.0352 | 0.3397 | 0.5151 | 0.3460 |
| XGBoost — moderated (tuned) | 0.3102 ± 0.0388 | 0.3210 | 0.5243 | 0.3626 |

All entries are development CV estimates on exactly matching outer validation rows. SD is population SD across overlapping outer folds, not an independent-sample standard error or confidence interval. The full CSV includes mean, SD, minimum and maximum for every metric. PR-AUC is macro OvR average precision; SVM uses native decision scores and the other procedures use native class probabilities. Ranking scores from different fitted models are not pooled.

## CatBoost metrics and per-class performance

| Metric | Unweighted | Balanced | SqrtBalanced | Custom |
|---|---:|---:|---:|---:|
| Macro F1 | 0.2826 ± 0.0155 | 0.3250 ± 0.0445 | 0.3262 ± 0.0497 | 0.3116 ± 0.0425 |
| Balanced Accuracy | 0.2841 ± 0.0151 | 0.3675 ± 0.0585 | 0.3278 ± 0.0435 | 0.3350 ± 0.0581 |
| Quadratic Weighted Kappa | 0.5195 ± 0.0392 | 0.5429 ± 0.0396 | 0.5529 ± 0.0415 | 0.5356 ± 0.0493 |
| Macro PR-AUC (average precision, OvR) | 0.3810 ± 0.0352 | 0.3630 ± 0.0316 | 0.3772 ± 0.0324 | 0.3874 ± 0.0418 |
| Macro ROC-AUC (OvR) | 0.8040 ± 0.0280 | 0.7925 ± 0.0257 | 0.8081 ± 0.0256 | 0.8100 ± 0.0286 |
| MAE | 0.4439 ± 0.0281 | 0.5748 ± 0.0564 | 0.4713 ± 0.0304 | 0.4803 ± 0.0381 |
| ±1 accuracy | 0.9616 ± 0.0094 | 0.9181 ± 0.0224 | 0.9526 ± 0.0111 | 0.9499 ± 0.0118 |

Per-class **F1 mean ± SD**:

| Quality | Unweighted | Balanced | SqrtBalanced | Custom |
|---|---:|---:|---:|---:|
| 3 | 0.0000 ± 0.0000 | 0.1243 ± 0.1852 | 0.1546 ± 0.2490 | 0.1475 ± 0.1881 |
| 4 | 0.0045 ± 0.0284 | 0.1398 ± 0.0715 | 0.0821 ± 0.0762 | 0.0073 ± 0.0329 |
| 5 | 0.6956 ± 0.0280 | 0.6536 ± 0.0349 | 0.6909 ± 0.0257 | 0.6879 ± 0.0309 |
| 6 | 0.5770 ± 0.0326 | 0.4681 ± 0.0481 | 0.5455 ± 0.0376 | 0.5377 ± 0.0584 |
| 7 | 0.4185 ± 0.0681 | 0.4682 ± 0.0528 | 0.4620 ± 0.0557 | 0.4310 ± 0.0972 |
| 8 | 0.0000 ± 0.0000 | 0.0957 ± 0.1319 | 0.0218 ± 0.0795 | 0.0580 ± 0.1129 |

Per-class **Recall mean ± SD**:

| Quality | Unweighted | Balanced | SqrtBalanced | Custom |
|---|---:|---:|---:|---:|
| 3 | 0.0000 ± 0.0000 | 0.2000 ± 0.2693 | 0.1500 ± 0.2291 | 0.2250 ± 0.2487 |
| 4 | 0.0025 ± 0.0156 | 0.2211 ± 0.1210 | 0.0648 ± 0.0621 | 0.0050 ± 0.0218 |
| 5 | 0.7353 ± 0.0457 | 0.6297 ± 0.0520 | 0.7136 ± 0.0442 | 0.7161 ± 0.0690 |
| 6 | 0.6103 ± 0.0467 | 0.4072 ± 0.0655 | 0.5409 ± 0.0521 | 0.5451 ± 0.1050 |
| 7 | 0.3565 ± 0.0795 | 0.6200 ± 0.0868 | 0.4766 ± 0.0866 | 0.4311 ± 0.1337 |
| 8 | 0.0000 ± 0.0000 | 0.1271 ± 0.1728 | 0.0208 ± 0.0740 | 0.0875 ± 0.1717 |

Each validation fold contains only two quality-3 wines and three or four quality-8 wines. Rare-class metrics are sensitive to individual observations.

Per-class **mean F1** across all compared procedures:

| Procedure | Quality 3 | Quality 4 | Quality 5 | Quality 6 | Quality 7 | Quality 8 |
|---|---:|---:|---:|---:|---:|---:|
| CatBoost — unweighted | 0.0000 | 0.0045 | 0.6956 | 0.5770 | 0.4185 | 0.0000 |
| CatBoost — Balanced | 0.1243 | 0.1398 | 0.6536 | 0.4681 | 0.4682 | 0.0957 |
| CatBoost — SqrtBalanced | 0.1546 | 0.0821 | 0.6909 | 0.5455 | 0.4620 | 0.0218 |
| CatBoost — custom weights | 0.1475 | 0.0073 | 0.6879 | 0.5377 | 0.4310 | 0.0580 |
| LDA + SMOTE (fixed) | 0.3310 | 0.1813 | 0.6573 | 0.4422 | 0.4631 | 0.1054 |
| RBF SVM (tuned) | 0.0690 | 0.1019 | 0.6378 | 0.5490 | 0.4380 | 0.0636 |
| XGBoost — unweighted (tuned) | 0.0000 | 0.0033 | 0.6853 | 0.5597 | 0.4172 | 0.0200 |
| XGBoost — frequency (tuned) | 0.1102 | 0.0993 | 0.6464 | 0.4621 | 0.4488 | 0.0686 |
| XGBoost — moderated (tuned) | 0.0692 | 0.0564 | 0.6795 | 0.5317 | 0.4319 | 0.0923 |

## Runtime

| Procedure | Inner search (s) | 40 outer fits (s) | Outer scoring (s) | Measured total (s) | Prediction ms/row |
|---|---:|---:|---:|---:|---:|
| CatBoost — unweighted | 311.050 | 7.000 | 0.762 | 318.811 | 0.006 |
| CatBoost — Balanced | 316.369 | 7.328 | 0.755 | 324.452 | 0.006 |
| CatBoost — SqrtBalanced | 313.750 | 5.433 | 0.808 | 319.990 | 0.006 |
| CatBoost — custom weights | 315.088 | 4.253 | 0.760 | 320.102 | 0.006 |
| LDA + SMOTE (fixed) | 0.000 | 0.244 | 0.736 | 0.980 | 0.005 |
| RBF SVM (tuned) | 158.438 | 0.893 | 1.347 | 160.678 | 0.033 |
| XGBoost — unweighted (tuned) | 232.981 | 4.173 | 0.872 | 238.026 | 0.011 |
| XGBoost — frequency (tuned) | 253.849 | 3.950 | 0.857 | 258.656 | 0.011 |
| XGBoost — moderated (tuned) | 257.295 | 2.841 | 0.830 | 260.966 | 0.009 |

CatBoost completed **11,680 new fits** in **1287.49 seconds** of experiment wall time, excluding kernel startup. Execution was serial with one native CPU thread. Times include wrapper/audit overhead. LDA, SVM and XGBoost runtimes are retained from their original runs; no reference model was retrained for this comparison. Search budgets differ: 24 recipes per CatBoost/XGBoost arm, 60 for SVM, and no new search for fixed LDA. LDA’s historical development cost is excluded. These totals are not equal-budget or hardware-independent speed rankings.

## Paired comparisons on identical folds

Differences below are CatBoost minus each reference for **Macro F1**. They are descriptive; overlapping folds are not independent trials.

| CatBoost arm | Reference | Mean difference | SD | Positive / negative / tied folds |
|---|---|---:|---:|---:|
| CatBoost — unweighted | RBF SVM (tuned) | -0.0273 | 0.0367 | 9 / 31 / 0 |
| CatBoost — unweighted | LDA + SMOTE (fixed) | -0.0808 | 0.0543 | 2 / 38 / 0 |
| CatBoost — unweighted | XGBoost — unweighted (tuned) | +0.0017 | 0.0221 | 24 / 16 / 0 |
| CatBoost — unweighted | XGBoost — frequency (tuned) | -0.0233 | 0.0412 | 12 / 28 / 0 |
| CatBoost — unweighted | XGBoost — moderated (tuned) | -0.0276 | 0.0385 | 12 / 28 / 0 |
| CatBoost — Balanced | RBF SVM (tuned) | +0.0151 | 0.0513 | 25 / 15 / 0 |
| CatBoost — Balanced | LDA + SMOTE (fixed) | -0.0384 | 0.0680 | 15 / 25 / 0 |
| CatBoost — Balanced | XGBoost — unweighted (tuned) | +0.0440 | 0.0500 | 32 / 8 / 0 |
| CatBoost — Balanced | XGBoost — frequency (tuned) | +0.0191 | 0.0485 | 25 / 15 / 0 |
| CatBoost — Balanced | XGBoost — moderated (tuned) | +0.0148 | 0.0553 | 22 / 18 / 0 |
| CatBoost — SqrtBalanced | RBF SVM (tuned) | +0.0163 | 0.0465 | 27 / 13 / 0 |
| CatBoost — SqrtBalanced | LDA + SMOTE (fixed) | -0.0372 | 0.0589 | 12 / 28 / 0 |
| CatBoost — SqrtBalanced | XGBoost — unweighted (tuned) | +0.0452 | 0.0505 | 35 / 5 / 0 |
| CatBoost — SqrtBalanced | XGBoost — frequency (tuned) | +0.0203 | 0.0506 | 28 / 12 / 0 |
| CatBoost — SqrtBalanced | XGBoost — moderated (tuned) | +0.0160 | 0.0586 | 25 / 15 / 0 |
| CatBoost — custom weights | RBF SVM (tuned) | +0.0017 | 0.0505 | 20 / 20 / 0 |
| CatBoost — custom weights | LDA + SMOTE (fixed) | -0.0518 | 0.0543 | 6 / 34 / 0 |
| CatBoost — custom weights | XGBoost — unweighted (tuned) | +0.0307 | 0.0385 | 31 / 9 / 0 |
| CatBoost — custom weights | XGBoost — frequency (tuned) | +0.0057 | 0.0447 | 17 / 23 / 0 |
| CatBoost — custom weights | XGBoost — moderated (tuned) | +0.0014 | 0.0433 | 15 / 25 / 0 |

## Registered search and leakage controls

| Parameter | Values |
|---|---|
| iterations | 80, 150, 250, 400 |
| depth | 2, 3, 4 |
| learning_rate | 0.02, 0.04, 0.07, 0.12 |
| l2_leaf_reg | 1.0, 3.0, 10.0, 30.0 |
| random_strength | 0.0, 0.5, 1.0, 2.0 |
| bagging_temperature | 0.0, 0.5, 1.0, 2.0 |

The 24 joint tree recipes are generated before fitting with seed 6242 and balanced marginal coverage; all four weighting arms share them. Custom class weights vary independently: 2/4/8/12 for qualities 3 and 8; 1/1.5/2/3 for qualities 4 and 7; 0.75/1/1.25 for qualities 5 and 6. Each inner fit starts from raw training rows and a new model.

Native automatic weights use current-fit counts: `Balanced = max_class_count / class_count`, and `SqrtBalanced = sqrt(max_class_count / class_count)`. Custom weights are passed explicitly by original quality label. Native weight scales are preserved without normalization; automatic and custom policies are never combined. Effective fitted weights are checked after every fit. Bayesian bootstrap creates separate stochastic row weights during training.

Fixed settings: multiclass loss, CPU, one thread, seed 42, Plain boosting, 64 borders, Bayesian bootstrap, `verbose=False`, `allow_writing_files=False`, and `use_best_model=False`. No validation `eval_set`, early stopping, scaling, resampling, global quantization, external fitted Pool, feature engineering, calibration or threshold tuning is used. Iterations are chosen by inner CV; model selection uses sklearn Macro F1, not native training loss. See [CatBoost common parameters](https://catboost.ai/docs/en/references/training-parameters/common).

The benchmark manifests, file hashes, source data hash, development membership, inner/outer assignments and validation labels are checked. All XGBoost arms are retained; none is selected or discarded using its outer mean. The direct comparison uses saved development OOF evidence and opens no benchmark model packages.

## Interpretation

CatBoost Macro F1 means were **0.2826** (unweighted), **0.3250** (Balanced), **0.3262** (SqrtBalanced), **0.3116** (custom weights). CatBoost — SqrtBalanced had the highest observed mean among the four registered CatBoost procedures.

For context, fixed LDA + SMOTE achieved **0.3634**, tuned SVM **0.3099**, and the three tuned XGBoost procedures **0.2809 / 0.3059 / 0.3102** (unweighted / frequency / moderated). The tables retain all arms and paired differences instead of treating the highest outer mean as a newly validated selection rule.

SqrtBalanced exceeded Balanced by only **0.0012 Macro F1** on average; the paired-fold SD was **0.0520**, so this does not establish a definitive winner. Balanced had higher Balanced Accuracy (**0.3675 versus 0.3278**) and quality-8 F1 (**0.0957 versus 0.0218**). SqrtBalanced had higher QWK (**0.5529 versus 0.5429**). The custom-weight procedure had the highest CatBoost Macro PR-AUC (**0.3874**), but this supporting metric does not override the primary Macro F1 objective. Rare-class performance remains weak and variable; unweighted CatBoost had zero F1 for both quality 3 and quality 8 across these outer folds.

Every CatBoost procedure remained below LDA + SMOTE in mean Macro F1. SqrtBalanced's paired mean difference was **−0.0372 versus LDA**, **+0.0163 versus tuned SVM**, and **+0.0160 versus moderated XGBoost**. These descriptive comparisons characterize the registered procedures; they do not establish statistical superiority from overlapping folds or justify selecting a new final model by the outer means.

These results characterize the finite registered tuning procedures on already explored development data. They do not prove that an entire model family is unsuitable, establish a causal benefit of class weighting alone, or erase prior development selection. Custom weights and tree settings vary jointly. No search expansion or parameter change responds to the outer scores.

No final model is promoted or fitted on all development rows. The original holdout is not accessed or evaluated by this experiment, and Version 1 results remain unchanged.

Evidence: [registered plan](catboost_20261013/plan.json), [CatBoost metrics](catboost_20261013/metric_comparison.csv), [direct comparison](catboost_20261013/direct_metric_comparison.csv), [per-class comparison](catboost_20261013/direct_per_class_comparison.csv), [runtime](catboost_20261013/direct_runtime_comparison.csv), [paired differences](catboost_20261013/direct_paired_fold_differences.csv), [inner candidate scores](catboost_20261013/inner_candidate_scores.csv), [selected outer recipes](catboost_20261013/outer_fold_metrics.csv), and [effective weights and training audits](catboost_20261013/training_audits.csv).
