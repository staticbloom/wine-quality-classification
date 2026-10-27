# Notebook editorial and reproducibility review

The wine notebook was reviewed from start to finish and cleaned into a complete
report of the already frozen study. It preserves all fourteen baseline family
sections, their results, comparisons, final evaluation, interpretation, packaging
and inference demonstration.

## Findings and corrections

- The previous preliminary benchmark cells created a fresh benchmark and would
  train again and overwrite historical tables during Run All. Other sections still
  contained training, search, packaging or evaluation entry points. Replaced these
  report calls with verified saved-result replay. Original experiment modules are
  preserved; the report now fails on missing/changed evidence rather than silently
  rerunning an experiment after model selection and final-test evaluation.
- Replaced fragmented current-status notes, future-phase placeholders and stale
  execution commentary with a completed-study narrative. Final limitations now
  describe actual rare-class failures, selection optimism, correlated folds,
  subjective ordinal targets, incomplete group provenance, unvalidated calibration,
  noncausal interpretation and environment-dependent runtime.
- Reduced code cells from 101 to 71 (184 to 157 total cells). Every code cell has
  explanatory markdown immediately before it. All code cells have at most 20 lines.
  There is one level-one title, level-two major sections and level-three subsections.
- Centralized baseline metric/per-class/runtime displays, artifact reads, figure
  display and warning summaries in the new reporting module. Repeated imports,
  progress cells and redundant family execution loops were removed. The fourteen
  preliminary results remain necessary evidence for the shortlist, not obsolete
  experiments. No historical artifact was deleted or modified.
- Tables use six significant digits and scroll rather than truncate. Missing values
  remain visibly unavailable. Small probabilities are not rounded to false zeros;
  HTML text is escaped and formatting does not modify data.
- Selection rationale remains Macro F1 first with the original explicit deterministic
  tie order. The narrative distinguishes preliminary ranking, bounded search,
  precision-collapse screening, repeated CV and the later holdout diagnostic.
  It acknowledges that final eligibility gates followed earlier development review.
- All 21 displayed figures were visually inspected for titles, axes, support/scope
  labels and readability. Their content was already suitable; notebook display
  widths were standardized and original PNG/PDF artifacts were preserved.

## Leakage, results and integrity checks

The report loads aggregate tables and existing figures; it does not parse the
source observation CSV or per-wine final-test prediction file. The once-only final
holdout diagnostic remains separate from development model-selection evidence.
Only the two pre-existing handwritten inference examples receive new predictions.

924 development aggregate means/standard deviations were independently reconciled
to saved fold metrics across preliminary benchmarking, selected tuning diagnostics,
imbalance experiments and final repeated CV. The preliminary shortlist and frozen
final ranking match the recorded rules. Final-test macro precision/recall/F1 and
rare-class statements match the saved classification report. Numeric champion and
interpretation claims were checked against source tables. No metric values were
fabricated or changed, and no model decision was revisited from test results.

Before/after SHA256 checks confirm all existing source modules, models, metadata,
selection/holdout records, dataset files, prior tables and figures remain identical.
The existing Telco notebook also remains identical. The new replay snapshot is an
additional integrity record, not authentication or proof of methodological validity.

## Tests and execution

- Four reporting unit tests passed: verified precision/missingness/read-only behavior;
  changed/missing/unregistered artifact and per-wine test-result rejection; separation
  of fold mean, fold SD and pooled OOF values; safe non-mutating formatting.
- A fresh Jupyter kernel executed all 71 code cells from the notebook directory with
  no cell errors. Temporary guards blocked training, resampling, dataset loading,
  experiment execution, packaging, interpretation generation and holdout evaluation.
- Prediction guards allowed exactly one label call and one probability call, each
  on the two handwritten example rows. No test wine was predicted.
- Notebook schema, Python syntax, heading hierarchy, unique headings, code-cell
  size, markdown coverage and the absence of inline helper definitions were checked.
- The notebook embeds 21 verified figures and records completed replay outputs.
  Report-body time excludes kernel startup and saving; historical experiment timings
  were not overwritten or relabeled as replay timings.

Command used for unit tests:

```bash
MPLBACKEND=Agg MPLCONFIGDIR=/private/tmp/wine-quality-mpl .venv/bin/python -m unittest discover -s tests -p 'test_reporting.py' -v
```

## Confirmed structural reference — 2026-10-12

The user clarified that the intended reference is `Telco-Churn.ipynb`. The earlier
filename ambiguity is resolved. Its cell ordering, heading sequence, paragraph
placement, code-cell lengths and output types were inspected read-only. No Telco
implementation, feature engineering, parameters, results or project-specific prose
were inspected for reuse or copied into the wine report.

The completed wine notebook already follows the reference's general storytelling
sequence, so this confirmation requires no further notebook changes:

| Reference presentation pattern | Wine report correspondence |
| --- | --- |
| Title, libraries, objective, metrics, analytical approach | Same introductory sequence, with original wine-specific content |
| Loading and cleaning followed by exploration and partitioning | Preserved; markdown explains that holdout reservation preceded development EDA |
| Shared preprocessing/validation utilities before separate preliminary models | Centralized modules and fourteen individually explained baseline sections |
| Preliminary comparison before final cross-validated selection | Preserved, with wine-specific tuning and imbalance sections between them |
| Final training/evaluation before final results and interpretation | Preserved, clearly replaying the frozen historical evidence |
| Packaging and reproducibility followed by limitations | Preserved, with runtime comparison and validated inference also documented |
| Explanatory markdown introducing code and displayed results | Every wine code cell has preceding explanatory markdown |

The wine report deliberately uses one title with nested section levels and keeps
helpers in `src`; it does not imitate the reference's large helper cell. Its code
cells are at most 12 lines. These choices satisfy the requested cleanup while
retaining the reference's overall presentation style.

Checks for this clarification: both notebooks passed nbformat schema validation;
markdown coverage, all fourteen wine baseline sections and maximum code-cell length
were checked; the saved report's evidence verification passed. SHA256 checks confirm
both notebooks remained unchanged. No training, prediction or test evaluation was
performed. Only `tables/notebook_review_report.md` changed in this follow-up.

Reference SHA256: `7ff69dd05b3ddfe06192d98f8db85e7eead71fa5744253d508c64f5aba6ed435`.

## Warnings

There is no outstanding reference-file issue.

Jupyter emitted a non-blocking local TCP transport encryption warning. Execution
completed successfully. There are no unresolved notebook execution failures.

## Files changed

- Updated: `notebook/Wine-Quality-Classification.ipynb`
- Updated: `README.md`
- Created: `src/wine_quality/reporting.py`
- Created: `tests/test_reporting.py`
- Created: `tables/notebook_report_manifest.json`
- Created: `tables/notebook_report_execution.json`
- Created: `tables/notebook_review_report.md`

Fresh-kernel verification completed at 2026-10-11T17:41:54.507391+00:00; wall time including kernel startup: 3.421570 seconds.
