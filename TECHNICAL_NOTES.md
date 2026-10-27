# Red Wine Quality Classification

## Objective and Context

Version 2 is complete. The report uses saved results and the fitted model without further training or tuning.

The project predicts six ordered wine-quality classes, **3 < 4 < 5 < 6 < 7 < 8**, from eleven physicochemical measurements. Start with the [final notebook](notebook/Wine-Quality-Classification.ipynb): it contains the report, local plotting and prediction helpers and the prediction example. No local Python package or editable installation is required.

## Data and Model Availability

Saved-model inference and the report run without the raw CSV. See [data acquisition and attribution](data/README.md). The final model and saved evaluation tables are included; historical pickles requiring the absent `wine_quality` package are not supported.

## Dataset and Source

The supplied `data/wine-quality-red.csv` is the red-wine component of the [UCI Wine Quality dataset](https://archive.ics.uci.edu/dataset/186/wine+quality), describing Portuguese Vinho Verde wines through physicochemical tests and sensory quality scores. Dataset attribution: Cortez, Cerdeira, Almeida, Matos and Reis (2009), DOI [10.24432/C56S3T](https://doi.org/10.24432/C56S3T), **CC BY 4.0**. The project's saved local audit records:

- 1,599 source rows and eleven predictors plus `quality`.
- 240 exact duplicate rows removed, leaving 1,359 observations; no missing values or imputation.
- One locked stratified split: **1,087 development wines** and **272 historical holdout wines**.
- Development class counts for qualities 3–8: **8, 42, 461, 428, 134, 14**.

Qualities 3 and 8 are extremely rare. Accuracy or frequency-weighted F1 can hide failures on these classes, so **Macro F1** gives each of the six class F1 values equal weight. It must not be confused with **weighted F1**. Balanced Accuracy complements it with equal-class recall. The ordered target also motivates QWK, MAE and ±1 accuracy, but ordinal closeness does not replace exact six-class recognition.

## Methodology

Version 1 locked its model before one recorded evaluation of the original holdout. Its existing results and package are preserved for documentation. The final notebook displays the saved Version 1 aggregate result separately; it does not refit, predict or score that holdout again.

Version 2 uses development data only. Scaling, resampling, class-frequency weighting, model tuning and regression cutpoint/class-multiplier selection stay within their appropriate training/inner folds. No synthetic observations enter validation folds. Four folds preserve at least two genuine quality-3 validation observations; five folds can leave only one. Ten-fold CV was excluded.

The old holdout must not choose algorithms, hyperparameters, weights, features, resampling, thresholds or ensembles. Repartitioning previously used data does not create an equivalent new independent test set. **There is no new independent holdout result for Version 2.** Saved code and execution guards support this protocol; they cannot prove unrecorded historical human decisions.

## Results

The selected model is **LDA (`solver="lsqr"`, `shrinkage=0.8`) with StandardScaler, gentle capped SMOTE (`k=1`) and protected Tomek cleaning**. Cleaning affects only quality-5/6 training observations. All eleven original features are retained. There are no custom class weights, engineered features, optimized prediction thresholds, class multipliers or ensemble. Inference uses the fitted scaler and LDA only.

| Development validation metric | Result |
|---|---:|
| Macro F1 | **0.366587** |
| Macro F1 fold SD (`ddof=0`) | **0.054874** |
| Balanced Accuracy | 0.391318 |
| Quadratic Weighted Kappa (QWK) | 0.527035 |
| Macro PR-AUC (OvR average precision) | 0.392060 |
| Accuracy | 0.539736 |
| MAE | 0.535891 |
| ±1 Accuracy | 0.930539 |

These are **development CV estimates**, using outer stratified **4 folds × 10 repeats**, with **3-fold inner CV**. Macro F1 ranges from 0.263072 to 0.475494 across outer folds. The SD describes dependent split variability, not an independent-sample confidence interval. **Macro F1 ≥0.50 was not achieved.**

The score estimates the procedure that selects sampler settings inside each outer training split. The final gentle/k=1 artifact was selected from existing inner-CV records and fitted once on all development rows; its exact fixed recipe has no separately unseen validation estimate. The protected-Tomek advantage over capped standard SMOTE is only 0.000019, a practical tie. Repeated comparison across model families can still introduce selection optimism.

See the [concise final leaderboard](tables/final_leaderboard.csv), [immutable final summary](tables/final_version2_model_summary.csv), [metadata](models/final/wine_quality_classifier_v2.metadata.json) and [complete freeze audit](tables/version_2/freeze_verification/final_audit_report.md).

## Installation and Execution

Use **Python 3.14**; the verified interpreter is **3.14.7**. Exact package versions are pinned to the working environment, including the versions used to serialize the model.

```bash
python3.14 -m venv .venv
source .venv/bin/activate                  # Windows: .venv\Scripts\activate
python -m pip install -r requirements.txt
python -m pip check
```

The requirements contain report/inference packages, Jupyter execution tools, and `imbalanced-learn` for the separate future-version trainer. Historical boosting libraries, resampling libraries, SHAP, pytest and build tools are not imported by the final notebook. The historical dependency listing referenced under `notebook/archive/` is also absent from this workspace.

A clean dependency download and every operating system have not been independently verified. Keep NumPy/scikit-learn/joblib versions aligned with the saved artifact. The replay verifier checks these versions and the frozen-file checksums before execution; direct notebook execution checks feature ordering, classes and the recorded Macro F1.

### Run the Report

From the project root:

```bash
python -m jupyterlab notebook/Wine-Quality-Classification.ipynb
```

Choose the installed environment, then **Restart Kernel and Run All**. The kernel may start in the project root or `notebook/`. The report logic is contained in the notebook, with shared helpers near the beginning. Standalone CSV inference is available through `predict.py`. Ordinary execution reads saved evidence, checks mean-fold and pooled Macro F1, displays tables and six embedded plots, loads the final model, and predicts two handwritten examples. It does not regenerate the historical CSVs or figure exports. **It performs no training or tuning.**

For a sequential clean-kernel check with training/data-access guards:

```bash
python verify_notebook_replay.py --cwd notebook --write
python verify_notebook_replay.py --cwd root
```

From `notebook/`, use `python ../verify_notebook_replay.py --cwd notebook --write`. The verifier uses the same Python executable, permits only the two declared illustrative wines, blocks fitting/searching and raw-data parsing, and confirms frozen evidence remains unchanged. `--write` updates notebook outputs only after successful execution. Results are recorded in `tables/submission/execution_notebook.json` and `execution_root.json`. Jupyter kernels require local sockets; restrictive sandboxes may need permission for localhost kernel communication.

The verifier refreshes manifest checksums for the active report, its documentation, `predict.py` and the new execution record after a successful run. Historical result entries and model/evidence locks remain unchanged. `--write` is optional and replaces notebook outputs only after successful execution; omit it to preserve the saved presentation.

### Prediction

Use the root-level script to score new wines without running the notebook:

```bash
python predict.py data/example_wines.csv --output outputs/wine_predictions.csv
```

The input must contain exactly the eleven numeric feature columns in metadata order, with no `quality` target or identifier column. Missing, nonfinite and negative measurements are rejected; density must be positive, pH is 0–14 and alcohol is 0–100 percent by volume. These broad checks do not establish that a wine is within the training distribution. Output rows retain input order and contain `predicted_quality` plus `probability_quality_3` through `probability_quality_8`. Without `--output`, the CSV is saved beside the input with a `_predictions` suffix. Existing output files are not overwritten.

For example, create the input from the same illustrative wines used in the notebook:

```python
import pandas as pd
from predict import load_model, predict_quality

model, metadata = load_model()
examples = pd.DataFrame([
    [7.6, 0.51, 0.18, 2.3, 0.076, 17, 48, 0.9964, 3.30, 0.67, 10.6],
    [9.1, 0.34, 0.43, 2.1, 0.080, 13, 39, 0.9971, 3.19, 0.74, 11.4],
], columns=metadata["feature_columns"])
examples.to_csv("wine_inputs.csv", index=False)
print(predict_quality(model, examples))
```

These examples have no known labels and are not an accuracy test. The script checks the saved model and metadata against the release lock, checks serialization-library versions, and applies the fitted scaler and LDA without training or resampling. Model paths are relative to the script; input/output paths are relative to the working directory. The notebook's existing prediction helper remains available after running its cells. Probabilities are not demonstrated calibrated confidence; load only the supplied trusted model artifact.

### Reuse and Future Versions

Keep the source dataset's laboratory measurement units and quality-label meaning. Do not substitute alcohol fractions for percentages, or a different concentration/density convention without a verified conversion. Matching column names alone is insufficient for a different laboratory, wine population or sensory panel. Batch/vintage identifiers are not available in the original data, so independence across wine samples cannot be established from this table alone.

```bash
# Supply all eleven measurements plus a quality column containing integer labels 3..8.
python train.py new_labeled_wines.csv --evaluate-only --output-dir runs/wine_evaluation_v1
python train.py new_labeled_wines.csv --output-dir runs/wine_candidate_v3
python predict.py data/example_wines.csv --model runs/wine_candidate_v3/model.joblib --output outputs/candidate_predictions.csv
```

`train.py` retains the recorded fixed gentle/k=1 recipe: scale real training rows, capped SMOTE, Tomek removal restricted to classes 5/6, then LDA with `solver=lsqr` and `shrinkage=0.8`. The implementation follows sampling logic inspected in the local historical executed snapshot (excluded from the public repository); it is not a reconstruction of the missing complete development archive or the historical search. A new stratified 80/20 split with seed 42 evaluates this fixed candidate. All learned preprocessing and sampling use training rows only; the exported model is not refitted on test rows. Training requires at least five real examples of each class and rejects duplicate measurement records for resolution before splitting.

Each new directory contains the model and companion metadata, hashes, versions, split membership, sampling counts, a majority-class baseline and labeled evaluation predictions. Six-class Macro F1, per-class support/precision/recall/F1, ordinal errors and log loss are reported. This candidate's result must not inherit the original nested-CV score. No unseen validation or calibrated-probability claim is made by creating it. For clustered batches or a new domain, define an appropriate external/group-based evaluation before training. Existing holdout results remain consumed; do not use them to choose future settings.

## Visualizations and Interpretation

The report embeds class support, feature summaries/correlations, repeated OOF confusion counts, class F1 and centered LDA coefficients; exports are in `visuals/submission/`. Ten predictions per wine across repeats are not ten independent observations. Coefficients describe class-score associations.

## Repository Structure

```text
data/                         Original CSV, locked split and access records
models/
  final/
    wine_quality_classifier_v2.joblib
    wine_quality_classifier_v2.metadata.json
    version2_freeze_lock.json
notebook/
  Wine-Quality-Classification.ipynb   Active submission report and local helpers
predict.py                          Standalone CSV inference
train.py                            Separate future-version training/evaluation
verify_notebook_replay.py            Guarded report execution
tables/
  final_leaderboard.csv              Ten development procedures
  final_version2_model_summary.csv   Frozen champion summary
  submission/                       New report tables and execution checks
  version_2/                        Immutable experiments and freeze evidence
visuals/
  submission/                       Final labeled report plots
requirements.txt                    Report/inference and future training dependencies
README.md
```

Version 1 numerical evidence remains alongside the explicitly named Version 2 package. Six legacy pickles require the absent `wine_quality` package and are excluded from Git; see [artifact notes](models/README.md). Use the `_v2` model for the final submission. Retained experiment/audit files are evidence, not active experiments. Historical manifests refer to a development notebook under `notebook/archive/`, but that archive is absent from this workspace. The active report does not require it. The replay verifier reports its presence separately and hashes it if available; a successful replay does not certify that the historical archive is complete.

Keep the published model/table/visual tree when copying the project; raw data are optional for the active report. The active report resolves paths relative to the detected project root and does not follow historical absolute paths. Existing immutable records may still contain old paths or retired package names as historical identifiers; they are not runtime dependencies. A plain model inference application needs only the Version 2 model, metadata and inference dependencies.

## Limitations and Reproducibility

- Quality-4 and quality-8 fold-mean F1 are only **0.148437** and **0.111171**. Pooled quality-8 precision is **0.086957**, recall **0.128571**.
- There are **10,870 repeated OOF predictions but only 1,087 unique wines**. Pooled Macro F1 **0.364593** differs from the mean-fold Macro F1 **0.366587**; both are correctly labeled.
- Synthetic observations do not increase independent sample size. Protected cleaning can remove informative majority boundaries.
- Correlated chemistry features and missing wine/batch identifiers limit interpretation and independence claims. There is no external validation or established probability calibration.
- Broad development-data exploration can make the selected estimate optimistic. The final limited feature and decision-rule experiments did not establish a consistent improvement.

The final notebook includes the concise leaderboard, class support/correlation plots, OOF confusion matrix, class F1 plot, fitted LDA coefficient interpretation and prediction example. All plots have titles and labeled axes. The final model and all legitimate historical result files remain unchanged. Historical submission checks are retained for context; the current replay records describe the active notebook. See [submission readiness](tables/submission/SUBMISSION_READINESS_REPORT.md) and the [sixteen-point validity audit](tables/version_2/freeze_20261016/validity_audit_16_checks.csv).

