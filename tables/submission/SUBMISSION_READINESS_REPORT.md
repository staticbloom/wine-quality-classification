# SUBMISSION READINESS REPORT

**Ready — verified in the pinned Python 3.14.7 environment.**

- **Final model:** FROZEN Version 2 LDA (`lsqr`, shrinkage 0.8), StandardScaler, gentle capped SMOTE (`k=1`) and protected Tomek cleaning. Inference contains only the fitted standard scikit-learn scaler/LDA pipeline; model bytes are unchanged.
- **Final credible Macro F1:** **0.366587 ± 0.054874** (population fold SD), using development-only outer 4-fold × 10-repeat / inner 3-fold stratified CV. Balanced Accuracy 0.391318, QWK 0.527035, Macro PR-AUC/AP 0.392060, Accuracy 0.539736, MAE 0.535891 and ±1 Accuracy 0.930539. The 0.50 target was not achieved.
- **Execution:** the complete 50-cell notebook (23 code cells) ran sequentially in fresh kernels from the project root, from `notebook/`, and from a relocated project copy. All runs embedded six figures and loaded the model successfully. Each permitted only two handwritten examples and three synthetic packaging probes. There were **zero fitting/search attempts, zero raw wine-data parses and zero holdout predictions**.
- **Preservation:** all 506 pre-existing data/model/table/visual evidence files remain byte-identical. The original 469-cell development notebook is preserved byte-for-byte as an archive; all original legitimate outputs remain available. Empty directory placeholders and obsolete bytecode/OS caches were removed. No frozen results were deleted.

## Submission audit

| Check | Outcome |
|---|---|
| Notebook organization | All requested ML-report sections; concise unsuccessful-experiment discussion |
| Self-contained project logic | Eleven unique shared helpers in the main notebook; archive read as inert provenance JSON only |
| Removed source package | No dependency, imports or directory references in the active notebook; runtime imports/access blocked by verifier |
| Paths | Root, notebook directory and relocated project all passed |
| Tables | Ten-model final leaderboard, champion highlighted; fourteen readable HTML tables; full-precision CSVs |
| Plots | Six embedded/saved PNGs visually inspected; titles, axis labels, class order and scale annotations present |
| Model and prediction | Library-only model loads; synthetic probes match frozen outputs; handwritten examples work; five invalid-input cases rejected |
| Metrics | Macro F1 explicitly separated from weighted F1; all 40 champion folds manually reconstructed from six class F1 values |
| Probability metrics | Macro PR-AUC means OvR average precision; regression without ranking scores remains N/A |
| Holdout methodology | Version 1 aggregate results documented separately; no new holdout evaluation or claim of independent Version 2 testing |
| Requirements | Twelve active report/inference dependencies, all installed at declared versions; `pip check` and offline install dry-run pass |
| Frozen artifacts | No model tuning, replacement model fit or historical result changes |

## Remaining warnings

1. **Statistical limits:** rare-class performance remains weak; repeated CV and across-study selection can be optimistic. Macro F1 describes the nested sampler-selection procedure, not separate validation of the exact fixed deployment recipe. There is no new independent Version 2 holdout result. These are documented limitations, not execution blockers.
2. **Installation scope:** a fresh package download/install and every operating system have not been independently tested. Use the pinned versions, especially NumPy/scikit-learn/joblib for serialization compatibility.
3. **Historical evidence:** archive files retain original code identities and absolute paths as historical records. Active report paths are portable; keep the complete evidence/archive tree when sharing. Do not execute archived research notebooks or include local virtual environments/caches in the submission bundle.

## Artifact locations

- [Final notebook](../../notebook/Wine-Quality-Classification.ipynb)
- [README](../../README.md) and [requirements](../../requirements.txt)
- [Final leaderboard](../final_leaderboard.csv)
- [Immutable champion summary](../final_version2_model_summary.csv)
- [Frozen model](../../models/final/wine_quality_classifier_v2.joblib), [metadata](../../models/final/wine_quality_classifier_v2.metadata.json), and [freeze lock](../../models/final/version2_freeze_lock.json)
- [Final plots](../../visuals/submission/)
- [Historical development archive](../../notebook/archive/Wine-Quality-Development-2026-10-16.ipynb)
- [Root execution](execution_root.json), [notebook execution](execution_notebook.json), [relocation execution](execution_relocated.json), and [static audit](static_audit.json)
- [Freeze validity audit](../version_2/freeze_verification/final_audit_report.md)

**Model development remains CLOSED.**
