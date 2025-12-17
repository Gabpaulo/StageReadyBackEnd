"""
Script to train the speech analysis model
"""

import pandas as pd
import sys
from pathlib import Path
import json

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

from ml_models.speech_predictor import SpeechPredictor


def train_model(dataset_path, model_dir, model_type='random_forest'):
    """
    Train the speech analysis model

    Args:
        dataset_path: Path to the CSV dataset
        model_dir: Directory to save the trained model
        model_type: 'random_forest' or 'gradient_boosting'
    """
    print("=" * 60)
    print("STAGE READY - Speech Coach Model Training")
    print("=" * 60)

    # Load dataset
    print(f"\nLoading dataset from: {dataset_path}")
    df = pd.read_csv(dataset_path)
    print(f"Dataset shape: {df.shape}")
    print(f"Columns: {list(df.columns)}\n")

    # Display dataset info
    print("Dataset Info:")
    print(f"  - Total samples: {len(df)}")
    print(f"  - Categories: {df['category'].value_counts().to_dict()}")
    print()

    # Check for missing values
    print("Missing values:")
    missing = df.isnull().sum()
    print(missing[missing > 0] if missing.any() else "  None")
    print()

    # Initialize and train model
    print(f"Initializing {model_type} model...")
    predictor = SpeechPredictor(model_type=model_type)

    print("\nTraining model...")
    metrics = predictor.train(df, test_size=0.2, random_state=42)

    # Display results
    print("\n" + "=" * 60)
    print("TRAINING RESULTS")
    print("=" * 60)
    print(f"\nOverall Metrics:")
    print(f"  Train MAE:  {metrics['train_mae']:.4f}")
    print(f"  Test MAE:   {metrics['test_mae']:.4f}")
    print(f"  Train RMSE: {metrics['train_rmse']:.4f}")
    print(f"  Test RMSE:  {metrics['test_rmse']:.4f}")
    print(f"  Train R²:   {metrics['train_r2']:.4f}")
    print(f"  Test R²:    {metrics['test_r2']:.4f}")

    print(f"\nPer-Target Performance (Test Set):")
    for target in predictor.TARGET_COLUMNS:
        mae = metrics[f'{target}_mae']
        r2 = metrics[f'{target}_r2']
        print(f"  {target:25s} - MAE: {mae:.4f}, R²: {r2:.4f}")

    # Feature importance (if Random Forest)
    if model_type == 'random_forest':
        print("\n" + "=" * 60)
        print("TOP 10 MOST IMPORTANT FEATURES")
        print("=" * 60)
        importance_df = predictor.get_feature_importance()
        print(importance_df.head(10).to_string(index=False))

    # Save model
    print(f"\n\nSaving model to: {model_dir}")
    predictor.save(model_dir)

    # Save metrics
    metrics_path = Path(model_dir) / 'training_metrics.json'
    with open(metrics_path, 'w') as f:
        json.dump(metrics, f, indent=2)
    print(f"Metrics saved to: {metrics_path}")

    print("\n" + "=" * 60)
    print("TRAINING COMPLETE!")
    print("=" * 60)

    return predictor, metrics


if __name__ == '__main__':
    # Default paths
    BASE_DIR = Path(__file__).parent.parent

    # Updated path to use the expanded dataset
    DATASET_PATH = BASE_DIR / '..' / 'StageReadyIonic' / 'Speeches_Dataset_Clean.csv'
    MODEL_DIR = BASE_DIR / 'ml_models' / 'trained_models'

    # Check if dataset exists
    if not DATASET_PATH.exists():
        print(f"ERROR: Dataset not found at {DATASET_PATH}")
        print("Please provide the correct path to the dataset.")
        sys.exit(1)

    # Train model with expanded dataset
    train_model(
        dataset_path=str(DATASET_PATH),
        model_dir=str(MODEL_DIR),
        model_type='random_forest'  # Best performer on this dataset
    )
