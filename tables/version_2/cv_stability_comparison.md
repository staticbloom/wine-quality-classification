# Experiment Version 2 — Development CV Estimate

Fixed-baseline validation-stability comparison; 1,087 existing development rows only.
Single stratified CV is a diagnostic comparator; the repeated runs use no inner search.
All baselines preserve their prior development-selected settings. Seed 42; no 10-fold CV.

| Strategy | Baseline | Macro F1 mean ± SD | Balanced Accuracy mean ± SD | QWK mean ± SD | Repeat-mean Macro F1 SD | Minimum support: quality 3 / 8 |
|---|---|---:|---:|---:|---:|---:|
| SKF_4 | LDA + SMOTE | 0.3543 ± 0.0482 | 0.3650 ± 0.0380 | 0.5269 ± 0.0150 | unavailable | 2 / 3 |
| SKF_4 | Logistic + random oversampling | 0.3444 ± 0.0363 | 0.3410 ± 0.0259 | 0.5168 ± 0.0101 | unavailable | 2 / 3 |
| SKF_4 | Gaussian Naive Bayes | 0.3009 ± 0.0340 | 0.3078 ± 0.0445 | 0.4561 ± 0.0250 | unavailable | 2 / 3 |
| SKF_5 | LDA + SMOTE | 0.3669 ± 0.0355 | 0.3990 ± 0.0565 | 0.5308 ± 0.0466 | unavailable | 1 / 2 |
| SKF_5 | Logistic + random oversampling | 0.3196 ± 0.0365 | 0.3217 ± 0.0310 | 0.5266 ± 0.0436 | unavailable | 1 / 2 |
| SKF_5 | Gaussian Naive Bayes | 0.3222 ± 0.0459 | 0.3398 ± 0.0752 | 0.4831 ± 0.0523 | unavailable | 1 / 2 |
| RSKF_4x10 | LDA + SMOTE | 0.3634 ± 0.0533 | 0.3919 ± 0.0618 | 0.5223 ± 0.0435 | 0.0094 | 2 / 3 |
| RSKF_4x10 | Logistic + random oversampling | 0.3509 ± 0.0526 | 0.3651 ± 0.0599 | 0.5198 ± 0.0405 | 0.0141 | 2 / 3 |
| RSKF_4x10 | Gaussian Naive Bayes | 0.3247 ± 0.0499 | 0.3425 ± 0.0587 | 0.4825 ± 0.0548 | 0.0217 | 2 / 3 |
| RSKF_5x10 | LDA + SMOTE | 0.3702 ± 0.0676 | 0.4055 ± 0.0834 | 0.5262 ± 0.0559 | 0.0157 | 1 / 2 |
| RSKF_5x10 | Logistic + random oversampling | 0.3346 ± 0.0520 | 0.3486 ± 0.0667 | 0.5204 ± 0.0476 | 0.0077 | 1 / 2 |
| RSKF_5x10 | Gaussian Naive Bayes | 0.3251 ± 0.0505 | 0.3468 ± 0.0762 | 0.4848 ± 0.0601 | 0.0120 | 1 / 2 |

Values are unweighted fold means and population SD (`ddof=0`). Repeat-mean SD uses
the ten complete-CV averages and is unavailable for a single repeat. Single SKF
shares its identical first repetition with RSKF; these comparisons are not independent.

| Folds | Training rows | Validation rows | Minimum validation support for classes 3, 4, 5, 6, 7, 8 |
|---|---:|---:|---|
| 4 | 815–816 (75%) | 271–272 | 2, 10, 115, 107, 33, 3 |
| 5 | 869–870 (80%) | 217–218 | 1, 8, 92, 85, 26, 2 |

The [complete comparison CSV](cv_stability_20261012/cv_stability_comparison.csv)
includes per-class recall/F1 means and SDs, all six classes' minimum/maximum support,
and separately pooled per-repeat OOF scores. The [per-class table](cv_stability_20261012/per_class_comparison.csv)
provides the same class metrics in a long format (72 rows). See also the
[registered plan](cv_stability_20261012/plan.json),
[fold metrics](cv_stability_20261012/fold_metrics.csv),
[repeat metrics](cv_stability_20261012/repeat_metrics.csv),
[split assignments](cv_stability_20261012/validation_assignments.csv), and
[recorded decision](cv_stability_20261012/selected_validation.json).

## Decision and interpretation

**Selected design: 4 folds × 10 repeats, seed 42.** Four folds use **815–816 training rows** and **271–272 validation rows**, versus **869–870** and **217–218** for five folds. The cost is about 54 training observations per fit. The benefit is a minimum of **2 quality-3 and 3 quality-8 observations** in each validation fold, instead of **1 and 2**. With one quality-3 example, a fold's class recall can only be 0 or 1; with two it moves in steps of 0.5. Neither is precise, but four folds meets the registered minimum-support criterion.

The repeated four-fold design has fold-level Macro F1 SD **0.0533 / 0.0526 / 0.0499** for LDA / logistic regression / Naive Bayes, compared with **0.0676 / 0.0520 / 0.0505** for repeated five-fold CV. Quality-3 recall SD also falls for all three references: **0.278 / 0.283 / 0.247**, versus **0.400 / 0.334 / 0.362**. This supports better rare-class fold representation, without a claim that four folds minimizes every measure of variance.

The tradeoff is visible in **repeat-mean Macro F1 SD**: four folds gives **0.0094 / 0.0141 / 0.0217**, while five gives **0.0157 / 0.0077 / 0.0120**. Five-fold repeat averages are steadier for logistic regression and Naive Bayes; four-fold averages are steadier for LDA. Repetition reveals this sensitivity, while a single seeded run cannot measure between-repeat variability. For example, LDA's single five-fold SD is only **0.0355**, but its repeated five-fold SD is **0.0676**. The single first repeat should not be treated as representative of all possible partitions.

The selection does **not** maximize scores: repeated five-fold LDA has mean Macro F1 **0.3702**, compared with **0.3634** for repeated four-fold LDA. The registered support criterion takes precedence; it leaves only the four-fold designs eligible, and ten repeats characterize split sensitivity more fully than one run. No baseline winner is chosen and no parameters or sampling rules are changed.

Rare-class uncertainty remains substantial. Under the selected design, LDA quality-3 recall averages **0.350 ± 0.278** and quality-8 recall **0.135 ± 0.169** across folds (descriptive SD). There are still only **8** distinct quality-3 and **14** distinct quality-8 observations. Repeated predictions must not be presented as 80 or 140 independent rare wines. Prior development-based tuning/selection also limits generalization claims; this fixed-reference comparison is not a nested estimate of that earlier search. Future changes require inner CV, and the original holdout remains closed.

The recorded run completed **270 fold-local fits**. Scaler means and original sampler counts matched each training fold. Predictions and fits were guarded to require development indices, while historical result/model reads, source imports and access to the removed source directory were blocked. The pinned environment emitted pandas `FutureWarning` messages; these are counted in `warnings.json`, and all requested metrics were independently reproduced from the saved OOF labels. They did not trigger retries or changes to estimator settings.
