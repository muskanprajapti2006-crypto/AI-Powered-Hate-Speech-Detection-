# 🛡️ AI Hate Speech Detection System

**Advanced Multi-Model AI System for Detecting Hate Speech with Emotion Analysis**

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-3.0%2B-green.svg)](https://flask.palletsprojects.com/)
[![Transformers](https://img.shields.io/badge/Transformers-4.30%2B-orange.svg)](https://huggingface.co/transformers/)

## 🌟 Features

### 🤖 **Triple AI Model Analysis**
- **Basic Model**: Logistic Regression (87% accuracy) - Fast and efficient
- **Deep Model**: RoBERTa BERT - State-of-the-art transformer model
- **Advanced Analyzer**: Custom emotion tracking with tone shift detection

### 🧠 **Advanced Emotion Detection**
- ✅ Word-by-word emotion tracking
- ✅ Mixed emotions detection (e.g., "I love everyone but I hate...")
- ✅ Tone shift analysis (POSITIVE→HATE or HATE→POSITIVE)
- ✅ Real-time sentiment scoring

### 🎯 **Smart Content Classification**
- 4 levels: HATE_SPEECH, MODERATE_HATE, BORDERLINE, NOT_HATE
- Comprehensive dataset (200+ categorized items)
- Categories: Religion, Race, Ethnicity, Gender, LGBTQ+, Violence, Dehumanizing

## 🚀 Quick Start

### Installation

1. **Install dependencies**
```bash
pip install -r requirements.txt
```

2. **Start the server**
```bash
python app_server.py
```

Or use the batch file:
```bash
start_server.bat
```

3. **Open in browser**
```
http://localhost:5000
```

## 📁 Project Structure

```
research project/
├── app_server.py          # Flask backend server (Main)
├── advanced_analyzer.py   # Advanced emotion analyzer
├── datasets.py            # Hate speech datasets (200+ items)
├── test_analyzer.py       # Testing script
├── index.html             # Frontend interface
├── styles.css             # Styling
├── Script.js              # Frontend logic
├── basic_hate_model.pkl   # Trained model
├── vectorizer.pkl         # Text vectorizer
├── requirements.txt       # Dependencies
└── start_server.bat       # Quick start
```

## 🎨 API Endpoints

### Predictions

**Basic Model**
```bash
POST /predict/basic
```

**Deep Model**
```bash
POST /predict/deep
```

**Advanced Analyzer** (Mixed Emotions + Tone Shift)
```bash
POST /predict/advanced
```

**All Models Consensus**
```bash
POST /predict/all
```

### Request Format
```json
{
  "text": "Your text here"
}
```

### Response Format
```json
{
  "prediction": "Hate Speech | Not Hate Speech",
  "confidence": 0.95,
  "classification": "HATE_SPEECH",
  "tone_shift": {
    "shift_type": "POSITIVE_TO_HATE"
  },
  "scores": {
    "hate": 3.8,
    "safe": 0.8,
    "final": 3.24
  }
}
```

## 🧪 Testing

Run the test suite:
```bash
python test_analyzer.py
```

## 🔄 Production Deployment

### Using Gunicorn (Recommended)
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app_server:app
```

### Using Docker
```bash
docker build -t hate-speech-detector .
docker run -p 5000:5000 hate-speech-detector
```

## 📊 Model Performance

- **Basic Model**: 50-100ms response time, 87% accuracy
- **Deep Model**: 100-300ms response time, 95%+ accuracy
- **Advanced Analyzer**: 50-150ms, Explainable AI

## 🛡️ Security Features

- CORS protection
- Input validation (max 1000 chars)
- Thread-safe inference
- Automatic memory cleanup
- Error handling & logging

## 🎯 Use Cases

- Social media content moderation
- Chat/messaging platform filtering
- Email abuse detection
- Gaming community moderation
- Comment section filtering

## 👨‍💻 Author

**Muskan Prajapati and Rishika Singh**

📱 Contact: +91 8418034346 (WhatsApp)
💬 For codebase understanding, support, or collaboration

---

**Made with ❤️ for a safer internet**

