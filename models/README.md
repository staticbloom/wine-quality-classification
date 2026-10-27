# Wine model artifacts

Use `final/wine_quality_classifier_v2.joblib` with its companion metadata and `version2_freeze_lock.json`. It contains only fitted scikit-learn StandardScaler/LDA components, loads successfully in the recorded environment, and requires no historical project package.

The five `candidates/*.joblib` files and Version 1 `final/wine_quality_classifier.joblib` remain local and are excluded from Git. They require the absent `wine_quality` package. Their metadata and evaluation summaries remain historical evidence. Restore the matching original implementation and environment to inspect/re-export them; the current fixed-recipe trainer cannot faithfully recreate those old experiments.

Only load trusted pickle/joblib artifacts.
