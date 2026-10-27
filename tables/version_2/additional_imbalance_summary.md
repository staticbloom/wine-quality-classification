# Version 2 — Additional Imbalance Methods

**Development CV estimates only.** Two fixed model families, 1,087 existing development wines, outer stratified 4-fold ×10 repeats and inner stratified 3-fold. The old holdout was not evaluated. This is an exploratory continuation on previously studied development data; repeated folds do not supply a new independent test.

## Method suitability

| Method | Decision | What it does | Small-sample concern / protection |
|---|---|---|---|
| RandomOverSampler | evaluate | Duplicate existing training observations with replacement; no new independent information. | Does not need neighbors but can memorize rare wines. Use the same conservative target caps as SMOTE. |
| SMOTE | reference | Interpolate between same-class training neighbors. | k=1,2,3 is feasible with four inner-training quality-3 wines; feasibility is not robust independent evidence. Keep targets conservative. |
| BorderlineSMOTE | evaluate restricted to qualities 4/7 | Generate from minority points classified as in danger using a local one-versus-rest neighborhood; borderline-1 interpolates within class. | Do not infer boundaries from four quality-3 or six-eight quality-8 inner-training wines. Keep these classes unchanged. Use m=5, audit safe/danger/noise anchors, and compare with matched SMOTE on 4/7. No-danger classes receive no additions; never silently substitute ordinary SMOTE. |
| ADASYN | defer this initial study | Allocate more generated samples to minority observations with more other-class neighbors. | With tiny genuine classes this local difficulty estimate can amplify noise/overlap. Installed implementation rounds per-point allocations, can miss exact caps or generate zero rows at small budgets. A capped allocation redesign would be a separate method; no claim of universal unsuitability. |
| SMOTEENN | defer this initial study | Follow SMOTE with edited-nearest-neighbor removal of observations whose local labels disagree. | Default cleaning targets every class and may discard legitimate minority boundary wines. With tiny genuine counts this is too aggressive for the initial comparison. A protected ENN design needs separate removal controls; computational feasibility would not establish statistical suitability. |
| SMOTETomek | evaluate protected cleaning variant | Follow capped SMOTE with removal of specified-class endpoints of mutual nearest-neighbor pairs having different labels. | Clean only qualities 5/6; never remove genuine or generated minority rows. This differs explicitly from default all-class cleaning. Audit all removed real rows and retained support; cleaning may still discard useful majority boundary information. |

Mechanics are documented in the official [BorderlineSMOTE](https://imbalanced-learn.org/stable/references/generated/imblearn.over_sampling.BorderlineSMOTE.html), [ADASYN](https://imbalanced-learn.org/stable/references/generated/imblearn.over_sampling.ADASYN.html), [SMOTEENN](https://imbalanced-learn.org/stable/references/generated/imblearn.combine.SMOTEENN.html), and [TomekLinks](https://imbalanced-learn.org/stable/references/generated/imblearn.under_sampling.TomekLinks.html) references. The suitability decisions are this study’s conservative judgments. Deferred methods have no measured performance result and are not declared universally unsuitable.

## Registered design

LDA uses lsqr with shrinkage .8; Logistic Regression uses C=1, lbfgs and max_iter=2000. Every scaler is fitted on genuine training rows before sampling or cleaning. Model settings are fixed across samplers. No weights, new features, calibration, threshold optimization or early stopping. Boundary detection and Tomek geometry operate only on current training data; validation distributions remain untouched.

There are 27 candidates per family: no sampling (1), ROS (2), standard SMOTE (6), SMOTE targeting only 4/7 (6), BorderlineSMOTE targeting only 4/7 (6), and SMOTE followed by protected Tomek cleaning (6). Gentle/moderate target profiles and k=1,2,3 are fixed before training; Borderline m=5 is fixed. Targets use current-fold genuine counts, rare multiplier caps 2×/3× and absolute q3/q8 caps 18/30. Tomek deletes only genuine quality 5/6 rows. Classes 3/4/7/8, including generated rows, cannot be deleted.

Optimize mean inner six-class Macro F1. Exact ties prefer fewer additions, then fewer removals, then candidate order. Each method has its own nested estimate; a joint sampler-selection procedure chooses from all 27 candidates inside inner CV and reuses the appropriate outer refit. The joint results do not estimate retrospectively selecting the best model family.

## Development CV comparison

| Model / procedure | Macro F1 mean ± SD | Balanced Accuracy | QWK | Macro PR-AUC |
|---|---:|---:|---:|---:|
| LDA / None | 0.3558 ± 0.0675 | 0.3506 | 0.5269 | 0.3933 |
| LDA / ROS | 0.3566 ± 0.0562 | 0.3759 | 0.5254 | 0.3877 |
| LDA / Standard SMOTE (3/4/7/8) | 0.3666 ± 0.0558 | 0.3850 | 0.5286 | 0.3937 |
| LDA / SMOTE (4/7 only) | 0.3415 ± 0.0634 | 0.3463 | 0.5298 | 0.3928 |
| LDA / BorderlineSMOTE (4/7 only) | 0.3354 ± 0.0591 | 0.3416 | 0.5149 | 0.3875 |
| LDA / SMOTE + protected Tomek | 0.3666 ± 0.0549 | 0.3913 | 0.5270 | 0.3921 |
| LDA / Joint inner-selected sampler | 0.3588 ± 0.0574 | 0.3774 | 0.5272 | 0.3934 |
| Logistic Regression / None | 0.2975 ± 0.0467 | 0.2943 | 0.4999 | 0.3923 |
| Logistic Regression / ROS | 0.3432 ± 0.0531 | 0.3475 | 0.5205 | 0.3841 |
| Logistic Regression / Standard SMOTE (3/4/7/8) | 0.3453 ± 0.0532 | 0.3496 | 0.5212 | 0.3874 |
| Logistic Regression / SMOTE (4/7 only) | 0.2968 ± 0.0351 | 0.2978 | 0.5210 | 0.3940 |
| Logistic Regression / BorderlineSMOTE (4/7 only) | 0.2986 ± 0.0358 | 0.2996 | 0.5165 | 0.3876 |
| Logistic Regression / SMOTE + protected Tomek | 0.3446 ± 0.0505 | 0.3508 | 0.5205 | 0.3873 |
| Logistic Regression / Joint inner-selected sampler | 0.3406 ± 0.0500 | 0.3456 | 0.5198 | 0.3853 |

SD is population SD across 40 dependent outer folds. CSV evidence retains min/max and all supporting metrics. PR-AUC is macro OvR average precision from native class-aligned probabilities; rankings are not pooled across fitted folds.

## Paired comparisons against SMOTE

| Model / procedure | Reference | Mean Δ Macro F1 | SD of paired differences | Min / max Δ |
|---|---|---:|---:|---:|
| LDA / BorderlineSMOTE (4/7 only) | Standard SMOTE (3/4/7/8) | -0.0312 | 0.0515 | -0.1678 / +0.0526 |
| LDA / BorderlineSMOTE (4/7 only) | SMOTE (4/7 only) | -0.0061 | 0.0371 | -0.1152 / +0.0882 |
| LDA / Joint inner-selected sampler | Standard SMOTE (3/4/7/8) | -0.0078 | 0.0254 | -0.1147 / +0.0526 |
| LDA / None | Standard SMOTE (3/4/7/8) | -0.0108 | 0.0341 | -0.0886 / +0.0915 |
| LDA / ROS | Standard SMOTE (3/4/7/8) | -0.0100 | 0.0336 | -0.0851 / +0.0608 |
| LDA / SMOTE (4/7 only) | Standard SMOTE (3/4/7/8) | -0.0250 | 0.0574 | -0.1806 / +0.0714 |
| LDA / SMOTE + protected Tomek | Standard SMOTE (3/4/7/8) | +0.0000 | 0.0206 | -0.0401 / +0.0649 |
| Logistic Regression / BorderlineSMOTE (4/7 only) | Standard SMOTE (3/4/7/8) | -0.0468 | 0.0582 | -0.1772 / +0.0438 |
| Logistic Regression / BorderlineSMOTE (4/7 only) | SMOTE (4/7 only) | +0.0017 | 0.0170 | -0.0343 / +0.0442 |
| Logistic Regression / Joint inner-selected sampler | Standard SMOTE (3/4/7/8) | -0.0047 | 0.0369 | -0.1463 / +0.0916 |
| Logistic Regression / None | Standard SMOTE (3/4/7/8) | -0.0479 | 0.0435 | -0.1751 / +0.0210 |
| Logistic Regression / ROS | Standard SMOTE (3/4/7/8) | -0.0022 | 0.0341 | -0.1164 / +0.0713 |
| Logistic Regression / SMOTE (4/7 only) | Standard SMOTE (3/4/7/8) | -0.0485 | 0.0579 | -0.2214 / +0.0483 |
| Logistic Regression / SMOTE + protected Tomek | Standard SMOTE (3/4/7/8) | -0.0007 | 0.0330 | -0.0834 / +0.0916 |

BorderlineSMOTE’s primary method comparison is the matched 4/7-only SMOTE control. Comparing it with full SMOTE also changes which classes are augmented. These are paired estimates of complete tuning procedures, not an isolated causal sampler effect at identical selected settings.

## Minority precision, recall and F1

| Model / procedure | Quality | Precision | Recall | F1 | Mean false positives / fold | Zero-positive-prediction folds |
|---|---:|---:|---:|---:|---:|---:|
| LDA / None | 3 | 0.4487 | 0.3500 | 0.3671 | 1.18 | 2/40 |
| LDA / None | 4 | 0.1621 | 0.0409 | 0.0621 | 2.02 | 4/40 |
| LDA / None | 7 | 0.4570 | 0.4080 | 0.4270 | 16.32 | 0/40 |
| LDA / None | 8 | 0.1237 | 0.0646 | 0.0789 | 2.25 | 8/40 |
| LDA / ROS | 3 | 0.2988 | 0.3875 | 0.3093 | 2.05 | 0/40 |
| LDA / ROS | 4 | 0.1704 | 0.1073 | 0.1191 | 5.70 | 1/40 |
| LDA / ROS | 7 | 0.4341 | 0.4832 | 0.4525 | 21.60 | 0/40 |
| LDA / ROS | 8 | 0.1148 | 0.1000 | 0.0899 | 2.67 | 6/40 |
| LDA / Standard SMOTE (3/4/7/8) | 3 | 0.3524 | 0.4125 | 0.3400 | 2.25 | 0/40 |
| LDA / Standard SMOTE (3/4/7/8) | 4 | 0.1980 | 0.1052 | 0.1250 | 5.62 | 1/40 |
| LDA / Standard SMOTE (3/4/7/8) | 7 | 0.4335 | 0.4953 | 0.4588 | 22.12 | 0/40 |
| LDA / Standard SMOTE (3/4/7/8) | 8 | 0.1120 | 0.1354 | 0.1155 | 4.42 | 2/40 |
| LDA / SMOTE (4/7 only) | 3 | 0.2417 | 0.2125 | 0.2125 | 0.97 | 10/40 |
| LDA / SMOTE (4/7 only) | 4 | 0.1763 | 0.1291 | 0.1386 | 7.60 | 0/40 |
| LDA / SMOTE (4/7 only) | 7 | 0.4308 | 0.5176 | 0.4672 | 23.23 | 0/40 |
| LDA / SMOTE (4/7 only) | 8 | 0.1071 | 0.0583 | 0.0723 | 2.25 | 8/40 |
| LDA / BorderlineSMOTE (4/7 only) | 3 | 0.1937 | 0.1500 | 0.1592 | 0.85 | 14/40 |
| LDA / BorderlineSMOTE (4/7 only) | 4 | 0.1485 | 0.1789 | 0.1565 | 10.97 | 0/40 |
| LDA / BorderlineSMOTE (4/7 only) | 7 | 0.4256 | 0.5057 | 0.4574 | 23.57 | 0/40 |
| LDA / BorderlineSMOTE (4/7 only) | 8 | 0.1357 | 0.0729 | 0.0893 | 2.25 | 7/40 |
| LDA / SMOTE + protected Tomek | 3 | 0.3403 | 0.4125 | 0.3374 | 2.25 | 0/40 |
| LDA / SMOTE + protected Tomek | 4 | 0.1663 | 0.1477 | 0.1484 | 7.92 | 1/40 |
| LDA / SMOTE + protected Tomek | 7 | 0.4160 | 0.5309 | 0.4636 | 25.48 | 0/40 |
| LDA / SMOTE + protected Tomek | 8 | 0.1051 | 0.1333 | 0.1112 | 4.72 | 1/40 |
| LDA / Joint inner-selected sampler | 3 | 0.3382 | 0.3750 | 0.3191 | 1.73 | 2/40 |
| LDA / Joint inner-selected sampler | 4 | 0.1652 | 0.1248 | 0.1341 | 7.20 | 0/40 |
| LDA / Joint inner-selected sampler | 7 | 0.4247 | 0.5177 | 0.4628 | 24.00 | 0/40 |
| LDA / Joint inner-selected sampler | 8 | 0.0834 | 0.1021 | 0.0860 | 3.90 | 2/40 |
| Logistic Regression / None | 3 | 0.1792 | 0.1250 | 0.1408 | 0.47 | 20/40 |
| Logistic Regression / None | 4 | 0.1708 | 0.0191 | 0.0338 | 0.68 | 16/40 |
| Logistic Regression / None | 7 | 0.4841 | 0.2925 | 0.3603 | 10.60 | 0/40 |
| Logistic Regression / None | 8 | 0.0000 | 0.0000 | 0.0000 | 0.20 | 33/40 |
| Logistic Regression / ROS | 3 | 0.2646 | 0.3000 | 0.2692 | 1.30 | 7/40 |
| Logistic Regression / ROS | 4 | 0.1863 | 0.0673 | 0.0924 | 3.08 | 3/40 |
| Logistic Regression / ROS | 7 | 0.4448 | 0.3966 | 0.4146 | 16.75 | 0/40 |
| Logistic Regression / ROS | 8 | 0.0775 | 0.0667 | 0.0648 | 2.62 | 7/40 |
| Logistic Regression / Standard SMOTE (3/4/7/8) | 3 | 0.2850 | 0.3000 | 0.2735 | 1.27 | 8/40 |
| Logistic Regression / Standard SMOTE (3/4/7/8) | 4 | 0.1942 | 0.0605 | 0.0861 | 2.92 | 2/40 |
| Logistic Regression / Standard SMOTE (3/4/7/8) | 7 | 0.4393 | 0.4124 | 0.4218 | 17.80 | 0/40 |
| Logistic Regression / Standard SMOTE (3/4/7/8) | 8 | 0.0788 | 0.0792 | 0.0777 | 2.65 | 1/40 |
| Logistic Regression / SMOTE (4/7 only) | 3 | 0.0583 | 0.0375 | 0.0433 | 0.38 | 26/40 |
| Logistic Regression / SMOTE (4/7 only) | 4 | 0.1795 | 0.0723 | 0.0986 | 3.42 | 1/40 |
| Logistic Regression / SMOTE (4/7 only) | 7 | 0.4331 | 0.4243 | 0.4243 | 18.85 | 0/40 |
| Logistic Regression / SMOTE (4/7 only) | 8 | 0.0000 | 0.0000 | 0.0000 | 0.25 | 32/40 |
| Logistic Regression / BorderlineSMOTE (4/7 only) | 3 | 0.0583 | 0.0375 | 0.0433 | 0.35 | 27/40 |
| Logistic Regression / BorderlineSMOTE (4/7 only) | 4 | 0.1898 | 0.0864 | 0.1096 | 4.80 | 0/40 |
| Logistic Regression / BorderlineSMOTE (4/7 only) | 7 | 0.4342 | 0.4267 | 0.4251 | 18.82 | 0/40 |
| Logistic Regression / BorderlineSMOTE (4/7 only) | 8 | 0.0000 | 0.0000 | 0.0000 | 0.17 | 34/40 |
| Logistic Regression / SMOTE + protected Tomek | 3 | 0.2904 | 0.2750 | 0.2613 | 1.25 | 7/40 |
| Logistic Regression / SMOTE + protected Tomek | 4 | 0.1764 | 0.0748 | 0.0997 | 3.67 | 1/40 |
| Logistic Regression / SMOTE + protected Tomek | 7 | 0.4219 | 0.4542 | 0.4340 | 20.93 | 0/40 |
| Logistic Regression / SMOTE + protected Tomek | 8 | 0.0661 | 0.0813 | 0.0719 | 2.88 | 1/40 |
| Logistic Regression / Joint inner-selected sampler | 3 | 0.2729 | 0.2625 | 0.2500 | 1.12 | 10/40 |
| Logistic Regression / Joint inner-selected sampler | 4 | 0.1772 | 0.0745 | 0.1014 | 3.58 | 1/40 |
| Logistic Regression / Joint inner-selected sampler | 7 | 0.4282 | 0.4446 | 0.4317 | 20.10 | 0/40 |
| Logistic Regression / Joint inner-selected sampler | 8 | 0.0502 | 0.0646 | 0.0558 | 2.60 | 3/40 |

All six classes are retained in the notebook and per_class_comparison.csv. Precision uses zero_division=0 with undefined/no-prediction folds counted separately. Only two quality-3 and three–four quality-8 genuine wines occur in each outer validation fold.

## Recall–precision warning flags

Flags require a paired recall gain and either precision<.10 with positive predictions, or precision at most half a positive reference precision with increased false positives. They are descriptive and never alter inner selection. Zero-TP folds may have many false positives without a recall gain, so absence of flags is not evidence of acceptable precision. The full CSV contains every fold/class; the table below shows the new variants against their relevant controls.

| Procedure | Reference | Quality | Mean Δ recall | Mean Δ precision | Mean Δ FP | Low-precision flags | Halved-precision flags |
|---|---|---:|---:|---:|---:|---:|---:|
| LDA / BorderlineSMOTE (4/7 only) | SMOTE (4/7 only) | 3 | -0.0625 | -0.0479 | -0.12 | 0/40 | 0/40 |
| LDA / BorderlineSMOTE (4/7 only) | SMOTE (4/7 only) | 4 | +0.0498 | -0.0278 | +3.38 | 0/40 | 0/40 |
| LDA / BorderlineSMOTE (4/7 only) | SMOTE (4/7 only) | 7 | -0.0118 | -0.0052 | +0.35 | 0/40 | 0/40 |
| LDA / BorderlineSMOTE (4/7 only) | SMOTE (4/7 only) | 8 | +0.0146 | +0.0286 | +0.00 | 0/40 | 0/40 |
| LDA / SMOTE + protected Tomek | Standard SMOTE (3/4/7/8) | 3 | +0.0000 | -0.0121 | +0.00 | 0/40 | 0/40 |
| LDA / SMOTE + protected Tomek | Standard SMOTE (3/4/7/8) | 4 | +0.0425 | -0.0317 | +2.30 | 0/40 | 0/40 |
| LDA / SMOTE + protected Tomek | Standard SMOTE (3/4/7/8) | 7 | +0.0356 | -0.0176 | +3.35 | 0/40 | 0/40 |
| LDA / SMOTE + protected Tomek | Standard SMOTE (3/4/7/8) | 8 | -0.0021 | -0.0069 | +0.30 | 0/40 | 0/40 |
| Logistic Regression / BorderlineSMOTE (4/7 only) | SMOTE (4/7 only) | 3 | +0.0000 | +0.0000 | -0.03 | 0/40 | 0/40 |
| Logistic Regression / BorderlineSMOTE (4/7 only) | SMOTE (4/7 only) | 4 | +0.0141 | +0.0103 | +1.38 | 0/40 | 0/40 |
| Logistic Regression / BorderlineSMOTE (4/7 only) | SMOTE (4/7 only) | 7 | +0.0024 | +0.0011 | -0.03 | 0/40 | 0/40 |
| Logistic Regression / BorderlineSMOTE (4/7 only) | SMOTE (4/7 only) | 8 | +0.0000 | +0.0000 | -0.07 | 0/40 | 0/40 |
| Logistic Regression / SMOTE + protected Tomek | Standard SMOTE (3/4/7/8) | 3 | -0.0250 | +0.0054 | -0.03 | 0/40 | 0/40 |
| Logistic Regression / SMOTE + protected Tomek | Standard SMOTE (3/4/7/8) | 4 | +0.0143 | -0.0179 | +0.75 | 0/40 | 0/40 |
| Logistic Regression / SMOTE + protected Tomek | Standard SMOTE (3/4/7/8) | 7 | +0.0418 | -0.0174 | +3.12 | 0/40 | 0/40 |
| Logistic Regression / SMOTE + protected Tomek | Standard SMOTE (3/4/7/8) | 8 | +0.0021 | -0.0127 | +0.23 | 0/40 | 0/40 |

## Boundary stability and genuine support

Boundary geometry is identical across model families/candidates on the same training fold. The following table deduplicates those repeated audits, so counts describe unique training folds. Safe/danger/noise classification uses five neighbors on genuine scaled training rows. Borderline1 interpolates within class from danger anchors only.

| Fitting stage | Quality | Unique folds | Genuine count | Danger anchors | Noise anchors | Safe anchors | No-danger folds | Single-anchor folds |
|---|---:|---:|---:|---:|---:|---:|---:|
| inner_fit | 4 | 120 | 20–22 | 0–10 | 11–21 | 0–1 | 1 | 1 |
| inner_fit | 7 | 120 | 66–68 | 19–43 | 9–22 | 9–33 | 0 | 0 |
| outer_refit | 4 | 40 | 31–32 | 3–12 | 20–29 | 0 | 0 | 0 |
| outer_refit | 7 | 40 | 100–101 | 39–56 | 14–26 | 23–44 | 0 | 0 |

A skipped class is recorded as no generation, never replaced by ordinary SMOTE. Single/few anchors can amplify individual borderline wines even when total class support exceeds k. This is why qualities 3/8 were excluded from the boundary method rather than treating computable neighborhoods as reliable.

| Fitting stage | Tomek-cleaned quality | Genuine before | Genuine removed | Genuine retained | Removed fraction range |
|---|---:|---:|---:|---:|
| inner_fit | 5 | 230–231 | 21–52 | 179–209 | 9.1%–22.5% |
| inner_fit | 6 | 214 | 27–57 | 157–187 | 12.6%–26.6% |
| outer_refit | 5 | 345–346 | 43–65 | 281–303 | 12.4%–18.8% |
| outer_refit | 6 | 321 | 46–75 | 246–275 | 14.3%–23.4% |

All minority genuine and generated rows were preserved by cleaning. Retaining rare observations does not prove the deleted majority boundary information was unimportant. Separate CSV counts record genuine/duplicate/synthetic/removed/retained/final support for every fit. Added observations are not independent new wines.

## Runtime and selection

| Model | Inner search seconds | Six outer refits seconds | Outer scoring seconds |
|---|---:|---:|---:|
| LDA | 37.54 | 2.32 | 4.41 |
| Logistic Regression | 54.34 | 3.84 | 4.39 |

| Model / procedure | Inner fit+predict seconds | Outer fit seconds | Outer scoring seconds |
|---|---:|---:|---:|
| LDA / None | 0.80 | 0.22 | 0.74 |
| LDA / ROS | 1.77 | 0.25 | 0.73 |
| LDA / Standard SMOTE (3/4/7/8) | 6.39 | 0.47 | 0.74 |
| LDA / SMOTE (4/7 only) | 5.75 | 0.27 | 0.73 |
| LDA / BorderlineSMOTE (4/7 only) | 7.39 | 0.40 | 0.74 |
| LDA / SMOTE + protected Tomek | 10.65 | 0.71 | 0.73 |
| Logistic Regression / None | 1.40 | 0.48 | 0.73 |
| Logistic Regression / ROS | 3.05 | 0.54 | 0.73 |
| Logistic Regression / Standard SMOTE (3/4/7/8) | 10.07 | 0.60 | 0.73 |
| Logistic Regression / SMOTE (4/7 only) | 9.57 | 0.56 | 0.73 |
| Logistic Regression / BorderlineSMOTE (4/7 only) | 11.40 | 0.69 | 0.73 |
| Logistic Regression / SMOTE + protected Tomek | 14.07 | 0.98 | 0.74 |

Method-level inner time sums measured fit/predict components and excludes F1 calculation/aggregation overhead. Candidate budgets differ (1,2 or6 per method); runtime is not a budget-normalized speed comparison. Joint selection reuses these fits and is not counted twice.

Total measured experiment time: **112.60s (1.9 minutes)**, including audit/report overhead, on serial one-thread CPU execution. 6,480 inner fits + 480 outer refits = 6,960. No final all-development model was fitted.

| Model | Jointly selected method | Outer training folds |
|---|---|---:|
| LDA | BorderlineSMOTE (4/7 only) | 4/40 |
| LDA | ROS | 1/40 |
| LDA | Standard SMOTE (3/4/7/8) | 16/40 |
| LDA | SMOTE (4/7 only) | 8/40 |
| LDA | SMOTE + protected Tomek | 11/40 |
| Logistic Regression | BorderlineSMOTE (4/7 only) | 1/40 |
| Logistic Regression | ROS | 4/40 |
| Logistic Regression | Standard SMOTE (3/4/7/8) | 10/40 |
| Logistic Regression | SMOTE (4/7 only) | 2/40 |
| Logistic Regression | SMOTE + protected Tomek | 23/40 |

## Interpretation

**The additional variants did not show a clear descriptive Macro F1 improvement over their appropriate SMOTE controls.** Standard conservative SMOTE reached **0.3666 ± 0.0558 for LDA** and **0.3453 ± 0.0532 for Logistic Regression**. Protected SMOTE–Tomek reached **0.3666 ± 0.0549** and **0.3446 ± 0.0505**: paired mean changes of approximately **+0.00002** and **−0.00071**. These small mean differences do not establish equivalence or statistical significance; repeated folds overlap.

For BorderlineSMOTE, use the matched **4/7-only SMOTE** comparison. LDA changed from **0.3415 to 0.3354** (−0.0061), while Logistic Regression changed from **0.2968 to 0.2986** (+0.0017). Its larger gap from full SMOTE also changes whether qualities 3 and 8 are augmented, so that gap cannot be attributed solely to the boundary algorithm. ROS remained a useful simple reference (LDA **0.3566**, Logistic Regression **0.3432**). These reference procedures search only gentle/moderate profiles here; their numbers must not overwrite the earlier six-profile experiment.

**Some recall gains came with a substantial false-positive burden.** LDA BorderlineSMOTE raised quality-4 recall from **0.1291 to 0.1789**, but precision fell from **0.1763 to 0.1485**, and mean false positives rose from **7.60 to 10.98 per validation fold**, versus matched 4/7-only SMOTE. Against full SMOTE, two quality-4 folds met the predeclared recall-gain/precision-below-.10 flag; the matched-control comparison had no such flags. The increased false-positive burden remains material even without crossing that strict threshold.

Protected Tomek cleaning also traded precision for recall. For LDA quality 4, recall rose **0.1052 → 0.1477**, precision fell **0.1980 → 0.1663**, and mean false positives increased **5.63 → 7.93**. For Logistic Regression quality 7, recall rose **0.4124 → 0.4542**, precision fell **0.4393 → 0.4219**, and false positives increased **17.80 → 20.93**. Quality-8 precision remained poor: **0.1051 for LDA** and **0.0661 for Logistic Regression** under protected Tomek. These tradeoffs do not support treating higher recall alone as success. Neither protected-Tomek comparison crossed the strict paired collapse flags, which do not flag every poor-precision outcome.

The boundary diagnostics show why small-class caution matters even for qualities 4 and 7. Across **120 unique inner training folds**, quality 4 had **0–10 danger anchors**: one fold had none and one had only one. Most quality-4 wines were classified as noise (**11–21 per inner fold**); safe anchors numbered only **0–1**. Quality 7 had **19–43 danger anchors** and no zero/single-anchor cases. The no-danger fold received no synthetic quality-4 additions and was not omitted or replaced by standard SMOTE. This variability supports keeping the untested quality-3/8 boundary variants out of this study.

Protected cleaning preserved every genuine minority wine and every generated minority row, but removed **9.1–22.5% of genuine quality-5 rows** and **12.6–26.6% of quality-6 rows** in inner training fits. Thus even minority-protected cleaning can remove substantial training information. The unchanged Macro F1 gives no compelling reason here to add that cleaning step automatically. No removal thresholds or new sampling caps were tuned after seeing these results.

The joint inner-selected procedure reached **0.3588 ± 0.0574 for LDA** and **0.3406 ± 0.0500 for Logistic Regression**. It chose protected Tomek in **11/40** and **23/40** outer training sets, respectively; those choices were made exclusively from inner scores. More frequent inner selection did not translate into a clear outer advantage. No final model is promoted from the highest outer mean, no original holdout is accessed for evaluation, and ADASYN/SMOTEENN remain documented deferrals rather than measured failures.


## Evidence and validation

Notebook-local utilities, synthetic framework tests and guarded fresh-kernel execution verify training-only processing. Evidence validation reconstructs deterministic development folds, inner rankings, target counts, preserved/removed memberships, all outer metrics and paired comparisons. Deliberate evidence corruption tests exercise count, precision, cleaning-membership, boundary and selection checks.

Raw evidence: `tables/version_2/additional_imbalance_20261014/`. The immutable `plan.json` registers the design and `manifest.json` hashes saved outputs. Important tables include `metric_comparison.csv`, `per_class_comparison.csv`, `paired_smote_differences.csv`, `minority_precision_vs_smote.csv`, `sampling_counts.csv`, `boundary_audits.csv` and `runtime_by_family_fold.csv`. The method-review file documents deferred methods. Earlier notebook cells/results remain preserved; the original holdout was not evaluated.
