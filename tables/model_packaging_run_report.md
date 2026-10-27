# Persistent fitted wine models

Completed packaging run `d4a5cf60-7f86-4db5-8bd8-b4d5fb0fa7b3` from immutable selection run
`5096bbc9-6dc2-47bc-8ee6-85c4114da6e0`. **Five fits, six joblib artifacts, six adjacent
metadata JSON files.** Every fit used all 1,087 original locked development rows.
The final test set was not loaded, predicted or evaluated.

[Production package](../models/final/wine_quality_classifier.joblib) ·
[Production metadata](../models/final/wine_quality_classifier.metadata.json) ·
[Fitted model registry](model_registry.csv) ·
[Packaging manifest](model_packaging_manifest.json)

## Saved artifacts

| Role | Model | Joblib | Metadata |
|---|---|---|---|
| candidate | lda | [lda.joblib](../models/candidates/lda.joblib) | [lda.metadata.json](../models/candidates/lda.metadata.json) |
| champion | lda | [wine_quality_classifier.joblib](../models/final/wine_quality_classifier.joblib) | [wine_quality_classifier.metadata.json](../models/final/wine_quality_classifier.metadata.json) |
| candidate | logistic_regression | [logistic_regression.joblib](../models/candidates/logistic_regression.joblib) | [logistic_regression.metadata.json](../models/candidates/logistic_regression.metadata.json) |
| candidate | gaussian_nb | [gaussian_nb.joblib](../models/candidates/gaussian_nb.joblib) | [gaussian_nb.metadata.json](../models/candidates/gaussian_nb.metadata.json) |
| candidate | random_forest | [random_forest.joblib](../models/candidates/random_forest.joblib) | [random_forest.metadata.json](../models/candidates/random_forest.metadata.json) |
| candidate | gradient_boosting | [gradient_boosting.joblib](../models/candidates/gradient_boosting.joblib) | [gradient_boosting.metadata.json](../models/candidates/gradient_boosting.metadata.json) |

The champion remains LDA with StandardScaler and capped SMOTE, `solver="lsqr"`
and `shrinkage=0.8`. Gaussian NB retains its original distribution, Logistic
Regression and Gradient Boosting use capped RandomOverSampler, and Random Forest
uses balanced class weights. Every default and explicit setting matches the
lock-bound candidate specification. The champion package reuses its fitted LDA
candidate; no sixth fit occurred and no configuration was changed.

The fitted registry has one row per shortlisted family. Earlier CV scores below
are copied unchanged from the frozen repeated-CV evidence; they are not scores
from fitting or predicting the full development data.

| Model | CV Macro F1 | Balanced accuracy | QWK | Full-development fit (s) | Candidate file size (bytes) | Champion |
|---|---:|---:|---:|---:|---:|---|
| lda | 0.3774 | 0.4057 | 0.5264 | 0.021894 | 10029 | yes |
| logistic_regression | 0.3339 | 0.3440 | 0.5207 | 0.019589 | 9808 | no |
| gaussian_nb | 0.3181 | 0.3303 | 0.4882 | 0.002269 | 7020 | no |
| random_forest | 0.3144 | 0.3424 | 0.5428 | 0.357217 | 839315 | no |
| gradient_boosting | 0.3141 | 0.3178 | 0.5288 | 0.300021 | 67794 | no |

The production package is 10,029 bytes.
Summed fit time for five models was 0.700990 seconds;
summed serialization time for six artifacts was
0.064449 seconds. These are separate scopes,
measured using `perf_counter()`. Hardware, thread pools and machine load affect
wall time. Native pools and model workers were limited to one where applicable.

## Bundle format and recoverability

All files deserialize to a dictionary with `format_version`, `pipeline` and
`metadata`. The pipeline is a fitted quality-label classifier wrapping the complete
preprocessing/sampling/model pipeline. Sampling is skipped at prediction time.
Metadata records:

- Original quality classes and probability order (3–8), label mapping, target name
  `quality`, and all 11 feature names in their expected order.
- Model identity, algorithm, all native model hyperparameters and the entire locked
  nested configuration, including scaler and sampler settings.
- Seed 42, UTC creation timestamp, source dataset filename `wine-quality-red.csv`,
  source/split/development fingerprints, and selection-lock identity/checksum.
- Locked development-CV metrics and variability, training counts/sampling audits,
  measured fit time, Python/library versions and project implementation hashes.
- Shared fit identity linking the champion package to its fitted candidate.

Each `.metadata.json` duplicates the embedded metadata and adds the joblib checksum,
file size, serialization duration and measured round-trip verification. The public
`load_model_package()` loader checks these records before returning the bundle.
Inference needs the project package and recorded library versions, but does not
need the original dataset, split files or CV tables. Only trusted joblib files
should be loaded; checksum checks establish integrity rather than authenticity.

## Verification

Six synthetic persistence tests passed (6.203 seconds), including measured synthetic
CV/selection fixtures, complete metadata, every artifact's predictions, checksum
validation before deserialization, metadata/version failure handling, schema
validation, overwrite refusal and idempotent reuse without refitting.

The notebook's five marked fitting/packaging/prediction code cells executed
successfully. Earlier audit/CV cells were not rerun; final holdout evaluation cells
remain unimplemented. The existing whole-notebook duration was not replaced by a
section duration.

All six models reloaded successfully and gave exactly matching predictions and
probabilities on 32 evenly spaced development-feature rows selected without targets
(192 artifact-row predictions). No accuracy or other performance score was computed
on these probes. The features and predictions are saved in
`model_artifact_probe_features.csv` and `model_artifact_predictions.csv`; timing and
checks are in `model_packaging_round_trip.csv`.

A second, fresh Python process launched from `notebook/` independently reloaded all
six artifacts and verified every saved prediction/probability exactly. It checked
that scaler statistics use the full development predictors, training-audit counts
match development labels, every fitted/template configuration matches the lock,
and registry CV metrics exactly match prior evidence. It confirmed identical fit
identities for the two champion copies.

A rerun with fitting explicitly disabled verified/reused the saved packages and
left artifact, registry and runtime bytes unchanged. Runtime accounting contains
six packaging records: five measured fits, one champion serialization without
another fit, and no final-test prediction/search/CV duration. For the champion
candidate, `fit_seconds` and `final_fit_seconds` are two names for the same fit and
must not be added together. Smoke prediction timing is not final-test timing.

The prior 14-model baseline registry is preserved byte-for-byte in
`baseline_model_registry.csv`; `model_registry.csv` now records fitted models as
requested. The original source CSV, read-only Telco notebook, selection lock,
holdout lock, split manifest, prior CV/tuning/imbalance results and all earlier
figures retain their pre-task checksums. No frozen implementation file was edited;
the new packaging module is recorded separately in artifact fingerprints.

## Warnings and unresolved work

Zero model warnings were captured. Jupyter emitted its local unencrypted-TCP startup
notice. There are no unresolved persistence or test failures. The champion retains
the previously documented rare-class limitations; creating a production-named
artifact does not supply new generalization evidence. Final test evaluation and
later interpretation remain separate phases requiring authorization.

## Files changed

- `README.md`
- `models/candidates/gaussian_nb.joblib`
- `models/candidates/gaussian_nb.metadata.json`
- `models/candidates/gradient_boosting.joblib`
- `models/candidates/gradient_boosting.metadata.json`
- `models/candidates/lda.joblib`
- `models/candidates/lda.metadata.json`
- `models/candidates/logistic_regression.joblib`
- `models/candidates/logistic_regression.metadata.json`
- `models/candidates/random_forest.joblib`
- `models/candidates/random_forest.metadata.json`
- `models/final/wine_quality_classifier.joblib`
- `models/final/wine_quality_classifier.metadata.json`
- `notebook/Wine-Quality-Classification.ipynb`
- `src/wine_quality/packaging.py`
- `tables/baseline_model_registry.csv`
- `tables/model_artifact_predictions.csv`
- `tables/model_artifact_probe_features.csv`
- `tables/model_packaging_manifest.json`
- `tables/model_packaging_round_trip.csv`
- `tables/model_packaging_run_report.md`
- `tables/model_packaging_warnings.csv`
- `tables/model_registry.csv`
- `tables/model_runtime_comparison.csv`
- `tests/test_packaging.py`
