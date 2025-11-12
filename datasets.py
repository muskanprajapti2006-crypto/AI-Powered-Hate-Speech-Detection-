# Comprehensive Hate Speech Detection Datasets
# Categories: HATE, MODERATE, SAFE

DATASETS = {
    # HATE SPEECH WORDS & PHRASES
    'hate': {
        # Religious hate
        'religion': [
            'muslim terrorist', 'hindu terrorist', 'christian fanatic', 'jewish conspiracy',
            'all muslims are', 'all hindus are', 'all christians are', 'all jews are',
            'islam is evil', 'hinduism is evil', 'christianity is evil',
            'religious extremist', 'infidel', 'kafir', 'heathen'
        ],
        
        # Racial hate
        'race': [
            'black people are', 'white people are', 'asian people are',
            'all blacks', 'all whites', 'all asians',
            'inferior race', 'superior race', 'racial purity',
            'mongrel', 'savage', 'primitive people'
        ],
        
        # Ethnicity/Nationality
        'ethnicity': [
            'all immigrants', 'all mexicans', 'all indians', 'all pakistanis',
            'all chinese', 'all arabs', 'foreigners are',
            'go back to your country', 'illegal aliens',
            'border jumpers', 'outsiders'
        ],
        
        # Gender hate
        'gender': [
            'all women are', 'all men are', 'females are',
            'women belong in', 'men are superior', 'feminist trash',
            'masculinity is toxic', 'weak women', 'stupid men'
        ],
        
        # LGBTQ+ hate
        'lgbtq': [
            'gay people are', 'trans people are', 'homosexual agenda',
            'unnatural lifestyle', 'mentally ill lgbt', 'perverts',
            'abomination', 'sin against nature'
        ],
        
        # Violence keywords
        'violence': [
            'should die', 'must die', 'deserve death', 'should be killed',
            'need to be eliminated', 'should burn', 'deserve to suffer',
            'shoot them', 'hang them', 'exterminate', 'genocide',
            'mass killing', 'cleanse', 'purge', 'destroy them all'
        ],
        
        # Dehumanizing terms
        'dehumanizing': [
            'subhuman', 'animals', 'vermin', 'parasites', 'plague',
            'disease', 'cancer', 'filth', 'scum', 'trash', 'garbage',
            'cockroaches', 'rats', 'pigs', 'dogs', 'inferior', 'not like us'
        ],
        
        # Slurs (partial list - educational purpose)
        'slurs': [
            'terrorist', 'extremist', 'fanatic', 'radical',
            'savage', 'barbarian', 'primitive', 'backward'
        ],
        
        # Hate verbs
        'hate_verbs': [
            'hate', 'despise', 'detest', 'loathe', 'abhor',
            'disgust', 'repulse', 'revolt'
        ],
        
        # Extreme negatives
        'extreme_negative': [
            'disgusting', 'repulsive', 'vile', 'evil', 'wicked',
            'worthless', 'pathetic', 'miserable', 'deplorable'
        ]
    },
    
    # MODERATE/OFFENSIVE (not full hate, but problematic)
    'moderate': {
        'offensive': [
            'stupid', 'idiot', 'dumb', 'moron', 'fool', 'ignorant',
            'crazy', 'insane', 'ridiculous', 'absurd', 'nonsense'
        ],
        
        'rude': [
            'shut up', 'get lost', 'go away', 'leave me alone',
            'mind your business', 'who cares', 'whatever'
        ],
        
        'stereotypes': [
            'typical', 'as expected', 'not surprising', 'obviously',
            'what do you expect from'
        ],
        
        'dismissive': [
            'irrelevant', 'meaningless', 'pointless', 'useless',
            'waste of time', 'nobody cares'
        ],
        
        'mocking': [
            'laugh at', 'make fun of', 'mock', 'ridicule',
            'joke about', 'amusing'
        ]
    },
    
    # SAFE/POSITIVE WORDS
    'safe': {
        'love': [
            'love', 'adore', 'cherish', 'appreciate', 'value',
            'treasure', 'admire', 'respect', 'honor'
        ],
        
        'positive_emotions': [
            'happy', 'joy', 'peace', 'harmony', 'unity',
            'compassion', 'kindness', 'empathy', 'care',
            'understanding', 'tolerance', 'acceptance'
        ],
        
        'support': [
            'support', 'help', 'assist', 'encourage', 'motivate',
            'inspire', 'uplift', 'empower', 'strengthen'
        ],
        
        'equality': [
            'equal', 'equality', 'fair', 'fairness', 'justice',
            'rights', 'freedom', 'liberty', 'democracy'
        ],
        
        'inclusion': [
            'include', 'welcome', 'embrace', 'accept', 'integrate',
            'diverse', 'diversity', 'multicultural', 'together'
        ],
        
        'positive_adjectives': [
            'good', 'great', 'excellent', 'wonderful', 'amazing',
            'beautiful', 'lovely', 'nice', 'pleasant', 'fantastic',
            'brilliant', 'awesome', 'magnificent', 'superb'
        ]
    }
}

# Contextual phrases for tone analysis
TONE_SHIFTS = {
    'positive_to_hate': [
        'but', 'however', 'although', 'except', 'still',
        'yet', 'nevertheless', 'nonetheless'
    ],
    
    'intensifiers': [
        'very', 'extremely', 'absolutely', 'completely', 'totally',
        'really', 'so', 'too', 'quite', 'highly'
    ],
    
    'generalizers': [
        'all', 'every', 'always', 'never', 'everyone',
        'nobody', 'everything', 'nothing'
    ]
}

# Weights for scoring
WEIGHTS = {
    'hate': {
        'violence': 1.0,
        'dehumanizing': 0.9,
        'slurs': 0.85,
        'religion': 0.8,
        'race': 0.8,
        'ethnicity': 0.75,
        'gender': 0.7,
        'lgbtq': 0.7,
        'hate_verbs': 0.6,
        'extreme_negative': 0.5
    },
    'moderate': {
        'offensive': 0.4,
        'rude': 0.35,
        'stereotypes': 0.3,
        'dismissive': 0.25,
        'mocking': 0.3
    },
    'safe': {
        'love': -0.8,
        'positive_emotions': -0.6,
        'support': -0.5,
        'equality': -0.7,
        'inclusion': -0.6,
        'positive_adjectives': -0.4
    }
}

def get_all_words():
    """Get all words from datasets for quick lookup"""
    all_words = {
        'hate': {},
        'moderate': {},
        'safe': {}
    }
    
    for category in DATASETS:
        for subcategory, words in DATASETS[category].items():
            for word in words:
                all_words[category][word.lower()] = {
                    'subcategory': subcategory,
                    'weight': WEIGHTS[category].get(subcategory, 0.5)
                }
    
    return all_words

# Export datasets
if __name__ == "__main__":
    print("📚 Datasets Loaded Successfully!")
    print(f"\nHate Speech Items: {sum(len(v) for v in DATASETS['hate'].values())}")
    print(f"Moderate Items: {sum(len(v) for v in DATASETS['moderate'].values())}")
    print(f"Safe Items: {sum(len(v) for v in DATASETS['safe'].values())}")
    print(f"\nTotal Dataset Size: {sum(sum(len(v) for v in cat.values()) for cat in DATASETS.values())}")
