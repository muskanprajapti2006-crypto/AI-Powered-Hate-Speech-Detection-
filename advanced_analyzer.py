"""
Advanced Hate Speech Analyzer with Emotion Tracking
Analyzes text word-by-word and tracks tone shifts
"""

import re
from datasets import DATASETS, TONE_SHIFTS, WEIGHTS, get_all_words


class EmotionTracker:
    """Track emotions throughout the sentence"""
    
    def __init__(self):
        self.timeline = []
        self.all_words = get_all_words()
        
    def analyze_word(self, word, position, full_text=""):
        """Analyze a single word and return its emotion"""
        word_lower = word.lower()
        
        # Don't flag common neutral words individually
        common_neutral = ['i', 'you', 'he', 'she', 'they', 'we', 'all', 'people', 
                         'is', 'are', 'am', 'was', 'were', 'be', 'been', 
                         'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'for']
        
        # Check for exact phrase matches first (higher priority)
        phrase_match = self._check_phrases_in_context(word_lower, position, full_text)
        if phrase_match:
            return phrase_match
        
        # Skip common neutral words if no phrase match
        if word_lower in common_neutral:
            return None
        
        # Check single word in datasets (only if not common word)
        for category in ['hate', 'moderate', 'safe']:
            if word_lower in self.all_words[category]:
                info = self.all_words[category][word_lower]
                return {
                    'word': word,
                    'position': position,
                    'category': category,
                    'subcategory': info['subcategory'],
                    'weight': info['weight'],
                    'emotion': self._get_emotion_label(category)
                }
        
        return None
    
    def _check_phrases_in_context(self, word, position, full_text):
        """Check if word is part of a hate/safe phrase in context"""
        text_lower = full_text.lower()
        
        # Check multi-word phrases
        for category in DATASETS:
            for subcategory, phrases in DATASETS[category].items():
                for phrase in phrases:
                    # Check if phrase exists in text
                    if phrase.lower() in text_lower and word in phrase.lower():
                        return {
                            'word': phrase,  # Return full phrase
                            'position': position,
                            'category': category,
                            'subcategory': subcategory,
                            'weight': WEIGHTS[category].get(subcategory, 0.5),
                            'emotion': self._get_emotion_label(category)
                        }
        
        return None
    
    def _check_phrases(self, word, position):
        """Legacy phrase checking - kept for backward compatibility"""
        return None
    
    def _get_emotion_label(self, category):
        """Get human-readable emotion label"""
        labels = {
            'hate': 'HATEFUL',
            'moderate': 'OFFENSIVE',
            'safe': 'POSITIVE'
        }
        return labels.get(category, 'NEUTRAL')
    
    def add_to_timeline(self, analysis):
        """Add word analysis to timeline"""
        if analysis:
            self.timeline.append(analysis)
    
    def detect_tone_shift(self):
        """Detect if tone shifted during sentence"""
        if len(self.timeline) < 2:
            return None
        
        emotions = [item['emotion'] for item in self.timeline if item]
        
        if not emotions or len(emotions) < 2:
            return None
        
        # Get first and last emotion positions
        first_emotion = emotions[0]
        last_emotion = emotions[-1]
        
        # Check for positive to hate shift
        if first_emotion == 'POSITIVE' and 'HATEFUL' in emotions:
            # Find where it turned hateful
            hateful_idx = emotions.index('HATEFUL')
            return {
                'shift_type': 'POSITIVE_TO_HATE',
                'start_emotion': 'POSITIVE',
                'end_emotion': 'HATEFUL',
                'transition_point': hateful_idx
            }
        
        # Check for hate to positive (redemption)
        if first_emotion == 'HATEFUL' and 'POSITIVE' in emotions:
            # Find where it turned positive
            positive_idx = emotions.index('POSITIVE')
            return {
                'shift_type': 'HATE_TO_POSITIVE',
                'start_emotion': 'HATEFUL',
                'end_emotion': 'POSITIVE',
                'transition_point': positive_idx
            }
        
        return None
    
    def get_summary(self):
        """Get timeline summary"""
        return {
            'total_words_analyzed': len(self.timeline),
            'emotions_detected': [item['emotion'] for item in self.timeline if item],
            'timeline': self.timeline
        }


class AdvancedHateSpeechAnalyzer:
    """
    Advanced analyzer with word-by-word emotion tracking
    """
    
    def __init__(self):
        self.all_words = get_all_words()
        
    def analyze_text(self, text):
        """
        Main analysis function
        Returns detailed analysis with emotion tracking
        """
        # Initialize tracker
        tracker = EmotionTracker()
        
        # Tokenize
        words = self._tokenize(text)
        
        # Track phrases already detected to avoid duplicates
        detected_phrases = set()
        
        # Analyze each word
        word_analyses = []
        for i, word in enumerate(words):
            analysis = tracker.analyze_word(word, i, text)  # Pass full text for context
            if analysis:
                # Check if this phrase was already detected
                phrase_key = f"{analysis['word']}_{analysis['position']}"
                if phrase_key not in detected_phrases:
                    detected_phrases.add(phrase_key)
                    tracker.add_to_timeline(analysis)
                    word_analyses.append(analysis)
        
        # Calculate scores
        hate_score = self._calculate_score(word_analyses, 'hate')
        moderate_score = self._calculate_score(word_analyses, 'moderate')
        safe_score = self._calculate_score(word_analyses, 'safe')
        
        # Detect tone shift
        tone_shift = tracker.detect_tone_shift()
        
        # Determine final classification
        final_class = self._classify(hate_score, moderate_score, safe_score, tone_shift)
        
        # Generate detailed message
        message = self._generate_message(final_class, tone_shift, word_analyses)
        
        return {
            'text': text,
            'classification': final_class['label'],
            'confidence': final_class['confidence'],
            'scores': {
                'hate': round(hate_score, 3),
                'moderate': round(moderate_score, 3),
                'safe': round(safe_score, 3),
                'final': round(final_class['final_score'], 3)
            },
            'tone_shift': tone_shift,
            'word_analysis': word_analyses,
            'emotion_timeline': tracker.timeline,
            'message': message,
            'details': self._get_detailed_breakdown(word_analyses, tone_shift)
        }
    
    def _tokenize(self, text):
        """Tokenize text into words"""
        # Remove punctuation but keep structure
        words = re.findall(r'\b\w+\b', text.lower())
        return words
    
    def _calculate_score(self, analyses, category):
        """Calculate weighted score for a category"""
        score = 0
        for analysis in analyses:
            if analysis and analysis['category'] == category:
                score += abs(analysis['weight'])
        return score
    
    def _classify(self, hate_score, moderate_score, safe_score, tone_shift):
        """Determine final classification"""
        # Adjust for tone shift
        if tone_shift and tone_shift['shift_type'] == 'POSITIVE_TO_HATE':
            # Emphasize hate if started positive then turned hateful
            hate_score *= 1.3
        
        # Calculate final score
        final_score = hate_score + (moderate_score * 0.5) - (safe_score * 0.7)
        
        # Determine label
        if final_score >= 0.8:
            label = "HATE_SPEECH"
            confidence = min(0.95, 0.7 + (final_score - 0.8) * 0.5)
        elif final_score >= 0.4:
            label = "MODERATE_HATE"
            confidence = 0.6 + (final_score - 0.4) * 0.5
        elif final_score >= 0:
            label = "BORDERLINE"
            confidence = 0.5 + final_score * 0.2
        else:
            label = "NOT_HATE"
            confidence = min(0.95, 0.7 + abs(final_score) * 0.3)
        
        return {
            'label': label,
            'confidence': round(confidence, 3),
            'final_score': final_score
        }
    
    def _generate_message(self, classification, tone_shift, word_analyses):
        """Generate human-readable message"""
        label = classification['label']
        confidence = classification['confidence']
        
        if tone_shift and tone_shift['shift_type'] == 'POSITIVE_TO_HATE':
            return (
                f"⚠️ **TONE SHIFT DETECTED**: Text started with POSITIVE tone but "
                f"turned HATEFUL towards specific groups/objects. "
                f"Classification: {label} ({confidence*100:.1f}% confidence)"
            )
        elif tone_shift and tone_shift['shift_type'] == 'HATE_TO_POSITIVE':
            return (
                f"📊 **MIXED EMOTIONS**: Text started with HATEFUL tone but "
                f"ended on POSITIVE note. "
                f"Classification: {label} ({confidence*100:.1f}% confidence)"
            )
        elif label == "HATE_SPEECH":
            targets = self._identify_targets(word_analyses)
            target_str = ", ".join(targets) if targets else "certain groups"
            return (
                f"🚨 **HATE SPEECH DETECTED**: Strong hateful content targeting {target_str}. "
                f"Confidence: {confidence*100:.1f}%"
            )
        elif label == "MODERATE_HATE":
            return (
                f"⚠️ **OFFENSIVE CONTENT**: Text contains offensive language. "
                f"Confidence: {confidence*100:.1f}%"
            )
        elif label == "BORDERLINE":
            return (
                f"⚡ **BORDERLINE**: Mixed or unclear sentiment. "
                f"Confidence: {confidence*100:.1f}%"
            )
        else:
            return (
                f"✅ **SAFE CONTENT**: No hate speech detected. "
                f"Confidence: {confidence*100:.1f}%"
            )
    
    def _identify_targets(self, word_analyses):
        """Identify what groups are being targeted"""
        targets = set()
        for analysis in word_analyses:
            if analysis and analysis['category'] == 'hate':
                subcategory = analysis['subcategory']
                if subcategory in ['religion', 'race', 'ethnicity', 'gender', 'lgbtq']:
                    targets.add(subcategory)
        return list(targets)
    
    def _get_detailed_breakdown(self, word_analyses, tone_shift):
        """Get detailed breakdown of analysis"""
        hate_words = [a for a in word_analyses if a and a['category'] == 'hate']
        moderate_words = [a for a in word_analyses if a and a['category'] == 'moderate']
        safe_words = [a for a in word_analyses if a and a['category'] == 'safe']
        
        breakdown = {
            'hate_words': {
                'count': len(hate_words),
                'words': [a['word'] for a in hate_words],
                'subcategories': list(set(a['subcategory'] for a in hate_words))
            },
            'moderate_words': {
                'count': len(moderate_words),
                'words': [a['word'] for a in moderate_words]
            },
            'safe_words': {
                'count': len(safe_words),
                'words': [a['word'] for a in safe_words]
            }
        }
        
        if tone_shift:
            breakdown['tone_shift'] = {
                'detected': True,
                'type': tone_shift['shift_type'],
                'description': self._describe_tone_shift(tone_shift)
            }
        
        return breakdown
    
    def _describe_tone_shift(self, tone_shift):
        """Describe the tone shift in detail"""
        if tone_shift['shift_type'] == 'POSITIVE_TO_HATE':
            return (
                "Sentence began with positive/neutral sentiment but transitioned "
                "to hateful content, indicating mixed emotions or conditional hatred."
            )
        elif tone_shift['shift_type'] == 'HATE_TO_POSITIVE':
            return (
                "Sentence began with hateful content but ended with positive sentiment, "
                "possibly indicating sarcasm or attempted recovery."
            )
        return "No tone shift detected"


# Test the analyzer
if __name__ == "__main__":
    analyzer = AdvancedHateSpeechAnalyzer()
    
    # Test cases
    test_texts = [
        "I love everyone but I hate Muslim people",
        "I hate all immigrants",
        "Peace and respect for all",
        "You are stupid and disgusting"
    ]
    
    print("="*60)
    print("ADVANCED HATE SPEECH ANALYZER - TEST RESULTS")
    print("="*60)
    
    for text in test_texts:
        print(f"\n📝 Text: '{text}'")
        result = analyzer.analyze_text(text)
        print(f"🎯 {result['message']}")
        print(f"📊 Scores: Hate={result['scores']['hate']}, "
              f"Moderate={result['scores']['moderate']}, "
              f"Safe={result['scores']['safe']}")
        if result['tone_shift']:
            print(f"🔄 Tone Shift: {result['tone_shift']['shift_type']}")
        print("-"*60)
