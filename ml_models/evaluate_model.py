"""
Script to evaluate the trained model
"""

import pandas as pd
import numpy as np
import sys
from pathlib import Path
import json
import matplotlib.pyplot as plt
import seaborn as sns

sys.path.append(str(Path(__file__).parent.parent))

from ml_models.speech_predictor import SpeechPredictor


def evaluate_model(model_dir, dataset_path=None):
    """
    Evaluate the trained model

    Args:
        model_dir: Directory containing the trained model
        dataset_path: Optional path to evaluation dataset (if different from training)
    """
    print("=" * 60)
    print("MODEL EVALUATION")
    print("=" * 60)

    # Load model
    print(f"\nLoading model from: {model_dir}")
    predictor = SpeechPredictor()
    predictor.load(model_dir)

    # Load metrics if available
    metrics_path = Path(model_dir) / 'training_metrics.json'
    if metrics_path.exists():
        with open(metrics_path, 'r') as f:
            metrics = json.load(f)

        print("\n" + "=" * 60)
        print("TRAINING METRICS")
        print("=" * 60)
        print(f"\nOverall Performance:")
        print(f"  Test MAE:   {metrics['test_mae']:.4f}")
        print(f"  Test RMSE:  {metrics['test_rmse']:.4f}")
        print(f"  Test R²:    {metrics['test_r2']:.4f}")

        print(f"\nPer-Target Performance:")
        for target in predictor.TARGET_COLUMNS:
            mae = metrics.get(f'{target}_mae', 'N/A')
            r2 = metrics.get(f'{target}_r2', 'N/A')
            if mae != 'N/A':
                print(f"  {target:25s} - MAE: {mae:.4f}, R²: {r2:.4f}")

    # Test prediction with sample data
    print("\n" + "=" * 60)
    print("SAMPLE PREDICTION TEST")
    print("=" * 60)

    if dataset_path and Path(dataset_path).exists():
        df = pd.read_csv(dataset_path)
        sample = df.iloc[0].to_dict()

        print(f"\nTesting with sample: {sample.get('file', 'Unknown')}")
        print(f"Category: {sample.get('category', 'Unknown')}")

        # Make prediction
        predictions = predictor.predict(sample)

        print("\nPredicted Scores:")
        for metric, score in predictions.items():
            actual = sample.get(metric, 'N/A')
            print(f"  {metric:25s}: {score}/5  (Actual: {actual})")

    # Feature importance
    if predictor.model_type == 'random_forest':
        print("\n" + "=" * 60)
        print("TOP 15 MOST IMPORTANT FEATURES")
        print("=" * 60)
        importance_df = predictor.get_feature_importance()
        print(importance_df.head(15).to_string(index=False))

    print("\n" + "=" * 60)
    print("EVALUATION COMPLETE")
    print("=" * 60)


if __name__ == '__main__':
    BASE_DIR = Path(__file__).parent.parent
    MODEL_DIR = BASE_DIR / 'ml_models' / 'trained_models'
    DATASET_PATH = BASE_DIR / '..' / 'Speeches Dataset - Clean.csv'

    if not MODEL_DIR.exists():
        print(f"ERROR: Model not found at {MODEL_DIR}")
        print("Please train the model first using: python ml_models/train_model.py")
        sys.exit(1)

    evaluate_model(
        model_dir=str(MODEL_DIR),
        dataset_path=str(DATASET_PATH) if DATASET_PATH.exists() else None
    )
