# Final reproducibility and leakage audit

Audit date: 2026-10-12 (Asia/Dubai).

Dependency-file follow-up: the separate audit dependency snapshot was subsequently
consolidated into the single `requirements.txt` at the user's request and removed.
The historical file inventory below records the audit-time state; use
`requirements.txt` for current setup. No installed packages or frozen artifacts
were changed by this consolidation.

**Outcome: no detected train/test leakage, metric implementation defect or model
reload failure.** Eighteen requested checks passed; two passed only within the
current checkout/environment and retain portability/dependency limitations. All
126 tests passed. A fresh kernel executed all 71 wine notebook code cells with
21 embedded figures and no errors. This is verification of the completed report
and frozen evidence, not a new end-to-end training experiment.

The selected algorithm, predictors, preprocessing, imbalance treatment,
hyperparameters, fitted objects and final-test results were not changed. The
original wine notebook and read-only `Telco-Churn.ipynb` remain byte-identical.
No new final-test predictions or evaluations were performed.

## Requested checks

| # | Check | Result | Evidence |
| --- | --- | --- | --- |
| 1 | Duplicate leakage | PASS | 1,599 source rows; 240 redundant exact rows; 1,359 first occurrences exactly cover the locked split. Development/test have zero overlapping indices, full-row hashes or predictor-only hashes. All 1,359 retained predictor rows are distinct. |
| 2 | Learned preprocessing before splitting | PASS | `data.py:88` deduplicates before `partitioning.py:35–37` permits splitting. Cleaning validates schema/types; no learned imputation, outlier removal, scaling or feature construction precedes the split. |
| 3 | Scaling outside CV pipelines | PASS | `preprocessing.py:100–108` constructs unfitted scalers. `timing.py:155–169` clones and fits whole pipelines on training slices. The SVM calibrator wraps the full pipeline, so inner calibration preprocessing is also fold-local. |
| 4 | Resampling before CV | PASS | `imbalance.py:134–140` uses an imbalanced-learn pipeline. Sampling targets and SMOTE neighbor counts depend only on current training labels. The scaler fitted inside the tree SMOTE sampler is training-fold distance preprocessing; synthetic rows are transformed back before the tree fit. Validation/prediction does not call the sampler. |
| 5 | Test data in feature selection | PASS, with scope caveat | Original 11 predictors retained. All eight saved numeric EDA summaries reproduce from the 1,087 development rows. Initial source-wide integrity summaries predate partitioning; they include eventual test observations but are not feature-selection evidence. |
| 6 | Test data in tuning | PASS | Bounded searches use `development_xy`, frozen five-fold assignments, seed 42 and Macro F1 refitting. Saved tuning OOF records contain zero test IDs. |
| 7 | Test data in algorithm selection | PASS | Preliminary, imbalance and final OOF records contain development IDs only. Selection was locked before test access. Accuracy does not determine the rank; supporting metrics, variability and experiment name supply deterministic tie-breaking. |
| 8 | Target leakage | PASS | Feature construction explicitly selects the 11 expected chemical predictors. Input schema rejects `quality` as a feature. No target-derived feature or cross-partition feature duplicate was found. |
| 9 | Probability/class-label alignment | PASS | Six unique original classes are required and columns explicitly aligned. XGBoost maps quality 3–8 to internal 0–5 and restores original labels. Actual saved OOF probabilities are finite, bounded and normalized. |
| 10 | Multiclass ROC-AUC | PASS | Macro OvR with explicit six-class order agrees with an independent mean of six binary ROC-AUCs. Undefined classes yield explicit unavailable metrics rather than fabricated values. |
| 11 | Multiclass PR-AUC | PASS | One-hot class indicators and aligned probabilities produce macro average precision, independently verified per class. It is correctly identified as AP; it is not mislabeled trapezoidal PR area. |
| 12 | QWK | PASS | Fixed ordinal score order and quadratic disagreement match sklearn's quadratic weighted kappa. Undefined degenerate cases are explicit. |
| 13 | ±1 accuracy | PASS | Defined as mean of `abs(actual_quality - predicted_quality) <= 1` using original numeric scores. Independent artifact checks and edge-case tests agree. |
| 14 | Random states | PASS | Registry estimators, holdout, shuffled CV, calibration, sampling and randomized search consistently use 42 where supported. Deterministic algorithms need no seed. Hardware/library nondeterminism remains possible. |
| 15 | Reload saved models | PASS | All five candidates and the champion reloaded. Their label and probability predictions exactly reproduce saved 32-row development-feature probes, with unchanged fitted-state hashes and no scoring or refitting. |
| 16 | Notebook execution order | PASS | Outputs cleared and 71 original code cells executed sequentially in a fresh verified project interpreter from `notebook/`. Guards permit only two handwritten prediction examples and prohibit training, source loading and test inference. No hidden prior kernel state required. |
| 17 | Filesystem assumptions | PARTIAL | Config paths and report verification work from both root and notebook directories; no user-specific path is hard-coded in the source modules. Frozen experiment manifests nevertheless bind absolute checkout paths. Relocating the report is not currently supported. |
| 18 | Dependencies | PARTIAL | All installed distributions pass `pip check`, all 65 captured audit pins match, and all tests/report cells work. Declared `shap`, Jupyter metapackage and `pytest` are absent. The current workflow uses analytic linear SHAP, installed kernel/client components and unittest. A clean dependency installation has not been verified. |
| 19 | Required saved outputs | PASS locally | 43 required nonempty artifact files, including all six models and sidecars, verified. All 142 saved-report snapshot bindings and original phase integrity checks pass. Generated evidence is ignored by `.gitignore`; source-only distribution is insufficient. |
| 20 | Telco contamination | PASS | No Telco/churn implementation or narrative found in wine notebook source, modules or tests. README's intentional reference attribution is not contamination. Reference notebook checksum is unchanged; no reference code/results were used. |

## Independent checks of actual saved evidence

- Raw-row hashes confirm exactly the first-occurrence rows were split: 1,087
  development and 272 holdout observations. Predictor-only hashes were calculated
  without interpreting the quality token. No cross-partition duplicate was found.
- Original development folds reproduce exactly from the recorded seed/settings.
  Every OOF configuration/repetition covers development once, with recorded folds
  agreeing with regenerated assignments: 15,218 preliminary rows, 5,435 tuned rows,
  19,566 imbalance rows and 27,175 final repeated-CV rows.
- Independently recomputed all 11 metrics for 310 saved development validation
  folds: 70 preliminary, 25 tuning, 90 imbalance and 125 final. All **3,410 metric
  comparisons** agree within **3.33 × 10⁻¹⁶** across 67,394 OOF records. No new models
  were fitted for this check, and no per-row final-test results were parsed.
- All eight saved numeric EDA summaries agree with development-only recomputation
  at tolerance 1e-12.
- Selection lock time (2026-10-10 18:19 UTC) precedes test access (2026-10-11
  11:58 UTC). Existing final-test records specify one label call, one probability
  call, zero fits and no configuration change. These records are not proof against
  activity outside the project workflow, but no contradictory evidence was found.
- Model smoke checks used previously saved development features only. They verify
  persistence consistency, not predictive quality or a new test score.
- Before/after checks confirm every pre-existing file outside README,
  requirements and `.gitignore` is byte-identical: source modules, tests, raw data,
  locks, fitted models, metadata, historical tables/figures and both notebooks.

## Tests and fresh-kernel execution

Command run from the project root:

```bash
MPLBACKEND=Agg MPLCONFIGDIR=/private/tmp/wine-final-audit-mpl \
  .venv/bin/python -m unittest discover -s tests -v
```

**126 tests passed in 32.650 seconds; no failures or skips.** Coverage includes
all 14 registered classifiers on synthetic samples, deduplication, partition
integrity, scaler training statistics, fold-local resampling, probability mapping,
custom metrics, tuning, selection locks, synthetic once-only holdout recovery,
packaging, interpretation, inference, runtime and report integrity. Synthetic test
fits/evaluations are distinct from the frozen real-wine study.

The finished notebook verifier was run using:

```bash
MPLBACKEND=Agg MPLCONFIGDIR=/private/tmp/wine-final-audit-mpl \
  .venv/bin/python scripts/verify_notebook_replay.py
```

It clears old outputs, launches a fresh kernel, isolates Jupyter history/config
and Matplotlib cache in a temporary directory, verifies `sys.executable` and
`sys.prefix`, and executes from `notebook/`. Temporary guards block fitting,
resampling, experiment runners, source observation loading and holdout evaluation.
Exactly one label and one probability call are allowed on the two handwritten
example rows. Audit guards are removed from the delivered executed copy.

The kernel uses the existing verified Python 3.12.14 environment. **This is a
fresh kernel, not a newly installed dependency environment.** It replays the
frozen report; training/search histories are verified from existing evidence and
tested on synthetic data, not reproduced by rerunning the wine experiments.

`final_audit_notebook_execution.json` records the final successful run, timing,
interpreter, cell/figure counts and checksums. The executed audit copy contains
current execution metadata. The original notebook and prior notebook execution
record remain unchanged. The replay runner also passed Python syntax compilation.

## Failed checks and unresolved limitations

1. **Complete declared environment is not installed.** `shap`, the Jupyter
   metapackage and `pytest` are missing. This did not block any current test/report
   operation, but `pip check` alone does not certify that every requirements entry
   is installed. No environment upgrades were performed during this audit.
2. **Arbitrary relocation of frozen report evidence fails.** Locks and phase
   manifests directly dereference absolute paths (`selection.py:431–433`,
   `reporting.py:60–61`). Working-directory independence does not imply checkout
   relocatability. Silent hash/path rewriting would invalidate the historical
   provenance, so this audit does not attempt it. Model inference can accept an
   explicit package path and does not require the training CSV.
3. **No clean-install or cross-platform reproduction was performed.** The new
   pinned file captures the passing installed dependency closure, without wheel
   hashes or a tested package-index installation. Existing native boosting
   dependencies and strict model-version checks may constrain other machines.
4. **Statistical limitations remain.** Development CV includes selection bias;
   tuning and imbalance choices reuse development evidence. Precision-collapse
   eligibility gates followed earlier development inspection and were frozen
   before final repeated CV, not preregistered before all experimentation. Repeated
   folds are dependent and fold SD is not a confidence interval. No nested CV or
   external replication is claimed.
5. **Tiny classes and uncertain grouping.** The recorded final test has only two
   quality-3 and three quality-8 wines; both classes have zero recorded recall/F1.
   These existing diagnostics did not alter the model. Missing winery/batch/vintage
   identifiers prevent proving independence among related, nonidentical wines.
6. **Source-wide integrity summaries were intentionally generated.** The original
   dataset audit includes descriptive and class statistics for eventual holdout
   rows. All actual exploratory/model-selection evidence audited here is
   development-only; a claim that test source rows were never read would be false.
7. **Distribution and workflow controls.** Current artifacts all exist, but
   `.gitignore` excludes models/results/figures, and there is no Git repository in
   this checkout. Archive the complete evidence bundle separately. Checksums and
   once-only receipts detect workflow changes; they are not authentication or an
   operating-system access boundary. Only trusted joblib packages should be loaded.

Non-blocking warnings: joblib's sandboxed macOS physical-core detection fallback,
a seaborn/Matplotlib pending deprecation, and Jupyter's local TCP encryption warning.
The initial sandbox denied Jupyter socket creation; an approved local-socket rerun
completed. The replay runner was run again after improving the executed-copy
metadata, with the same guard restrictions. No test evaluation was repeated.

## Fixes made

- Added direct declarations for the actually used notebook/runtime tools
  (`nbclient`, `ipykernel`, `ipython`, `threadpoolctl`), and clarified unittest versus
  the optional pytest runner.
- Added `requirements-audit-lock.txt`, capturing 65 exact installed dependency
  versions, including all seven versions required by the model loader. This
  improves environment specification without changing the active environment.
- Added a reusable guarded fresh-kernel verifier that writes only separate audit
  outputs, asserts the project interpreter, preserves the frozen report and records
  execution provenance. Added `.venv-audit/` to ignore rules for the documented
  separate-environment setup.
- Updated README with the audited entry point, reproduction commands and explicit
  path/environment/evidence-distribution limits. No modeling fix was necessary or
  made; immutable source hashes and all six fitted model files remain unchanged.

## Final artifact locations

All paths below are relative to the project root.

| Artifact | Location |
| --- | --- |
| Main report | `notebook/Wine-Quality-Classification.ipynb` |
| Freshly executed audit copy | `tables/final_audit_executed_notebook.ipynb` |
| Champion and adjacent metadata | `models/final/wine_quality_classifier.joblib`, `models/final/wine_quality_classifier.metadata.json` |
| Locked selection | `models/final/selection_lock.json`, `models/final/selection_lock.sha256` |
| Five candidates and sidecars | `models/candidates/` — lda, logistic_regression, gaussian_nb, random_forest, gradient_boosting |
| Development selection | `tables/final_cv_model_selection.csv` |
| Existing final-test outputs | `tables/final_test_metrics.csv`, `tables/final_classification_report.csv`, `tables/final_test_predictions.csv` |
| Model registry and efficiency | `tables/model_registry.csv`, `tables/final_performance_runtime_comparison.csv` |
| Figures | `visuals/` |
| Audit evidence and 43-file inventory | `tables/final_audit_evidence.json` |
| Reload checks | `tables/final_audit_model_reload.json` |
| Execution record and logs | `tables/final_audit_notebook_execution.json`, `tables/final_audit_notebook.log`, `tables/final_audit_tests.log` |
| Current dependency file and verifier | `requirements.txt`, `scripts/verify_notebook_replay.py` |

## Files changed by this audit

Updated: `.gitignore`, `README.md`, `requirements.txt`.

Created: `requirements-audit-lock.txt`, `scripts/verify_notebook_replay.py`,
`tables/final_audit_report.md`, `tables/final_audit_evidence.json`,
`tables/final_audit_model_reload.json`, `tables/final_audit_notebook_execution.json`,
`tables/final_audit_executed_notebook.ipynb`, `tables/final_audit_notebook.log`,
`tables/final_audit_tests.log`.

No existing notebook, source module, test, dataset, model, lock or historical
result was changed. Disposable temporary files and Python caches are excluded.
