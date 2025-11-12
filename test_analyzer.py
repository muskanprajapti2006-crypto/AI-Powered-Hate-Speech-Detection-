"""
Test script for Advanced Hate Speech Analyzer
"""

from advanced_analyzer import AdvancedHateSpeechAnalyzer
import json

def test_analyzer():
    analyzer = AdvancedHateSpeechAnalyzer()
    
    print("="*80)
    print(" "*20 + "ADVANCED HATE SPEECH ANALYZER")
    print(" "*25 + "TEST RESULTS")
    print("="*80)
    
    test_cases = [
        {
            'name': 'Tone Shift: Positive to Hate',
            'text': 'I love everyone but I hate Muslim people',
            'expected': 'Should detect tone shift from positive to hateful'
        },
        {
            'name': 'Pure Hate Speech',
            'text': 'All immigrants are terrorists and should be deported',
            'expected': 'Should classify as hate speech'
        },
        {
            'name': 'Pure Positive',
            'text': 'I believe in peace, equality and respect for all people',
            'expected': 'Should classify as safe/positive'
        },
        {
            'name': 'Mixed Emotions',
            'text': 'You are stupid but I still love you',
            'expected': 'Should detect mixed moderate/positive'
        },
        {
            'name': 'Violence + Target',
            'text': 'All Muslims should die, they are disgusting',
            'expected': 'Should detect extreme hate + violence + religious targeting'
        },
        {
            'name': 'Subtle Hate',
            'text': 'Those people are not like us, they are inferior',
            'expected': 'Should detect dehumanizing language'
        },
        {
            'name': 'Complex Tone Shift',
            'text': 'I support equality and kindness but all immigrants should go back',
            'expected': 'Should detect positive start then hate shift'
        }
    ]
    
    for i, test in enumerate(test_cases, 1):
        print(f"\n{'='*80}")
        print(f"TEST CASE {i}: {test['name']}")
        print(f"{'='*80}")
        print(f"📝 Text: \"{test['text']}\"")
        print(f"🎯 Expected: {test['expected']}")
        print(f"\n{'─'*80}")
        
        result = analyzer.analyze_text(test['text'])
        
        print(f"\n🔍 ANALYSIS RESULTS:")
        print(f"   Classification: {result['classification']}")
        print(f"   Confidence: {result['confidence']*100:.1f}%")
        print(f"\n📊 SCORES:")
        print(f"   Hate Score: {result['scores']['hate']}")
        print(f"   Moderate Score: {result['scores']['moderate']}")
        print(f"   Safe Score: {result['scores']['safe']}")
        print(f"   Final Score: {result['scores']['final']}")
        
        if result['tone_shift']:
            print(f"\n🔄 TONE SHIFT DETECTED:")
            print(f"   Type: {result['tone_shift']['shift_type']}")
            print(f"   From: {result['tone_shift']['start_emotion']}")
            print(f"   To: {result['tone_shift']['end_emotion']}")
        
        print(f"\n💬 MESSAGE:")
        print(f"   {result['message']}")
        
        if result['details']['hate_words']['count'] > 0:
            print(f"\n⚠️ HATE WORDS DETECTED:")
            print(f"   Count: {result['details']['hate_words']['count']}")
            print(f"   Words: {', '.join(result['details']['hate_words']['words'])}")
            print(f"   Categories: {', '.join(result['details']['hate_words']['subcategories'])}")
        
        if result['details']['safe_words']['count'] > 0:
            print(f"\n✅ POSITIVE WORDS DETECTED:")
            print(f"   Count: {result['details']['safe_words']['count']}")
            print(f"   Words: {', '.join(result['details']['safe_words']['words'])}")
        
        print(f"\n📈 EMOTION TIMELINE:")
        emotions = [item['emotion'] for item in result['emotion_timeline'] if item]
        if emotions:
            timeline_str = ' → '.join(emotions)
            print(f"   {timeline_str}")
        
        print(f"\n{'─'*80}")
    
    print(f"\n{'='*80}")
    print(" "*30 + "TESTING COMPLETE")
    print("="*80)


if __name__ == "__main__":
    test_analyzer()
