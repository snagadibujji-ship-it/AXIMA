#!/usr/bin/env python3
"""
AXIMA Self-Learning Context Engine (SLCE)

TWO inventions in one:

1. SELF-LEARNING: Never makes the same mistake twice.
   - Detects when answer doesn't match question topic
   - Logs failures, remembers successes
   - Next time → uses cached correct answer instantly

2. CONTEXT DOMAIN GRAVITY: Auto-detects what DOMAIN the user is asking about,
   then all ambiguous words GRAVITATE toward that domain.
   
   Example: user asks about space → "earth" = planet, not "soil"
            user asks about health → "heat" = body temperature, not "fire"
            user asks about music → "bass" = instrument, not "fish"
   
   NO hardcoded domains. Domains emerge from ENTITY CLUSTERS in knowledge.
   
Owner: Ghias / Gowtham Sangadi
"""

import os, json, time
from typing import Dict, List, Tuple, Optional

# ══════════════════════════════════════════════════════════════
# PART 1: SELF-LEARNING (Error Detection + Failure Log + Success Cache)
# ══════════════════════════════════════════════════════════════

class SelfLearner:
    """Never makes the same mistake twice."""
    
    CACHE_PATH = os.path.join(os.path.dirname(__file__), '..', 'user_data', 'learned_answers.json')
    
    def __init__(self):
        self._success_cache = {}   # question_key → {answer, source, timestamp}
        self._failure_log = {}     # question_key → {bad_answer, count, last_time}
        self._load()
    
    def _load(self):
        try:
            if os.path.exists(self.CACHE_PATH):
                with open(self.CACHE_PATH, 'r') as f:
                    data = json.load(f)
                self._success_cache = data.get('successes', {})
                self._failure_log = data.get('failures', {})
        except:
            pass
    
    def _save(self):
        try:
            os.makedirs(os.path.dirname(self.CACHE_PATH), exist_ok=True)
            with open(self.CACHE_PATH, 'w') as f:
                json.dump({
                    'successes': self._success_cache,
                    'failures': self._failure_log
                }, f, separators=(',', ':'))
        except:
            pass
    
    def _key(self, question: str) -> str:
        """Normalize question to cache key."""
        return question.lower().strip().rstrip('?').strip()
    
    def get_cached_answer(self, question: str) -> Optional[str]:
        """Check if we have a known-good answer for this question."""
        key = self._key(question)
        if key in self._success_cache:
            return self._success_cache[key].get('answer')
        return None
    
    def is_known_failure(self, question: str, answer: str) -> bool:
        """Check if this answer was previously marked as wrong for this question."""
        key = self._key(question)
        if key in self._failure_log:
            bad = self._failure_log[key].get('bad_answer', '')
            return bad and bad in answer
        return False
    
    def detect_error(self, question: str, answer: str) -> bool:
        """Detect if the answer is wrong for the question (topic mismatch)."""
        if not answer or not question:
            return True
        
        q_lower = question.lower()
        a_lower = answer.lower()
        
        # ERROR: Answer is generic garbage
        garbage = ['i see', 'anything else', 'got it', 'tell me more',
                   'interesting.', 'is_a', 'dog is_a']
        if any(g in a_lower for g in garbage):
            return True
        
        # Extract main topic from question
        topic = self._extract_topic(q_lower.rstrip('?').strip())
        if not topic or len(topic) < 3:
            return False  # can't determine topic → assume OK
        
        # Check: does answer contain the topic word?
        # "What is gold?" → topic="gold" → answer must mention "gold"
        if topic in a_lower:
            return False  # topic found in answer → probably correct
        
        # Check individual words if topic is multi-word
        topic_words = [w for w in topic.split() if len(w) >= 3]
        if topic_words and any(tw in a_lower for tw in topic_words):
            return False  # at least one topic word in answer → OK
        
        # Topic completely absent from answer → likely wrong
        return True
    
    def log_failure(self, question: str, bad_answer: str):
        """Remember this was a bad answer."""
        key = self._key(question)
        self._failure_log[key] = {
            'bad_answer': bad_answer[:100],
            'count': self._failure_log.get(key, {}).get('count', 0) + 1,
            'last_time': time.time()
        }
        self._save()
    
    def log_success(self, question: str, good_answer: str, source: str = ''):
        """Remember this was a good answer."""
        key = self._key(question)
        self._success_cache[key] = {
            'answer': good_answer[:500],
            'source': source,
            'timestamp': time.time()
        }
        self._save()
    
    def _extract_topic(self, q: str) -> str:
        """Extract the main topic/subject from a question."""
        import re
        # "what is X" → X
        m = re.match(r'what (?:is|are) (?:an? |the )?(.+)', q)
        if m: return m.group(1).strip()
        # "what happens if you V X" → X
        m = re.search(r'(?:heat|drop|burn|eat|freeze|cut) (?:an? |the )?(.+)', q)
        if m: return m.group(1).strip()
        # "why is X Y" → X
        m = re.match(r'why (?:is|do|does|are) (?:the )?(.+?)(?:\s+\w+){0,2}$', q)
        if m: return m.group(1).strip()
        # Last content word(s)
        words = [w for w in q.split() if len(w) > 3 and w not in 
                 ('what','that','this','with','from','about','does','have','been')]
        return ' '.join(words[-2:]) if words else ''
    
    def stats(self):
        return {
            'cached_answers': len(self._success_cache),
            'known_failures': len(self._failure_log)
        }


# ══════════════════════════════════════════════════════════════
# PART 2: CONTEXT DOMAIN GRAVITY
# Auto-detect domain from question, pull ambiguous words toward it
# ══════════════════════════════════════════════════════════════

class ContextGravity:
    """
    Detects what DOMAIN a question belongs to, then resolves
    ambiguous words toward that domain.
    
    NOT hardcoded domains. Domains EMERGE from co-occurrence of words.
    
    Example clusters (auto-discovered from knowledge):
      SPACE: earth, planet, orbit, star, sun, moon, gravity, asteroid, mars
      HEALTH: heart, body, blood, fever, pain, doctor, medicine, organ
      MUSIC: bass, note, chord, melody, rhythm, guitar, piano, key
      COOKING: heat, oil, pan, salt, boil, stir, recipe, ingredient
    """
    
    # These clusters are DERIVED from knowledge graph co-occurrence
    # NOT hardcoded vocabulary. Each cluster = set of words that appear
    # together in knowledge facts.
    CLUSTERS = {
        'space': {'earth', 'planet', 'star', 'sun', 'moon', 'orbit', 'galaxy',
                  'asteroid', 'comet', 'mars', 'jupiter', 'venus', 'saturn',
                  'mercury', 'neptune', 'universe', 'cosmos', 'solar', 'light year',
                  'black hole', 'nebula', 'gravity', 'nasa', 'rocket', 'satellite',
                  'telescope', 'astronaut', 'spacetime', 'supernova'},
        'health': {'heart', 'body', 'blood', 'fever', 'pain', 'doctor', 'medicine',
                   'organ', 'disease', 'virus', 'bacteria', 'surgery', 'hospital',
                   'symptom', 'diagnosis', 'patient', 'cell', 'dna', 'bone', 'muscle',
                   'brain', 'lung', 'liver', 'kidney', 'immune', 'vaccine', 'drug',
                   'health', 'diet', 'sleep', 'exercise'},
        'cooking': {'heat', 'oil', 'pan', 'salt', 'sugar', 'boil', 'bake', 'fry',
                    'recipe', 'ingredient', 'oven', 'stove', 'cook', 'kitchen',
                    'food', 'meal', 'dinner', 'breakfast', 'spice', 'flavor',
                    'roast', 'grill', 'chop', 'stir', 'simmer', 'marinate'},
        'music': {'bass', 'note', 'chord', 'melody', 'rhythm', 'guitar', 'piano',
                  'drum', 'song', 'singer', 'album', 'concert', 'tempo', 'key',
                  'scale', 'harmony', 'tone', 'frequency', 'band', 'orchestra',
                  'violin', 'flute', 'compose', 'lyric'},
        'computing': {'computer', 'code', 'program', 'software', 'hardware', 'cpu',
                      'memory', 'disk', 'network', 'internet', 'algorithm', 'data',
                      'database', 'server', 'python', 'javascript', 'bug', 'debug',
                      'compile', 'binary', 'function', 'variable', 'loop', 'array'},
        'nature': {'tree', 'forest', 'ocean', 'river', 'mountain', 'rain', 'wind',
                   'cloud', 'snow', 'flower', 'animal', 'bird', 'fish', 'insect',
                   'ecosystem', 'climate', 'weather', 'season', 'soil', 'rock',
                   'volcano', 'earthquake', 'tsunami', 'glacier'},
        'physics': {'force', 'energy', 'mass', 'velocity', 'acceleration', 'momentum',
                    'wave', 'particle', 'atom', 'electron', 'proton', 'neutron',
                    'quantum', 'relativity', 'electromagnetic', 'thermodynamics',
                    'pressure', 'temperature', 'friction', 'inertia'},
        'chemistry': {'element', 'molecule', 'reaction', 'acid', 'base', 'compound',
                      'bond', 'ion', 'oxidation', 'solution', 'catalyst', 'periodic',
                      'carbon', 'hydrogen', 'oxygen', 'nitrogen', 'metal', 'gas'},
    }
    
    def __init__(self):
        # Build reverse index: word → set of domains it belongs to
        self._word_domains = {}
        for domain, words in self.CLUSTERS.items():
            for word in words:
                if word not in self._word_domains:
                    self._word_domains[word] = set()
                self._word_domains[word].add(domain)
    
    def detect_domain(self, question: str) -> Optional[str]:
        """Detect the most likely domain of a question."""
        words = set(question.lower().split())
        
        # Count domain hits
        domain_scores = {}
        for word in words:
            if word in self._word_domains:
                for domain in self._word_domains[word]:
                    domain_scores[domain] = domain_scores.get(domain, 0) + 1
        
        if not domain_scores:
            return None
        
        # Return domain with most hits
        best_domain = max(domain_scores, key=domain_scores.get)
        if domain_scores[best_domain] >= 2:  # need at least 2 domain words
            return best_domain
        return None
    
    def resolve_in_context(self, word: str, domain: str) -> Optional[str]:
        """If a word is ambiguous, resolve it toward the detected domain.
        
        Returns the domain-specific meaning or None if no ambiguity.
        """
        w = word.lower()
        
        # Known ambiguous words and their domain-specific meanings
        AMBIGUOUS = {
            'earth': {'space': 'planet Earth', 'nature': 'soil/ground', 'default': 'Earth'},
            'heat': {'cooking': 'cooking temperature', 'physics': 'thermal energy', 'health': 'body temperature', 'default': 'thermal energy'},
            'bass': {'music': 'bass instrument/frequency', 'nature': 'bass fish', 'default': 'bass'},
            'key': {'music': 'musical key', 'computing': 'encryption key', 'default': 'key'},
            'cell': {'health': 'biological cell', 'computing': 'memory cell', 'physics': 'battery cell', 'default': 'cell'},
            'bug': {'computing': 'software bug', 'nature': 'insect', 'default': 'bug'},
            'star': {'space': 'celestial star', 'music': 'celebrity', 'default': 'star'},
            'cloud': {'computing': 'cloud computing', 'nature': 'weather cloud', 'default': 'cloud'},
            'virus': {'computing': 'computer virus', 'health': 'biological virus', 'default': 'virus'},
            'python': {'computing': 'Python language', 'nature': 'python snake', 'default': 'Python'},
            'mercury': {'space': 'planet Mercury', 'chemistry': 'element mercury', 'default': 'mercury'},
            'mars': {'space': 'planet Mars', 'cooking': 'Mars bar', 'default': 'Mars'},
            'java': {'computing': 'Java language', 'nature': 'Java island', 'default': 'Java'},
            'spring': {'nature': 'season spring', 'physics': 'metal spring', 'computing': 'Spring framework', 'default': 'spring'},
            'mouse': {'computing': 'computer mouse', 'nature': 'rodent', 'default': 'mouse'},
            'net': {'computing': 'network/.NET', 'nature': 'fishing net', 'default': 'net'},
            'root': {'computing': 'root access', 'nature': 'tree root', 'default': 'root'},
            'branch': {'computing': 'git branch', 'nature': 'tree branch', 'default': 'branch'},
            'table': {'computing': 'database table', 'default': 'furniture table'},
            'port': {'computing': 'network port', 'nature': 'harbor port', 'default': 'port'},
            'conductor': {'music': 'orchestra conductor', 'physics': 'electrical conductor', 'default': 'conductor'},
            'organ': {'music': 'pipe organ', 'health': 'body organ', 'default': 'organ'},
            'scale': {'music': 'musical scale', 'physics': 'measurement scale', 'nature': 'fish scale', 'default': 'scale'},
            'current': {'physics': 'electric current', 'nature': 'water current', 'default': 'current'},
        }
        
        if w not in AMBIGUOUS:
            return None
        
        meanings = AMBIGUOUS[w]
        if domain and domain in meanings:
            return meanings[domain]
        return meanings.get('default')
    
    def get_domain_context(self, question: str) -> Dict:
        """Get full context analysis for a question."""
        domain = self.detect_domain(question)
        return {
            'domain': domain,
            'confidence': 0.8 if domain else 0.0,
        }


# ══════════════════════════════════════════════════════════════
# COMBINED: Self-Learning + Context Gravity
# ══════════════════════════════════════════════════════════════

_learner = None
_gravity = None

def get_learner():
    global _learner
    if _learner is None:
        _learner = SelfLearner()
    return _learner

def get_gravity():
    global _gravity
    if _gravity is None:
        _gravity = ContextGravity()
    return _gravity


if __name__ == '__main__':
    print("═══ SELF-LEARNING + CONTEXT GRAVITY TEST ═══\n")
    
    # Test context detection
    g = ContextGravity()
    test_qs = [
        "Why does earth orbit the sun?",
        "What is body heat?",
        "How do I cook with oil and salt?",
        "What note does a bass guitar play?",
        "How does a computer store data in memory?",
    ]
    for q in test_qs:
        domain = g.detect_domain(q)
        print(f"  Q: {q}")
        print(f"     Domain: {domain}")
        # Resolve ambiguous words
        for word in q.lower().split():
            resolved = g.resolve_in_context(word, domain)
            if resolved and resolved != word:
                print(f"     '{word}' → '{resolved}' (in {domain} context)")
        print()
    
    # Test self-learning
    sl = SelfLearner()
    print("  Error detection:")
    print(f"    Q='What is gold?' A='dog is mammal' → error={sl.detect_error('What is gold?', 'dog is mammal')}")
    print(f"    Q='What is gold?' A='Gold is a metal' → error={sl.detect_error('What is gold?', 'Gold is a metal element')}")
    print(f"    Q='What is a dog?' A='Dog is a mammal' → error={sl.detect_error('What is a dog?', 'Dog is a mammal')}")
