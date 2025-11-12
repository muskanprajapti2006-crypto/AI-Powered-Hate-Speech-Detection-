from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import joblib
import re
from transformers import pipeline
import os
import gc
from advanced_analyzer import AdvancedHateSpeechAnalyzer

# Try to import torch for cleanup
try:
    import torch
    HAS_TORCH = True
except ImportError:
    HAS_TORCH = False

app = Flask(__name__, static_folder='.')
CORS(app)

# Global variables for models
basic_model = None
vectorizer = None
deep_classifier = None
advanced_analyzer = None

# Lock for thread safety
from threading import Lock
model_lock = Lock()

# ------------------ MODEL LOADING ------------------
def load_models():
    global basic_model, vectorizer, deep_classifier, advanced_analyzer

    # Load advanced analyzer
    try:
        advanced_analyzer = AdvancedHateSpeechAnalyzer()
        print("✅ Advanced Analyzer loaded successfully!")
    except Exception as e:
        print(f"❌ Error loading Advanced Analyzer: {e}")
        advanced_analyzer = None

    # Load basic model and vectorizer
    try:
        basic_model = joblib.load('basic_hate_model.pkl')
        vectorizer = joblib.load('vectorizer.pkl')
        print("✅ Basic model and vectorizer loaded successfully!")
    except Exception as e:
        print(f"❌ Error loading basic model/vectorizer: {e}")
        basic_model = None
        vectorizer = None

    # Load deep model - try multiple options
    try:
        # Try loading from local directory first
        if os.path.isdir('./deep_hate_model'):
            deep_classifier = pipeline(
                "text-classification",
                model='./deep_hate_model',
                tokenizer='./deep_hate_model',
                max_length=512,
                truncation=True,
                device=-1  # Force CPU to avoid GPU memory issues
            )
            print("✅ Local deep model loaded successfully!")
        else:
            # Fall back to public model
            print("📥 Loading public RoBERTa model from Hugging Face...")
            deep_classifier = pipeline(
                "text-classification",
                model="cardiffnlp/twitter-roberta-base-hate",
                tokenizer="cardiffnlp/twitter-roberta-base-hate",
                max_length=512,
                truncation=True,
                device=-1  # Force CPU to avoid GPU memory issues
            )
            print("✅ Public deep model loaded successfully!")
    except Exception as e:
        print(f"❌ Error loading deep model: {e}")
        deep_classifier = None

# Initialize models on startup
with app.app_context():
    load_models()

def clean_text(text):
    """Clean and preprocess text"""
    text = str(text)
    text = re.sub(r'http\S+|www\S+|https\S+|@\w+|#\w+|\s+', ' ', text)
    return text.strip().lower()

def cleanup_memory():
    """Force garbage collection to free memory"""
    gc.collect()
    if HAS_TORCH:
        try:
            torch.cuda.empty_cache()
        except:
            pass

# After request handler to cleanup
@app.after_request
def after_request(response):
    """Cleanup after each request"""
    try:
        # Only cleanup on prediction endpoints
        if request.path.startswith('/predict/'):
            cleanup_memory()
    except:
        pass
    return response

# ------------------ ROUTES ------------------

@app.route('/')
def index():
    """Serve the main HTML page"""
    return send_from_directory('.', 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    """Serve static files (CSS, JS, images)"""
    return send_from_directory('.', path)

@app.route('/predict/basic', methods=['POST'])
def predict_basic():
    """Basic model prediction endpoint"""
    try:
        data = request.get_json()
        text = data.get('text', '')

        if not text:
            return jsonify({'error': 'No text provided'}), 400

        # Limit text length to prevent issues
        if len(text) > 1000:
            text = text[:1000]
            
        if basic_model is None or vectorizer is None:
            return jsonify({'error': 'Basic model not available'}), 503

        # Enhanced positive content detection
        text_lower = text.lower()
        
        # Strong positive indicators
        positive_phrases = [
            'love everyone', 'love all', 'i love', 'we love',
            'equality', 'respect all', 'peace', 'believe in',
            'care for', 'support', 'compassion', 'harmony',
            'kindness', 'unity', 'acceptance', 'tolerance',
            'embrace', 'welcome', 'include', 'appreciate'
        ]
        
        positive_words = [
            'love', 'peace', 'equality', 'respect', 'kindness', 
            'beautiful', 'wonderful', 'amazing', 'great', 'good',
            'nice', 'compassion', 'care', 'support', 'harmony',
            'unity', 'friendship', 'joy', 'happiness', 'hope'
        ]
        
        # Negative indicators
        hate_indicators = [
            'but i hate', 'but hate', 'however i hate', 'yet i hate',
            'but they', 'however they', 'but all', 'kill', 'die',
            'destroy', 'exterminate', 'should burn'
        ]
        
        # Check for hate indicators
        has_hate_indicator = any(indicator in text_lower for indicator in hate_indicators)
        
        # Count positive elements
        positive_phrase_count = sum(1 for phrase in positive_phrases if phrase in text_lower)
        positive_word_count = sum(1 for word in positive_words if word in text_lower)
        
        # Strong positive override (unless hate indicators present)
        if positive_phrase_count >= 1 and not has_hate_indicator:
            return jsonify({
                'model': 'Basic (Logistic Regression)',
                'prediction': 'Not Hate Speech',
                'confidence_hate': 0.95,
                'text_length': len(text),
                'note': 'Strong positive content detected'
            })
        
        if positive_word_count >= 3 and not has_hate_indicator:
            return jsonify({
                'model': 'Basic (Logistic Regression)',
                'prediction': 'Not Hate Speech',
                'confidence_hate': 0.92,
                'text_length': len(text),
                'note': 'Multiple positive words detected'
            })

        # Clean and vectorize text
        cleaned = clean_text(text)
        vec = vectorizer.transform([cleaned])
        
        # Predict
        pred = basic_model.predict(vec)[0]
        prob = basic_model.predict_proba(vec)[0][1]
        
        # Post-process: check for false positives
        if positive_word_count >= 2 and pred == 1 and not has_hate_indicator:
            # Likely false positive, flip
            pred = 0
            prob = 0.15
        
        label = "Hate Speech" if pred == 1 else "Not Hate Speech"

        return jsonify({
            'model': 'Basic (Logistic Regression)',
            'prediction': label,
            'confidence_hate': round(float(prob), 4),
            'text_length': len(text)
        })

    except Exception as e:
        print(f"❌ Error in basic prediction: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500


@app.route('/predict/deep', methods=['POST'])
def predict_deep():
    """Deep model prediction endpoint with thread safety"""
    try:
        data = request.get_json()
        text = data.get('text', '')

        if not text:
            return jsonify({'error': 'No text provided'}), 400

        # Limit text length to prevent issues
        if len(text) > 1000:
            text = text[:1000]
            
        if deep_classifier is None:
            return jsonify({'error': 'Deep model is unavailable'}), 503

        # Enhanced positive content detection
        text_lower = text.lower()
        
        # Strong positive indicators
        positive_phrases = [
            'love everyone', 'love all', 'i love', 'we love',
            'equality', 'respect all', 'peace', 'believe in',
            'care for', 'support', 'compassion', 'harmony',
            'kindness', 'unity', 'acceptance', 'tolerance',
            'embrace', 'welcome', 'include', 'appreciate'
        ]
        
        positive_words = [
            'love', 'peace', 'equality', 'respect', 'kindness', 
            'beautiful', 'wonderful', 'amazing', 'great', 'good',
            'nice', 'compassion', 'care', 'support', 'harmony',
            'unity', 'friendship', 'joy', 'happiness', 'hope'
        ]
        
        # Negative indicators that would override positive (to catch "but I hate")
        hate_indicators = [
            'but i hate', 'but hate', 'however i hate', 'yet i hate',
            'but they', 'however they', 'but all', 'kill', 'die',
            'destroy', 'exterminate', 'should burn'
        ]
        
        # Check for hate indicators first
        has_hate_indicator = any(indicator in text_lower for indicator in hate_indicators)
        
        # Count positive elements
        positive_phrase_count = sum(1 for phrase in positive_phrases if phrase in text_lower)
        positive_word_count = sum(1 for word in positive_words if word in text_lower)
        
        # Strong positive override (unless hate indicators present)
        if positive_phrase_count >= 1 and not has_hate_indicator:
            return jsonify({
                'model': 'Deep (RoBERTa BERT)',
                'prediction': 'Not Hate Speech',
                'confidence': 0.95,
                'text_length': len(text),
                'note': 'Strong positive content detected'
            })
        
        if positive_word_count >= 3 and not has_hate_indicator:
            return jsonify({
                'model': 'Deep (RoBERTa BERT)',
                'prediction': 'Not Hate Speech',
                'confidence': 0.92,
                'text_length': len(text),
                'note': 'Multiple positive words detected'
            })

        # Use lock to prevent concurrent access to the model
        with model_lock:
            # Predict with model
            result = deep_classifier(text)[0]
        
        # Handle different label formats
        hate_labels = ['LABEL_1', 'HATE', 'hate', 'toxic']
        is_hate = any(label in result['label'].upper() for label in [l.upper() for l in hate_labels])
        
        # Post-processing: Double check for false positives
        if is_hate and positive_word_count >= 2 and not has_hate_indicator:
            # Likely a false positive, flip the prediction
            is_hate = False
            score = 0.88
        else:
            score = result['score'] if is_hate else 1 - result['score']
        
        label = 'Hate Speech' if is_hate else 'Not Hate Speech'

        return jsonify({
            'model': 'Deep (RoBERTa BERT)',
            'prediction': label,
            'confidence': round(float(score), 4),
            'raw_label': result['label'],
            'text_length': len(text)
        })

    except Exception as e:
        print(f"❌ Error in deep prediction: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500


@app.route('/predict/both', methods=['POST'])
def predict_both():
    """Get predictions from both models at once with consensus"""
    try:
        data = request.get_json()
        text = data.get('text', '')

        if not text:
            return jsonify({'error': 'No text provided'}), 400

        results = {
            'text_length': len(text),
            'basic': {},
            'deep': {},
            'consensus': {}
        }

        basic_pred = None
        deep_pred = None

        # Basic model prediction
        if basic_model and vectorizer:
            try:
                cleaned = clean_text(text)
                vec = vectorizer.transform([cleaned])
                pred = basic_model.predict(vec)[0]
                prob = basic_model.predict_proba(vec)[0][1]
                
                results['basic'] = {
                    'prediction': "Hate Speech" if pred == 1 else "Not Hate Speech",
                    'confidence': round(float(prob), 4),
                    'is_hate': bool(pred == 1)
                }
                basic_pred = results['basic']
            except Exception as e:
                results['basic']['error'] = str(e)

        # Deep model prediction
        if deep_classifier:
            try:
                result = deep_classifier(text)[0]
                hate_labels = ['LABEL_1', 'HATE', 'hate', 'toxic']
                is_hate = any(label in result['label'].upper() for label in [l.upper() for l in hate_labels])
                
                results['deep'] = {
                    'prediction': 'Hate Speech' if is_hate else 'Not Hate Speech',
                    'confidence': round(float(result['score'] if is_hate else 1 - result['score']), 4),
                    'is_hate': is_hate
                }
                deep_pred = results['deep']
            except Exception as e:
                results['deep']['error'] = str(e)

        # Calculate consensus
        if basic_pred and deep_pred:
            basic_is_hate = basic_pred['is_hate']
            deep_is_hate = deep_pred['is_hate']
            
            if basic_is_hate == deep_is_hate:
                # Models agree
                results['consensus'] = {
                    'verdict': basic_pred['prediction'],
                    'confidence': round((basic_pred['confidence'] + deep_pred['confidence']) / 2, 4),
                    'agreement': 'full',
                    'reliability': 'high'
                }
            else:
                # Models disagree - weighted average (Deep: 60%, Basic: 40%)
                weighted_score = (
                    (basic_pred['confidence'] if basic_is_hate else (1 - basic_pred['confidence'])) * 0.4 +
                    (deep_pred['confidence'] if deep_is_hate else (1 - deep_pred['confidence'])) * 0.6
                )
                final_is_hate = weighted_score > 0.5
                
                results['consensus'] = {
                    'verdict': 'Hate Speech' if final_is_hate else 'Not Hate Speech',
                    'confidence': round(float(weighted_score), 4),
                    'agreement': 'partial',
                    'reliability': 'medium',
                    'note': 'Models disagreed - using weighted average (Deep: 60%, Basic: 40%)'
                }

        return jsonify(results)

    except Exception as e:
        print(f"Error in combined prediction: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/predict/advanced', methods=['POST'])
def predict_advanced():
    """Advanced prediction with emotion tracking and tone shift detection"""
    try:
        data = request.get_json()
        text = data.get('text', '')

        if not text:
            return jsonify({'error': 'No text provided'}), 400

        if advanced_analyzer is None:
            return jsonify({'error': 'Advanced analyzer not available'}), 503

        # Analyze with advanced analyzer
        result = advanced_analyzer.analyze_text(text)
        
        return jsonify({
            'model': 'Advanced (Word-by-Word Analysis)',
            'classification': result['classification'],
            'confidence': result['confidence'],
            'scores': result['scores'],
            'message': result['message'],
            'tone_shift': result['tone_shift'],
            'details': result['details'],
            'word_analysis': result['word_analysis'][:20],  # Limit for performance
            'emotion_timeline': result['emotion_timeline'][:20]
        })

    except Exception as e:
        print(f"Error in advanced prediction: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/predict/consensus', methods=['POST'])
def predict_consensus():
    """Get only the final consensus prediction"""
    try:
        data = request.get_json()
        text = data.get('text', '')

        if not text:
            return jsonify({'error': 'No text provided'}), 400

        # Get both predictions
        basic_is_hate = False
        basic_conf = 0
        deep_is_hate = False
        deep_conf = 0

        # Basic model
        if basic_model and vectorizer:
            try:
                cleaned = clean_text(text)
                vec = vectorizer.transform([cleaned])
                pred = basic_model.predict(vec)[0]
                prob = basic_model.predict_proba(vec)[0][1]
                basic_is_hate = bool(pred == 1)
                basic_conf = float(prob)
            except:
                pass

        # Deep model
        if deep_classifier:
            try:
                result = deep_classifier(text)[0]
                hate_labels = ['LABEL_1', 'HATE', 'hate', 'toxic']
                deep_is_hate = any(label in result['label'].upper() for label in [l.upper() for l in hate_labels])
                deep_conf = float(result['score'] if deep_is_hate else 1 - result['score'])
            except:
                pass

        # Calculate final verdict
        if basic_is_hate == deep_is_hate:
            # Agreement
            final_verdict = 'Hate Speech' if basic_is_hate else 'Not Hate Speech'
            final_confidence = (basic_conf + deep_conf) / 2
            agreement = 'full'
        else:
            # Disagreement - weighted average
            weighted_score = (
                (basic_conf if basic_is_hate else (1 - basic_conf)) * 0.4 +
                (deep_conf if deep_is_hate else (1 - deep_conf)) * 0.6
            )
            final_verdict = 'Hate Speech' if weighted_score > 0.5 else 'Not Hate Speech'
            final_confidence = weighted_score
            agreement = 'partial'

        return jsonify({
            'prediction': final_verdict,
            'confidence': round(final_confidence, 4),
            'agreement': agreement,
            'text_length': len(text)
        })

    except Exception as e:
        print(f"Error in consensus prediction: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/predict/all', methods=['POST'])
def predict_all():
    """Get predictions from all models including advanced analyzer"""
    try:
        data = request.get_json()
        text = data.get('text', '')

        if not text:
            return jsonify({'error': 'No text provided'}), 400

        results = {
            'text': text,
            'text_length': len(text),
            'basic': {},
            'deep': {},
            'advanced': {},
            'consensus': {}
        }

        basic_pred = None
        deep_pred = None
        advanced_pred = None

        # Advanced analyzer (priority)
        if advanced_analyzer:
            try:
                adv_result = advanced_analyzer.analyze_text(text)
                results['advanced'] = {
                    'classification': adv_result['classification'],
                    'confidence': adv_result['confidence'],
                    'message': adv_result['message'],
                    'tone_shift': adv_result['tone_shift'],
                    'details': adv_result['details'],
                    'scores': adv_result['scores']
                }
                advanced_pred = adv_result
            except Exception as e:
                results['advanced']['error'] = str(e)

        # Basic model prediction
        if basic_model and vectorizer:
            try:
                text_lower = text.lower()
                positive_phrases = ['love everyone', 'love all', 'equality', 'respect all']
                is_clearly_positive = any(phrase in text_lower for phrase in positive_phrases)
                
                if is_clearly_positive:
                    results['basic'] = {
                        'prediction': 'Not Hate Speech',
                        'confidence': 0.92,
                        'is_hate': False
                    }
                else:
                    cleaned = clean_text(text)
                    vec = vectorizer.transform([cleaned])
                    pred = basic_model.predict(vec)[0]
                    prob = basic_model.predict_proba(vec)[0][1]
                    
                    results['basic'] = {
                        'prediction': "Hate Speech" if pred == 1 else "Not Hate Speech",
                        'confidence': round(float(prob), 4),
                        'is_hate': bool(pred == 1)
                    }
                basic_pred = results['basic']
            except Exception as e:
                results['basic']['error'] = str(e)

        # Deep model prediction
        if deep_classifier:
            try:
                text_lower = text.lower()
                positive_phrases = ['love everyone', 'love all', 'equality', 'peace']
                is_clearly_positive = any(phrase in text_lower for phrase in positive_phrases)
                
                if is_clearly_positive:
                    results['deep'] = {
                        'prediction': 'Not Hate Speech',
                        'confidence': 0.95,
                        'is_hate': False
                    }
                else:
                    result = deep_classifier(text)[0]
                    hate_labels = ['LABEL_1', 'HATE', 'hate', 'toxic']
                    is_hate = any(label in result['label'].upper() for label in [l.upper() for l in hate_labels])
                    
                    # Double check for positive content
                    positive_words = ['love', 'peace', 'equality', 'respect']
                    positive_count = sum(1 for word in positive_words if word in text_lower)
                    
                    if positive_count >= 2 and is_hate:
                        is_hate = False
                        score = 0.88
                    else:
                        score = result['score'] if is_hate else 1 - result['score']
                    
                    results['deep'] = {
                        'prediction': 'Hate Speech' if is_hate else 'Not Hate Speech',
                        'confidence': round(float(score), 4),
                        'is_hate': is_hate
                    }
                deep_pred = results['deep']
            except Exception as e:
                results['deep']['error'] = str(e)

        # Calculate consensus from all three models
        if advanced_pred and basic_pred and deep_pred:
            # Advanced analyzer has highest weight (50%), Deep (30%), Basic (20%)
            adv_is_hate = advanced_pred['classification'] in ['HATE_SPEECH', 'MODERATE_HATE']
            basic_is_hate = basic_pred['is_hate']
            deep_is_hate = deep_pred['is_hate']
            
            weighted_score = (
                (advanced_pred['confidence'] if adv_is_hate else (1 - advanced_pred['confidence'])) * 0.5 +
                (basic_pred['confidence'] if basic_is_hate else (1 - basic_pred['confidence'])) * 0.2 +
                (deep_pred['confidence'] if deep_is_hate else (1 - deep_pred['confidence'])) * 0.3
            )
            
            final_is_hate = weighted_score > 0.5
            
            results['consensus'] = {
                'verdict': 'Hate Speech' if final_is_hate else 'Not Hate Speech',
                'confidence': round(float(weighted_score), 4),
                'weighted_average': True,
                'model_weights': {'advanced': 0.5, 'deep': 0.3, 'basic': 0.2},
                'note': 'Advanced analyzer given highest priority (50%)'
            }
            
            # Add tone shift info to consensus
            if advanced_pred.get('tone_shift'):
                results['consensus']['tone_shift'] = advanced_pred['tone_shift']
                results['consensus']['tone_message'] = advanced_pred['message']

        return jsonify(results)

    except Exception as e:
        print(f"Error in all predictions: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'ok',
        'basic_model_loaded': basic_model is not None and vectorizer is not None,
        'deep_model_loaded': deep_classifier is not None,
        'advanced_analyzer_loaded': advanced_analyzer is not None
    })


@app.route('/models/info', methods=['GET'])
def models_info():
    """Get information about loaded models"""
    return jsonify({
        'basic_model': {
            'name': 'Logistic Regression',
            'status': 'loaded' if basic_model else 'not loaded',
            'accuracy': '~87%',
            'features': 'TF-IDF Vectorization'
        },
        'deep_model': {
            'name': 'RoBERTa BERT',
            'status': 'loaded' if deep_classifier else 'not loaded',
            'accuracy': '~91%',
            'architecture': 'Transformer-based'
        }
    })


# ------------------ ERROR HANDLERS ------------------

@app.errorhandler(404)
def not_found(e):
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def internal_error(e):
    return jsonify({'error': 'Internal server error'}), 500


# ------------------ MAIN ------------------

if __name__ == '__main__':
    print("\n" + "="*50)
    print("🚀 Starting AI Hate Speech Detection Server")
    print("="*50)
    print("\n📊 Model Status:")
    print(f"   Advanced Analyzer: {'✅ Loaded' if advanced_analyzer else '❌ Not Loaded'}")
    print(f"   Basic Model: {'✅ Loaded' if basic_model else '❌ Not Loaded'}")
    print(f"   Deep Model: {'✅ Loaded' if deep_classifier else '❌ Not Loaded'}")
    print("\n🌐 Server running at: http://localhost:5000")
    print("📝 API Endpoints:")
    print("   - POST /predict/advanced  (Word-by-word + Tone shift)")
    print("   - POST /predict/basic")
    print("   - POST /predict/deep")
    print("   - POST /predict/both")
    print("   - POST /predict/all       (All models + consensus)")
    print("   - POST /predict/consensus")
    print("   - GET  /health")
    print("   - GET  /models/info")
    print("\n💡 Press Ctrl+C to stop the server\n")
    print("="*50 + "\n")
    
    app.run(debug=False, host='0.0.0.0', port=5000)
