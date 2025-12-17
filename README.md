# Stage Ready - Public Speaking Coach Backend

A Django REST API backend with Machine Learning capabilities for analyzing and coaching public speaking performances.

## Overview

This backend uses a **Multi-output Random Forest Regressor** to predict 8 expert-labeled speech quality metrics (scored 1-5):

1. **Speech Pace** - Speaking rate and rhythm
2. **Pausing Fluency** - Strategic use of pauses
3. **Loudness Control** - Volume projection and modulation
4. **Pitch Variation** - Vocal variety and intonation
5. **Articulation Clarity** - Pronunciation and enunciation
6. **Expressive Emphasis** - Emotional impact and conviction
7. **Filler Words** - Minimization of "um", "uh", etc.
8. **Overall** - General speaking quality

## Features Used by the ML Model

### Audio Features (26 total)
The model uses the following features extracted from audio:

#### Acoustic Features (10)
- `loud_mean` - Average loudness/volume
- `loud_std` - Loudness variation
- `pause_ratio` - Proportion of silence/pauses
- `pitch_mean` - Average pitch/frequency
- `pitch_std` - Pitch variation
- `syllables_per_sec` - Speaking rate
- `spectral_centroid` - Brightness of sound
- `spectral_rolloff` - Frequency rolloff
- `words_per_minute` - Speech tempo
- `zcr_mean` - Zero-crossing rate (voice quality)

#### MFCC Features (13)
- `mfcc_1` through `mfcc_13` - Mel-frequency cepstral coefficients (voice timber/quality)

#### Spectral Features (3)
- `spectral_bandwidth` - Frequency range
- `spectral_flux` - Spectral change rate
- `chroma_mean` - Pitch class distribution

#### Categorical Feature (1)
- `category` - Speech type (Informative/Motivational/Persuasive)

## Project Structure

```
backend/
├── stage_ready_api/          # Django project settings
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── speech_coach/             # Main Django app
│   ├── models.py            # Database models
│   ├── views.py             # API endpoints
│   ├── serializers.py       # Data serialization
│   ├── urls.py              # URL routing
│   └── admin.py             # Admin interface
├── ml_models/               # Machine Learning components
│   ├── speech_predictor.py  # ML model class
│   ├── train_model.py       # Training script
│   ├── evaluate_model.py    # Evaluation script
│   └── trained_models/      # Saved models (created after training)
├── data/                    # Dataset storage
├── requirements.txt         # Python dependencies
└── manage.py               # Django management script
```

## Setup Instructions

### 1. Create Virtual Environment

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**Linux/Mac:**
```bash
python -m venv venv
source venv/bin/activate
```

### 2. Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 3. Copy Dataset

Copy your `Speeches Dataset - Clean.csv` to the parent directory or update the path in `ml_models/train_model.py`.

### 4. Run Database Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Create Superuser (Optional)

```bash
python manage.py createsuperuser
```

### 6. Train the ML Model

```bash
python ml_models/train_model.py
```

This will:
- Load and preprocess the dataset
- Train a Random Forest model
- Evaluate performance
- Save the model to `ml_models/trained_models/`
- Display training metrics and feature importance

Expected performance:
- Test MAE: ~0.4-0.6 (on 1-5 scale)
- Test R²: ~0.6-0.8

### 7. Start Development Server

```bash
python manage.py runserver
```

The API will be available at `http://localhost:8000/`

## API Endpoints

### 1. Predict Speech Scores

**POST** `/api/speech-analysis/predict/`

Predict speech quality scores from audio features.

**Request Body:**
```json
{
  "category": "Informative",
  "loud_mean": 0.058551233,
  "loud_std": 0.07518595,
  "pause_ratio": 0.4089003431,
  "pitch_mean": 1407.3585,
  "pitch_std": 1014.5365,
  "syllables_per_sec": 4.416152642,
  "spectral_centroid": 4035.090042,
  "spectral_rolloff": 5335.657051,
  "words_per_minute": 150.5,
  "zcr_mean": 0.151318313,
  "mfcc_1": -412.73087,
  "mfcc_2": 65.27368,
  "mfcc_3": -1.3047426,
  "mfcc_4": 4.3274055,
  "mfcc_5": -4.424483,
  "mfcc_6": -4.7077556,
  "mfcc_7": -12.42341,
  "mfcc_8": -16.618635,
  "mfcc_9": -6.161702,
  "mfcc_10": -9.071879,
  "mfcc_11": -4.622205,
  "mfcc_12": -0.75195116,
  "mfcc_13": -1.7746159,
  "spectral_bandwidth": 1677.216022,
  "spectral_flux": 0.94476503,
  "chroma_mean": 0.32123125,
  "file_name": "my_speech.mp3"
}
```

**Response:**
```json
{
  "speech_pace": 3,
  "pausing_fluency": 4,
  "loudness_control": 4,
  "pitch_variation": 2,
  "articulation_clarity": 3,
  "expressive_emphasis": 2,
  "filler_words": 5,
  "overall": 3,
  "feedback": {
    "overall_assessment": "Average performance - Room for growth",
    "detailed_scores": {
      "speech_pace": {
        "score": 3,
        "description": "Adequate pace - could be improved"
      },
      // ... other scores
    }
  },
  "recommendations": [
    {
      "category": "Pitch Variation",
      "issue": "Limited vocal variety",
      "suggestion": "Practice varying your pitch to emphasize key words. Avoid monotone delivery."
    },
    // ... other recommendations
  ]
}
```

### 2. Get Model Information

**GET** `/api/speech-analysis/model_info/`

Get information about the loaded ML model.

**Response:**
```json
{
  "model_type": "random_forest",
  "is_trained": true,
  "features": ["loud_mean", "loud_std", ...],
  "targets": ["speech_pace", "pausing_fluency", ...],
  "feature_importance": [
    {"feature": "pitch_mean", "importance": 0.125},
    {"feature": "loud_mean", "importance": 0.098},
    // ...
  ]
}
```

### 3. Speech Analysis CRUD

**GET** `/api/speech-analysis/` - List all analyses
**POST** `/api/speech-analysis/` - Create new analysis
**GET** `/api/speech-analysis/{id}/` - Get specific analysis
**PUT** `/api/speech-analysis/{id}/` - Update analysis
**DELETE** `/api/speech-analysis/{id}/` - Delete analysis

## Model Training Details

### Algorithm: Multi-Output Random Forest Regressor

**Why this approach?**

1. **Multi-Output Regression**: Predicts all 8 scores simultaneously, capturing correlations between metrics
2. **Random Forest**: Handles non-linear relationships, robust to outliers, provides feature importance
3. **Excellent for Small Datasets**: Works well with ~150 samples due to ensemble approach

### Configuration

```python
RandomForestRegressor(
    n_estimators=100,      # 100 decision trees
    max_depth=15,          # Prevent overfitting
    min_samples_split=5,   # Conservative splitting
    min_samples_leaf=2,    # Minimum samples per leaf
    random_state=42        # Reproducibility
)
```

### Data Preprocessing

1. **Category Encoding**: Label encoding for speech category
2. **Feature Scaling**: StandardScaler for all numeric features
3. **Missing Value Handling**: Median imputation
4. **Train/Test Split**: 80/20 split

### Model Performance Metrics

The model is evaluated using:
- **MAE (Mean Absolute Error)**: Average prediction error (lower is better)
- **RMSE (Root Mean Squared Error)**: Penalizes larger errors (lower is better)
- **R² Score**: Proportion of variance explained (higher is better, max 1.0)

Expected results on test set:
- Overall MAE: 0.4-0.6 (on 1-5 scale)
- Overall R²: 0.6-0.8
- Per-target MAE varies by metric complexity

## Evaluation and Testing

### Evaluate the Model

```bash
python ml_models/evaluate_model.py
```

This shows:
- Training and test set metrics
- Per-target performance
- Feature importance ranking
- Sample predictions

### Test API with cURL

```bash
# Get model info
curl http://localhost:8000/api/speech-analysis/model_info/

# Make prediction (use actual feature values)
curl -X POST http://localhost:8000/api/speech-analysis/predict/ \
  -H "Content-Type: application/json" \
  -d @sample_features.json
```

## Integration with Ionic Frontend

### CORS Configuration

The backend is configured to accept requests from your Ionic app (see `settings.py`).

For production, update:
```python
CORS_ALLOW_ALL_ORIGINS = False
CORS_ALLOWED_ORIGINS = [
    "http://localhost:8100",  # Ionic dev server
    "https://your-app.com",   # Production URL
]
```

### Recommended Workflow

1. **Audio Recording**: User records speech in Ionic app
2. **Feature Extraction**: Extract audio features using librosa (can be done client or server-side)
3. **API Call**: Send features to `/api/speech-analysis/predict/`
4. **Display Results**: Show scores, feedback, and recommendations in UI

## Future Enhancements

### Potential Improvements

1. **Deep Learning**: Try LSTM/CNN models for raw audio processing
2. **Real-time Analysis**: WebSocket streaming for live feedback
3. **User Profiles**: Track progress over time
4. **Audio Upload**: Direct audio file upload with server-side feature extraction
5. **Comparative Analysis**: Compare against top speakers in category
6. **Custom Training**: Allow users to add their own labeled data

### Adding Audio Upload Feature

To enable direct audio upload:

1. Install audio processing dependencies
2. Create endpoint to accept audio files
3. Extract features server-side using librosa
4. Return predictions

Example implementation available in comments within the codebase.

## Dataset Information

**Current Dataset:**
- 150 samples (expert-labeled speeches)
- 3 categories: Informative, Motivational, Persuasive
- 26 audio features per sample
- 8 expert-labeled scores (1-5 scale)

**Features:**
- Extracted from real speech audio files
- Scaled from 1-5: Expert ratings on specific aspects

**Recommendations:**
- Consider expanding dataset to 300+ samples for better generalization
- Collect more diverse speaker demographics
- Add more categories if needed

## Troubleshooting

### Model not loading
- Ensure you've run `python ml_models/train_model.py`
- Check that `ml_models/trained_models/` directory exists with model files

### Import errors
- Activate virtual environment: `venv\Scripts\activate` (Windows) or `source venv/bin/activate` (Linux/Mac)
- Reinstall requirements: `pip install -r requirements.txt`

### Poor predictions
- Retrain with more data
- Try gradient boosting: Change `model_type='gradient_boosting'` in `train_model.py`
- Check feature extraction quality

## License

MIT License - Feel free to use for your Stage Ready project!

## Support

For questions about the ML model or API, refer to:
- `ml_models/speech_predictor.py` - Model implementation
- `speech_coach/views.py` - API endpoints
- Dataset documentation

---

**Built with Django REST Framework + Scikit-learn for Stage Ready Ionic App**
