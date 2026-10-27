# Final performance and efficiency comparison

Completed the reporting phase using verified saved results. No fitting, search, prediction or test-observation loading was performed. The algorithm, preprocessing, resampling and hyperparameters remain locked.

## Implemented

- Reusable, validated aggregation in `wine_quality.efficiency`, including source identity, metric, timing, file-size and cached-output integrity checks.
- Required comparison CSV with five frozen candidate rows and a separate existing champion-test diagnostic row. Candidate metrics use the common 5-repeat × 5-fold development CV; the diagnostic row cannot influence ranking or plots.
- Two 300-dpi figures: Macro F1 versus mean CV fit duration, and four cost panels for final fit, historical search, common-probe prediction and model size. All figures are closed after saving.
- Notebook explanations, executed displays, observed tradeoffs, provenance and README usage guidance. Missing/not-applicable values stay blank.

## Observed tradeoffs

**Observed tradeoffs in the frozen results.** LDA with SMOTE retains the highest development-CV Macro F1 (0.3774), with mean CV fit time 0.0054 s and a 0.010029 MB package. Gaussian Naive Bayes fits fastest (0.0025 s per CV fit) and has the smallest package (0.007020 MB), but its Macro F1 is lower (0.3181). Its simpler computation does not make it the preferred predictive model.

Random Forest has higher QWK (0.5428 versus LDA's 0.5264), but lower Macro F1 (0.3144), longer mean CV fitting (0.3009 s), a larger package (0.839315 MB), and greater recorded batch prediction cost (0.2138 versus 0.0300 ms/sample). Logistic regression has higher ROC-AUC (0.8064), while gradient boosting has lower MAE (0.4813) and higher ±1 accuracy (0.9523); neither leads on the primary Macro F1 criterion. These supporting metrics describe different tradeoffs and do not reopen selection.

LDA's and logistic regression's tiny probe-timing difference (0.0300 versus 0.0280 ms/sample) is not evidence of a reliable latency advantage. All of these inference values come from the same 32-row development probe, measured once. Performance variability and rare-class support also limit strong comparisons.

## Scope and limitations

- Macro PR-AUC denotes macro OvR Average Precision. CV scores are mean validation-fold metrics; fold standard deviations are descriptive, not independent confidence intervals.
- Historical hyperparameter-search times refer to original-distribution family searches before imbalance experiments. Candidate budgets differ. They are not searches of the final resampling configuration or total workflow costs.
- Candidate prediction timing is one saved post-reload label-prediction call on the same 32 development-feature rows. Loading and probability prediction are excluded. The diagnostic champion-test timing uses its prior 272-row batch and is not directly comparable.
- Mean CV scoring includes prediction and metric calculation. Final full-development fitting is counted once per family; production packaging reused the fitted champion. Timing scopes overlap and should not be added indiscriminately.
- Serialized size uses decimal MB and includes the compressed fitted pipeline and embedded metadata; it does not measure RAM.
- Hardware, parallelism, thread pools, scheduling, warm-up, batch size and pipeline overhead affect wall-clock duration. Single-shot timings do not establish production latency or precise speed rankings.
- No new top-to-bottom notebook execution was performed; the duration recorded for this reporting section is not a full notebook runtime. Rare quality classes and repeated use of development CV limit performance certainty.

## Tests and checks

- Five synthetic unit tests passed: `MPLBACKEND=Agg MPLCONFIGDIR=/private/tmp/wine-quality-mpl .venv/bin/python -m unittest discover -s tests -p test_efficiency.py -v`.
- Tests cover source/scope mapping, frozen ranking, missing values, inconsistent identities/configurations/probe sizes, timing validation, output integrity, cached replay and figure closure.
- All 48 predictive values (six rows × eight metrics) independently reconciled to their original saved sources; every candidate cost/size field reconciled to its source and model file size.
- Four notebook reporting cells executed successfully with fit/predict/probability and holdout entry points patched to fail. No guards fired; two figures are embedded, zero cell errors and valid notebook schema.
- Cached replay from the notebook directory completed with model calls, observation loading and table rebuilding disabled; artifact hashes stayed unchanged.
- All previously existing frozen modules, models, data, final-test evidence, prior tables/figures and the Telco reference notebook remained byte-identical. Only the intended README and wine notebook were changed among pre-existing files.
- Both figures were visually inspected for labels, layout, units and readable comparisons.

## Warnings and unresolved problems

- The first notebook display attempted pandas Styler, which required unavailable Jinja2. Replaced it with standard DataFrame display; successful rerun required no dependency installation. There are no remaining notebook errors.
- Jupyter emitted a local TCP transport encryption warning during the reporting-cell execution. The run completed successfully.
- No unresolved implementation problems. The measurement and comparability limitations above remain; this task did not initiate a new production latency benchmark.

## Files changed

- Created: `src/wine_quality/efficiency.py`
- Created: `tests/test_efficiency.py`
- Updated: `README.md`
- Updated: `notebook/Wine-Quality-Classification.ipynb`
- Created: `tables/final_performance_runtime_comparison.csv`
- Created: `tables/final_efficiency_comparison_manifest.json`
- Created: `tables/final_efficiency_run_report.md`
- Created: `visuals/final_performance_vs_training_time.png`
- Created: `visuals/final_model_runtime_comparison.png`
