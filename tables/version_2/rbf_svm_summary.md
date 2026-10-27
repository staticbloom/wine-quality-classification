# Experiment Version 2 — Development CV Estimate

Dedicated RBF-SVM nested random search versus fixed LDA + SMOTE.
Outer **4 folds × 10 repeats**, inner **3 folds**; existing development rows only.
The 60 registered joint candidates cover C **0.1–1000**, gamma `scale`/`auto` and
numeric **1e-4–10**, with **12 unit-weight controls** and **48 custom-weight configurations**.
All six class weights are independently sampled; no inverse-frequency balanced rule is used.

| Metric | Tuned RBF SVM mean ± SD | Fixed LDA + SMOTE mean ± SD |
|---|---:|---:|
| Macro F1 | 0.3099 ± 0.0376 | 0.3634 ± 0.0533 |
| Balanced Accuracy | 0.3285 ± 0.0525 | 0.3919 ± 0.0618 |
| Quadratic Weighted Kappa | 0.4929 ± 0.0472 | 0.5223 ± 0.0435 |
| Macro PR-AUC (average precision, OvR) | 0.3455 ± 0.0399 | 0.3881 ± 0.0528 |
| Macro ROC-AUC (OvR) | 0.7781 ± 0.0259 | 0.7960 ± 0.0245 |
| MAE | 0.5389 ± 0.0342 | 0.5660 ± 0.0384 |
| ±1 accuracy | 0.9269 ± 0.0167 | 0.9232 ± 0.0161 |

SD is descriptive population SD across dependent outer folds. Macro PR-AUC is
macro OvR average precision from SVC decision scores or LDA probabilities, without
pooling ranking scores across differently fitted models. No probability calibration
or hidden CV is used by SVC.

| Quality | SVM recall mean ± SD | LDA recall mean ± SD | SVM F1 mean ± SD | LDA F1 mean ± SD |
|---|---:|---:|---:|---:|
| 3 | 0.1500 ± 0.2291 | 0.3500 ± 0.2784 | 0.0690 ± 0.1088 | 0.3310 ± 0.2776 |
| 4 | 0.1216 ± 0.1070 | 0.2573 ± 0.1036 | 0.1019 ± 0.0818 | 0.1813 ± 0.0757 |
| 5 | 0.6037 ± 0.0514 | 0.6750 ± 0.0440 | 0.6378 ± 0.0301 | 0.6573 ± 0.0262 |
| 6 | 0.5715 ± 0.0738 | 0.3801 ± 0.0444 | 0.5490 ± 0.0444 | 0.4422 ± 0.0388 |
| 7 | 0.4474 ± 0.1173 | 0.5534 ± 0.0782 | 0.4380 ± 0.0667 | 0.4631 ± 0.0575 |
| 8 | 0.0771 ± 0.1349 | 0.1354 ± 0.1694 | 0.0636 ± 0.1141 | 0.1054 ± 0.1399 |

| Runtime | Tuned RBF SVM | Fixed LDA + SMOTE |
|---|---:|---:|
| Inner searches (seconds) | 158.438 | 0.000 |
| 40 outer fits (seconds) | 0.893 | 0.244 |
| 40 outer scoring calls (seconds) | 1.347 | 0.736 |
| Measured total (seconds) | 160.678 | 0.980 |

The fixed benchmark has zero new search cost; its historical development cost is not included.

Evidence: [registration and candidate pool](rbf_svm_20261012/plan.json),
[metric table](rbf_svm_20261012/metric_comparison.csv),
[per-class table](rbf_svm_20261012/per_class_comparison.csv),
[runtime table](rbf_svm_20261012/runtime_comparison.csv),
[selected recipes and outer-fold metrics](rbf_svm_20261012/outer_fold_metrics.csv),
[inner candidate scores](rbf_svm_20261012/inner_candidate_scores.csv), and
[paired fold differences](rbf_svm_20261012/paired_fold_differences.csv).

## Interpretation and limitations

The registered SVM procedure achieved outer **Macro F1 0.3099 ± 0.0376**, versus **0.3634 ± 0.0533** for the fixed LDA + SMOTE benchmark. The mean paired difference (SVM minus LDA) was **−0.0535**, with descriptive paired-fold SD **0.0548**. SVM had higher Macro F1 in **9 of 40 folds** and lower Macro F1 in **31**, with no ties. These dependent folds do not provide 40 independent trials or a significance test. **This bounded SVM search did not improve the primary development-CV objective over the benchmark.** No candidate pool, weight ranges or thresholds were changed after seeing these outer scores.

Supporting outer means were **Balanced Accuracy 0.3285 versus 0.3919**, **QWK 0.4929 versus 0.5223**, and **Macro PR-AUC (average precision) 0.3455 versus 0.3881**, for SVM versus LDA respectively. SVM had lower MAE (**0.5389 versus 0.5660**) and slightly higher ±1 accuracy (**0.9269 versus 0.9232**), but these supporting ordinal metrics do not override the registered Macro F1 objective.

Rare-class performance remains weak and variable. For quality 3, SVM recall/F1 averaged **0.1500 / 0.0690**, versus LDA **0.3500 / 0.3310**. For quality 8, SVM recall/F1 averaged **0.0771 / 0.0636**, versus LDA **0.1354 / 0.1054**. Each validation fold has only two quality-3 and three or four quality-8 wines. The full per-class table reports dispersion and all six labels, rather than inferring success from weighting alone.

Inner CV selected a custom-weight candidate in **39 of 40 outer folds**, and a unit-weight candidate once. The marginal medians of selected weights for classes 3–8 were **16, 3, 0.75, 1, 1.5, 6**. Those medians are descriptive summaries, **not a jointly selected recipe** and must not be deployed as one. C, gamma and weights varied jointly, and custom candidates had a larger allocation than controls; the selection frequency does not establish a causal benefit of class weighting. The full selected dictionaries, C and gamma are retained for each outer fold.

The SVM inner searches took **158.44 seconds** in this serial run. All 40 selected SVM refits took **0.89 seconds**, compared with **0.24 seconds** for the 40 fixed LDA refits. Measured search + outer fit + scoring totaled **160.68 seconds** for SVM and **0.98 seconds** for fixed LDA. The benchmark's previous development cost is excluded; these are measurements for the executed procedures, not a universal speed ratio. Runtime details also separate batch prediction cost from search.

All **7,280 fits** completed. Clean-kernel guards verified the expected raw training/validation calls; all inner choices, actual class weights, scaler statistics and source-row memberships were audited. All 80 outer evaluations, per-class scores, paired differences, repeat summaries and runtime totals were reproduced from saved development evidence. Every one of the **10,870 fresh LDA benchmark labels** also matched the prior development-only stability study on the identical folds. Synthetic tests confirmed that changing outer validation features and labels does not affect inner search scores or selection. The pinned environment's pandas compatibility notices were recorded without changing the method or retrying candidates.

Keep this result as evidence for this finite, registered SVM search. It does not show that every possible RBF-SVM configuration is inferior, and it does not restore independent test evidence after prior development exploration. No model was promoted, no full-development winner was fitted, and the original final holdout was not accessed or evaluated.
