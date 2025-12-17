"""
Machine Learning Model for Public Speaking Analysis
Multi-output regression model to predict 8 expert-labeled scores
"""

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.linear_model import Ridge
from sklearn.multioutput import MultiOutputRegressor
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import joblib
import os
from pathlib import Path


class SpeechPredictor:
    """
    Multi-output regression model to predict public speaking scores
    """

    # Feature columns (what we use for prediction)
    FEATURE_COLUMNS = [
        'loud_mean', 'loud_std', 'pause_ratio', 'pitch_mean', 'pitch_std',
        'syllables_per_sec', 'spectral_centroid', 'spectral_rolloff',
        'words_per_minute', 'zcr_mean',
        'mfcc_1', 'mfcc_2', 'mfcc_3', 'mfcc_4', 'mfcc_5', 'mfcc_6',
        'mfcc_7', 'mfcc_8', 'mfcc_9', 'mfcc_10', 'mfcc_11', 'mfcc_12', 'mfcc_13',
        'spectral_bandwidth', 'spectral_flux', 'chroma_mean',
        'category_encoded'  # One-hot encoded category
    ]

    # Target columns (what we predict - expert labels 1-5)
    TARGET_COLUMNS = [
        'speech_pace',
        'pausing_fluency',
        'loudness_control',
        'pitch_variation',
        'articulation_clarity',
        'expressive_emphasis',
        'filler_words',
        'overall'
    ]

    def __init__(self, model_type='random_forest'):
        """
        Initialize the speech predictor

        Args:
            model_type: 'random_forest' or 'gradient_boosting'
        """
        self.model_type = model_type
        self.model = None
        self.scaler = StandardScaler()
        self.label_encoder = LabelEncoder()
        self.is_trained = False

    def _create_model(self):
        """Create the multi-output regression model"""
        if self.model_type == 'random_forest':
            base_model = RandomForestRegressor(
                n_estimators=200,
                max_depth=5,
                min_samples_split=10,
                min_samples_leaf=5,
                max_features='sqrt',
                random_state=42,
                n_jobs=-1
            )
        elif self.model_type == 'gradient_boosting':
            base_model = GradientBoostingRegressor(
                n_estimators=150,
                max_depth=3,
                min_samples_split=10,
                min_samples_leaf=5,
                learning_rate=0.05,
                subsample=0.8,
                random_state=42
            )
        elif self.model_type == 'ridge':
            base_model = Ridge(
                alpha=10.0,
                random_state=42
            )
        else:
            raise ValueError(f"Unknown model type: {self.model_type}")

        return MultiOutputRegressor(base_model)

    def preprocess_data(self, df):
        """
        Preprocess the dataset

        Args:
            df: pandas DataFrame with raw data

        Returns:
            X: Feature matrix
            y: Target matrix (if target columns exist)
        """
        df = df.copy()

        # Encode category (Informative, Motivational, Persuasive)
        if 'category' in df.columns:
            df['category_encoded'] = self.label_encoder.fit_transform(df['category'])

        # Handle missing words_per_minute (calculate from syllables_per_sec if needed)
        if 'words_per_minute' not in df.columns and 'syllables_per_sec' in df.columns:
            # Rough approximation: average word has ~1.5 syllables
            df['words_per_minute'] = df['syllables_per_sec'] * 60 / 1.5

        # Extract features
        X = df[self.FEATURE_COLUMNS].copy()

        # Fill any missing values with median
        X = X.fillna(X.median())

        # Extract targets if they exist
        y = None
        if all(col in df.columns for col in self.TARGET_COLUMNS):
            y = df[self.TARGET_COLUMNS].copy()

        return X, y

    def train(self, df, test_size=0.2, random_state=42):
        """
        Train the model on the dataset

        Args:
            df: pandas DataFrame with training data
            test_size: proportion of data to use for testing
            random_state: random seed

        Returns:
            dict: Training metrics
        """
        print("Preprocessing data...")
        X, y = self.preprocess_data(df)

        if y is None:
            raise ValueError("Dataset must contain target columns for training")

        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, random_state=random_state
        )

        print(f"Training set size: {X_train.shape[0]}")
        print(f"Test set size: {X_test.shape[0]}")

        # Scale features
        print("Scaling features...")
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)

        # Create and train model
        print(f"Training {self.model_type} model...")
        self.model = self._create_model()
        self.model.fit(X_train_scaled, y_train)
        self.is_trained = True

        # Evaluate
        print("Evaluating model...")
        y_pred_train = self.model.predict(X_train_scaled)
        y_pred_test = self.model.predict(X_test_scaled)

        # Clip predictions to valid range [1, 5]
        y_pred_train = np.clip(np.round(y_pred_train), 1, 5)
        y_pred_test = np.clip(np.round(y_pred_test), 1, 5)

        metrics = {
            'train_mae': mean_absolute_error(y_train, y_pred_train),
            'test_mae': mean_absolute_error(y_test, y_pred_test),
            'train_rmse': np.sqrt(mean_squared_error(y_train, y_pred_train)),
            'test_rmse': np.sqrt(mean_squared_error(y_test, y_pred_test)),
            'train_r2': r2_score(y_train, y_pred_train),
            'test_r2': r2_score(y_test, y_pred_test),
        }

        # Per-target metrics
        for i, target in enumerate(self.TARGET_COLUMNS):
            metrics[f'{target}_mae'] = mean_absolute_error(y_test.iloc[:, i], y_pred_test[:, i])
            metrics[f'{target}_r2'] = r2_score(y_test.iloc[:, i], y_pred_test[:, i])

        return metrics

    def predict(self, features_dict):
        """
        Predict scores for new speech data

        Args:
            features_dict: Dictionary with feature names and values

        Returns:
            dict: Predicted scores for each target
        """
        if not self.is_trained:
            raise ValueError("Model must be trained before prediction")

        # Convert to DataFrame
        df = pd.DataFrame([features_dict])

        # Preprocess
        X, _ = self.preprocess_data(df)

        # Scale
        X_scaled = self.scaler.transform(X)

        # Predict
        predictions = self.model.predict(X_scaled)[0]

        # Clip to valid range and round
        predictions = np.clip(np.round(predictions), 1, 5).astype(int)

        # Return as dictionary
        result = {
            target: int(pred)
            for target, pred in zip(self.TARGET_COLUMNS, predictions)
        }

        return result

    def save(self, save_dir):
        """Save the trained model and preprocessors"""
        save_dir = Path(save_dir)
        save_dir.mkdir(parents=True, exist_ok=True)

        joblib.dump(self.model, save_dir / 'model.joblib')
        joblib.dump(self.scaler, save_dir / 'scaler.joblib')
        joblib.dump(self.label_encoder, save_dir / 'label_encoder.joblib')
        joblib.dump({
            'model_type': self.model_type,
            'is_trained': self.is_trained
        }, save_dir / 'metadata.joblib')

        print(f"Model saved to {save_dir}")

    def load(self, load_dir):
        """Load a trained model and preprocessors"""
        load_dir = Path(load_dir)

        self.model = joblib.load(load_dir / 'model.joblib')
        self.scaler = joblib.load(load_dir / 'scaler.joblib')
        self.label_encoder = joblib.load(load_dir / 'label_encoder.joblib')

        metadata = joblib.load(load_dir / 'metadata.joblib')
        self.model_type = metadata['model_type']
        self.is_trained = metadata['is_trained']

        print(f"Model loaded from {load_dir}")

    def get_feature_importance(self):
        """
        Get feature importance scores (for Random Forest)

        Returns:
            DataFrame with feature importance
        """
        if not self.is_trained:
            raise ValueError("Model must be trained first")

        if self.model_type != 'random_forest':
            raise ValueError("Feature importance only available for Random Forest")

        # Get average importance across all output models
        importances = []
        for estimator in self.model.estimators_:
            importances.append(estimator.feature_importances_)

        avg_importance = np.mean(importances, axis=0)

        importance_df = pd.DataFrame({
            'feature': self.FEATURE_COLUMNS,
            'importance': avg_importance
        }).sort_values('importance', ascending=False)

        return importance_df
