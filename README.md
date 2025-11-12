# 🛡️ AI Hate Speech Detection System

**Project Description:**

The AI-Powered Hate Speech Detection System is designed to automatically identify and classify hateful, toxic, or offensive language in user-generated text content. This project leverages Natural Language Processing (NLP) and Deep Learning techniques to enhance online safety and promote respectful communication. The system utilizes pre-trained transformer models such as BERT (Bidirectional Encoder Representations from Transformers) for contextual text understanding. The input text is tokenized, encoded, and passed through the model to predict whether it contains hate speech, offensive language, or neutral content.The backend is implemented using Python with libraries like Transformers, Datasets, and Scikit-learn for model training and evaluation. The frontend interface, developed using HTML, CSS, and JavaScript, allows users to input text and view real-time predictions. The system can be further extended to support multi-lingual detection, dataset expansion, and integration with social media monitoring tools. Overall, this project demonstrates the application of AI and NLP in solving a critical real-world problem—automated hate speech detection for maintaining a safer digital environment. 

**Project Objectives:**

To develop an AI model capable of accurately detecting and classifying hate speech, offensive language, and neutral text using Natural Language Processing (NLP) techniques.
To implement a deep learning approach (using pre-trained transformer models like BERT) for contextual understanding and sentiment classification of text data.
To create an interactive web interface that allows users to input text and receive real-time predictions about its toxicity or hate content.
To build a scalable and efficient backend system using Python for model integration, prediction handling, and dataset management.
To evaluate model performance using metrics such as accuracy, precision, recall, and F1-score to ensure reliable classification results.
To contribute toward online safety by developing a tool that can help reduce the spread of hate speech across digital communication platforms.

**🛠️ Technologies Used**

Python: Core programming language used for implementing machine learning models and backend logic.

Flask: Lightweight web framework used to build and deploy the web application for real-time hate speech detection.

HTML, CSS, JavaScript: Frontend technologies used to design an interactive and responsive user interface.

Scikit-learn: Used for model evaluation, preprocessing, and performance analysis.

Pandas & NumPy: Utilized for data cleaning, manipulation, and numerical computations during dataset preparation and feature extraction.

**🧩 System Architecture / Working Process**

The AI-Powered Hate Speech Detection System follows a modular architecture consisting of several key components that work together to process user input and produce accurate predictions.

1. Data Collection and Preprocessing: A dataset containing labeled text samples (hate, offensive, or neutral) is collected from reliable sources. The text data undergoes preprocessing steps such as tokenization, stopword removal, lowercasing, and punctuation cleaning using NLP techniques.

2. Model Training: Pre-trained transformer models like BERT are fine-tuned on the cleaned dataset for contextual text classification. The model learns semantic and linguistic patterns to distinguish between hate speech and normal content. Training and evaluation are performed using Scikit-learn metrics such as accuracy, precision, recall, and F1-score.

3. Backend Integration: The trained model is integrated with a Flask backend for deployment. Flask handles HTTP requests, processes input text, loads the model, and returns predictions in JSON format.

4. Frontend Interface: A user-friendly web interface built with HTML, CSS, and JavaScript allows users to input text or comments. When the user submits text, the frontend sends the request to the Flask API and displays the classification result (e.g., Hate Speech, Offensive, Neutral).

5. Output and Visualization: The system displays the predicted category and confidence score in real-time. Additional features such as sentiment visualization or percentage-based toxicity indicators can be added for better interpretability.

6. Future Enhancements: Expanding support for multilingual detection. Integration with social media APIs for live monitoring. Deployment on cloud platforms for large-scale use.

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

**## Conclusion** 

The AI-Powered Hate Speech Detection System successfully demonstrates the use of machine learning and natural language processing (NLP) techniques to identify and filter hateful or toxic content from online text. By leveraging trained models and real-time text analysis, the system provides an efficient solution for promoting safer online communication. The integration of Flask for the backend and HTML, CSS, and JavaScript for the frontend ensures a smooth and user-friendly interface. Overall, the project contributes to building a more positive and respectful digital environment.

What I Have Learned
During the development of this project, I gained valuable technical and practical experience in several key areas:

Machine Learning: Understanding text classification, data preprocessing, and model training using libraries like Scikit-learn, Pandas, and NumPy.
Natural Language Processing (NLP): Working with text data, tokenization, and feature extraction techniques for sentiment and hate speech detection.
Web Development: Building a complete web application using Flask as the backend framework and HTML, CSS, and JavaScript for the frontend.
Integration: Connecting the machine learning model with the web interface to perform real-time predictions.
Problem-Solving: Enhancing debugging skills, handling data imbalance, and improving model accuracy through testing and optimization.
Ethical AI Awareness: Understanding the importance of responsible AI use and the role of technology in promoting respectful digital communication.

## 👨‍💻 Author

**Muskan Prajapati and Rishika Singh**

📱 Contact: +91 9319978381 (WhatsApp)
💬 For codebase understanding, support, or collaboration

---

**Made with ❤️ for a safer internet**


