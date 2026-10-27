# Champion interpretation run report

Completed 2026-10-11 17:21:46 +04. Selected configuration:
`lda__smote`; selection run
`5096bbc9-6dc2-47bc-8ee6-85c4114da6e0`.

## Scope and method

Explained the existing fitted LDA champion using **1087 original
development observations**. The full original development set is the SHAP
background; no synthetic SMOTE rows or final-test observations are used. No model,
scaler, sampler, feature set, threshold or hyperparameter was fitted or changed.

Three complementary views are saved:

1. **Class-centered standardized coefficients.** Subtract the unweighted mean
   class coefficient/intercept from each class. This removes score components
   shared by every class and preserves all score differences, labels and softmax
   probabilities. A coefficient describes a class-score change per fitted training
   standard deviation, with other inputs fixed in the model.
2. **Exact analytic linear SHAP.** The marginal-background attribution is
   `centered_coefficient × (standardized_value − development_background_mean)`.
   Baseline plus contributions reconstructs each centered class score. This
   follows the [SHAP linear-explainer definition](https://shap.readthedocs.io/en/latest/generated/shap.LinearExplainer.html).
   It explains discriminant scores, **not probability-point contributions**.
   The optional `shap` library is absent; the closed form is implemented directly
   and tested against independent enumeration of the Shapley game. No dependency
   versions were changed.
3. **Permutation importance.** Twenty seed-42 shuffles per feature measure the
   decrease in training Macro F1. This is descriptive dependence on training
   observations, not another validation result. Permutation SD is not a confidence
   interval. The [scikit-learn guidance](https://scikit-learn.org/stable/modules/permutation_importance.html) explains the
   scoring and correlated-predictor limitations.

Global SHAP averages absolute contributions over all development observations and
six equally weighted class scores. Each SHAP panel contains every development
wine, not only wines of the named true class. Colors encode within-feature value
percentiles; class-panel horizontal scales differ and their numerical ticks must
be read when comparing magnitudes. The coefficient heatmap retains signs and all
six original quality labels.

**Importance describes this model's dependence/association, not causality. Changing a chemical property does not necessarily cause wine quality to change.**

## Measured global findings

| Feature | Mean absolute score SHAP | Training Macro F1 permutation drop | Permutation SD |
|---|---:|---:|---:|
| volatile acidity | 0.7077 | 0.0870 | 0.0138 |
| alcohol | 0.6012 | 0.0802 | 0.0116 |
| citric acid | 0.3630 | 0.0010 | 0.0090 |
| density | 0.3278 | 0.0494 | 0.0135 |
| sulphates | 0.3254 | 0.0136 | 0.0088 |
| pH | 0.2692 | 0.0081 | 0.0073 |
| free sulfur dioxide | 0.2194 | -0.0009 | 0.0088 |
| total sulfur dioxide | 0.1932 | 0.0084 | 0.0107 |
| residual sugar | 0.1259 | 0.0295 | 0.0074 |
| fixed acidity | 0.0980 | 0.0110 | 0.0115 |
| chlorides | 0.0936 | -0.0037 | 0.0042 |

Volatile acidity and alcohol lead both summaries. In the fixed classifier, higher
volatile acidity raises the quality-3 centered score and lowers quality-7/8
scores; higher alcohol raises quality-7/8 scores. These are associations in this
specific trained model. They are not recommendations to alter wine chemistry.

Citric acid has a sizeable contribution to class scores but very little unique
training Macro F1 sensitivity under single-feature shuffling. This can reflect
both correlated inputs and the distinction between a score change and crossing a
classification boundary; this analysis does not isolate a cause. In development
data its Spearman correlation with fixed acidity is
0.679,
and with volatile acidity it is
-0.603.
Low/negative permutation drops are retained and do not trigger feature removal.

## Three local explanations

The original rows were sampled uniformly with seed 42 **before** inspecting
predictions, confidence or errors. No favorable-example filtering occurred.
The contrast is the predicted class versus its runner-up; its baseline plus all
11 feature contributions equals the model log probability ratio.

- Source row **136**: observed quality **5**, predicted **5** (model probability 0.630), runner-up **6** (0.225). The largest positive contribution to this contrast is **alcohol** (+0.696); the largest negative contribution is **sulphates** (-0.258). Baseline -0.166 plus all feature contributions 1.196 gives a final log-odds margin of 1.030.
- Source row **1044**: observed quality **6**, predicted **7** (model probability 0.502), runner-up **6** (0.258). The largest positive contribution to this contrast is **alcohol** (+1.456); the largest negative contribution is **fixed acidity** (-0.342). Baseline -1.880 plus all feature contributions 2.546 gives a final log-odds margin of 0.666.
- Source row **1225**: observed quality **5**, predicted **5** (model probability 0.823), runner-up **6** (0.149). The largest positive contribution to this contrast is **alcohol** (+0.769); the largest negative contribution is **volatile acidity** (-0.203). Baseline -0.166 plus all feature contributions 1.875 gives a final log-odds margin of 1.709.

These are illustrative training examples. Row 1044 is misclassified, showing that
a coherent additive explanation does not establish that a prediction is correct.
Probabilities are model outputs, not independently calibrated confidence levels.

## Artifacts and execution

- [Global importance table](/Users/shivsharma/Documents/projects/Finesse-Project3/tables/global_feature_importance.csv) and [figure](/Users/shivsharma/Documents/projects/Finesse-Project3/visuals/global_feature_importance.png).
- [Class coefficient heatmap](/Users/shivsharma/Documents/projects/Finesse-Project3/visuals/lda_coefficient_heatmap.png) and [coefficient table](/Users/shivsharma/Documents/projects/Finesse-Project3/tables/lda_feature_coefficients.csv).
- [Six-class SHAP summary](/Users/shivsharma/Documents/projects/Finesse-Project3/visuals/shap_summary.png), per-class magnitudes and all 6,522 observation/class decompositions.
- [Local explanation figure](/Users/shivsharma/Documents/projects/Finesse-Project3/visuals/local_prediction_explanations.png), summary table and 33 feature contributions.
- Supporting background, development membership, original class support, feature correlations, baseline scores, permutation repetitions, runtime and hashed provenance manifest.

The four 300-dpi figures were visually inspected and have readable titles, axes,
class labels, legends and caveats. All generated Matplotlib figures are closed.
Native thread pools were limited to one; runtime depends on hardware and software.

Measured stages: coefficient/SHAP validation
0.016 s; permutation
0.473 s; plotting
2.278 s. Total interpretation was
2.930 s before final runtime/manifest
writes. Six notebook cells plus one temporary execution-guard cell ran in
5.440 s including kernel/client overhead.
This is not a top-to-bottom notebook duration. Earlier benchmarking/timing results
were not rewritten.

## Checks run

- `python -m unittest discover -s tests -p 'test_interpretation.py' -v`: **7 tests passed**, all on temporary synthetic data.
- Exact linear SHAP matched exhaustive coalition/permutation enumeration; coefficient centering preserved predictions under an arbitrary common class-score shift.
- Tests cover explicit original-class order, invalid arrays/schema/algorithm rejection, unchanged fitted state, no fitting/resampling, deterministic sampling, local margin reconstruction and cached artifact integrity/tamper detection.
- The real notebook execution temporarily patched fitting, scaler fitting, LDA fitting, resampling, test parsing and final-test evaluation to fail immediately if called; no guard fired.
- All 6,522 saved centered class scores reconstruct from their baseline and feature contributions. Maximum in-memory score additivity error: 3.55e-15; maximum probability reconstruction error: 8.88e-16.
- Independently reconciled saved global/class SHAP summaries, coefficient magnitudes, all permutation means/SDs and the three local predicted-versus-runner-up log-odds margins.
- All 1,087 explanation/background source IDs equal the locked development partition and are disjoint from test IDs; the three local IDs exactly match the seed-42 sampling rule.
- Fresh-process replay from `notebook/` succeeded with data loading, explanation generation, fitting and prediction disabled; no artifact bytes changed.
- Notebook schema valid; six executed interpretation cells, four embedded figures, zero errors. Every pre-existing fitted model, metadata file, source module, dataset/split/selection lock, final-test artifact, runtime table and Telco reference notebook remains byte-identical.

## Warnings and limitations

- These are training explanations, not unbiased generalization evidence. Background choice and equal class weighting influence global summaries.
- Correlated chemical measurements can share or mask reliance. Marginal SHAP and single-feature shuffling ignore conditional dependence and can describe implausible combinations.
- SMOTE affected learned coefficients and priors. Only **8** real quality-3 and **14** real quality-8 wines occur in development; their patterns are unstable.
- SHAP values explain centered class scores; local contrasts explain model log-odds, not causal effects or calibrated confidence. There is no claim that modifying a measured property changes actual quality.
- Synthetic plotting emitted Seaborn's `set_bad` pending-deprecation warning. Jupyter emitted a local TCP-without-encryption transport warning. Neither prevented successful execution.
- The `shap` package is uninstalled, but exact analytic SHAP is complete and verified; no required output was skipped. No unresolved implementation failures remain. No later project phase was started.

## Files changed

Modified (2):

- [README.md](/Users/shivsharma/Documents/projects/Finesse-Project3/README.md)
- [notebook/Wine-Quality-Classification.ipynb](/Users/shivsharma/Documents/projects/Finesse-Project3/notebook/Wine-Quality-Classification.ipynb)

Created (21):

- [src/wine_quality/interpretation.py](/Users/shivsharma/Documents/projects/Finesse-Project3/src/wine_quality/interpretation.py)
- [tables/global_feature_importance.csv](/Users/shivsharma/Documents/projects/Finesse-Project3/tables/global_feature_importance.csv)
- [tables/interpretation_background.csv](/Users/shivsharma/Documents/projects/Finesse-Project3/tables/interpretation_background.csv)
- [tables/interpretation_class_support.csv](/Users/shivsharma/Documents/projects/Finesse-Project3/tables/interpretation_class_support.csv)
- [tables/interpretation_development_rows.csv](/Users/shivsharma/Documents/projects/Finesse-Project3/tables/interpretation_development_rows.csv)
- [tables/interpretation_feature_correlations.csv](/Users/shivsharma/Documents/projects/Finesse-Project3/tables/interpretation_feature_correlations.csv)
- [tables/lda_class_baselines.csv](/Users/shivsharma/Documents/projects/Finesse-Project3/tables/lda_class_baselines.csv)
- [tables/lda_feature_coefficients.csv](/Users/shivsharma/Documents/projects/Finesse-Project3/tables/lda_feature_coefficients.csv)
- [tables/local_feature_contributions.csv](/Users/shivsharma/Documents/projects/Finesse-Project3/tables/local_feature_contributions.csv)
- [tables/local_prediction_explanations.csv](/Users/shivsharma/Documents/projects/Finesse-Project3/tables/local_prediction_explanations.csv)
- [tables/model_interpretation_manifest.json](/Users/shivsharma/Documents/projects/Finesse-Project3/tables/model_interpretation_manifest.json)
- [tables/model_interpretation_run_report.md](/Users/shivsharma/Documents/projects/Finesse-Project3/tables/model_interpretation_run_report.md)
- [tables/model_interpretation_runtime.csv](/Users/shivsharma/Documents/projects/Finesse-Project3/tables/model_interpretation_runtime.csv)
- [tables/permutation_importance_repeats.csv](/Users/shivsharma/Documents/projects/Finesse-Project3/tables/permutation_importance_repeats.csv)
- [tables/shap_development_values.csv](/Users/shivsharma/Documents/projects/Finesse-Project3/tables/shap_development_values.csv)
- [tables/shap_global_by_class.csv](/Users/shivsharma/Documents/projects/Finesse-Project3/tables/shap_global_by_class.csv)
- [tests/test_interpretation.py](/Users/shivsharma/Documents/projects/Finesse-Project3/tests/test_interpretation.py)
- [visuals/global_feature_importance.png](/Users/shivsharma/Documents/projects/Finesse-Project3/visuals/global_feature_importance.png)
- [visuals/lda_coefficient_heatmap.png](/Users/shivsharma/Documents/projects/Finesse-Project3/visuals/lda_coefficient_heatmap.png)
- [visuals/local_prediction_explanations.png](/Users/shivsharma/Documents/projects/Finesse-Project3/visuals/local_prediction_explanations.png)
- [visuals/shap_summary.png](/Users/shivsharma/Documents/projects/Finesse-Project3/visuals/shap_summary.png)
