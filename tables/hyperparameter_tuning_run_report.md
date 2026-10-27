# Shortlisted hyperparameter tuning run report

Run ID: `a41c9614-88f2-4136-a7dd-824d9d8a29a3`. Preliminary run: `4bf08b3e-875b-4233-9f78-3a00a874760b`.

Only the five strongest model families from the saved preliminary development leaderboard were tuned. The same 1,087 development rows and five shuffled stratified folds (seed 42) were used. Test labels were never passed to the CSV parser or used for selection or evaluation.

RandomizedSearchCV used only Macro F1 for optimization and refitting. The fixed sampled plan included the original baseline for every family, with no weighting/resampling or search-budget changes after scores were observed.

| Family | Candidates | Best CV Macro F1 ± SD | Balanced Accuracy | QWK | Search seconds |
| --- | ---: | ---: | ---: | ---: | ---: |
| Linear discriminant analysis | 9 | 0.3474 ± 0.0476 | 0.3569 | 0.5461 | 0.257 |
| Gaussian naive Bayes | 12 | 0.3222 ± 0.0459 | 0.3398 | 0.4831 | 0.302 |
| Gradient boosting | 20 | 0.3052 ± 0.0622 | 0.3045 | 0.5099 | 52.541 |
| Logistic regression | 16 | 0.3014 ± 0.0389 | 0.2938 | 0.5034 | 1.006 |
| Random forest | 20 | 0.2856 ± 0.0143 | 0.2879 | 0.5216 | 21.518 |

Total measured search wall time: **75.625 seconds**, including five automatic full-development candidate refits. There were **77 combinations, 385 search-CV fits, 5 refits and 25 selected-configuration diagnostic CV fits: 415 total estimator fit calls**. Diagnostic CV runtime is recorded separately.

LDA has the highest selected development Macro F1 in this run, using LSQR and 0.8 covariance shrinkage. Gaussian Naive Bayes retained its original variance smoothing and unchanged score. No final model was chosen, and no model artifacts were packaged.

Best parameter overrides (all other registered defaults remain unchanged):

- Linear discriminant analysis: `{"shrinkage": 0.8, "solver": "lsqr"}`
- Gaussian naive Bayes: `{"var_smoothing": 1e-09}`
- Gradient boosting: `{"learning_rate": 0.05, "max_depth": 2, "min_samples_leaf": 10, "n_estimators": 50, "subsample": 0.8}`
- Logistic regression: `{"C": 6.2101694189156165}`
- Random forest: `{"max_depth": 8, "max_features": 0.75, "min_samples_leaf": 1, "n_estimators": 200}`

The required CSVs contain best parameters, budgets, fits and timing. Results additionally contain fold means, population SDs and pooled OOF metrics for Balanced Accuracy, QWK, macro Average Precision OvR, macro ROC-AUC OvR, accuracy, MAE, ±1 accuracy and the complete original metric suite. OOF predictions, per-class metrics, full classification reports and every sampled candidate score are retained.

Checks completed:

- 50 relevant synthetic unit/integration tests passed. Tests cover selected-only CSV parsing, locked development membership, provenance mismatch rejection, repeatable/unique bounded candidates, legal LDA solver/shrinkage combinations, baseline inclusion, Macro F1 refitting, pipelines, timing, probability alignment and fit accounting.
- All nine new tuning-section code cells executed independently in a Jupyter kernel from notebook/. Earlier full-source audit and preliminary fitting cells were not rerun; their saved outputs and notebook-duration record were preserved.
- Recomputed all 25 fold metric suites and five pooled OOF evaluations from 5,435 saved predictions. Every row ID belongs to development and matches its predeclared fold.
- Verified 77 distinct within-family candidate combinations, the five selected parameter dictionaries and exact total fit counts. Each unchanged baseline reproduces its saved preliminary Macro F1.
- Confirmed search runtimes agree with the standardized runtime table. Final-fit, final-test-prediction and serialization timings remain unmeasured.
- Dataset bytes, Telco reference, locked split, model registry, preliminary tables/figures and model directories are unchanged.

Warnings and limitations: no model-training warnings or failed candidate fits occurred. Jupyter emitted its local TCP encryption startup warning; execution succeeded. These post-selection metrics reuse the search folds and are selection-biased, not nested-CV estimates. Rare-class support remains small, fold SD is not a confidence interval, and wall time depends on hardware/thread settings. No unresolved execution failure remains.

Files created or changed:

- [README.md](/Users/shivsharma/Documents/projects/Finesse-Project3/README.md)
- [notebook/Wine-Quality-Classification.ipynb](/Users/shivsharma/Documents/projects/Finesse-Project3/notebook/Wine-Quality-Classification.ipynb)
- [src/wine_quality/partitioning.py](/Users/shivsharma/Documents/projects/Finesse-Project3/src/wine_quality/partitioning.py)
- [src/wine_quality/tuning.py](/Users/shivsharma/Documents/projects/Finesse-Project3/src/wine_quality/tuning.py)
- [tables/best_parameters_by_model.csv](/Users/shivsharma/Documents/projects/Finesse-Project3/tables/best_parameters_by_model.csv)
- [tables/hyperparameter_search_plan.json](/Users/shivsharma/Documents/projects/Finesse-Project3/tables/hyperparameter_search_plan.json)
- [tables/hyperparameter_tuning_metadata.json](/Users/shivsharma/Documents/projects/Finesse-Project3/tables/hyperparameter_tuning_metadata.json)
- [tables/hyperparameter_tuning_results.csv](/Users/shivsharma/Documents/projects/Finesse-Project3/tables/hyperparameter_tuning_results.csv)
- [tables/hyperparameter_tuning_run_report.md](/Users/shivsharma/Documents/projects/Finesse-Project3/tables/hyperparameter_tuning_run_report.md)
- [tables/hyperparameter_tuning_warnings.csv](/Users/shivsharma/Documents/projects/Finesse-Project3/tables/hyperparameter_tuning_warnings.csv)
- [tables/model_runtime_comparison.csv](/Users/shivsharma/Documents/projects/Finesse-Project3/tables/model_runtime_comparison.csv)
- [tables/tuned_selected_classification_reports.json](/Users/shivsharma/Documents/projects/Finesse-Project3/tables/tuned_selected_classification_reports.json)
- [tables/tuned_selected_fold_metrics.csv](/Users/shivsharma/Documents/projects/Finesse-Project3/tables/tuned_selected_fold_metrics.csv)
- [tables/tuned_selected_oof_predictions.csv](/Users/shivsharma/Documents/projects/Finesse-Project3/tables/tuned_selected_oof_predictions.csv)
- [tables/tuned_selected_per_class_metrics.csv](/Users/shivsharma/Documents/projects/Finesse-Project3/tables/tuned_selected_per_class_metrics.csv)
- [tables/tuning_search_candidates.csv](/Users/shivsharma/Documents/projects/Finesse-Project3/tables/tuning_search_candidates.csv)
- [tests/test_tuning.py](/Users/shivsharma/Documents/projects/Finesse-Project3/tests/test_tuning.py)
