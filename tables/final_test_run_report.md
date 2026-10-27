# Final holdout evaluation record

Completed 2026-10-11 15:58:45 +04. Evaluation run `a8fe4add-1814-4b01-8481-b4462fc231bd`.
Selection run `5096bbc9-6dc2-47bc-8ee6-85c4114da6e0` remains frozen.

## Scope and immutable configuration

Evaluated the saved `lda__smote` production champion on the **272**
original reserved test rows exactly once. The champion was already fitted on all
1,087 development rows. Its 11 input features and feature order, StandardScaler,
capped fold-safe SMOTE recipe, LDA `solver="lsqr"`, `shrinkage=0.8`, all other
hyperparameters and fitted state were unchanged. No test resampling, fitting,
calibration, threshold choice, candidate comparison or selection was performed.

One call to `predict` and one call to `predict_proba` supplied all diagnostics;
zero fit calls occurred. Probability columns explicitly map to qualities 3–8.
Predictions were persisted before calculations/plots, with exclusive partition-bound
access and checksum receipts. Completed reruns display the saved result only.
**Test results are diagnostic final results and were NOT fed back into selection.**

## Overall final test metrics

| Metric | Final test value |
|---|---:|
| Macro F1 | 0.358565 |
| Balanced Accuracy | 0.401573 |
| Quadratic Weighted Kappa | 0.560540 |
| Macro Precision | 0.339110 |
| Macro Recall | 0.401573 |
| Weighted F1 | 0.580190 |
| Macro ROC-AUC OvR | 0.759959 |
| Macro Average Precision OvR | 0.358622 |
| Accuracy | 0.580882 |
| MAE (quality points) | 0.485294 |
| Accuracy within ±1 point | 0.941176 |

Macro F1 remains primary. Accuracy is context only. PR performance is macro
One-vs-Rest Average Precision, not trapezoidal PR area. These are single-holdout
estimates, not cross-validation fold means; no fold SD is fabricated.

## Per-class final results

| Quality | Precision | Recall | F1 | Support |
|---|---:|---:|---:|---:|
| 3 | 0.000000 | 0.000000 | 0.000000 | 2 |
| 4 | 0.333333 | 0.636364 | 0.437500 | 11 |
| 5 | 0.686957 | 0.681034 | 0.683983 | 116 |
| 6 | 0.597701 | 0.485981 | 0.536082 | 107 |
| 7 | 0.416667 | 0.606061 | 0.493827 | 33 |
| 8 | 0.000000 | 0.000000 | 0.000000 | 3 |

Quality 3 has **2** test wines and quality 8 has
**3**. One wine moves recall by 50.0 and 33.3
percentage points respectively. Both have zero observed recall and F1. No quality-3
predictions were made, so its undefined precision is reported as zero under the
shared evaluation policy. Do not overinterpret these individual metrics or curves.
Ranking performance in OvR curves does not imply correct multiclass decisions or
well-calibrated probabilities. The SMOTE-trained classifier's probabilities have
not been independently calibrated.

## Outputs and runtime

Required metric, classification-report and prediction CSVs are saved under `tables/`.
Additional tables contain supports, raw and row-normalized confusion matrices,
OvR ROC/PR coordinates and per-class AUC/AP, runtime, warnings and immutable run
receipts. Four 300-dpi figures are saved under `visuals/` and embedded in the
notebook. Each figure was visually inspected; labels, counts, legends and titles
are readable. Matplotlib figures are closed after saving.

- Final label prediction: 0.013605 seconds.
- Final probability prediction: 0.001173 seconds.
- Batch label-prediction milliseconds per sample: 0.050017.
- Scoring including the two prediction calls and metric calculation: 0.031660 seconds; excludes file and plot I/O.
- Inference used one native thread. Timings depend on hardware, thread settings and warm-up.
- Seven final-test notebook cells executed successfully in 4.562 seconds including kernel/client overhead. This is a phase duration, **not** a full-notebook runtime.

The cumulative runtime table has exactly one new final-test row; every prior byte
is preserved. Model fitting/serialization times remain in their previous phase.
Package metadata's `test_evaluation_status=NOT_PERFORMED` is the historical creation
state. Current completion is recorded separately in `final_test_evaluation.json`,
without rewriting immutable model artifacts.

## Checks performed

- `python -m unittest discover -s tests -p 'test_holdout.py' -v`: **4 tests passed**, using temporary synthetic data only. The integration test checks exactly one label/probability pass, no fit, recovery after a simulated reporting failure, replay without inference, output-directory bypass rejection, artifact tampering, protected bytes and independent metrics.
- `python -m unittest discover -s tests -p 'test_evaluation.py' -v`: **17 tests passed**, including ±1 accuracy, ordinal QWK, class-probability ordering and the evaluation suite.
- All 11 actual final metrics and 24 per-class values independently recomputed with sklearn/NumPy from the **saved prediction CSV** and matched to numerical precision; no new model calls.
- All 272 saved source-row identifiers exactly match the reserved manifest and are disjoint from development; class probabilities are valid and ordered, confusion matrices and curve means reconcile.
- Fresh-process cached replay from `notebook/` succeeded with fit, predict, predict_proba, original test parsing and metric evaluation patched to fail. No artifact changed.
- Frozen package/selection verification passed. All candidate/champion binaries and metadata, source data, split and original holdout lock, selection lock/checksum, prior source/tests, Telco reference notebook and frozen CV evidence remain byte-identical.
- Notebook schema valid; seven executed final-test cells, four embedded figures, zero cell errors. Only those phase cells were executed.

## Warnings and unresolved limitations

- Extremely low quality-3/8 support and zero observed recall/F1 limit class-specific conclusions. Quality-3 precision uses the documented undefined-to-zero policy.
- No inference warnings were captured and no overall metric was undefined. The local Jupyter launcher emitted a TCP-without-encryption transport warning; execution still completed. This is retained here separately from model warnings.
- A single holdout does not establish deployment reliability, calibration or stability. No post-test model improvements were attempted.
- The persistent one-time guard intentionally prevents automatic retry if a future first-pass interruption occurs before its prediction receipt. Preserve the access record, receipt and completion evidence together; deleting them undermines the workflow guarantee.
- No later interpretation or deployment phase was started. No unresolved implementation/test failure remains.

## Files changed

Modified (3):

- `README.md`
- `notebook/Wine-Quality-Classification.ipynb`
- `tables/model_runtime_comparison.csv`

Created (22):

- `data/final_test_evaluation_access.json`
- `src/wine_quality/holdout.py`
- `tables/final_classification_report.csv`
- `tables/final_test_class_support.csv`
- `tables/final_test_classification_report.json`
- `tables/final_test_confusion_matrix.csv`
- `tables/final_test_curve_summary.csv`
- `tables/final_test_evaluation.json`
- `tables/final_test_metrics.csv`
- `tables/final_test_normalized_confusion_matrix.csv`
- `tables/final_test_pr_curve_points.csv`
- `tables/final_test_prediction_receipt.json`
- `tables/final_test_predictions.csv`
- `tables/final_test_roc_curve_points.csv`
- `tables/final_test_run_report.md`
- `tables/final_test_runtime.csv`
- `tables/final_test_warnings.csv`
- `tests/test_holdout.py`
- `visuals/final_test_confusion_matrix.png`
- `visuals/final_test_multiclass_precision_recall_curves.png`
- `visuals/final_test_multiclass_roc_curves.png`
- `visuals/final_test_normalized_confusion_matrix.png`
