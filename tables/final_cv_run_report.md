# Final development-CV model selection

Status: **LOCKED**. Selected experiment: `lda__smote`.
Run: `5096bbc9-6dc2-47bc-8ee6-85c4114da6e0`. No final-test evaluation or full-development final fit has
occurred. This record describes development selection evidence only.

[Comparison CSV](final_cv_model_selection.csv) ·
[Comparison figure](../visuals/final_cv_model_comparison.png) ·
[Immutable recipe](../models/final/selection_lock.json) ·
[Recipe checksum](../models/final/selection_lock.sha256)

## Frozen pipeline

- Algorithm: sklearn LinearDiscriminantAnalysis, `solver="lsqr"`, `shrinkage=0.8`.
- Predictors: all 11 original numeric features, validated in canonical order;
  no feature engineering, removal or target-derived predictors.
- Preprocessing: StandardScaler (`with_mean=True`, `with_std=True`) fitted within
  each training fold, followed by the sampler and classifier.
- Imbalance treatment: SMOTE with seed 42, requested `k_neighbors=3`; adapt k to
  training support, skip targeted singleton classes. Each targeted training class
  grows to at most three times its original count, capped at half the largest
  training-class count (rounded up). The rule, not fixed class counts derived
  from validation data, is locked for later full-development fitting.
- Original quality labels and probability column order: 3, 4, 5, 6, 7, 8.
- The lock retains every other estimator default, complete nested pipeline,
  versions, source/evidence fingerprints and prediction policy. No calibration,
  class weighting or threshold adjustment is added to the selected LDA recipe.

## Design and deterministic decision

One tuned configuration per family was chosen from the prior imbalance results.
Before new CV, severe precision-collapse review flags became explicit eligibility
gates: a macro-precision loss of at least 10 percentage points or any pooled class
precision loss of at least 20 points versus that family's original distribution.
This is a newly declared selection policy based on prior development evidence;
those gates were not retroactive exclusions in the earlier experiment.

Logistic Regression with SMOTE was excluded because quality-3 precision fell from
33.3% to 7.7%; ROS became its best eligible configuration. Low absolute precision
alone remains a reported warning. LDA+SMOTE, original Gaussian NB, Gradient
Boosting+ROS, Logistic Regression+ROS and balanced-weight Random Forest were
frozen before fitting. Their hyperparameters were not retuned.

Each candidate uses five repetitions of five stratified folds with seed 42,
requiring 125 fits per complete run. The first repetition reproduces the prior
five-fold split. OOF predictions remain separate for each repetition: 1,087 original
development rows per candidate/repetition, 27,175 rows across five candidates and
five repetitions. No averaged-probability ensemble is scored as a single model.

Ranking uses mean fold Macro F1, then mean Balanced Accuracy, QWK, macro OvR Average
Precision and macro OvR ROC-AUC. Further ties prefer lower SD of repetition-level
mean Macro F1, lower fold Macro F1 SD, then alphabetical experiment identity.
Numeric tie keys are rounded to 12 decimals. Accuracy and runtime cannot change
ranking. Runtime is inspected as a supporting operational consideration.

## Results

Values below are validation-fold means; SD uses `ddof=0` over 25 dependent folds.

| Rank | Configuration | Macro F1 ± fold SD | Balanced accuracy | QWK | Macro AP | Macro ROC-AUC |
|---:|---|---:|---:|---:|---:|---:|
| 1 | lda__smote | 0.3774 ± 0.0696 | 0.4057 | 0.5264 | 0.3947 | 0.7937 |
| 2 | logistic_regression__random_over | 0.3339 ± 0.0479 | 0.3440 | 0.5207 | 0.3851 | 0.8064 |
| 3 | gaussian_nb__original | 0.3181 ± 0.0483 | 0.3303 | 0.4882 | 0.3407 | 0.7235 |
| 4 | random_forest__class_weight_balanced | 0.3144 ± 0.0442 | 0.3424 | 0.5428 | 0.3595 | 0.7647 |
| 5 | gradient_boosting__random_over | 0.3141 ± 0.0522 | 0.3178 | 0.5288 | 0.3755 | 0.7713 |

LDA+SMOTE ranks first in all five repetition-level mean Macro F1 comparisons. Its
fold Macro F1 SD is 0.0696; the SD of five repetition-level means
is 0.0172. The mean of its separately pooled OOF
Macro F1 scores is 0.3757, a different aggregation
from the primary fold-mean score. Repetition-dependent evidence is descriptive;
these are not significance tests or independent estimates.

The selected model's mean MAE is 0.5656, ±1 accuracy is
92.27%, and accuracy is 51.78%.
It does not lead every supporting metric: Random Forest has higher QWK, Logistic
Regression has higher ROC-AUC, and Gradient Boosting has lower MAE/higher ±1
accuracy. These tradeoffs are retained rather than using accuracy to override
Macro F1.

## Per-class limitations

These are means of the five separate pooled OOF reports. Original support is not
multiplied by the repeat count. Fold-level per-class summaries are also saved and
can differ because their small denominators receive equal fold weight.

| Quality | Mean pooled precision | Mean pooled recall | Mean pooled F1 | Original development support |
|---:|---:|---:|---:|---:|
| 3 | 0.3261 | 0.4250 | 0.3681 | 8 |
| 4 | 0.1365 | 0.2429 | 0.1746 | 42 |
| 5 | 0.6398 | 0.6751 | 0.6570 | 461 |
| 6 | 0.5277 | 0.3780 | 0.4405 | 428 |
| 7 | 0.3925 | 0.5478 | 0.4573 | 134 |
| 8 | 0.1293 | 0.2000 | 0.1568 | 14 |

Quality-8 mean pooled precision is only 12.9%, and
quality-4 precision is 13.6%. Qualities 3 and 8 have
only 8 and 14 independent development rows. SMOTE adds synthetic observations,
not independent evidence, and can overfit or interpolate implausible chemistry.
Earlier tuning and treatment/eligibility decisions used development evidence;
repeated CV remains selection-biased rather than nested or unbiased evaluation.
The locked model is selected under the stated criterion, not certified reliable
for rare-class predictions or production deployment.

## Runtime, checks and warnings

The final verified run (`5096bbc9-6dc2-47bc-8ee6-85c4114da6e0`) recorded 125 fits and summed CV wall time
of 17.324 seconds. The selected model's mean fold
fit time is 0.005356 seconds. Fit and scoring times are
separate. Native thread pools and models were limited to one; machine load,
hardware and software affect timings. This is not a full-notebook execution time.

Nine new synthetic selection tests and ten existing timing tests passed. Tests
cover precision gates, every tie-break, exactly-once OOF coverage per repeat,
metric recomputation, training-only sampler audits, complete configuration
reconstruction, overwrite refusal and detection of evidence/source/version changes.
The full notebook was not rerun; its five new CV/report cells and one lock cell
executed successfully, and notebook schema/code compilation checks passed.

An independent audit passed 2,255 metric comparisons, 4,680 per-class comparisons,
4,950 classification-report comparisons and 550 sampling checks. It also verified
fold reconstruction, original-repeat equivalence, confusion matrices, eligibility,
ranking, runtime summaries and code/source/evidence hashes.

The first run (`2ac48fad-9940-474b-9c53-6b20c578121b`) needed only a figure-label
placement repair. Because implementation hashes are frozen before CV, the same
125 fits were rerun after that code edit to maintain truthful provenance. All
27,175 predictions/probability rows, predictive metrics, reports and sampler audits
are exactly unchanged. Both run identities remain in the cumulative runtime CSV:
50 records, 250 total outer-fold fits across the original and verification runs.
No candidate settings or ranking rules changed in response to the scores.

The final run captured zero model warnings. Jupyter reported its local unencrypted
TCP startup notice. There are no unresolved implementation/test failures; the
statistical limitations above remain.

The final lock was verified and rebuilt as an unfitted identical pipeline.
Attempted overwrite was rejected. Replaying the notebook selection cells with
new-selection construction disabled performed no refits and left all saved
results/figure/runtime bytes unchanged. Source CSV, read-only Telco notebook,
original split/holdout lock, tuning/imbalance outputs and earlier figures retain
their pre-task checksums. Saved probability CSVs should be read using
`float_precision="round_trip"` to preserve score ties during metric reproduction.

## Files changed

- `.gitignore`
- `README.md`
- `models/final/selection_lock.json`
- `models/final/selection_lock.sha256`
- `notebook/Wine-Quality-Classification.ipynb`
- `src/wine_quality/selection.py`
- `tables/final_cv_candidate_eligibility.csv`
- `tables/final_cv_class_support.csv`
- `tables/final_cv_classification_reports.json`
- `tables/final_cv_completion.json`
- `tables/final_cv_environment.json`
- `tables/final_cv_fold_audits.json`
- `tables/final_cv_fold_metrics.csv`
- `tables/final_cv_model_selection.csv`
- `tables/final_cv_oof_predictions.csv`
- `tables/final_cv_per_class_metrics.csv`
- `tables/final_cv_plan.json`
- `tables/final_cv_repeat_metrics.csv`
- `tables/final_cv_run_report.md`
- `tables/final_cv_validation_assignments.csv`
- `tables/final_cv_warnings.csv`
- `tables/model_runtime_comparison.csv`
- `tests/test_selection.py`
- `visuals/final_cv_model_comparison.png`

Final fitting, holdout evaluation, final-model interpretation and packaging remain
separate phases. The algorithm, preprocessing, imbalance treatment and parameters
must never be changed to improve observed test performance.
