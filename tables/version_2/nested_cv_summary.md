# Experiment Version 2 — Development CV Estimate

Repeated nested stratified CV: **4 outer folds × 10 repeats**, **3 inner folds**.
The complete registered search jointly selects family, hyperparameters and imbalance
strategy by inner Macro F1 only. There are 20 candidates, 2,400 inner fits and 40
fresh outer-training refits. All 1,087 observations come from the existing development
partition. The original holdout was not loaded or evaluated.

| Outer metric | Mean | SD | Minimum | Maximum |
|---|---:|---:|---:|---:|
| Macro F1 | 0.3419 | 0.0534 | 0.1981 | 0.4654 |
| Balanced Accuracy | 0.3613 | 0.0622 | 0.2079 | 0.4987 |
| Quadratic Weighted Kappa | 0.5156 | 0.0440 | 0.4048 | 0.5933 |
| Macro PR-AUC (average precision, OvR) | 0.3823 | 0.0506 | 0.3041 | 0.5029 |
| Macro ROC-AUC (OvR) | 0.8014 | 0.0271 | 0.7244 | 0.8541 |
| MAE | 0.5359 | 0.0455 | 0.4228 | 0.6236 |
| ±1 accuracy | 0.9304 | 0.0176 | 0.8930 | 0.9706 |

SD is population SD (`ddof=0`) across 40 outer folds. Overlapping training data and
repeated observations make this descriptive spread, not a confidence interval.
Macro PR-AUC is macro OvR average precision, not trapezoidal PR area.

| Quality | Validation support | Recall mean ± SD | F1 mean ± SD |
|---|---:|---:|---:|
| 3 | 2–2 | 0.3250 ± 0.2861 | 0.2864 ± 0.2676 |
| 4 | 10–11 | 0.1345 ± 0.1083 | 0.1141 ± 0.0843 |
| 5 | 115–116 | 0.7039 ± 0.0544 | 0.6743 ± 0.0288 |
| 6 | 107–107 | 0.4360 ± 0.0671 | 0.4790 ± 0.0496 |
| 7 | 33–34 | 0.5015 ± 0.1222 | 0.4449 ± 0.0796 |
| 8 | 3–4 | 0.0667 ± 0.1253 | 0.0526 ± 0.1082 |

The full [metric summary](nested_cv_20261012/metric_summary.csv),
[outer-fold metrics](nested_cv_20261012/outer_fold_metrics.csv),
[per-class summary](nested_cv_20261012/per_class_summary.csv),
[per-class fold results](nested_cv_20261012/outer_per_class.csv), and
[repeat-level results](nested_cv_20261012/repeat_metrics.csv) retain all estimates.
The [plan](nested_cv_20261012/plan.json) was saved before fitting; the
[inner candidate scores](nested_cv_20261012/inner_candidate_scores.csv),
[inner fold scores](nested_cv_20261012/inner_fold_scores.csv),
[inner assignments](nested_cv_20261012/inner_assignments.csv) and
[outer assignments](nested_cv_20261012/outer_assignments.csv) document selection and nesting.

## Interpretation and limits

The complete registered search produced outer-fold **Macro F1 0.3419 ± 0.0534**, with **minimum 0.1981** and **maximum 0.4654**, across 40 outer validation folds. Supporting outer means are **Balanced Accuracy 0.3613**, **QWK 0.5156**, **macro average precision 0.3823**, **macro ROC-AUC 0.8014**, **MAE 0.5359** and **±1 accuracy 0.9304**. The summary table reports each metric's SD and range. These are repeated nested **development CV estimates**, conditional on the registered search and prior development exposure; they are not a new final-test result.

Rare-class metrics remain unstable despite stratification. Quality-3 outer recall is **0.3250 ± 0.2861**, with F1 **0.2864 ± 0.2676**; quality-8 recall is **0.0667 ± 0.1253**, with F1 **0.0526 ± 0.1082**. Each outer validation fold still contains only two quality-3 and three or four quality-8 wines. High macro ROC-AUC or ±1 accuracy does not remove the weak rare-class recall shown by the per-class table. No settings were revised in response to these outer results.

The inner search selected LDA in **26** outer folds and logistic regression in **14**. Across family/treatment pairs, it selected LDA+SMOTE **17** times, original LDA **6**, LDA+random oversampling **3**, logistic+random oversampling **8**, and logistic+SMOTE **6**. All 20 configurations—including Gaussian Naive Bayes and balanced class weights—were evaluated within every outer training set. Selection frequency is descriptive; it does not designate a new final model or authorize choosing a recipe using outer scores.

Validation verified all **2,400 inner fits**, **40 outer refits**, outer-only evaluation calls, candidate completeness, deterministic inner-only selection, split membership and actual scaler/resampler training inputs. All seven outer metrics, all six classes' recall/F1, aggregate ranges/SDs and per-repeat pooled results were reproduced from saved development evidence. Synthetic tests also verified that changing outer validation features and labels leaves inner scores and selection unchanged. The pinned environment emitted the same pandas compatibility `FutureWarning` seen in prior work; it did not cause candidate failures or changes to the procedure.

Keep this result as the evaluation of the declared 20-candidate procedure. Any subsequent search-space change needs a new registered run and remains subject to development-reuse optimism. The original Version 1 holdout stays closed; no source rows were reassigned and no full-development winner was fitted or packaged.
