# Historical workflow before notebook migration

This document preserves the original study narrative and implementation notes. Package imports, source paths, test commands and old cell instructions below describe the previous layout and are **not current setup instructions**. Use [the current README](../README.md) and the self-contained notebook for setup, validation and replay. Frozen metrics, artifacts, model configurations and holdout policy were preserved during migration.

# Red Wine Quality

## Final reproducibility and leakage audit

See `tables/final_audit_report.md` for the 20-check audit, test results, fresh-kernel
execution record, artifact inventory and unresolved limitations. The audit preserves
the selected model, original notebook, Telco reference and all historical evidence.

`requirements.txt` is the single dependency file. It pins the 65 installed package
versions used to pass the tests and replay the report, including the model loader's
exact dependencies and notebook execution tools. SHAP, the Jupyter metapackage and
pytest remain additional unpinned tools because they were absent from the tested
environment. This is not a hash-locked or independently verified clean installation.
From the project root, a separate environment can be prepared with:

```bash
python3.12 -m venv .venv-audit
source .venv-audit/bin/activate
python -m pip install -r requirements.txt
python -m pip check
MPLBACKEND=Agg python -m unittest discover -s tests -v
python scripts/verify_notebook_replay.py
```

The replay verifier starts a fresh kernel from `notebook/`, clears previous outputs,
checks the interpreter, blocks training and test inference, and writes an executed
copy to `tables/final_audit_executed_notebook.ipynb`. It leaves the original notebook
untouched. This replays the frozen report; it does not reproduce the entire training
study from scratch or claim that a fresh dependency installation has been tested.

`requirements.txt` also includes optional SHAP, the Jupyter metapackage
and pytest, which were absent in the audited environment. Analytic linear SHAP,
installed Jupyter kernel/client components and standard-library unittest supported
the completed workflow. Do not upgrade the recorded model dependencies casually:
the saved-model loader deliberately rejects version mismatches.

Paths work from the root and notebook directories, but frozen experiment manifests
contain absolute paths to the original checkout. Moving the complete report requires
a separately designed manifest migration; silently rewriting the frozen hashes is
not supported. Inference accepts an explicit package path and does not need the
training CSV. Preserve the complete `data/`, `models/`, `tables/` and `visuals/` evidence
alongside the source: generated artifacts are ignored by `.gitignore`, so a future
source-only checkout cannot replay this study.

## Reading the completed notebook (current entry point)

`notebook/Wine-Quality-Classification.ipynb` is now a complete, executable report
of the frozen study. Restart the project kernel and run it top to bottom to replay
verified saved tables and figures. It does not retrain baselines, launch searches,
regenerate historical evidence, or re-evaluate the final holdout. Only the two
handwritten inference examples receive new predictions. Missing/changed artifacts
fail explicitly instead of reopening model selection.

`wine_quality.reporting.SavedWineReport` verifies the original selection lock,
phase manifests and `tables/notebook_report_manifest.json`; shared display helpers
keep numeric precision, per-class reporting and timing scopes consistent. The
notebook records report replay duration separately from the historical experiment
runtimes. The review execution record is `tables/notebook_report_execution.json`.

The phase-specific instructions below document the original implementation and
historical workflow; their old notebook-cell execution advice is superseded by this
completed report entry point. Original training/evaluation modules and all frozen
results remain unchanged. See `tables/notebook_review_report.md` for review findings,
checks, warnings and the changed-file list.


Predict red wine quality as an ordinal multiclass classification problem with
classes **3, 4, 5, 6, 7, and 8**. The target is `quality`, and **Macro F1** is the
primary model-selection metric because the dataset is imbalanced.

## Current scope

The project implements source loading, validation, exact-row deduplication, a
locked stratified holdout, development-only exploratory analysis, five-fold
validation, reusable evaluation/runtime utilities, model-specific pipelines, and
preliminary benchmarking of all 14 conservative classifier baselines on the same
five development-only folds. Fold means/standard deviations, pooled OOF metrics,
per-class reports and comparison figures are saved. Bounded hyperparameter tuning
is implemented for the five strongest preliminary families. Controlled class-imbalance
experiments now compare those fixed tuned configurations on development folds.
Final model selection now compares five frozen configurations with repeated
development CV and locks the chosen recipe. All five frozen family candidates are
now fitted on full development data and persisted, with an additional champion
package. The final-test section evaluates the locked champion once and saves diagnostic
results. Completed reruns verify and display cached outputs without new inference;
test results are never fed back into model selection.

## Layout

```text
data/wine-quality-red.csv
models/
    candidates/
    final/
notebook/
    Wine-Quality-Classification.ipynb
tables/
visuals/
src/wine_quality/
    __init__.py
    config.py
    data.py
    partitioning.py
    eda.py
    evaluation.py
    preprocessing.py
    modeling.py
    registry.py
    timing.py
    benchmarking.py
    tuning.py
    imbalance.py
    selection.py
    packaging.py
    holdout.py
    interpretation.py
    efficiency.py
    utils.py
tests/
README.md
requirements.txt
pyproject.toml
.gitignore
```

The CSV already resides in `data/`; setup preserves its original bytes. Treat it
as immutable source data and perform subsequent cleaning in memory or in separate
artifacts. `Telco-Churn.ipynb` is a read-only presentation reference. Its code,
feature engineering, parameters, text, and results must not be copied.

## Environment setup

Use Python 3.10 or newer. From the project root:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

The requirements install this project in editable mode using `pyproject.toml`.
Use the same environment for Jupyter and its notebook kernel. After installation,
imports work from either the project root or `notebook/` without `sys.path` edits.
Paths are resolved from the configuration file location, not the current working
directory. Keep the editable checkout available; a standalone wheel deployment
with external data is outside the current scope.

Run this from either directory to verify the source dataset:

```bash
python -c "from wine_quality.config import DATASET_PATH; assert DATASET_PATH.is_file(), DATASET_PATH; print(DATASET_PATH)"
```

In future notebooks:

```python
from wine_quality.config import DATASET_PATH, RANDOM_STATE, TARGET_COLUMN
```

The single `requirements.txt` pins the tested runtime dependency versions. The
additional SHAP, Jupyter metapackage and pytest entries are unpinned and unverified.
Native libraries such as gradient-boosting packages may require platform-specific
runtime dependencies. XGBoost, LightGBM, and CatBoost have now passed local
fit/predict integration checks; exact versions are recorded in
`tables/model_registry_environment.csv`. Other future dependencies remain unverified.

## Analysis rules for subsequent phases

- Investigate and remove exact duplicate rows before any development/test split.
  Initial read-only inspection found 1,599 rows and 240 redundant exact duplicates,
  leaving 1,359 unique rows. These are dataset counts, not model results.
- Reserve the final test set and leave it untouched until model selection is
  complete. Do not tune against it or revise the chosen model to improve its test
  performance after viewing the final evaluation.
- Fit scaling, resampling, oversampling, and other learned transformations only
  inside fold-safe pipelines. Never apply SMOTE or another resampler before
  splitting or cross-validation. Prevent leakage throughout the workflow.
- Select models by Macro F1. Supporting metrics are Balanced Accuracy, Quadratic
  Weighted Kappa, Macro Precision, Macro Recall, Macro ROC-AUC (One-vs-Rest),
  Macro Average Precision (One-vs-Rest), Accuracy, MAE of quality predictions,
  and accuracy within one quality point. Also report per-class precision, recall,
  and F1. Accuracy is not the primary selection metric.
- Fix supported random seeds to `RANDOM_STATE = 42`, record model and tuning
  runtimes, reuse package modules, and compute all model metrics from actual
  predictions. Never fabricate notebook results.
- Follow the reference notebook's structural style with original wine-specific
  explanations. Keep preliminary models, comparisons, final evaluation,
  interpretation, packaging, and limitations clearly separated.

## Data audit

After environment setup, run from either the project root or `notebook/`:

```bash
python -m wine_quality.data
```

The audit validates the exact predictor schema and expected quality labels, prints
source and cleaned summaries, and saves ten CSV tables under `tables/`:

- `dataset_shape.csv`, `dataset_columns.csv`, and `dataset_dtypes.csv`
- `descriptive_statistics.csv` and `missing_values.csv`
- `quality_unique_values.csv` and `quality_class_distribution.csv`
- `duplicate_groups.csv`, `data_cleaning_audit.csv`, and `data_provenance.csv`

Duplicate counts refer to surplus occurrences beyond the first row of each exact
full-row group. The audit additionally records repeated groups, their sizes, and
identical-feature groups with conflicting labels. Cleaning retains first-occurrence
indices and casts valid quality labels to integers without modifying the source.
Missing predictors and extreme values are preserved; missing/invalid targets and
nonnumeric or infinite predictors cause validation errors rather than silent fixes.
No cleaned CSV overwrites the original dataset.

Whole-source descriptive summaries are integrity records only. Subsequent EDA and
modeling decisions must use development data after a holdout is reserved. Audit
CSVs are generated artifacts ignored by Git and can be regenerated by the command
above. The provenance table records the source checksum and runtime versions.

Run the data-integrity tests from the project root after setup:

```bash
python -m unittest discover -s tests -v
```

The tests cover schema and target failures, preservation of extreme/missing values,
duplicate handling, conflicting labels, audit exports, and source-file integrity.

## Development-only exploratory analysis

Run the notebook from top to bottom in the project environment. After duplicate
cleaning, its initial EDA section reserves a stratified 20% holdout with seed 42.
`data/split_manifest.json` preserves source row assignments and source fingerprints.
Keep this manifest with the project: reruns reuse its partition and reject changes
to the source or split settings rather than silently establishing another holdout.
Only development observations are returned for exploration. No holdout feature
summaries or test metrics are generated by EDA.

The EDA modules create nine `tables/eda_development_*.csv` files: class distribution,
feature summary, grouped summary, Pearson and Spearman predictor matrices, pairwise
sample counts, quality associations, ranked predictor pairs, and provenance.
They include skewness, percentiles, and 1.5-IQR diagnostic flags. Flags do not remove
or clip observations. Correlations are exploratory associations, not causal effects
or fitted model feature importance. All 11 predictors remain available.

Six designs are exported as 300-dpi PNGs and vector PDFs under `visuals/`:

- `eda_class_distribution`: counts and percentages in one chart.
- `eda_feature_distributions`: full-range histograms for all predictors.
- `eda_features_by_quality`: alcohol, volatile acidity, sulphates, and three
  additional predictors chosen for display by development rank association.
- `eda_feature_correlations`: predictor-only Spearman heatmap.
- `eda_quality_associations`: Pearson and Spearman associations with ordinal quality.
- `eda_strongest_feature_pairs`: three strongest predictor pairs by rank association.

The notebook explains how these findings inform future fold-safe comparisons,
without choosing transformations or models. Figures are closed after saving and
the notebook displays the saved images. Figure/table files are regenerable artifacts
and are ignored by Git under the existing policy. The split manifest is not ignored.

Additional tests cover persistent split reuse, disjoint partitions, refusal of
unpartitioned EDA inputs, predictor/target separation, summary correctness, and
figure cleanup. Plotting and Jupyter execution dependencies have been verified for
this phase; the three boosting libraries are also verified by registry integration
tests. Other future modeling dependencies remain unverified.

## Locked partition and cross-validation

The original 80/20 stratified split is unchanged: 1,087 development rows and 272
final test rows. `data/holdout_lock.json` marks it **LOCKED** and binds the policy
to the exact split-manifest checksum. The holdout is excluded from feature
selection, hyperparameter selection, resampling decisions, and algorithm selection.
Only final evaluation after model/configuration selection is permitted. This is a
workflow integrity guard, not a filesystem access restriction; no test-loading or
unlocking API is implemented here. Do not delete or rewrite either manifest.

`development_xy` checks development membership and separates the 11 original
predictors from `quality`. `build_development_cv` returns a shared plan using
`StratifiedKFold(n_splits=5, shuffle=True, random_state=42)`. Its `splits` are
positional indices for that same development-frame order, suitable for sklearn
searches. Training/validation support and original validation row assignments are
saved in `tables/development_cv_class_support.csv` and
`tables/development_cv_validation_assignments.csv`.

Pass `n_repeats=3` to request an optional `RepeatedStratifiedKFold` robustness plan;
ordinary five-fold validation remains the default. Repeats are not independent
experiments. Classes 3 and 8 have only 8 and 14 development examples, respectively,
giving 1–2 and 2–3 validation examples per fold. Their metrics can therefore have
high variance. Report fold variability and class support; do not overinterpret
small score differences or change the holdout to obtain preferable results.

## Evaluation API

`wine_quality.evaluation` provides:

- `within_one_accuracy` and `quadratic_weighted_kappa` on the fixed quality scale.
- `align_class_probabilities`, requiring explicit probability-column class labels.
- `evaluate_predictions` for original quality labels and optional probabilities.
- `evaluate_estimator` for an already fitted estimator or pipeline, without fitting.
- `model_selection_scorer`, the fixed-six-class Macro F1 scorer for searches.

The evaluation result contains all requested metrics, raw and row-normalized
confusion matrices, per-class metrics/support, and complete sklearn classification
reports in dictionary and text form. Metric keys are `accuracy`, `macro_precision`,
`macro_recall`, `macro_f1`, `weighted_f1`, `balanced_accuracy`,
`quadratic_weighted_kappa`, `macro_roc_auc_ovr`, `macro_average_precision_ovr`, `mae`,
and `within_one_accuracy`. Macro F1 is the primary selection metric; accuracy alone
must never determine the chosen model.

Probability columns are reordered to `(3, 4, 5, 6, 7, 8)` using explicit
`probability_classes` or estimator `classes_`. All six must appear exactly once.
Encoded estimators need a supplied `class_mapping={encoded_label: quality_label}`;
when searching with the Macro F1 scorer, use an estimator adapter that already
returns original quality labels. Probabilities must be finite, nonnegative, no
greater than one, and sum to one within 1e-6 per row. The helper neither clips nor
normalizes invalid inputs and never fills missing class columns with zeros.

`evaluate_estimator` uses only `predict_proba`, including that of a classifier
calibrated inside training folds. Raw `decision_function` outputs are never used as
probabilities. Direct evaluation callers must supply genuine probabilities;
numerical validation alone cannot establish calibration quality. Probability
metrics are `NaN` with explicit `undefined_metrics` reasons when probabilities are
unavailable or any true class is absent. Invalid supplied probabilities raise.
Macro PR performance is reported as Average Precision, not trapezoidal PR-AUC.

Class precision/recall/F1 use `zero_division=0` with diagnostic notes for absent or
never-predicted classes. Macro metrics always include the fixed six-class universe;
balanced accuracy averages over true classes present, following sklearn. Missing
true classes produce zero rows in the normalized confusion matrix. Degenerate QWK
with zero expected disagreement is `NaN`, not a fabricated perfect score.

No model is trained by these utilities. Unit tests use synthetic labels/probabilities
and prediction-only estimator stubs to check ordinal calculations, probability
ordering, undefined-metric behavior, and the Macro F1 selection rule. Partition
tests verify locking, fold membership, reproducibility, and optional repeated CV.

## Model-safe preprocessing

`build_model_pipeline(estimator, model_family=...)` in `wine_quality.modeling`
returns an unfitted sklearn pipeline containing a fresh numeric preprocessor and
a clone of the supplied classifier. It preserves estimator hyperparameters and
discards previous fitted state. Candidate definitions must supply fixed random
seeds where supported; the factory does not select model settings.

The centralized policy in `wine_quality.preprocessing` uses StandardScaler for
`logistic_regression`, `knn`, `svm`, `gaussian_nb`, and `lda`. Scaling helps control
regularization/distance scales and numerical conditioning. For GaussianNB it also
changes the scale used by its global variance-smoothing term; for LDA the main
motivation is conditioning across units. These are implementation choices to
validate later, not claims of guaranteed predictive improvement.

`dummy`, `decision_tree`, `random_forest`, `extra_trees`, `gradient_boosting`,
`hist_gradient_boosting`, `xgboost`, `lightgbm`, and `catboost` use an explicit
scaler passthrough. The XGBoost policy assumes a tree booster; a linear booster
would need its own policy. The caller must choose the family matching the supplied
classifier. External model libraries are not imported merely to build preprocessing.
The complete design table is saved as `tables/preprocessing_policy.csv`.

Every preprocessor first checks the exact 11 named real-valued numeric predictors,
rejects the target and invalid columns/values, and returns a copy in canonical
feature order. The current source has no missing values. Missing inputs therefore
raise until an explicit fold-local imputation policy is introduced. No rows are
removed, values clipped, or features engineered. Named DataFrames are required at
training and prediction time, preserving feature identity and allowing reordered
input columns to be handled safely.

Pass the **whole pipeline and raw development predictors** to cross-validation or
search with `cv=cv_plan.splits` and the Macro F1 scorer. Never fit a preprocessor on
the full development frame before CV. Cloning by sklearn gives each training fold
its own scaler statistics; held-out rows use only that fitted transform. Estimator
parameters remain addressable as `model__...`, such as `model__C`. If calibration
is introduced later, it must wrap the complete pipeline inside training folds.
Resampling is introduced only by the explicit imbalance experiment factory below;
the baseline registry and its preprocessing policies remain unchanged.

`tests/test_preprocessing.py` uses synthetic inputs and a recording classifier to
verify fold-local means/variances, unchanged scaler state during validation,
independent clones, unscaled value preservation, and rejection of target leakage.
These synthetic probes do not train or select models on wine data. The notebook
now applies these pipelines separately inside each development benchmark fold.

## Baseline model registry

Use `registered_model_names()` and `build_model(name)` from `wine_quality.registry`
to construct any of the 14 baselines through one API. Every returned classifier
supports sklearn cloning, `fit(X, y)`, `predict(X)`, `predict_proba(X)`, and the
existing Macro F1 scorer. Factory construction never fits data.

```python
from wine_quality.registry import build_model

candidate = build_model("xgboost")  # Fresh, unfitted, complete estimator.
```

The public `QualityLabelClassifier` wraps the full preprocessing/model pipeline.
It requires all six quality classes in each training sample, validates original
labels, and exposes `classes_ = [3, 4, 5, 6, 7, 8]`. XGBoost receives the fixed
encoded labels 0–5 internally, with `multi:softprob`, six classes, and `mlogloss`.
Its fitted `label_mapping_` and `inverse_label_mapping_` preserve both directions.
Predictions are decoded automatically, including during sklearn search scoring;
callers should not apply a second inverse mapping. CatBoost predictions are
flattened to one-dimensional integer quality labels. Probability columns are
validated and aligned explicitly for every model.

All baseline models are **unweighted with no resampling**. This avoids giving a
candidate undisclosed imbalance treatment. `tables/baseline_model_registry.csv` records
each classifier's parameters, scaling, objective, label mappings, probability
method, and `imbalance_treatment`. Copy that metadata into later performance
comparisons. Weighted/resampled variants must be explicitly distinguished and
record their actual parameters; the registry table describes unmodified baselines.

Supported seeds are 42. Forests use 100 estimators, and boosters use 100 stages or
iterations with conservative depth/leaf controls; multiclass boosting can create
multiple trees per stage. Third-party models use one worker/thread where supported,
quiet training parameters, and no CatBoost training-file output. HistGradientBoosting
uses a fixed budget with early stopping disabled, avoiding another small validation
partition. GaussianNB and LDA retain empirical class priors.

RBF SVC probability support uses sigmoid `CalibratedClassifierCV(ensemble=False)`
with three shuffled stratified inner folds, seed 42. Calibration wraps the **whole
SVC pipeline**, so scaling is fitted only on each inner training fold as well as
being isolated from outer validation. This also avoids the native SVC probability
option deprecated in the installed sklearn version. Allow at least three examples
of every class in an SVC training sample. Include its extra calibration fits in
runtime comparisons; this is probability support, not class-imbalance treatment.

Registry model parameters use `estimator__model__...`; SVC's calibration adds one
level, `estimator__estimator__model__...`. These prefixes are recorded in the table.
The lower-level `build_model_pipeline` API still accepts custom classifiers and
retains its existing `model__...` parameter paths. Optional external libraries are
loaded only for the requested model; a missing dependency raises a clear error.

`tests/test_model_registry.py` fits every baseline on 144 synthetic training rows
and checks prediction/probability output on 36 separate synthetic probe rows.
It also verifies Macro F1 scoring, explicit mapping, and XGBoost joblib round-trip
behavior. `tables/model_registry_smoke_tests.csv` records these checks and measured
fit/prediction runtimes under a one-thread test profile; they are not wine benchmark
scores or evidence for model selection. Each fitted wrapper additionally records
`fit_seconds_`. No actual model-performance values are hardcoded in the notebook.

## Standardized runtime tracking

`wine_quality.timing` uses `time.perf_counter()` for every duration. All duration
fields are seconds except those explicitly named milliseconds per sample. Runtime
supports interpretation; **Macro F1 remains the primary selection metric**.

| Measurement | Field and scope |
| --- | --- |
| Total CV | `cv_total_seconds`: complete sequential outer CV, including cloning, slicing, training, predictions, and metrics |
| CV fitting | `cv_fit_mean_seconds`, `cv_fit_std_seconds`: complete pipeline fit per fold; population SD (`ddof=0`) |
| CV scoring | `cv_score_mean_seconds`: validation prediction, probabilities, alignment, metrics, and reports; excludes fit |
| Search | `search_seconds`: complete search `.fit`, including scheduling and optional search refit |
| Final fit | `final_fit_seconds`: separately measured complete pipeline fit after selection is frozen |
| Final prediction | `final_prediction_seconds`: one label-prediction batch, including transforms; excludes probability prediction and metric computation |
| Prediction cost | `final_prediction_ms_per_sample`: final label-prediction seconds × 1000 / batch rows |
| Serialization | `serialization_seconds`: joblib file open/write/close including compression; excludes directory creation and file stat |
| Artifact size | `serialized_size_bytes`: actual saved file size in bytes |
| Notebook | `notebook_total_seconds` in `tables/notebook_runtime.csv`: first-to-last code-cell wall time |

`measure_call`, `timed_fit`, `timed_predict`, `timed_search`, and `timed_serialize`
are reusable building blocks. Fit/prediction helpers use generic fields unless
`final=True` is supplied. `evaluate_estimator` now attaches a `runtime` dictionary
to its returned `EvaluationResult`, separately recording label prediction,
`probability_prediction_seconds` (if available), and complete `scoring_seconds`.
Evaluating already-produced predictions leaves timing empty. Training time is
never included in prediction time. Batch milliseconds/sample is throughput cost,
not a measured isolated single-row request latency.

`timed_cross_validate` takes the **complete, unfitted estimator and raw development
X/y**, plus `cv=cv_plan.splits` or a stratified/repeated splitter. It clones the
estimator per fold, retaining each fold's metrics, reports, and timings together.
It returns mean metrics, metric standard deviations, and aggregate runtime. An
undefined fold metric propagates into its aggregate rather than being silently
excluded. Outer folds run sequentially; model-internal parallelism is unchanged.
The existing wrapper's `fit_seconds_` measures its inner pipeline; CV/final fit
timers cover the public complete `.fit` call, including the label adapter.

`tables/model_runtime_comparison.csv` contains the preliminary development CV
measurements. `ensure_runtime_table()` preserves existing records across runs.
Save evaluations with `record_model_result`, for example after an authorized CV run:

```python
record_model_result(
    model_name, cv_result, run_id=notebook_run.run_id, phase="development_cv",
    imbalance_treatment="none", parameters=candidate.get_params(deep=True),
)
```

For a final evaluation, pass separately measured final fit, search and artifact
timings through the `runtime` argument. Use distinct model variant names and
phases for experiments. Missing stages remain blank. Reusing a model/run/phase
identity raises instead of silently overwriting prior results. In-memory results
retain complete reports; the comparison CSV stores scalar predictive metrics and
runtime together. These helpers do not read, unlock or select against the holdout.
They never serialize a model automatically; serialization refuses existing paths.
`visuals/model_runtime_comparison.png` now plots measured preliminary fit and
scoring times separately. Tuned-candidate rows additionally record search duration.
Final-fit, final-prediction and serialization fields remain blank until those later
phases are performed.

Runtime scopes overlap: total CV contains its fold fits and scoring, and scoring
contains prediction. **Do not sum nested measurements.** Search refit is not a
separately measured final fit. Native sklearn search timing columns are not used
as standardized `perf_counter` fold measurements. Search configuration must use
the existing Macro F1 scorer/refit policy and only development data.

Each comparison row includes model parameters, imbalance treatment, platform,
logical CPU count, Python/core package versions, native thread pools and thread
environment settings. Parallel algorithms can show different wall-clock behavior
on different hardware. Core counts, configured workers, BLAS/OpenMP settings,
concurrent load, caches and disk speed all affect measurements. Compare equivalent
workloads under the same machine/thread profile; these durations are not CPU time
or guarantees about production latency. Standardized CSV writes assume one writer.

The first notebook code cell starts `NotebookRun` before project imports, and the
last finishes it. Restart the kernel and run all cells uninterrupted for a valid
top-to-bottom duration. It includes imports, displays, I/O and execution gaps;
it excludes kernel startup, the initial timer import, final timing-file write and
notebook saving. Interactive pauses inflate it. Each start gets a new run ID;
interrupted runs remain `started` with no completion duration. Finishing twice
raises. The recorded duration describes the notebook's currently implemented
work, not future training placeholders.

`tests/test_timing.py` uses synthetic inputs, mocked clock boundaries and temporary
artifacts to verify separate scopes, CV aggregation and fold isolation, search,
prediction normalization, serialization size/round-trip, preservation of results,
missing-value handling and notebook run lifecycle. No wine models are trained by
these tests.

## Preliminary development benchmark

Run `notebook/Wine-Quality-Classification.ipynb` from a fresh kernel, top to bottom.
Each preliminary model section calls `PreliminaryBenchmark.run_model(name)` and
displays that model's fold summaries, pooled OOF metrics, per-class results and
runtime. Implementation is centralized in `benchmarking.py`, `timing.py` and
`evaluation.py`. Re-executing a model cell reuses its result in the current run;
starting a fresh notebook run benchmarks every model again with a new run ID.

The benchmark validates membership in the locked development partition before
fitting: 1,087 rows, five shuffled stratified folds, seed 42. Registry parameters
remain unchanged, including no class weighting or resampling. Model-specific
scalers are fitted only to the current training fold; SVM calibration wraps the
entire pipeline inside three additional training-only folds. Candidates and outer
folds run sequentially, with native thread pools limited to one. Imports and
plotting/export work are outside per-model CV time, while pooled OOF metric
computation is included in total CV time. Thread and package details are recorded
in `tables/preliminary_benchmark_metadata.json`.

`timed_cross_validate(..., collect_oof=True)` retains one prediction and six
explicitly ordered probability columns for every development observation. It
rejects incomplete or repeated validation coverage in this mode. Generic repeated
CV remains available without OOF collection. Source row IDs and fold assignments
in the exports permit direct verification that no test row contributed to a score.

`tables/preliminary_model_comparison.csv` has `_mean`, `_std` and `_oof` columns for
all eleven metrics. The mean averages folds equally; SD uses `ddof=0`. Pooled OOF
metrics evaluate concatenated held-out predictions and can differ from fold means
because metrics are nonlinear. Pooled probability metrics additionally compare
probabilities from different fitted fold models; use them as supplemental context.
Average Precision is the PR summary, not trapezoidal PR-AUC. All 14 registered
models supplied valid probabilities in the recorded run, and no training warnings
were captured.

The leaderboard sorts by mean Macro F1, with exact ties resolved by Balanced
Accuracy, then QWK, then model name. Accuracy and runtime never enter ranking.
`tables/preliminary_shortlist.csv` contains the first five families. In the recorded
run these are Gaussian Naive Bayes, LDA, Logistic Regression, Gradient Boosting and
Random Forest. This is a tuning shortlist, not a final model decision. Gaussian
Naive Bayes leads Macro F1, while LDA has higher QWK and Random Forest has higher
accuracy; that illustrates why the ranking must not default to accuracy.

Rare-class performance remains weak: development class 3 has only eight rows and
class 8 only fourteen. Across these baselines, the largest pooled recall is 0.25
for class 3 and 1/14 for class 8. Gaussian Naive Bayes is the only baseline that
correctly predicts any class-8 observation in this run. The top two Macro F1 means
are close relative to their observed fold variability. Fold SD is not a confidence
interval, and neither this comparison nor the shortlist demonstrates statistical
superiority. Comparing many baselines on shared development folds adds selection
optimism. These preliminary results predate the tuning phase below; the holdout
remains unevaluated.

Additional evidence is saved as `preliminary_fold_metrics.csv`,
`preliminary_oof_predictions.csv`, `preliminary_per_class_metrics.csv`,
`preliminary_per_class_fold_metrics.csv`, `preliminary_oof_confusion_matrices.csv`,
`preliminary_classification_reports.json` and `preliminary_warnings.csv`, all in
`tables/`. Full and row-normalized confusion matrices use original quality labels.
Reports retain undefined-metric reasons and never-predicted class notes. Latest
complete benchmark exports are replaced on a new completed run; the standard
runtime and notebook-duration logs preserve separate run IDs.

Five figures are exported as 300-dpi PNG and vector PDF under `visuals/`: Macro F1,
Balanced Accuracy, QWK, performance versus mean fit time, and separate runtime
comparison. Metric error bars show fold SD. Figures retain Macro F1 ranking even
when displaying supporting metrics, and all figures are closed after saving.

## Bounded tuning of the shortlisted families

`wine_quality.tuning.ShortlistTuner` reads the saved preliminary leaderboard and
selects its first five families using mean Macro F1, with the same supporting
tie-breaks as the benchmark. It verifies the source checksum, development-row
fingerprint, split lock and exact five-fold assignments against the preliminary
metadata. A changed shortlist without matching search spaces fails explicitly.

`load_locked_development()` in `partitioning.py` supports this phase without
rerunning source audits. It hashes immutable CSV bytes for integrity, then passes
only the header and previously assigned development-row bytes to pandas. The
wine source has one numeric observation per line. Test labels and removed duplicate
rows are never parsed, summarized or exposed. The established split and deduplication
decisions are reused unchanged. The notebook tuning section can run independently
using this loader; prior source-audit and benchmark cells need not execute again.

Search settings are fixed before observing tuning scores:

| Model | Configurations evaluated | Parameters varied |
| --- | ---: | --- |
| Gaussian Naive Bayes | 12 | `var_smoothing`, log-spaced range 1e-11 to 1e-2 |
| LDA | 9 | Baseline SVD, or LSQR with no/automatic/bounded covariance shrinkage |
| Logistic Regression | 16 | L2 regularization strength `C`, log-spaced range 1e-3 to 100 |
| Gradient Boosting | 20 | 50–150 stages, learning rate 0.03–0.1, depth 1–3, minimum leaf 2–10, subsample 0.8 or 1 |
| Random Forest | 20 | 100/200 trees, bounded or unrestricted depth, minimum leaf 1–8, feature subsampling |

`ParameterSampler` selects unique combinations with seed 42 and includes the
original baseline explicitly. `RandomizedSearchCV` then evaluates the sampled
singleton subspaces once each; the nine small legal LDA configurations are all
evaluated. The full sampled plan is saved before the first fit as
`tables/hyperparameter_search_plan.json`. No budget, parameter space or candidate
family is expanded in response to scores. Registry baselines remain unchanged.
No class weighting, resampling, feature selection or early stopping is introduced.

The only search scorer is the fixed-six-class Macro F1 scorer, and
`refit="macro_f1"` governs selection. Every candidate includes its whole pipeline,
so StandardScaler is fitted separately inside each training fold. Candidates and
models run sequentially with `n_jobs=1` and native thread pools limited to one.
Invalid fits raise rather than silently giving incomplete searches favorable ranks.
Warnings are captured in `tables/hyperparameter_tuning_warnings.csv`.

There are **77 candidate configurations × 5 folds = 385 search CV fits**, plus one
automatic full-development refit for each family (390 search fits including refits).
After each best configuration is selected, it is cloned into five fresh fold fits
to record the complete metric suite, timings and OOF predictions. These 25 diagnostic
fits bring the total to **415 estimator fit calls**. Counts describe whole-pipeline
fits, not individual trees. The refitted candidate is not a final model decision and
is not evaluated on training rows or the test set.

`search_seconds` measures the complete search and automatic refit with
`perf_counter()`, excluding the subsequent diagnostic CV. Separate `cv_total_seconds`
and per-fold fitting/scoring durations describe that diagnostic pass. No native
sklearn search timing field is substituted for the standardized wall-clock timings.
Hardware/thread context is saved with the results and affects comparisons.

The required outputs are `tables/hyperparameter_tuning_results.csv` and
`tables/best_parameters_by_model.csv`. They include candidate counts, CV folds,
search/diagnostic/total fit counts, search runtime, best parameters and best CV
Macro F1. Supporting diagnostics include Balanced Accuracy, QWK, macro OvR Average
Precision, macro OvR ROC-AUC, accuracy, MAE and ±1 accuracy, plus the remaining
predefined metrics. Means, population SDs and pooled OOF values are retained.
Search details are in `tuning_search_candidates.csv`; selected configurations have
fold metrics, OOF predictions, per-class metrics and complete classification reports
in `tuned_selected_*` files. `hyperparameter_tuning_metadata.json` preserves the
search plan, benchmark provenance and measured execution environment.

These are **selection-biased development diagnostics**: although each prediction
comes from a model fitted without that row, hyperparameter selection has already
used every validation fold. Repeating the selected configuration on the same folds
does not make it nested CV or provide an unbiased generalization estimate. Rare-class
support and selection optimism remain limitations. No final test labels were
inspected, no final model was frozen, and no final artifacts were packaged.

For this phase, execute only the marked tuning section to preserve existing
benchmark outputs and avoid re-running full-source audits. A section-only run leaves
the previous whole-notebook duration unchanged; new search timings are recorded
under a separate run ID linked to the preliminary run. A later full top-to-bottom
execution will include tuning in the notebook-body timer.

## Controlled class-imbalance experiments

`wine_quality.imbalance.ImbalanceExperiments` uses `load_locked_development()` and
verifies the tuned parameter exports, run identity, source/development fingerprints
and exact CV folds. It freezes the five tuned configurations; it performs no new
search, feature selection or final-model refit. Every original-distribution condition
must reproduce all tuned reference metric means before differences are interpreted.

The predeclared plan has 21 rows: **18 evaluated conditions × 5 folds = 90 fits**,
plus three explicitly unsupported weighting combinations:

- Original training distribution for LDA, Gaussian NB, Gradient Boosting, Logistic
  Regression and Random Forest.
- `class_weight="balanced"` for Logistic Regression and Random Forest only. LDA,
  Gaussian NB and Gradient Boosting have no such parameter; no alternate prior or
  sample-weight policy is silently substituted.
- RandomOverSampler and SMOTE for all five families, each inside an imbalanced-learn
  Pipeline between fold-safe preprocessing and the classifier.
- Optional BalancedRandomForestClassifier using the tuned Random Forest's shared
  tree settings, explicitly setting `sampling_strategy="all"`, `replacement=True`,
  `bootstrap=False`, `class_weight=None`, seed 42 and one worker. This is a specialized
  internally undersampled ensemble, not the same intervention as oversampling.

ROS and SMOTE use the same **partial, capped oversampling** rule. Inside each
training fold, each targeted class grows to the smaller of three times its original
count or half the largest training-class count (rounded up), and only if that is an
increase. Thus qualities 3 and 8 are not inflated from a handful of examples to
hundreds. The rule is computed from training labels alone; no validation/test rows
are synthesized or replicated. Balanced weights and the specialized forest apply
stronger balancing than this capped policy; the results compare these particular
interventions, not all possible balancing strengths.

`FoldSafeResampler` exposes only `fit_resample`, so the imbalanced-learn pipeline
skips it during prediction. For SMOTE, k is the smaller of three and one less than
the smallest eligible targeted training-class count. Targeted singleton classes
are explicitly skipped while other eligible classes can still be sampled. All
actual before/after counts, chosen k, skipped classes and native sampler types are
captured from fitted models through the CV helper's training-only audit callback.

Linear/Gaussian models retain their training-fold StandardScaler before sampling.
Tree SMOTE fits a scaler inside the sampler solely for neighbor distances, then
inverse-transforms synthetic outputs and preserves original rows exactly, leaving
the classifier and validation data in original units. Tree ROS does not scale.
No learned transformation is fitted to a complete development frame before CV.

Quality 3 has only 6–7 original examples per training fold; quality 8 has 11–12.
Feasible SMOTE neighbors do not establish statistical adequacy. Interpolation can
replicate noise, overfit these tiny groups or create implausible physicochemical
combinations. ROS duplicates likewise add no independent evidence. BalancedRandomForest
draws only 36–42 observations per tree here (six classes times the rarest fold
support); per-tree draw sizes and counts are audited. Changed training class priors
can also impair probability calibration at natural prevalence; no recalibration
or decision-threshold tuning is performed in this phase.

`tables/class_imbalance_experiments.csv` records all evaluated/skipped conditions,
all predefined metric means/SDs and pooled OOF scores, per-class precision/recall/F1,
runtime and paired fold deltas relative to each model's original distribution.
Macro F1 is primary; Balanced Accuracy, QWK, macro Average Precision, precision and
class-level F1 explain minority-class tradeoffs. Accuracy is context only. Fold SD
and paired deltas are descriptive, not confidence intervals or significance tests.

Before fitting, three review flags are fixed: macro precision falls by at least
10 percentage points, any pooled class precision falls by at least 20 points, or
a class gains recall while its pooled precision is below 10%. These flags are
transparent review prompts, not universal acceptability cutoffs or automatic
strategy-selection rules. Per-class predicted counts help distinguish missing
predictions from many false positives. **No final imbalance strategy is selected.**

Additional `class_imbalance_*` outputs retain the plan, SMOTE feasibility, complete
per-fold and per-class metrics, OOF predictions/probabilities, fitted-sampler audits,
classification reports, warnings and environment metadata. Standardized runtimes
are appended to `model_runtime_comparison.csv`. Models/folds run sequentially with
native thread pools limited to one; wall time depends on hardware and workload.
Read exported probability CSVs with `pd.read_csv(path, float_precision="round_trip")`
when reproducing ROC-AUC or Average Precision. The default CSV parser can perturb
nearly tied scores and slightly change rank-based metrics.

The executed findings and verification record are in
[`tables/class_imbalance_run_report.md`](tables/class_imbalance_run_report.md).
LDA with capped SMOTE leads mean Macro F1 in this run, but its quality-8 precision
remains below 10% and QWK declines. Random oversampling helps Gradient Boosting and
Logistic Regression on Macro F1; balanced Logistic Regression and the balanced
forest gain recall while losing Macro F1. These outcomes support comparing the
full precision/recall tradeoff, not adopting a treatment from recall alone.

Nine synthetic tests in `tests/test_imbalance.py` check capped targets, adaptive
SMOTE and singleton handling, preservation of feature names and original units,
training-fold-only fitting, prediction-time sampler bypass, explicit weighting,
valid quality-label probabilities and complete experiment exports. They do not
read real wine labels. Run only this test module with:

```bash
python -m unittest discover -s tests -p 'test_imbalance.py' -v
```

The notebook's imbalance section is independently runnable and does not rerun
historical source audits, baseline fitting or tuning. Earlier full-notebook timing
remains the previous full-run measurement. Reusing previously selected parameters
and shared development folds makes these comparisons selection-biased; no final
test labels are parsed or evaluated. The next selection phase requires its own
authorization.

## Final development-CV selection and configuration lock

`wine_quality.selection` takes one fixed tuned configuration from each shortlisted
family. Before new CV, it applies explicit precision-collapse eligibility gates:
a macro-precision decrease of at least 10 percentage points, or a pooled precision
decrease of at least 20 points for any quality, relative to that family's original
distribution. These are **new final-selection gates** derived from prior review
flags and observed development evidence. Low absolute precision remains a warning.
The best eligible configuration is chosen by prior Macro F1, Balanced Accuracy,
QWK, macro OvR Average Precision, macro OvR ROC-AUC, lower fold Macro F1 SD, then
canonical experiment ID. This preserves Logistic Regression with ROS instead of
its higher-Macro-F1 SMOTE variant, whose quality-3 precision severely deteriorates.

The fixed representatives are LDA with capped SMOTE, Gaussian NB without resampling,
Gradient Boosting and Logistic Regression with capped RandomOverSampler, and Random
Forest with balanced class weights. All tuned parameters and complete estimator
defaults are recorded before fitting in `tables/final_cv_plan.json`. The plan also
hashes prior evidence, implementation code, the split and source data. Code,
dependencies or evidence changing during the run cause a failure.

Five repetitions of five-fold `RepeatedStratifiedKFold` use seed 42: **125 fits**
for five candidates. The first repetition is asserted to match the original
five-fold CV and reproduce its metrics. Each repetition retains a separate,
exactly-once OOF prediction for every original development row. No probabilities
are averaged into an ensemble score. Fold training contains every learned
preprocessing or resampling step; validation rows remain unchanged.

`tables/final_cv_model_selection.csv` ranks mean validation-fold **Macro F1** over
all 25 folds, then mean Balanced Accuracy, QWK, macro OvR Average Precision and
macro OvR ROC-AUC. Further ties use lower SD of repetition-level mean Macro F1,
lower fold Macro F1 SD, then alphabetical experiment ID. Numeric tie keys are
rounded to 12 decimal places. Accuracy is context only. Runtime is reviewed and
reported but cannot change the result through machine timing noise.

The CSV retains all metric means/SDs, separate repetition-level OOF means/SDs,
per-class precision/recall/F1, MAE, ±1 accuracy and timings. Supporting `final_cv_*`
files retain eligibility decisions, fold membership/support, predictions,
probabilities, class reports, fitted-sampler audits, warnings and environments.
`visuals/final_cv_model_comparison.png` compares Macro F1, Balanced Accuracy, QWK
and fit duration. Figures are closed after saving. Dependent fold SDs are
descriptive, not confidence intervals. Reusing previously tuned configurations and
development evidence remains selection-biased even with repeated stratification.

`lock_final_selection()` exclusively creates `models/final/selection_lock.json`
and its `.sha256` checksum after all outputs are complete. It records the selected
algorithm, all preprocessing and sampler settings, every estimator parameter,
feature schema, original quality mapping, exact package versions and code/evidence
checksums. `verify_selection_lock()` verifies these records, and
`build_locked_model()` returns an **unfitted** reconstruction only if its complete
configuration matches. No full-development final fit or test evaluation occurs
in this phase. The APIs refuse overwrite or renewed selection after locking.

Run only the notebook's marked final-CV section to preserve prior audit and model
artifacts. After locking, rerunning that section verifies and displays saved
evidence without fitting. Earlier sections that regenerate hashed evidence should
not be rerun after lock. Preserve the lock, checksum and evidence together at
their recorded paths; accidental changes or relocation fail closed. These are
workflow integrity guards, not filesystem security controls. The lock is kept
eligible for version control despite generated model artifacts being ignored.
Never revise this recipe to improve observed final-test performance.

The completed run locks **LDA with StandardScaler and capped SMOTE**, using
`solver="lsqr"` and `shrinkage=0.8`. Mean repeated-CV Macro F1 is **0.3774**;
Balanced Accuracy is **0.4057** and QWK **0.5264**. Mean pooled quality-8 precision
remains only **12.9%**, so this selection does not establish rare-class reliability.
Full results, execution accounting, checks and the changed-file inventory are in
[`tables/final_cv_run_report.md`](tables/final_cv_run_report.md).

Run the synthetic selection checks without reading real wine labels:

```bash
python -m unittest discover -s tests -p 'test_selection.py' -v
```

## Persistent fitted candidates and champion package

`wine_quality.packaging.fit_and_package_locked_models()` verifies the existing
selection lock, reconstructs each of the five family specifications from the
lock-bound final-CV plan, and fits each complete pipeline once on the 1,087 locked
development observations. It uses the selected imbalance treatments without
retuning. No test labels, features, predictions or metrics are used in this phase.

Saved candidate files are `gaussian_nb.joblib`, `lda.joblib`,
`logistic_regression.joblib`, `gradient_boosting.joblib` and `random_forest.joblib`
under `models/candidates/`. The already fitted LDA candidate is additionally saved
as `models/final/wine_quality_classifier.joblib`; it is not fitted a second time.
Unshortlisted model families receive no files.

All six joblib bundles have the same keys: `format_version`, `pipeline`, and
`metadata`. The pipeline includes fitted preprocessing, sampling and classifier
state. Embedded metadata includes the full frozen estimator configuration and
hyperparameters, original quality classes/probability order, target, feature schema,
seed, timestamp, source filename/checksum, development-CV performance, training
audit, library versions and code fingerprints. Every bundle has an adjacent
`.metadata.json` file with matching metadata plus checksum, file size, serialization
duration and reload-verification results.

The project environment must be installed before loading these trusted artifacts:

```python
from wine_quality.config import FINAL_MODELS_DIR
from wine_quality.packaging import load_model_package

package = load_model_package(FINAL_MODELS_DIR / "wine_quality_classifier.joblib")
pipeline = package["pipeline"]
# measurements is a DataFrame with all 11 original named numeric predictors.
predictions = pipeline.predict(measurements)
probabilities = pipeline.predict_proba(measurements)
quality_order = package["metadata"]["probability_class_order"]
```

The loader verifies the file before deserialization and checks embedded metadata,
dependency versions and project code. Inference does not require the original
CSV or CV result tables. Keep each joblib and its metadata sidecar together. Only
load trusted joblib files; checksums establish integrity, not authenticity.

`tables/model_registry.csv` now lists the five **fitted** candidates, including
their paths, algorithm, complete model parameters/configuration, locked CV Macro
F1/Balanced Accuracy/QWK, measured fit time, file size and champion flag. The old
14-model baseline table is archived byte-for-byte as `baseline_model_registry.csv`.
No CV results are recomputed or replaced by training-set scores.

All six artifacts are reloaded and checked on the same 32 evenly spaced development
feature rows chosen without targets. Predictions and probabilities must exactly
match before/after serialization. Inputs and results are retained in
`model_artifact_probe_features.csv` and `model_artifact_predictions.csv`; measured
load/prediction timings are in `model_packaging_round_trip.csv`. These are smoke
checks, not performance evaluations. Final-test prediction timing remains blank.

Fit, prediction and serialization times stay separate. Five candidate runtime
records contain measured fit time; the champion packaging record has no extra fit.
For the champion candidate, `fit_seconds` and `final_fit_seconds` describe the same
fit and must not be added together. The standard runtime table retains locked CV
metrics alongside these timings, explicitly labeled as prior development evidence.

Artifacts are checked in staging before publication. Existing files cannot be
overwritten; a complete rerun validates and reuses saved packages without refitting.
`model_packaging_manifest.json` identifies all six artifacts, their hashes and the
five actual fits. Partial or inconsistent outputs fail closed. The selection lock
and all previously frozen implementation/results remain unchanged.

Run the synthetic persistence tests separately from source-data audits:

```bash
python -m unittest discover -s tests -p 'test_packaging.py' -v
```

The completed packaging run and fresh-process reload checks are documented in
[`tables/model_packaging_run_report.md`](tables/model_packaging_run_report.md),
including the complete changed-file inventory. All six artifacts passed exact
prediction/probability round trips; the selection lock and final test remain
untouched.

## One-time final holdout evaluation

After model selection and full-development fitting are complete,
`wine_quality.holdout.evaluate_locked_champion_once()` verifies the frozen recipe,
source/split fingerprints and fitted-package checksums, then reads only the reserved
test rows. It calls the saved champion's `predict` and `predict_proba` once each,
without fitting, tuning, resampling or changing thresholds. Quality probability
columns explicitly follow scores 3, 4, 5, 6, 7 and 8.

```python
from wine_quality.holdout import evaluate_locked_champion_once
final_test_metrics = evaluate_locked_champion_once()
```

The partition-bound `data/final_test_evaluation_access.json` is exclusively created
before parsing test observations. Predictions are persisted before reporting, with
a checksum receipt. An interruption before that receipt fails closed and does not
automatically retry inference. An interruption after it can finish reporting from
the saved CSV only. A completed rerun verifies hashes and returns cached metrics,
without re-parsing test features or calling the model. Changing output directories
does not bypass the access guard. Preserve these records with the original locks.
These guards protect the workflow; they are not filesystem access controls.

Outputs include `final_test_metrics.csv`, `final_classification_report.csv` and
`final_test_predictions.csv` under `tables/`. Additional tables retain raw and
row-normalized confusion matrices, supports, OvR curve coordinates/summaries,
separate label/probability timings and any inference warnings. Four 300-dpi figures
are saved under `visuals/`; plotting closes each figure.

Macro F1 remains the primary metric. All predeclared supporting metrics are
reported, including macro OvR ROC-AUC and macro OvR Average Precision (the PR
summary, not trapezoidal PR area). Per-class reporting includes precision, recall,
F1 and support; zero-division and undefined probability metrics follow the shared
evaluation module. Confusion-matrix normalization is by actual-class row.
**Test results are diagnostic final results and were NOT fed back into selection.**
The immutable champion and all candidate artifacts remain unchanged. Their embedded
`test_evaluation_status=NOT_PERFORMED` records the historical packaging state; the
separate `final_test_evaluation.json` records current evaluation completion.

Qualities 3 and 8 have extremely small holdout support. The notebook explicitly
reports those counts and the recall change caused by one wine. Their precision,
recall, F1 and probability curves are unstable and must not be overinterpreted.
The SMOTE-trained classifier's probabilities are not independently calibrated;
these curves assess ranking, not calibration. Runtime depends on the machine and
thread settings, and cannot replace predictive quality as the selection criterion.

Run only the marked final-holdout cells after locking; do not regenerate earlier
hashed evidence by running the notebook from the top. No new top-to-bottom runtime
is claimed for this phase. Synthetic checks exercise once-only inference, reporting
recovery, cached replay, integrity verification and independent metric calculations:

```bash
python -m unittest discover -s tests -p 'test_holdout.py' -v
```

The measured final result and complete changed-file inventory are recorded in
[`tables/final_test_run_report.md`](tables/final_test_run_report.md).

## Champion interpretation on development data

`wine_quality.interpretation.run_champion_interpretation()` loads the existing
LDA champion and verifies its selection, package, source and split identities.
It uses all 1,087 original development wines for explanation and background,
without fitting, resampling, loading test observations or changing the model.
The notebook's marked `model_interpretation` cells run independently; completed
reruns verify and display saved outputs.

The module reports class-centered standardized coefficients, exact analytic
marginal-background linear SHAP, and 20-repeat seed-42 permutation importance
measured as the decrease in Macro F1. Subtracting the mean class coefficient
removes score components common to all classes while preserving their contrasts
and softmax probabilities. SHAP explains these centered scores, not probabilities.
Its closed-form calculation follows the [SHAP linear-explainer definition](https://shap.readthedocs.io/en/latest/generated/shap.LinearExplainer.html),
so the optional, currently uninstalled `shap` library is not needed. No frozen
dependency versions were changed. Synthetic tests independently enumerate the
Shapley game and verify score/probability reconstruction and class ordering.

Permutation drops are descriptive **training** dependence, not validation scores.
The [scikit-learn guidance](https://scikit-learn.org/stable/modules/permutation_importance.html)
explains the role of the scoring metric and correlated-feature limitations.
Permutation SD is not a confidence interval. Marginal shuffling/SHAP can disregard
real chemical correlations; neither describes a causal intervention. Global SHAP
averages absolute values across original development observations and six equally
weighted class scores. No feature is selected or removed from these rankings.

Three original development observations are sampled uniformly with seed 42 before
examining predictions, confidence or correctness. Their explanations include every
feature contribution to the predicted-class versus runner-up log probability
ratio, plus the background baseline. They are illustrative training examples,
not independent evidence of generalization or calibration.

**Importance indicates model dependence/association, not causality: changing a
chemical property does not necessarily cause wine quality to change.** SMOTE
affects the fitted coefficients/priors, while the background contains no synthetic
observations. Rare-class patterns remain unstable.

Tables include `global_feature_importance.csv`, coefficients/baselines, per-class
and per-observation SHAP values, permutation repetitions, original development
support/correlations and local explanations. Four 300-dpi figures cover global
importance, the coefficient heatmap, the six-class SHAP summary and three local
explanations; figures are closed after saving. `model_interpretation_manifest.json`
records provenance and hashes, and `model_interpretation_runtime.csv` records
separate interpretation stages. No final-test result or fitted model is modified.

```bash
python -m unittest discover -s tests -p 'test_interpretation.py' -v
```

See [`tables/model_interpretation_run_report.md`](tables/model_interpretation_run_report.md)
for measured findings, checks, warnings and the complete changed-file inventory.

## Final performance, runtime and efficiency comparison

`wine_quality.efficiency.create_final_efficiency_comparison()` produces
`tables/final_performance_runtime_comparison.csv` from verified saved evidence.
No fitting, prediction, search, new data partitioning or test-observation access
occurs. The five candidate rows use mean final development-CV scores over 5 × 5
folds; original locked rank and champion are retained. The existing champion
holdout aggregate appears in a sixth, explicitly diagnostic row that is excluded
from candidate plots. Missing/not-applicable values remain blank.

Columns include Macro F1, Balanced Accuracy, QWK, macro OvR Average Precision
(the PR-AUC summary), macro OvR ROC-AUC, Accuracy, MAE and ±1 Accuracy; mean CV
fit/score duration, earlier family search duration, full-development fit duration,
prediction seconds and milliseconds per sample, and serialized model size in
decimal MB. Extra columns retain scope, fold variability, sampling/budget details,
configuration complexity, artifact paths and source run identities.

Candidate prediction costs use each model's existing one-shot post-reload label
prediction on the same 32 development-feature probes. They exclude loading and
probability prediction; the latter remains a separate supporting column. The
champion diagnostic row uses the earlier 272-wine test batch and is not compared
as a candidate timing. Batch milliseconds/sample are not single-request or service
latency. One-shot measurements cannot support precise latency rankings.

Search costs describe earlier original-distribution family searches with unequal
budgets, before imbalance experiments. They are not retuning costs for the final
sampling configurations or total project development costs. Full-development
fit time includes the pipeline and any sampling. The champion production package
reuses its candidate fit, so that fit is shown once. CV scoring includes prediction
and metric calculation and must not be interpreted as pure inference. Timing
scopes overlap and must not be summed indiscriminately.

The two figures are `visuals/final_performance_vs_training_time.png` (CV Macro F1
versus mean CV fit time, with descriptive fold SD) and
`visuals/final_model_runtime_comparison.png` (full fit, family search, common-probe
inference and serialized package size). Both use only compatible candidate rows,
retain the frozen rank and close Matplotlib figures after saving. Package MB is
bytes / 1,000,000, includes embedded metadata, and does not describe RAM use.

**The fastest model is not automatically best.** Macro F1 and supporting predictive
criteria remain primary. Model complexity, search budgets, hardware, parallelism,
warm-up and pipeline overhead all affect cost. This report describes the frozen
models, without revising them after test evaluation or claiming deployment latency.

```bash
python -m unittest discover -s tests -p 'test_efficiency.py' -v
```

Run only the notebook cells tagged `final_efficiency_comparison` after the existing
locks. Cached reruns verify hashes and reuse outputs. The report manifest is
`tables/final_efficiency_comparison_manifest.json`; measured findings, checks,
warnings and the changed-file inventory are in
[`tables/final_efficiency_run_report.md`](tables/final_efficiency_run_report.md).

## Inference for unseen red wines

```python
import pandas as pd
from wine_quality.inference import predict_wine_quality

# Handwritten illustration, with no known true quality or performance claim.
new_data = pd.DataFrame([{
    "fixed acidity": 7.6, "volatile acidity": 0.51, "citric acid": 0.18,
    "residual sugar": 2.3, "chlorides": 0.076, "free sulfur dioxide": 17.0,
    "total sulfur dioxide": 48.0, "density": 0.9964, "pH": 3.30,
    "sulphates": 0.67, "alcohol": 10.6,
}])
predictions = predict_wine_quality(new_data)
```

Supply a nonempty pandas DataFrame containing exactly the eleven feature columns,
in their original measurement units. Column order may vary; the function restores
the stored order and preserves input row order/index, including duplicate index
labels. It rejects the target `quality`, missing/extra/duplicate columns, text,
booleans, complex numbers, missing values and infinities. It neither imputes nor
clips extreme values and does not silently coerce numeric-looking strings.

The function loads `models/final/wine_quality_classifier.joblib` and its adjacent
metadata through the existing integrity/version-checked loader. Paths work from
both the project root and `notebook/`. For a relocated trusted champion, pass
`model_path=...` with its `.metadata.json` sidecar alongside it. The installed
project code and recorded dependencies are required; training data, split locks
and evaluation tables are not. The exact stored pipeline performs all inference
preprocessing; no fitting or resampling occurs. Candidate packages are rejected.

The returned DataFrame contains:

- `predicted_quality`: the pipeline's original integer quality label, 3 through 8.
- `probability_quality_3` through `probability_quality_8`: aligned class probabilities.
- `highest_predicted_probability`: the largest class probability.
- `top_1_quality`, `top_2_quality`: probability-ranked labels, with lower labels
  first on ties. These rankings do not overwrite the pipeline's class prediction.

A label-only estimator returns only `predicted_quality`; probability availability
and class order are also recorded in DataFrame `attrs`. Invalid probabilities
raise rather than being silently omitted or fabricated. The current LDA champion
supports all six probabilities. These outputs are not guarantees of correctness
or independently demonstrated calibrated confidence.

Run only the notebook cells tagged `inference_example` for the two handwritten
illustrations; no observed target labels or datasets are loaded. Validation covers
schema failures, probability ordering, top-two ties, input/state preservation and
exact serialization/reload consistency, including the actual champion when present:

```bash
python -m unittest discover -s tests -p 'test_inference.py' -v
```

See [`tables/inference_run_report.md`](tables/inference_run_report.md) for the checks,
warnings and changed-file inventory.
