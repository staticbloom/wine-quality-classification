# Preliminary development benchmark run report

Run ID: `4bf08b3e-875b-4233-9f78-3a00a874760b`. All 14 unchanged registered baselines completed five shared development folds (70 evaluations). No tuning or final-test evaluation was performed.

The comparison includes all eleven requested predictive metrics as fold means, population standard deviations, and pooled OOF scores. Each of the 1,087 development rows has one OOF prediction per model. Original row identifiers and ordered probabilities are saved.

| Tuning candidate | Macro F1 mean ± SD | Balanced Accuracy | QWK |
| --- | ---: | ---: | ---: |
| Gaussian naive Bayes | 0.3222 ± 0.0459 | 0.3398 | 0.4831 |
| Linear discriminant analysis | 0.3156 ± 0.0556 | 0.3153 | 0.5255 |
| Logistic regression | 0.2957 ± 0.0424 | 0.2905 | 0.5002 |
| Gradient boosting | 0.2845 ± 0.0121 | 0.2855 | 0.5150 |
| Random forest | 0.2828 ± 0.0181 | 0.2853 | 0.5207 |

The shortlist uses mean Macro F1. Accuracy and runtime do not determine ranking. The small separation between the top two means relative to fold variability does not establish a clear winner. All five families merit a separately authorized tuning phase.

Limitations: class 3 has eight development examples, class 8 fourteen. The highest pooled recalls across all models are 25% and 1/14 respectively. All baselines except Gaussian Naive Bayes have zero class-8 recall. Fold SD is descriptive, not a confidence interval; comparisons on shared development folds can be optimistic.

Validation completed:

- 69 unit/integration tests passed, including OOF order/coverage, per-fold isolation, development membership, probability ordering, export consistency and ranking independent of accuracy/runtime.
- The notebook executed all 73 code cells from the notebook directory; its measured body duration was 18.017 seconds.
- Recomputed all fold and pooled OOF metrics from 15,218 saved prediction records; checked all means and population SDs against the leaderboard.
- Verified that every prediction row belongs to development and none belongs to the locked test partition.
- Confirmed runtime comparison values match the metric exports and final-fit/test/search/serialization timings remain blank.
- Dataset, Telco reference, split manifest and holdout lock are byte-identical to their pre-task snapshots.
- Inspected all five comparison figures. Refined chart labels using existing saved measurements without rerunning models. PNG exports use 300 dpi and PDFs remain vector.

No model-training warnings were captured. Jupyter emitted a local TCP encryption startup warning; notebook execution succeeded. No unresolved execution failures remain. Benchmark wall times depend on hardware, thread settings, workload and machine load.

Files created or changed (pre-existing EDA PDF bytes were restored after execution; existing EDA analysis is unchanged):

- [README.md](/Users/shivsharma/Documents/projects/Finesse-Project3/README.md)
- [notebook/Wine-Quality-Classification.ipynb](/Users/shivsharma/Documents/projects/Finesse-Project3/notebook/Wine-Quality-Classification.ipynb)
- [src/wine_quality/benchmarking.py](/Users/shivsharma/Documents/projects/Finesse-Project3/src/wine_quality/benchmarking.py)
- [src/wine_quality/evaluation.py](/Users/shivsharma/Documents/projects/Finesse-Project3/src/wine_quality/evaluation.py)
- [src/wine_quality/timing.py](/Users/shivsharma/Documents/projects/Finesse-Project3/src/wine_quality/timing.py)
- [tables/model_runtime_comparison.csv](/Users/shivsharma/Documents/projects/Finesse-Project3/tables/model_runtime_comparison.csv)
- [tables/notebook_runtime.csv](/Users/shivsharma/Documents/projects/Finesse-Project3/tables/notebook_runtime.csv)
- [tables/preliminary_benchmark_metadata.json](/Users/shivsharma/Documents/projects/Finesse-Project3/tables/preliminary_benchmark_metadata.json)
- [tables/preliminary_benchmark_run_report.md](/Users/shivsharma/Documents/projects/Finesse-Project3/tables/preliminary_benchmark_run_report.md)
- [tables/preliminary_classification_reports.json](/Users/shivsharma/Documents/projects/Finesse-Project3/tables/preliminary_classification_reports.json)
- [tables/preliminary_fold_metrics.csv](/Users/shivsharma/Documents/projects/Finesse-Project3/tables/preliminary_fold_metrics.csv)
- [tables/preliminary_model_comparison.csv](/Users/shivsharma/Documents/projects/Finesse-Project3/tables/preliminary_model_comparison.csv)
- [tables/preliminary_oof_confusion_matrices.csv](/Users/shivsharma/Documents/projects/Finesse-Project3/tables/preliminary_oof_confusion_matrices.csv)
- [tables/preliminary_oof_predictions.csv](/Users/shivsharma/Documents/projects/Finesse-Project3/tables/preliminary_oof_predictions.csv)
- [tables/preliminary_per_class_fold_metrics.csv](/Users/shivsharma/Documents/projects/Finesse-Project3/tables/preliminary_per_class_fold_metrics.csv)
- [tables/preliminary_per_class_metrics.csv](/Users/shivsharma/Documents/projects/Finesse-Project3/tables/preliminary_per_class_metrics.csv)
- [tables/preliminary_shortlist.csv](/Users/shivsharma/Documents/projects/Finesse-Project3/tables/preliminary_shortlist.csv)
- [tables/preliminary_warnings.csv](/Users/shivsharma/Documents/projects/Finesse-Project3/tables/preliminary_warnings.csv)
- [tests/test_benchmarking.py](/Users/shivsharma/Documents/projects/Finesse-Project3/tests/test_benchmarking.py)
- [visuals/model_runtime_comparison.pdf](/Users/shivsharma/Documents/projects/Finesse-Project3/visuals/model_runtime_comparison.pdf)
- [visuals/model_runtime_comparison.png](/Users/shivsharma/Documents/projects/Finesse-Project3/visuals/model_runtime_comparison.png)
- [visuals/preliminary_balanced_accuracy_comparison.pdf](/Users/shivsharma/Documents/projects/Finesse-Project3/visuals/preliminary_balanced_accuracy_comparison.pdf)
- [visuals/preliminary_balanced_accuracy_comparison.png](/Users/shivsharma/Documents/projects/Finesse-Project3/visuals/preliminary_balanced_accuracy_comparison.png)
- [visuals/preliminary_macro_f1_comparison.pdf](/Users/shivsharma/Documents/projects/Finesse-Project3/visuals/preliminary_macro_f1_comparison.pdf)
- [visuals/preliminary_macro_f1_comparison.png](/Users/shivsharma/Documents/projects/Finesse-Project3/visuals/preliminary_macro_f1_comparison.png)
- [visuals/preliminary_performance_vs_training_time.pdf](/Users/shivsharma/Documents/projects/Finesse-Project3/visuals/preliminary_performance_vs_training_time.pdf)
- [visuals/preliminary_performance_vs_training_time.png](/Users/shivsharma/Documents/projects/Finesse-Project3/visuals/preliminary_performance_vs_training_time.png)
- [visuals/preliminary_qwk_comparison.pdf](/Users/shivsharma/Documents/projects/Finesse-Project3/visuals/preliminary_qwk_comparison.pdf)
- [visuals/preliminary_qwk_comparison.png](/Users/shivsharma/Documents/projects/Finesse-Project3/visuals/preliminary_qwk_comparison.png)
