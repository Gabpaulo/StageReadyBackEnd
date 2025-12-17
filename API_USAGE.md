# Stage Ready API Usage Guide

## Quick Start

### 1. Start the Server

```bash
# Activate virtual environment
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac

# Run server
python manage.py runserver
```

Server runs at: `http://localhost:8000`

## API Endpoints

### Base URL
```
http://localhost:8000/api/
```

---

## Speech Analysis Endpoints

### 1. Make a Prediction

**Endpoint:** `POST /api/speech-analysis/predict/`

**Description:** Analyze speech features and get quality scores with feedback.

**Headers:**
```
Content-Type: application/json
```

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

**Response (200 OK):**
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
      "pausing_fluency": {
        "score": 4,
        "description": "Good use of pauses - natural flow"
      },
      "loudness_control": {
        "score": 4,
        "description": "Good volume control - well modulated"
      },
      "pitch_variation": {
        "score": 2,
        "description": "Limited variation - practice intonation"
      },
      "articulation_clarity": {
        "score": 3,
        "description": "Generally clear - some improvement needed"
      },
      "expressive_emphasis": {
        "score": 2,
        "description": "Limited expression - add more emotion"
      },
      "filler_words": {
        "score": 5,
        "description": "No fillers - clean, professional delivery"
      }
    }
  },
  "recommendations": [
    {
      "category": "Pitch Variation",
      "issue": "Limited vocal variety",
      "suggestion": "Practice varying your pitch to emphasize key words. Avoid monotone delivery."
    },
    {
      "category": "Expression",
      "issue": "Lacks emotional impact",
      "suggestion": "Connect emotionally with your content. Use vocal variety to convey passion and conviction."
    }
  ]
}
```

**cURL Example:**
```bash
curl -X POST http://localhost:8000/api/speech-analysis/predict/ \
  -H "Content-Type: application/json" \
  -d @sample_request.json
```

**JavaScript/TypeScript Example (Ionic):**
```typescript
import { HttpClient } from '@angular/common/http';

interface PredictionRequest {
  category: string;
  loud_mean: number;
  loud_std: number;
  // ... other features
}

interface PredictionResponse {
  speech_pace: number;
  pausing_fluency: number;
  loudness_control: number;
  pitch_variation: number;
  articulation_clarity: number;
  expressive_emphasis: number;
  filler_words: number;
  overall: number;
  feedback: any;
  recommendations: any[];
}

async predictSpeechQuality(features: PredictionRequest) {
  const url = 'http://localhost:8000/api/speech-analysis/predict/';

  try {
    const response = await this.http.post<PredictionResponse>(url, features).toPromise();
    console.log('Predictions:', response);
    return response;
  } catch (error) {
    console.error('Prediction failed:', error);
    throw error;
  }
}
```

---

### 2. Get Model Information

**Endpoint:** `GET /api/speech-analysis/model_info/`

**Description:** Get details about the ML model including features and importance.

**Response (200 OK):**
```json
{
  "model_type": "random_forest",
  "is_trained": true,
  "features": [
    "loud_mean",
    "loud_std",
    "pause_ratio",
    "pitch_mean",
    "pitch_std",
    "syllables_per_sec",
    "spectral_centroid",
    "spectral_rolloff",
    "words_per_minute",
    "zcr_mean",
    "mfcc_1",
    "mfcc_2",
    "mfcc_3",
    "mfcc_4",
    "mfcc_5",
    "mfcc_6",
    "mfcc_7",
    "mfcc_8",
    "mfcc_9",
    "mfcc_10",
    "mfcc_11",
    "mfcc_12",
    "mfcc_13",
    "spectral_bandwidth",
    "spectral_flux",
    "chroma_mean",
    "category_encoded"
  ],
  "targets": [
    "speech_pace",
    "pausing_fluency",
    "loudness_control",
    "pitch_variation",
    "articulation_clarity",
    "expressive_emphasis",
    "filler_words",
    "overall"
  ],
  "feature_importance": [
    {"feature": "pitch_mean", "importance": 0.125},
    {"feature": "loud_mean", "importance": 0.098},
    {"feature": "mfcc_1", "importance": 0.085},
    // ... more features
  ]
}
```

**cURL Example:**
```bash
curl http://localhost:8000/api/speech-analysis/model_info/
```

---

### 3. List All Speech Analyses

**Endpoint:** `GET /api/speech-analysis/`

**Description:** Get all stored speech analysis records.

**Response (200 OK):**
```json
[
  {
    "id": 1,
    "file_name": "my_speech.mp3",
    "category": "informative",
    "speech_pace": 3,
    "pausing_fluency": 4,
    "loudness_control": 4,
    "pitch_variation": 2,
    "articulation_clarity": 3,
    "expressive_emphasis": 2,
    "filler_words": 5,
    "overall": 3,
    "strengths": "Good pausing and volume control",
    "areas_for_improvement": "Work on pitch variation and expression",
    "created_at": "2025-12-17T10:30:00Z",
    "updated_at": "2025-12-17T10:30:00Z"
  },
  // ... more records
]
```

---

### 4. Get Single Speech Analysis

**Endpoint:** `GET /api/speech-analysis/{id}/`

**Response (200 OK):**
```json
{
  "id": 1,
  "file_name": "my_speech.mp3",
  "category": "informative",
  "speech_pace": 3,
  "pausing_fluency": 4,
  // ... all fields
}
```

---

### 5. Create Speech Analysis Record

**Endpoint:** `POST /api/speech-analysis/`

**Request Body:**
```json
{
  "file_name": "my_speech.mp3",
  "category": "informative",
  "loud_mean": 0.058551233,
  "loud_std": 0.07518595,
  // ... all features
  "speech_pace": 3,
  "pausing_fluency": 4,
  // ... all predictions
}
```

---

### 6. Update Speech Analysis

**Endpoint:** `PUT /api/speech-analysis/{id}/`

**Request Body:** Same as create

---

### 7. Delete Speech Analysis

**Endpoint:** `DELETE /api/speech-analysis/{id}/`

**Response:** `204 No Content`

---

## Error Responses

### 400 Bad Request
```json
{
  "error": "Invalid input",
  "details": {
    "pitch_mean": ["This field is required."]
  }
}
```

### 503 Service Unavailable
```json
{
  "error": "ML model not loaded. Please train the model first."
}
```

### 500 Internal Server Error
```json
{
  "error": "Prediction failed",
  "details": "Error message here"
}
```

---

## Feature Descriptions

| Feature | Description | Typical Range |
|---------|-------------|---------------|
| `loud_mean` | Average volume/loudness | 0.0 - 0.1 |
| `loud_std` | Volume variation | 0.0 - 0.1 |
| `pause_ratio` | Proportion of silence | 0.0 - 1.0 |
| `pitch_mean` | Average pitch (Hz) | 100 - 3000 |
| `pitch_std` | Pitch variation (Hz) | 50 - 2000 |
| `syllables_per_sec` | Speaking rate | 2.0 - 6.0 |
| `words_per_minute` | Speech tempo | 80 - 200 |
| `spectral_centroid` | Sound brightness | 1000 - 8000 |
| `spectral_rolloff` | Frequency rolloff | 2000 - 10000 |
| `zcr_mean` | Voice quality indicator | 0.0 - 0.3 |
| `mfcc_1` to `mfcc_13` | Voice timbre features | -600 to +100 |
| `spectral_bandwidth` | Frequency range | 500 - 3000 |
| `spectral_flux` | Spectral change rate | 0.0 - 2.0 |
| `chroma_mean` | Pitch class distribution | 0.0 - 1.0 |

---

## Score Interpretation

All scores are on a **1-5 scale**:

- **5** - Excellent
- **4** - Good
- **3** - Average/Adequate
- **2** - Below Average/Needs Work
- **1** - Poor/Needs Significant Improvement

### Score Meanings

| Metric | What it Measures |
|--------|------------------|
| `speech_pace` | Speaking rate and rhythm |
| `pausing_fluency` | Strategic use of pauses |
| `loudness_control` | Volume projection and modulation |
| `pitch_variation` | Vocal variety and intonation |
| `articulation_clarity` | Pronunciation and enunciation |
| `expressive_emphasis` | Emotional impact and conviction |
| `filler_words` | Minimization of "um", "uh", etc. |
| `overall` | General speaking quality |

---

## Testing the API

### Using Postman

1. Import the collection or create new requests
2. Set base URL: `http://localhost:8000/api/`
3. Use sample JSON from `sample_request.json`
4. Send POST to `/speech-analysis/predict/`

### Using Python

```python
import requests
import json

# Load sample data
with open('sample_request.json', 'r') as f:
    features = json.load(f)

# Make prediction
url = 'http://localhost:8000/api/speech-analysis/predict/'
response = requests.post(url, json=features)

# Print results
if response.status_code == 200:
    predictions = response.json()
    print(f"Overall Score: {predictions['overall']}/5")
    print(f"Recommendations: {len(predictions['recommendations'])}")
    for rec in predictions['recommendations']:
        print(f"  - {rec['category']}: {rec['suggestion']}")
else:
    print(f"Error: {response.status_code}")
    print(response.json())
```

---

## Integration Checklist for Ionic App

- [ ] Configure HTTP client with base URL
- [ ] Create service for API calls
- [ ] Extract audio features from recordings
- [ ] Send features to `/predict/` endpoint
- [ ] Display scores in UI (gauge/progress bars)
- [ ] Show feedback messages
- [ ] List recommendations
- [ ] Store history using `/speech-analysis/` CRUD
- [ ] Handle errors gracefully

---

## Admin Panel

Access Django admin at: `http://localhost:8000/admin/`

Login with superuser credentials to:
- View all speech analyses
- Manage training dataset
- Monitor API usage

---

For more details, see the main [README.md](README.md)
