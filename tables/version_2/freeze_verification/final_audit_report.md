# Final Version 2 freeze audit

**Status: FROZEN. No new exploratory modelling or optimization.**

LDA (`lsqr`, shrinkage 0.8) with original eleven numeric features, real-row StandardScaler, gentle capped SMOTE (`k=1`, seed42), and Tomek cleaning restricted to qualities5/6. No class weights, engineered features, decision multipliers, thresholds, ensemble or stacking. Class order is 3,4,5,6,7,8. Native class priors are learned from the resampled/cleaned training labels.

The strongest recorded procedure under the adopted4-fold ×10-repeat outer /3-fold inner design has mean Macro F1 **0.3665871810**, population fold SD **0.0548737400**, variance **0.0030111273**, and range **0.2630718954–0.4754939984**. Sample SD(ddof=1) is 0.0555727967. Repeats overlap: these are descriptive split variations, not confidence limits. The higher5-fold diagnostic is not substituted for the adopted design.

| Supporting metric | Fold mean |
|---|---:|
| Balanced Accuracy | 0.391318423 |
| QWK | 0.527034977 |
| Macro PR-AUC (OvR average precision) | 0.392060434 |
| Accuracy | 0.539735728 |
| MAE | 0.535890696 |
| ±1 accuracy | 0.930539464 |

## Manual Macro F1 reconstruction

| Quality | Fold-mean F1 | Pooled OOF F1 | Pooled true count | Pooled predicted count |
|---|---:|---:|---:|---:|
| 3 | 0.3374206349 | 0.3251231527 | 80 | 123 |
| 4 | 0.1484365643 | 0.1551939925 | 420 | 379 |
| 5 | 0.6739882329 | 0.6741712279 | 4610 | 5073 |
| 6 | 0.4649538037 | 0.4656278643 | 4280 | 3357 |
| 7 | 0.4635532154 | 0.4636926083 | 1340 | 1731 |
| 8 | 0.1111706349 | 0.1037463977 | 140 | 207 |

Arithmetic mean of the six fold-mean F1 values: **0.3665871810**. All 40 individual fold confusion matrices also reconstruct their reported Macro F1 to 1e-12.

The pooled six-class mean is **0.3645925406**, a different aggregation. There are **10,870 repeated OOF records from 1,087 unique wines**, each predicted ten times. Unique true counts in class order: **8,42,461,428,134,14**.

Pooled confusion matrix (rows true, columns predicted; order3,4,5,6,7,8):

```text
   33    15    32     0     0     0
   20    62   195   122    18     3
   63   164  3264   963   139    17
    7   120  1500  1778   781    94
    0    17    82   454   712    75
    0     1     0    40    81    18
```

## Selection and limitations

Protected Tomek and standard capped SMOTE are practically tied: Macro F1 difference0.0000187, positive20/40 folds and 5/10 repeats. The selected method has slightly lower split SD and higher Balanced Accuracy; ordinary SMOTE has slightly better QWK/MAE/±1 accuracy. No claim of statistical superiority is made. The deadline sprint produced no robust promotion.

The gentle/k=1 final recipe maximizes the aggregate of already saved INNER mean Macro F1 values across40 outer-training splits among six registered protected-sampler candidates; ties prefer fewer additions/removals, then candidate order. No outer score chooses profile/k and no new search ran. **The reported nested result evaluates per-fold inner sampler selection. It is not separate validation of the exact final fixed recipe.** Across-study family selection reused development validation and can be optimistic. There is no new independent test result.

Rare classes remain weak. Quality 8 pooled precision is 0.086957 and recall0.128571; quality 4 fold-mean F1 is 0.148437. Macro F1≥0.50 was **not achieved**.

## Sixteen validity checks

**1. Macro F1 is macro averaged — passed.** evaluate_predictions uses f1_score(labels=[3,4,5,6,7,8], average="macro", zero_division=0). Independent count-based reconstruction matched every one of 560 outer evaluations in the strongest additional-imbalance study. Weighted F1 is a distinct field.

**2. Manual six-class arithmetic mean — passed.** For every additional-imbalance outer evaluation, built a 6x6 confusion matrix from saved unseen predictions, calculated F1_q = 2TP_q/(actual_q+predicted_q), then averaged the six values. All matched reported Macro F1 within 1e-12. The arithmetic mean of six fold-averaged class F1 values reconstructs the mean-fold Macro F1. The pooled confusion matrix reconstructs pooled Macro F1, a different aggregation.

**3. No duplicates cross validation partitions — passed_exact_duplicate_rows.** Verified every outer source-row membership is unique/disjoint from training, reconstructed 6,960 inner/outer training memberships, and verified validation rows are registered genuine development indices. These checks establish row separation, but cannot determine equal raw predictors or equal full observations from saved IDs alone. Root is independently inspecting locked development data only. Repeated appearances across ten repeats are expected and must not be counted as independent wines. Root raw-data audit:1087 unique full and feature rows,160 disjoint fingerprint boundaries,6960 saved training feature hashes/scaler statistics matched locked development predictors. No wine/group IDs are available to rule out broader source dependencies.

**4. No target information in inputs — passed_source_and_saved_evidence.** NumericFeatureSchema rejects quality and any columns other than the exact 11 original numeric physicochemical predictors, and supplies canonical order. AdditionalImbalanceClassifier schema fit/transform receive X only. The saved scaler has exactly 11 features in each fit. No target encodings are included. Raw-data redundancy/feature-identity confirmation remains within root audit.

**5. Scaling and learned transformations fit inside training folds — passed_source_and_saved_provenance.** Champion StandardScaler is fitted on canonical genuine current-training rows before sampling; saved membership hashes, counts and finite 11-element moments checked for every fit. Runtime records report exact native scaler input guards. Regression Ridge scaling is similarly local. Deadline log selection uses nonnegative support/skew of current training X only. Root reconstructs actual scaler moments from locked development features.

**6. SMOTE/resampling only in training — passed.** AdditionalWineSampler is invoked only in classifier.fit. It sees the training-scaled current fold. Prediction paths apply only existing schema/scaler/model; they never call a sampler. All 6,960 audited training memberships and count equations match expected current training subsets. Protected Tomek removes only genuine classes 5/6 training endpoints; removal memberships and class labels independently checked.

**7. No synthetic observations in validation — passed.** All 560 outer evaluation prediction row sets exactly match the original registered stratified validation indices and actual labels. Each source index occurs once per model per repeat. Generated rows are confined to temporary training arrays; prediction code has no resampling path.

**8. Feature engineering independent of validation labels — passed.** Champion uses original 11 features with no derived engineering. DeadlineFeatures.fit ignores y, uses deterministic fixed chemistry formulas and training-only skew/positivity for log transforms; transform uses frozen selections. No feature direction was promoted or retained.

**9. Hyperparameter selection fold-safe — passed_with_selection_scope_limitation.** Reconstructed all 480 per-method winners by sorting existing inner mean Macro F1, fewer added rows, fewer removed rows, then registered order. Their identities match outer evaluation recipes. Inner splits are subsets of outer train. The champion fixes LDA shrinkage 0.8 and tunes six gentle/moderate × k=1/2/3 sampling choices inside each outer train. Across-study choice of model family/method is not nested; this is exploratory development validation. Aggregating existing inner scores to choose a concrete final sampler is allowed finalization, but does not supply a new unbiased score for that fixed instance.

**10. Regression thresholds fit from training/inner-CV evidence — passed.** Independently reconstructed 3,264 regressor fit memberships, including all inner subtrains. For every 960 threshold record, verified outer-training source hash and saved inner-OOF score hash, strictly ordered rational thresholds, and the recomputed six-class Macro F1 training objective. Source freezes those thresholds before decoding outer predictions. Threshold fitting uses pooled inner OOF labels and is explicitly an optimized tuning objective; only outer metrics are performance estimates. No threshold optimizations or model fits were executed in this audit.

**11. Probability/class multiplier tuning fold-safe — passed.** Independently recalculated all 12 multiplier-vector mean inner-fold Macro F1 scores for each of 8 saved deadline decisions from cached inner OOF probabilities, current outer-training labels and exact inner splits. Selected argmax indices and multiplier vectors match. Multiplier range 0.75–1.5 and classes 5/6 multipliers 1 enforced. No decision direction was promoted.

**12. Ensemble weighting without accepted outer-validation leakage — passed_for_executed_screening_not_accepted_model.** Deadline screened two fixed predeclared soft-vote weight pairs (0.5/0.5, 2/3 vs 1/3). They were not fit using outer labels. Screening comparison determines possible promotion and is labeled exploratory; neither passed, no ensemble was retained or robustly evaluated. Had promotion occurred, code selects weights only on inner OOF probabilities before outer prediction. Champion is a single LDA model.

**13. Stacking uses genuine OOF if present — not_applicable.** No stacking implementation or stacking result exists among the reviewed Version 2 studies. Only the explicitly fixed soft-vote screening was attempted.

**14. Historical holdout not used for Version 2 selection — supported_by_recorded_guards_and_source.** load_locked_development hashes immutable raw bytes, parses only saved development lines, and returns no holdout values. Study scripts consume these development rows and earlier development artifacts only. Saved fresh-kernel attestations record zero holdout evaluations and blocking of historical result/model reads during experimentation. V1 holdout display remains documentation in report replay. This audit read no raw dataset, no historical holdout result files, and performed no fits. Auditing software records cannot prove unrecorded human decisions never considered a previously seen result; no evidence of such use was found.

**15. Class/probability order 3, 4, 5, 6, 7, 8 — passed.** Champion fit asserts native LDA.classes_ equals expected original six labels. Probability alignment code checks/reorders by explicit classes. Independently verified every saved additional-imbalance probability vector is normalized and six named columns map by argmax exactly to saved predictions for all 560 evaluations. Deadline and ordinal outputs explicitly reconstruct the same order; regression decoder maps to fixed Q.

**16. Reported performance uses unseen CV predictions — passed_with_aggregation_caveat.** Every reported additional-imbalance outer prediction row equals its registered validation membership and is excluded from corresponding training. Manually reconstructed reported outer Macro F1. Inner tuning metrics and all-development final fitting are kept separate from outer performance. Averaging 40 folds provides the headline estimate; repeated predictions are correlated and pooled counts are not an independent test.

## Freeze execution and preservation

- One full-development training fit:1,087 real rows +65 synthetic rows −163 genuine quality 5/6 rows removed =989 final LDA training rows. All genuine minority rows remain. Final fit runtime: **0.095063 seconds**.
- Recorded validation components: **12.093363 seconds**;720 inner fit/predict operations plus40 outer fit/scoring operations. Outer scoring already includes prediction and probabilities. Inner metric/selection overhead is excluded. Full historical additional-imbalance study runtime was 112.604315 seconds.
- Fresh clean-kernel execution counted exactly one wrapper, scaler, SMOTE, Tomek and native LDA fit. No searches or holdout evaluations occurred. The source file was read only by the locked-development loader, which checks source bytes but parses only the saved development lines.
- Training data predictions were used only for export parity, never reported as validation. The fitted library-only scaler/LDA artifact reproduced the notebook wrapper exactly on all 1,087 development inputs. An isolated Python process in `/private/tmp`, with project imports and dataset access blocked and fitting disabled, verified synthetic-probe predictions/probabilities, class order and five invalid-input cases.
- All 449 pre-existing artifacts and all 463 prior notebook cells remain unchanged. The six new notebook cells compile and the final result cell has fresh-kernel outputs. Version1 model/results remain preserved. `/src` is absent and not required.
- Exact duplicate numeric feature/full rows are absent across development; all 160 fold boundaries and 6,960 scaler/feature-hash audit records pass. No grouping identifiers exist to prove broader wine-level independence.
- Saved code and runtime guards support the no-holdout-use protocol; an audit cannot prove unrecorded historical human choices.

Model: `models/final/wine_quality_classifier_v2.joblib`. Adjacent metadata and `version2_freeze_lock.json` preserve the full recipe, hashes and provenance. Summary: `tables/final_version2_model_summary.csv`. No further optimization is authorized by this freeze.
