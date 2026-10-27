# Deadline optimization — submission freeze recommendation

**No defensible improvement was established; stop the sprint and retain the existing result.** The previous best credible Macro F1 under the chosen 4-fold × 10-repeat framework remains **0.3666 ± 0.0549**. The retained value is unchanged, so the credible improvement is **0.0000**. **Macro F1 ≥0.50 was not achieved.**

The best new screening result was **LDA + SMOTE with inner-selected modest score multipliers: 0.3622 ± 0.0413**, versus **0.3543 ± 0.0482** for matched argmax on the same four folds. Its **+0.0078** gain was below .01 and positive in only **2/4 folds**. The screening score is not a replacement for the prior 40-fold estimate. The ordinal multiplier procedure decreased Macro F1 by **0.0142**.

The largest feature gain was **+0.0059** for augmented ordinal logistic classification, again positive in only **2/4 folds**. Both LDA feature sets reduced Macro F1. Equal-weight soft voting gained **0.0034** over LDA and improved only **1/4 folds**; the 2:1 mixture gained **0.0009**. No direction passed the registered gate, so **zero new repeated-validation fits** were run. No unsuccessful direction was expanded.

LDA's quality-4 score adjustment improved F1 **0.1497 → 0.1714**, precision **0.1174 → 0.1295**, and recall **0.2159 → 0.2614**; this gain did not involve precision collapse. Quality-7 F1 also improved slightly (**0.4570 → 0.4669**). Quality-8 F1 stayed **zero** for both decision rules. In the LDA screen, true quality-8 wines ranked in the top two only **8.3%** of the time, versus **50.0%** for quality 4 and **75.4%** for quality 7. The tail problem is not generally solved by changing argmax.

Feature engineering produced some correct quality-8 predictions but poor precision: **2.5%** for the LDA feature variants and **5.0%** for the ordinal feature variants, at **8.3%** recall. These are substantial false-positive burdens, not a compelling minority-class improvement.

The highest prior standard-framework mean belongs to **LDA (`lsqr`, shrinkage 0.8) with inner-selected capped SMOTE plus protected Tomek cleaning**: gentle/moderate targets, k=1/2/3 selected inside training folds, cleaning restricted to qualities 5/6. Its **0.3666** is effectively tied with standard conservative SMOTE (**0.366568 versus 0.366587**); the negligible cleaning advantage does not justify altering the existing submission pipeline. No saved model or Version 1 result was replaced.

All conclusions are development estimates on repeatedly studied data. Four screening folds contain only two quality-3 and three–four quality-8 observations apiece. There is no new independent test, no significance claim from overlapping folds, and no holdout evaluation.

## Requested outcome

- **Previous best credible Macro F1:** 0.366587 (chosen 4-fold × 10-repeat framework).
- **Best credible value retained after the sprint:** 0.366587.
- **Credible improvement:** 0.000000; no new candidate passed screening.
- **Best new screening candidate:** LDA + SMOTE with inner-selected bounded score multipliers, 0.362151; a four-fold screening estimate only.
- **Strongest recorded procedure:** LDA lsqr, shrinkage .8, conservative SMOTE profile/k selection with protected Tomek cleaning; practically tied with SMOTE without cleaning. Keep the existing submission pipeline unchanged.
- **Execution:** 48 new development model fits; 30 meaningful configurations maximum; no tree/boosting/regression reruns, no new dependencies and no expanded search.
- **Robust validation of new candidates:** not triggered because every direction failed the predeclared .01 / 3-of-4 gate. Existing robust estimates are retained.
- **Legitimate Macro F1 ≥.50:** **No**.
- **Historical holdout evaluations:** **Zero**.

| Metric | Retained prior 4×10 estimate |
| --- | --- |
| Macro F1 | 0.3666 |
| Balanced Accuracy | 0.3913 |
| QWK | 0.5270 |
| Macro PR-AUC | 0.3921 |
| Accuracy | 0.5397 |
| MAE | 0.5359 |
| ±1 accuracy | 0.9305 |
| Macro F1 SD | 0.0549 |
| Macro F1 variance | 0.003011 |
| Macro F1 min–max | 0.2631–0.4755 |

| Quality | F1 | Precision | Recall |
| --- | --- | --- | --- |
| 3 | 0.3374 | 0.3403 | 0.4125 |
| 4 | 0.1484 | 0.1663 | 0.1477 |
| 5 | 0.6740 | 0.6449 | 0.7080 |
| 6 | 0.4650 | 0.5324 | 0.4154 |
| 7 | 0.4636 | 0.4160 | 0.5309 |
| 8 | 0.1112 | 0.1051 | 0.1333 |

## Review of all Version 2 evidence

`version_2/deadline_20261015/prior_v2_review.csv` records every completed prior run and procedure, including single/repeated CV stability, nested conventional selection, SVM, XGBoost, CatBoost, LightGBM, forests, both imbalance studies, true ordinal classification, and regression with learned cutpoints. No Version 1 results were used for shortlisting. Every inspected prior source has a recorded hash.

The LDA/SMOTE variants lead the chosen validation framework. The higher 5-fold stability mean (0.3702) is also recorded, but that design was rejected earlier because some validation folds contain only one quality-3 wine. It is not silently treated as the project's adopted robust estimate.

The two sprint approaches are different training formulations: fixed multiclass LDA + SMOTE, and five ordered binary logistic heads with PAVA reconstruction. The latter freezes the most frequent earlier **inner-selected** recipe, C=.1 and square-root frequency weights; it does not inherit the performance estimate of the earlier searched procedure. Logistic/ROS is not added as a near-duplicate third linear candidate. Lower-performing forests, boosters, SVM, cumulative logit and regressors are not rerun.

Historic LDA and ordinal predictions disagree in 19.19% of repeated rows, with unique correct fractions 5.68% and 8.94%, and a Macro F1 gap of .0149. This passes the predeclared ensemble eligibility criteria. The ensemble screen still failed to deliver a useful gain.

## Registered budget and fold boundaries

1. **Decision rules:** exactly 12 fixed vectors per model, including identity. Only qualities 3/4/7/8 change; factors stay in [.75,1.5]. Select by mean 3-fold inner-validation six-class Macro F1. No threshold choice uses outer labels. Exact ties favor identity/registered order.
2. **Features:** three fixed sets per model. Original 11 features; original +6 derived variables; compact14 with training-only log eligibility. No broad polynomial grid or target-informed feature pruning.
3. **Ensemble:** equal and 2:1 LDA:ordinal soft voting only, using original features and raw normalized probabilities. Base predictions are reused. No stacking or calibration search.

This is **24 vector configurations +4 additional feature/model configurations +2 ensemble weights =30**. The 10 screening output rows evaluate the two adaptive decision rules, six feature/model argmax combinations and two mixtures. Scores from unselected multiplier vectors stay inside the inner-selection evidence.

The screen uses one standard stratified4-fold split, seed42. Directions must gain at least .01 over matched original argmax (ensemble over LDA) in at least3/4 folds. At most two passing direction/family procedures would receive4×10 outer/3-fold inner validation, reselecting among the same12 vectors,3 feature sets or2 weights inside outer training. There is no feature×multiplier×ensemble Cartesian expansion. All failed directions stopped without that additional work.

Supporting metrics do not choose multipliers. PR-AUC is macro OvR average precision from the **raw model probabilities**, before decision multipliers; adjusted decision scores are not presented as calibrated probabilities. Scaling and any SMOTE fit use only current training data. The ordinal weights derive from six-class frequencies in the actual training fold. [Decision-rule tuning](https://scikit-learn.org/stable/modules/classification_threshold.html).

## Compact feature definitions

Augmented features: total minus free sulfur dioxide; free/total sulfur fraction; alcohol × (density−1); volatile/fixed acidity; citric/fixed acidity; fixed acidity × 10^(3−pH). Ratios/interactions are numerical chemistry proxies, not claims of chemical mole fractions or causal effects. [Dataset variables](https://archive.ics.uci.edu/dataset/186/wine+quality).

Compact features replace free/total sulfur with bound/fraction, add alcohol-density, volatile/fixed and acidity-pH interactions, and omit the extra citric ratio. The result has14 columns. `log1p` applies only to predeclared residual sugar, chlorides, sulphates, bound sulfur dioxide and volatile acidity when the current training values are nonnegative with skewness>1. Validation data never choose a log transform. Feature definitions and thresholds were fixed before the run.

## Screening outcomes and stopping decisions

| Stage / configuration | Macro F1 ± SD | Gain vs matched original | Positive folds |
| --- | --- | --- | --- |
| previous / previous_best__lda__smote_tomek_protected | 0.3666 ± 0.0549 | — | — |
| screening / lda_smote__original__argmax | 0.3543 ± 0.0482 | — | — |
| screening / lda_smote__original__multipliers | 0.3622 ± 0.0413 | +0.0078 | 2/4 |
| screening / lda_smote__chemistry__argmax | 0.3382 ± 0.0469 | -0.0161 | 1/4 |
| screening / lda_smote__compact__argmax | 0.3408 ± 0.0554 | -0.0136 | 1/4 |
| screening / ordered_logit__original__argmax | 0.3488 ± 0.0395 | — | — |
| screening / ordered_logit__original__multipliers | 0.3346 ± 0.0490 | -0.0142 | 2/4 |
| screening / ordered_logit__chemistry__argmax | 0.3547 ± 0.0456 | +0.0059 | 2/4 |
| screening / ordered_logit__compact__argmax | 0.3481 ± 0.0586 | -0.0007 | 2/4 |
| screening / ensemble__original__argmax__w0.5000 | 0.3577 ± 0.0464 | +0.0034 | 1/4 |
| screening / ensemble__original__argmax__w0.6667 | 0.3552 ± 0.0458 | +0.0009 | 2/4 |

SD above is population fold SD, not a standard error. Screening and historical repeated results are explicitly separate stages. Failed screening does not prove no possible optimization could help; it establishes that this bounded sprint did not produce a defensible candidate worth further spending under the deadline.

## Precision and ranking diagnostics

Raw per-class AP, top-two recall, true-class rank, precision/recall/F1 and false-positive counts are saved. This separates a class ranking failure from losing only at the final argmax. Quality4 has some usable ranking signal, but the modest decision-rule gain is too small and inconsistent. Quality8 remains particularly weak; engineered features' recall gains carry very poor precision.

## Runtime and verification

The measured experiment took **2.135 seconds**, including prior-result review, data loading, screening and result assembly, excluding kernel startup and verification. It used **48 complete development fits/predictions/scaler fits**, with one locked-development load, four inner-CV caches and eight multiplier selections. All models are small linear fits; none of the expensive model-family searches was rerun.

Per-row `runtime_seconds` attributes required fitting/prediction components to each procedure and can share components across rows; do not sum it as elapsed wall time. The prior row contains historic outer fit/scoring time only, not its earlier search cost. `new_study_wall_seconds` and the outcome record provide the actual sprint execution total.

Seven synthetic checks use14 synthetic fits to verify original-model parity with prior implementations, feature behavior, inner-only selection, score bounds and invalid inputs. A fresh-kernel execution runs only the relevant utilities/new section, avoiding another expensive replay of every earlier experiment. Runtime guards inspect actual training and prediction rows and scaler statistics, allow one development-only loader, and block old holdout functions, Version1 result reads and packaged model access.

Saved-evidence validation independently recomputes all40 screening evaluations,240 class rows and8 inner selections, checks every fit's membership and sampling/weight provenance, and verifies source/result hashes. All earlier notebook cells and467 prior artifacts are checked for exact preservation. The notebook remains independent of `/src`. No final model refit or deployment change is introduced.

## Files

- Requested table: `tables/deadline_optimization_results.csv`.
- Immutable run evidence: `tables/version_2/deadline_20261015/`.
- Full review: `prior_v2_review.csv`.
- Gate decisions: `screening_decisions.csv` and `promotion.json`.
- Fold/class predictions and metrics: `outer_fold_metrics.csv`, `outer_per_class.csv`, `outer_oof_predictions.csv`.
- Inner evidence: `inner_oof_predictions.npz`, `inner_selections.json`, `training_audits.json`.
- Reproducibility: `plan.json`, `manifest.json`, `outcome.json`.
