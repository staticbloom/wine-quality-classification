# Validated inference for unseen red wine observations

Implemented `wine_quality.inference.predict_wine_quality(new_data)` and a two-row
notebook example. This is an inference implementation, with no new performance
claims or changes to the locked champion.

## Interface and behavior

- Default: load `models/final/wine_quality_classifier.joblib` with its metadata,
  preserving the existing checksum, dependency-version, implementation and fitted
  schema checks. A relocated trusted champion can be supplied with `model_path`.
- Require a nonempty pandas DataFrame with exactly the eleven stored feature names.
  Restore feature order and preserve row order/index, including duplicate index
  labels, without changing the caller's data.
- Reject the target `quality`, missing/extra/duplicate columns, text, booleans,
  complex numbers, missing values and infinities. Do not silently coerce, impute,
  clip, fit or resample; raw measurements must use the original training units.
- Invoke the complete fitted pipeline. Return integer `predicted_quality` labels
  from 3 through 8. Align all probability columns explicitly to original labels.
- Include `probability_quality_3` through `probability_quality_8`,
  `highest_predicted_probability`, `top_1_quality` and `top_2_quality` when supported.
  Probability ties use the lower quality label first. Preserve the classifier's
  own predicted class if it differs from the probability leader.
- A label-only estimator returns only predicted quality; invalid probabilities
  fail explicitly. DataFrame attrs record probability availability and class order.

## Notebook demonstration

Two handwritten illustrative measurement rows are displayed before calling the
API. No actual quality labels are assigned and no source, development or final
holdout observations are loaded. Predictions and probabilities are computed in the
notebook, with no fabricated results. These examples demonstrate the interface,
not performance or calibration. Only the two cells tagged `inference_example`
were executed; this was not a full notebook rerun.

## Tests and checks

Eight tests passed using:

```bash
MPLBACKEND=Agg MPLCONFIGDIR=/private/tmp/wine-quality-mpl .venv/bin/python -m unittest discover -s tests -p 'test_inference.py' -v
```

The tests check schema and numeric validation before prediction, column reordering,
single-row and batch inputs, duplicate-index preservation, nullable numeric types,
original-label validity, explicit probability alignment, deterministic top-two ties,
label-only behavior, invalid model outputs, non-champion rejection and artifact
corruption. Synthetic fitted pipelines are persisted only in temporary directories.

The actual champion was additionally serialized to a temporary package, reloaded
through the normal verified loader, and predicted on a handwritten input. Labels
and probabilities matched exactly before/after reload. Fitting, schema/scaler
fitting, LDA fitting and resampling were patched to fail during inference. Stored
model bytes and in-memory model state remained unchanged.

Both notebook cells executed successfully from `notebook/` with learning,
resampling and dataset-loading entry points patched to fail. Unit tests also
verified the default path from the project root. Notebook schema validation passed
and the two new cells contain no errors. Integrity checks confirm all pre-existing
model files, source modules, selection/holdout locks, data, prior result tables and
figures, and the Telco reference notebook stayed byte-identical. Only README and
the wine notebook changed among existing files.

## Warnings and limitations

- During synthetic SMOTE test setup, joblib could not determine physical CPU cores
  in the sandbox and fell back to logical cores. Tests passed; this did not change
  the deployed model or its parameters.
- The local Jupyter kernel emitted a TCP-without-encryption transport warning.
  The two guarded example cells executed successfully.
- Probabilities are model outputs, not guarantees or independently demonstrated
  calibrated confidence. Input validation enforces schema and finite numeric data;
  it does not certify plausible chemistry or detect distribution shift.
- No unresolved implementation failures. Dependencies and model artifacts remain
  unchanged, and no later project phase was initiated.

## Files changed

- Created: `src/wine_quality/inference.py`
- Created: `tests/test_inference.py`
- Updated: `notebook/Wine-Quality-Classification.ipynb`
- Updated: `README.md`
- Created: `tables/inference_run_report.md`

## Run provenance

- Report time (UTC): 2026-10-11T17:12:44.032255+00:00
- Champion SHA256: `ae353b49129fe8c788039ca68aa99367f91fca8ca10949dee4436b85ab55d7d8`
- Inference source SHA256: `83cea54affff15c33fad3f948785b7059cd1f766ec8733a31c60b26bb4ffdedd`
- Guarded notebook example execution: 2.382449 seconds (includes kernel startup; not full-notebook runtime or an inference latency benchmark).
