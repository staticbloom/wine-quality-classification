"""Predict wine quality from a CSV using the saved Version 2 scaler and LDA model."""

from __future__ import annotations

import argparse
import hashlib
import json
from importlib.metadata import version
from pathlib import Path

import joblib
import numpy as np
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parent
MODEL_PATH = PROJECT_ROOT / "models/final/wine_quality_classifier_v2.joblib"
METADATA_PATH = MODEL_PATH.with_suffix(".metadata.json")
LOCK_PATH = MODEL_PATH.parent / "version2_freeze_lock.json"


def load_model(model_path=MODEL_PATH):
    """Check the saved release and serialization versions before loading it."""
    model_path = Path(model_path).resolve()
    metadata_path = model_path.with_suffix(".metadata.json")
    metadata = json.loads(metadata_path.read_text())
    if model_path == MODEL_PATH.resolve():
        lock = json.loads(LOCK_PATH.read_text())
        for path in (model_path, metadata_path):
            relative = path.relative_to(PROJECT_ROOT).as_posix()
            if hashlib.sha256(path.read_bytes()).hexdigest() != lock["files"][relative]:
                raise ValueError(f"Frozen artifact checksum mismatch: {relative}")
    elif hashlib.sha256(model_path.read_bytes()).hexdigest() != metadata["model_sha256"]:
        raise ValueError("Model checksum does not match companion metadata")
    for package, expected in metadata["environment"]["versions"].items():
        installed = version(package)
        if installed != expected:
            raise ValueError(f"{package}: expected {expected}, found {installed}")

    model = joblib.load(model_path)
    if list(model.feature_names_in_) != metadata["feature_columns"]:
        raise ValueError("Model feature columns do not match the metadata")
    if list(model.classes_) != metadata["classes"]:
        raise ValueError("Model classes do not match the metadata")
    return model, metadata


def validate_features(wines, expected_columns):
    """Check the source schema without learning preprocessing from scoring rows."""
    if (
        not isinstance(wines, pd.DataFrame)
        or wines.empty
        or list(wines.columns) != expected_columns
    ):
        raise ValueError(
            "Supply a nonempty CSV with exactly these columns in order: "
            + ", ".join(expected_columns)
        )
    if not all(pd.api.types.is_numeric_dtype(dtype) for dtype in wines.dtypes):
        raise ValueError("Feature values must be numeric")
    if not np.isfinite(wines.to_numpy(dtype=float)).all():
        raise ValueError("Feature values must be finite and complete")
    if (wines < 0).any().any() or (wines["density"] <= 0).any():
        raise ValueError("Measurements must be nonnegative and density must be positive")
    if not wines["pH"].between(0, 14).all() or not wines["alcohol"].between(0, 100).all():
        raise ValueError("Use pH on the 0–14 scale and alcohol as percent by volume")


def predict_quality(model, wines):
    """Score the eleven finite numeric features in the saved model's column order."""
    validate_features(wines, list(model.feature_names_in_))
    predictions = model.predict(wines)
    probabilities = model.predict_proba(wines)
    results = pd.DataFrame({"predicted_quality": predictions}, index=wines.index)
    for column, quality in enumerate(model.classes_):
        results[f"probability_quality_{quality}"] = probabilities[:, column]
    return results


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input_csv", type=Path, help="CSV with the eleven input features, without quality")
    parser.add_argument("--model", type=Path, default=MODEL_PATH, help="Trusted model with companion .metadata.json")
    parser.add_argument(
        "--output", type=Path,
        help="Prediction CSV path; defaults beside the input file",
    )
    args = parser.parse_args()
    input_path = args.input_csv.resolve()
    output_path = (
        args.output.resolve()
        if args.output
        else input_path.with_name(f"{input_path.stem}_predictions.csv")
    )
    if output_path.exists():
        parser.error("Choose a new output path; existing files are not overwritten")

    wines = pd.read_csv(input_path)
    model, _ = load_model(args.model)
    results = predict_quality(model, wines)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    results.to_csv(output_path, index=False)
    print(f"Scored {len(results)} wine(s). Rows retain the input order.")
    print(f"Predictions: {output_path}")


if __name__ == "__main__":
    main()
