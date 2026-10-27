# Independent Version 2 freeze metrics audit

All 12 Version 2 experiment manifests (229 file hashes) verified. Independently rebuilt 3350 fold/model confusion matrices and manually recalculated six-class Macro F1, Balanced Accuracy, QWK, accuracy, MAE and ±1 accuracy wherever stored. No fits, raw-data access or historical holdout reads.

Recommended procedure: `lda__smote_tomek_protected`. Macro F1 0.3665871810 ± 0.0548737400. Fold-mean six-class F1: [0.337420634920635, 0.14843656431005928, 0.6739882329260929, 0.4649538036902617, 0.4635532153826686, 0.11117063492063492]; their mean 0.3665871810.

Pooled repeated OOF Macro F1 is 0.3645925406; pooled per-class F1 [0.3251231527093596, 0.15519399249061328, 0.6741712279252298, 0.46562786434463793, 0.4636926082709215, 0.1037463976945245]. These are distinct from the mean of 40 fold scores. OOF rows 10,870 = 1,087 unique wines × 10 repeats.

Pooled confusion matrix (rows=true; columns=predicted; class order 3,4,5,6,7,8):
```
[[  33   15   32    0    0    0]
 [  20   62  195  122   18    3]
 [  63  164 3264  963  139   17]
 [   7  120 1500 1778  781   94]
 [   0   17   82  454  712   75]
 [   0    1    0   40   81   18]]
```

True repeated counts [80, 420, 4610, 4280, 1340, 140]; predicted counts [123, 379, 5073, 3357, 1731, 207].

Capped SMOTE paired difference +0.000019; positive 20/40 folds, 5/10 repeat means. Do not claim established superiority.

## Caveats
- Headline standard deviation and variance use ddof=0, consistent with saved project summaries. Sample ddof=1 values are provided separately; neither is a confidence interval.
- The arithmetic mean of per-class fold-mean F1 exactly reconstructs reported mean fold Macro F1. A summed confusion matrix reconstructs pooled repeated OOF F1, a different aggregation. Both must be labelled separately.
- 10,870 OOF rows represent 1,087 distinct development wines each predicted in ten repetitions, not 10,870 independent observations.
- Repeated folds overlap in training and reuse observations: fold SD is split variability, not a standard error or confidence interval.
- The nested result estimates inner selection of capped sampler profile/k within the protected-Tomek procedure. Final full-development fit is an artifact of the procedure; it does not obtain a new independent validation score.
- Across-study model-family selection repeatedly consulted the same development validation. Report as development-CV estimate subject to model-selection optimism, not fresh external validation.
- No raw-data duplicate/target-feature inspection was performed by this read-only metrics audit; parent audit must address feature-identical rows and data lineage.

CV stability LDA+SMOTE 5-fold x10 has Macro F1 0.370179 versus adopted4x10 0.363380. Fivefold design was rejected for poorer rare-class validation support; choosing it now for higher score would cherry-pick validation. Champion ranking uses pre-adopted4x10.

The proposed final recipe is chosen by aggregate already recorded inner scores (gentle k=1) without new search. This deterministic final artifact selection differs from refitting the inner search anew on all development data; its exact fixed-recipe CV performance has not been separately estimated. Retain the nested procedure score as provenance, never as direct validation of the frozen fixed artifact.
