# Quick Start Guide - Stage Ready Backend

Get your public speaking coach backend running in 5 minutes!

## Prerequisites

- Python 3.8+ installed
- Dataset file: `Speeches Dataset - Clean.csv` in parent directory

## Step-by-Step Setup

### 1️⃣ Create Virtual Environment

**Windows:**
```bash
cd backend
python -m venv venv
venv\Scripts\activate
```

**Linux/Mac:**
```bash
cd backend
python -m venv venv
source venv/bin/activate
```

### 2️⃣ Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

⏱️ This takes ~2-3 minutes

### 3️⃣ Setup Database

```bash
python manage.py makemigrations
python manage.py migrate
```

### 4️⃣ (Optional) Create Admin User

```bash
python manage.py createsuperuser
```

Enter username, email, and password when prompted.

### 5️⃣ Train the ML Model

```bash
python ml_models/train_model.py
```

Expected output:
```
===========================================================
STAGE READY - Speech Coach Model Training
===========================================================

Loading dataset from: ...
Dataset shape: (150, 39)

Training model...

TRAINING RESULTS
===========================================================
Overall Metrics:
  Train MAE:  0.4523
  Test MAE:   0.5234
  Train R²:   0.7812
  Test R²:    0.6945

Per-Target Performance (Test Set):
  speech_pace               - MAE: 0.5123, R²: 0.6823
  pausing_fluency           - MAE: 0.4891, R²: 0.7012
  ...

TOP 10 MOST IMPORTANT FEATURES
===========================================================
        feature  importance
     pitch_mean      0.1245
     loud_mean       0.0987
     mfcc_1          0.0856
     ...

Model saved to: backend/ml_models/trained_models
```

### 6️⃣ Start the Server

```bash
python manage.py runserver
```

You should see:
```
Starting development server at http://127.0.0.1:8000/
```

## ✅ Verify Everything Works

### Test 1: Check Server
Open browser: `http://localhost:8000/api/speech-analysis/model_info/`

Should return JSON with model info.

### Test 2: Make Prediction

**Windows PowerShell:**
```powershell
$headers = @{ "Content-Type" = "application/json" }
$body = Get-Content sample_request.json -Raw
Invoke-RestMethod -Uri "http://localhost:8000/api/speech-analysis/predict/" -Method Post -Headers $headers -Body $body
```

**Linux/Mac/Git Bash:**
```bash
curl -X POST http://localhost:8000/api/speech-analysis/predict/ \
  -H "Content-Type: application/json" \
  -d @sample_request.json
```

Should return predictions with scores 1-5.

### Test 3: Admin Panel
1. Go to `http://localhost:8000/admin/`
2. Login with superuser credentials
3. View Speech Analyses

## 🎯 Next Steps

Now you can:

1. **Integrate with Ionic**: See [API_USAGE.md](API_USAGE.md)
2. **Customize Model**: Edit `ml_models/train_model.py`
3. **Add Features**: Modify `speech_coach/models.py` and `ml_models/speech_predictor.py`

## 📊 Understanding Your Model

### What the Model Does
- **Input**: 26 audio features (pitch, volume, MFCCs, etc.)
- **Output**: 8 scores (1-5 scale) + feedback + recommendations
- **Algorithm**: Random Forest Multi-Output Regression

### Key Features Used
1. **Pitch** (mean & variation) - How your voice rises/falls
2. **Volume** (mean & variation) - How loud/soft you speak
3. **Pauses** - How much silence in speech
4. **MFCCs** - Voice quality/timbre
5. **Speaking Rate** - Syllables per second

### Scores Predicted
1. **Speech Pace** - Is tempo appropriate?
2. **Pausing Fluency** - Good use of pauses?
3. **Loudness Control** - Volume well-modulated?
4. **Pitch Variation** - Vocal variety present?
5. **Articulation Clarity** - Clear pronunciation?
6. **Expressive Emphasis** - Emotional impact?
7. **Filler Words** - "Um", "uh" minimized?
8. **Overall** - General speaking quality

## 🔧 Troubleshooting

### "Model not found" error
➡️ Run: `python ml_models/train_model.py`

### "Dataset not found" error
➡️ Copy `Speeches Dataset - Clean.csv` to parent directory
   Or update path in `ml_models/train_model.py` line 66

### Import errors
➡️ Make sure virtual environment is activated:
   - Windows: `venv\Scripts\activate`
   - Linux/Mac: `source venv/bin/activate`

### Port 8000 already in use
➡️ Run on different port: `python manage.py runserver 8001`

### Poor model performance
➡️ Check dataset has all required columns
➡️ Try gradient boosting: Edit `train_model.py` line 73

## 📱 Connect to Ionic App

In your Ionic app, create a service:

```typescript
// services/speech-analysis.service.ts
import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Injectable({
  providedIn: 'root'
})
export class SpeechAnalysisService {
  private apiUrl = 'http://localhost:8000/api/speech-analysis';

  constructor(private http: HttpClient) {}

  async predictScores(features: any) {
    return this.http.post(`${this.apiUrl}/predict/`, features).toPromise();
  }

  async getModelInfo() {
    return this.http.get(`${this.apiUrl}/model_info/`).toPromise();
  }

  async getHistory() {
    return this.http.get(this.apiUrl).toPromise();
  }
}
```

## 📚 Documentation

- [README.md](README.md) - Full documentation
- [API_USAGE.md](API_USAGE.md) - API reference
- [sample_request.json](sample_request.json) - Example request

## 🎤 Feature Extraction (For Ionic)

To extract features from audio in your Ionic app, you'll need:

1. Record audio in app
2. Send to backend OR extract features client-side
3. Options:
   - **Server-side**: Upload audio, extract features on backend
   - **Client-side**: Use Web Audio API + librosa.js (if available)

See README.md for implementation details.

## 🚀 Production Deployment

Before deploying:

1. Change `SECRET_KEY` in `settings.py`
2. Set `DEBUG = False`
3. Configure `ALLOWED_HOSTS`
4. Update `CORS_ALLOWED_ORIGINS`
5. Use PostgreSQL instead of SQLite
6. Use Gunicorn/uWSGI
7. Setup NGINX reverse proxy
8. Enable HTTPS

---

**You're all set! 🎉**

Your ML-powered public speaking coach backend is ready to help users improve their speeches!
