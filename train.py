"""Fit a separate fixed-recipe wine model, or evaluate a saved model on new labels."""

import argparse
import hashlib
import json
from importlib.metadata import version
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from imblearn.over_sampling import SMOTE
from imblearn.under_sampling import TomekLinks
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.metrics import accuracy_score, classification_report, cohen_kappa_score, f1_score, log_loss, mean_absolute_error
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

from predict import MODEL_PATH, load_model, predict_quality, validate_features


def fit_model(features, labels, recipe):
    """Scale real training rows, then apply the recorded gentle/k=1 sampler and LDA."""
    counts = labels.value_counts()
    targets = {}
    for quality in (3, 4, 7, 8):
        key = str(quality)
        caps = [int(np.ceil(recipe["sampling_profile"]["ratios"][key] * counts.max())),
                int(np.floor(recipe["sampling_profile"]["multipliers"][key] * counts[quality]))]
        if key in recipe["rare_absolute_caps"]:
            caps.append(recipe["rare_absolute_caps"][key])
        target = max(int(counts[quality]), min(caps))
        if target > counts[quality]:
            targets[quality] = target
    scaler = StandardScaler().fit(features)
    scaled = scaler.transform(features)
    if targets:
        sampled, sampled_labels = SMOTE(sampling_strategy=targets, k_neighbors=1, random_state=42).fit_resample(scaled, labels)
    else:
        sampled, sampled_labels = scaled, labels.to_numpy()
    cleaner = TomekLinks(sampling_strategy=recipe["cleaning_classes"], n_jobs=1)
    cleaned, cleaned_labels = cleaner.fit_resample(sampled, sampled_labels)
    if set(cleaned_labels) != set(recipe["classes"]):
        raise ValueError("Cleaning removed an entire quality class")
    classifier = LinearDiscriminantAnalysis(**recipe["hyperparameters"]).fit(cleaned, cleaned_labels)
    model = Pipeline([("scale", scaler), ("classifier", classifier)])
    audit = {
        "real_training_rows": len(labels), "synthetic_rows_added": len(sampled_labels) - len(labels),
        "rows_removed": len(sampled_labels) - len(cleaned_labels),
        "target_counts": {str(k): int(v) for k, v in targets.items()},
        "final_class_counts": {str(k): int(v) for k, v in pd.Series(cleaned_labels).value_counts().items()},
    }
    return model, audit


def wine_metrics(labels, scored, classes):
    predicted = scored.predicted_quality
    return {
        "macro_f1_all_six_classes": float(f1_score(labels, predicted, labels=classes, average="macro", zero_division=0)),
        "accuracy": float(accuracy_score(labels, predicted)),
        "mae_quality_points": float(mean_absolute_error(labels, predicted)),
        "within_one_accuracy": float((np.abs(labels.to_numpy() - predicted.to_numpy()) <= 1).mean()),
        "quadratic_weighted_kappa": float(cohen_kappa_score(labels, predicted, labels=classes, weights="quadratic")),
        "log_loss": float(log_loss(labels, scored[[f"probability_quality_{q}" for q in classes]], labels=classes)),
        "per_class": classification_report(labels, predicted, labels=classes, output_dict=True, zero_division=0),
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input_csv", type=Path, help="Eleven laboratory measurements plus quality=3..8")
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--model", type=Path, default=MODEL_PATH)
    parser.add_argument("--evaluate-only", action="store_true", help="Score all supplied labels without training or resampling")
    args = parser.parse_args()
    if args.output_dir.exists():
        parser.error("--output-dir must not already exist")
    reference_model, recipe = load_model(args.model)
    data = pd.read_csv(args.input_csv)
    if set(data.columns) != set(recipe["feature_columns"] + ["quality"]):
        raise ValueError("Expected exactly the eleven features and quality")
    features = data.loc[:, recipe["feature_columns"]]
    validate_features(features, recipe["feature_columns"])
    labels = pd.to_numeric(data.quality, errors="raise")
    if labels.isna().any() or not labels.isin(recipe["classes"]).all():
        raise ValueError("quality must contain integer labels from 3 through 8")
    labels = labels.astype(int)
    if features.duplicated().any():
        raise ValueError("Resolve duplicate/conflicting measurement records before splitting or evaluating")
    if labels.nunique() < 2:
        raise ValueError("Evaluation needs at least two observed quality classes")
    split = pd.Series("evaluation", index=data.index)
    if args.evaluate_only:
        test_indices = data.index.to_numpy()
        model = reference_model
    else:
        if set(labels) != set(recipe["classes"]) or labels.value_counts().min() < 5:
            raise ValueError("Training requires at least five real examples of each quality 3..8")
        train_indices, test_indices = train_test_split(data.index, test_size=0.2, stratify=labels, random_state=42)
        model, sampling_audit = fit_model(features.loc[train_indices], labels.loc[train_indices], recipe)
        split.loc[train_indices] = "train"
        split.loc[test_indices] = "test"
    scored = predict_quality(model, features.loc[test_indices])
    report = {
        "status": "evaluation_only" if args.evaluate_only else "candidate_not_promoted",
        "source_filename": args.input_csv.name,
        "source_sha256": hashlib.sha256(args.input_csv.read_bytes()).hexdigest(),
        "reference_model_sha256": hashlib.sha256(args.model.read_bytes()).hexdigest(),
        "split_counts": {str(k): int(v) for k, v in split.value_counts().items()},
        "test_metrics": wine_metrics(labels.loc[test_indices], scored, recipe["classes"]),
        "protocol": "No fitting" if args.evaluate_only else "Seed 42; stratified 80/20; all scaling, sampling and fitting on train only; fixed recipe; no search or final refit",
        "evaluation_note": "Data independence, measurement units and label comparability require source verification. Probabilities are not established calibrated confidence.",
        "versions": {name: version(name) for name in ["numpy", "pandas", "scikit-learn", "joblib", "imbalanced-learn"]},
    }
    if not args.evaluate_only:
        report["sampling_audit"] = sampling_audit
        majority = labels.loc[train_indices].mode().iloc[0]
        report["majority_baseline_macro_f1"] = float(f1_score(labels.loc[test_indices], np.full(len(test_indices), majority), labels=recipe["classes"], average="macro", zero_division=0))
    args.output_dir.mkdir(parents=True, exist_ok=False)
    if not args.evaluate_only:
        path = args.output_dir / "model.joblib"
        joblib.dump(model, path)
        metadata = {key: recipe[key] for key in ["feature_columns", "classes", "hyperparameters", "sampling_profile", "rare_absolute_caps", "cleaning_classes"]}
        metadata.update({
            "status": "candidate_not_promoted", "training_rows": len(train_indices),
            "model_sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
            "environment": {"versions": {name: version(name) for name in ["numpy", "scikit-learn", "joblib"]}},
            "recipe_note": "Fixed gentle/k=1 protected-Tomek LDA; see report.json for this candidate's own split and evaluation",
        })
        path.with_suffix(".metadata.json").write_text(json.dumps(metadata, indent=2) + "\n")
        restored, _ = load_model(path)
        np.testing.assert_allclose(predict_quality(restored, features.loc[test_indices]), scored, rtol=1e-12)
        report["model_sha256"] = metadata["model_sha256"]
    scored.assign(actual_quality=labels.loc[test_indices]).to_csv(args.output_dir / "evaluation_predictions.csv", index_label="source_row_index")
    split.rename("split").to_csv(args.output_dir / "split.csv", index_label="source_row_index")
    (args.output_dir / "report.json").write_text(json.dumps(report, indent=2, allow_nan=False) + "\n")
    print(f"Saved {report['status']} to {args.output_dir}")


if __name__ == "__main__":
    main()
