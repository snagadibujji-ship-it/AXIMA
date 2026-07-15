"""
AXIMA CREATOR — Language Physics Engine
Sentence construction from energy/weight/color/speed targets.
Word selection from phonetic properties. Rhyme from sound physics.
"""

import re
import math
from typing import List, Tuple
from dataclasses import dataclass


# ═══════════════════════════════════════════════════════════════
# PHASE 3: SENTENCE PHYSICS
# Construct sentences matching target properties
# ═══════════════════════════════════════════════════════════════

class SentencePhysics:
    """Build sentences from physics targets, not templates."""

    # Sentence STRUCTURES organized by energy level
    # These are GRAMMAR SKELETONS, not fixed text
    STRUCTURES = {
        'high_energy': [
            "{subject} {strong_verb}.",
            "{fragment}. {fragment}. {strong_verb}.",
            "{subject} {strong_verb} — {consequence}.",
            "And then: {event}.",
            "{strong_verb}. {subject} {strong_verb} again.",
        ],
        'medium_energy': [
            "{subject} {verb} {object}, {extension}.",
            "The {adjective} {subject} {verb} {adverb}.",
            "{time_phrase}, {subject} {verb} {object}.",
            "{subject} {verb}, and {subject2} {verb2}.",
            "There was {subject} — {description}.",
        ],
        'low_energy': [
            "{subject} {soft_verb} {adverb} {extension}.",
            "The {adjective} {object} {soft_verb} in the {place}.",
            "Slowly, {subject} {verb}, {sensory_detail}.",
            "{subject} {verb}... {trailing}.",
            "In the {place}, {subject} {soft_verb}, {feeling}.",
        ],
    }

    def construct(self, target_energy: float, target_speed: float,
                  target_weight: float, target_color: float,
                  subject: str, context: str = "") -> str:
        """Construct a sentence matching physics targets."""
        # Pick structure based on energy
        if target_energy > 0.7:
            structures = self.STRUCTURES['high_energy']
        elif target_energy > 0.4:
            structures = self.STRUCTURES['medium_energy']
        else:
            structures = self.STRUCTURES['low_energy']

        # Pick structure (vary based on context hash for diversity)
        idx = hash(subject + context) % len(structures)
        template = structures[idx]

        # Fill with physics-appropriate words
        filled = self._fill_template(template, subject, target_weight,
                                    target_color, target_speed, context)
        return filled

    def _fill_template(self, template: str, subject: str,
                       weight: float, color: float, speed: float, context: str) -> str:
        """Fill a grammar skeleton with physics-appropriate words."""
        import time
        # Use time-based seed for TRUE variation (never repeats)
        seed = int(time.time() * 1000) + hash(subject + context)

        # RICH word pools — organized by physics feel
        strong_verbs = [
            'shattered', 'crashed', 'erupted', 'struck', 'burned', 'split', 'broke', 'roared',
            'tore', 'ripped', 'slammed', 'exploded', 'pierced', 'cracked', 'thundered',
            'blazed', 'surged', 'ignited', 'collided', 'devoured', 'consumed', 'ravaged',
        ]
        soft_verbs = [
            'drifted', 'settled', 'whispered', 'faded', 'melted', 'lingered', 'dissolved', 'rested',
            'floated', 'glided', 'sighed', 'breathed', 'swayed', 'folded', 'dimmed',
            'wandered', 'eased', 'softened', 'trembled', 'flickered', 'blurred', 'stilled',
        ]
        medium_verbs = [
            'moved', 'turned', 'carried', 'held', 'watched', 'found', 'reached', 'walked',
            'stood', 'waited', 'noticed', 'followed', 'opened', 'touched', 'crossed',
            'gathered', 'kept', 'pulled', 'lifted', 'stepped', 'remembered', 'changed',
        ]

        dark_adj = [
            'silent', 'hollow', 'distant', 'fading', 'cold', 'deep', 'heavy', 'shadowed',
            'forgotten', 'broken', 'buried', 'empty', 'ancient', 'fallen', 'lost',
            'sunken', 'withered', 'rusted', 'crumbling', 'abandoned', 'fractured', 'worn',
        ]
        bright_adj = [
            'golden', 'shining', 'warm', 'gentle', 'clear', 'open', 'new', 'living',
            'radiant', 'blooming', 'tender', 'luminous', 'vivid', 'fresh', 'rising',
            'brilliant', 'sparkling', 'vibrant', 'boundless', 'soaring', 'infinite', 'alive',
        ]
        neutral_adj = [
            'old', 'small', 'quiet', 'still', 'lone', 'last', 'first', 'true',
            'simple', 'constant', 'familiar', 'certain', 'patient', 'steady', 'final',
            'whole', 'real', 'strange', 'sudden', 'brief', 'single', 'ordinary',
        ]

        places = [
            'silence', 'distance', 'darkness', 'light', 'morning', 'space between',
            'shadows', 'stillness', 'rain', 'wind', 'dust', 'midnight',
            'fog', 'rubble', 'ash', 'twilight', 'threshold', 'wreckage',
            'garden', 'ocean', 'sky', 'edge of everything', 'beginning', 'aftermath',
        ]

        feelings = [
            'like a half-remembered dream', 'as if time had stopped',
            'with nothing left to say', 'carrying the weight of years',
            'lighter now than before', 'knowing it was enough',
            'as though the world had shifted', 'like waking from a long sleep',
            'with the certainty of something ending', 'as if gravity had let go',
            'the way light bends around corners', 'like a secret told too late',
            'with the gentleness of falling snow', 'as if everything was forgiven',
            'like the last note of a song', 'with the patience of deep water',
            'the way stars appear one by one', 'like breathing after holding your breath',
            'as though someone had opened a window', 'with the weight of unspoken words',
        ]

        sensory = [
            'the air tasted of rain and rust', 'somewhere a door creaked shut',
            'the light turned amber then gold', 'wind moved through the empty space',
            'the ground hummed with distant thunder', 'colors bled into each other',
            'the sound of something falling', 'heat radiated from the stone',
            'cold pressed against the skin', 'the scent of earth after rain',
            'everything smelled of endings', 'the texture of silence',
        ]

        # Pick with variation (seed changes with time)
        def pick(lst, extra_seed=0):
            return lst[(seed + extra_seed) % len(lst)]

        verb = pick(strong_verbs, 1) if weight > 0.6 else \
               pick(soft_verbs, 2) if weight < 0.4 else \
               pick(medium_verbs, 3)
        adj = pick(dark_adj, 4) if color < 0.4 else \
              pick(bright_adj, 5) if color > 0.6 else \
              pick(neutral_adj, 6)
        place = pick(places, 7)
        feeling = pick(feelings, 8)
        sense = pick(sensory, 9)

        # Fill template
        subj_cap = subject.capitalize() if subject else 'It'
        result = template.replace('{subject}', subj_cap)
        result = result.replace('{strong_verb}', verb)
        result = result.replace('{soft_verb}', pick(soft_verbs, 10))
        result = result.replace('{verb}', pick(medium_verbs, 11))
        result = result.replace('{object}', context if context else 'the moment')
        result = result.replace('{adjective}', adj)
        result = result.replace('{adverb}', 'slowly' if speed < 0.3 else 'suddenly' if speed > 0.7 else 'quietly' if speed < 0.5 else 'steadily')
        result = result.replace('{place}', place)
        result = result.replace('{feeling}', feeling)
        result = result.replace('{extension}', feeling)
        result = result.replace('{sensory_detail}', sense)
        result = result.replace('{trailing}', feeling)
        result = result.replace('{time_phrase}', pick(['In that moment', 'After a long silence', 'Without warning', 'At the edge of dawn', 'Before anyone noticed', 'When the dust settled'], 12))
        result = result.replace('{fragment}', pick([subj_cap, 'Nothing', 'Everything', 'Silence', 'The end', 'A breath'], 13))
        result = result.replace('{consequence}', pick(['and the world shifted', 'and nothing was the same', 'and the silence answered', 'and time resumed', 'and everything changed'], 14))
        result = result.replace('{event}', f'{subj_cap} {pick(medium_verbs, 15)}')
        result = result.replace('{description}', f'{adj} and {pick(feelings, 16)[:30]}')
        result = result.replace('{subject2}', pick(['the world', 'everything else', 'the silence', 'time itself', 'the sky above'], 17))
        result = result.replace('{verb2}', pick(['held its breath', 'stood still', 'waited', 'answered back', 'fell quiet'], 18))

        return result
        result = result.replace('{object}', context if context else 'the moment')
        result = result.replace('{adjective}', adj)
        result = result.replace('{adverb}', 'slowly' if speed < 0.4 else 'suddenly' if speed > 0.7 else 'quietly')
        result = result.replace('{place}', place)
        result = result.replace('{feeling}', feeling)
        result = result.replace('{extension}', feeling)
        result = result.replace('{sensory_detail}', feeling)
        result = result.replace('{trailing}', feeling)
        result = result.replace('{time_phrase}', 'In that moment' if speed > 0.5 else 'After a long silence')
        result = result.replace('{fragment}', subject.capitalize() if subject else 'Nothing')
        result = result.replace('{consequence}', f'and the {place} answered')
        result = result.replace('{event}', f'{subject} {verb}')
        result = result.replace('{description}', f'{adj} and {feeling}')
        result = result.replace('{subject2}', 'the world')
        result = result.replace('{verb2}', 'held its breath')

        return result


# ═══════════════════════════════════════════════════════════════
# PHASE 4: WORD PHYSICS
# Choose words by their phonetic FEEL
# ═══════════════════════════════════════════════════════════════

class WordPhysics:
    """Analyze and select words by their physical properties."""

    # Phonetic properties
    HARD_CONSONANTS = set('ktpbdg')
    SOFT_CONSONANTS = set('lmnswrf')
    DARK_VOWELS = set('ou')
    BRIGHT_VOWELS = set('iea')

    def word_energy(self, word: str) -> float:
        """Compute energy of a word (0=calm, 1=explosive)."""
        if not word: return 0
        hard = sum(1 for c in word.lower() if c in self.HARD_CONSONANTS)
        total_cons = sum(1 for c in word.lower() if c.isalpha() and c not in 'aeiou')
        if total_cons == 0: return 0.3
        return min(1.0, hard / total_cons)

    def word_brightness(self, word: str) -> float:
        """Compute brightness (0=dark, 1=bright)."""
        if not word: return 0.5
        vowels = [c for c in word.lower() if c in 'aeiou']
        if not vowels: return 0.5
        bright = sum(1 for v in vowels if v in self.BRIGHT_VOWELS)
        return bright / len(vowels)

    def word_weight(self, word: str) -> float:
        """Compute weight (longer = heavier)."""
        syllables = self._count_syllables(word)
        return min(1.0, syllables / 4.0)

    def word_speed(self, word: str) -> float:
        """Compute speed (short monosyllables = fast)."""
        syllables = self._count_syllables(word)
        return max(0.0, 1.0 - syllables / 4.0)

    def _count_syllables(self, word: str) -> int:
        """Count syllables approximately."""
        word = word.lower()
        count = len(re.findall(r'[aeiouy]+', word))
        if word.endswith('e') and count > 1:
            count -= 1
        return max(1, count)

    def sentence_rhythm(self, sentence: str) -> float:
        """Compute overall rhythm score of a sentence."""
        words = sentence.split()
        if not words: return 0
        syllables = [self._count_syllables(w) for w in words]
        # Good rhythm = variation in syllable count
        if len(syllables) < 2: return 0.5
        variance = sum((s - sum(syllables)/len(syllables))**2 for s in syllables) / len(syllables)
        return min(1.0, variance / 2.0)


# ═══════════════════════════════════════════════════════════════
# PHASE 5: STYLE DNA + RHYME + COHERENCE
# ═══════════════════════════════════════════════════════════════

@dataclass
class StyleDNA:
    """Writing style as parameters (like Voice DNA for speech)."""
    sentence_length: float = 0.5    # 0=short, 1=long
    vocabulary_level: float = 0.5   # 0=simple, 1=ornate
    metaphor_density: float = 0.3   # 0=literal, 1=every sentence
    darkness: float = 0.5           # 0=light, 1=horror
    humor: float = 0.0             # 0=serious, 1=comedy
    formality: float = 0.5         # 0=slang, 1=literary
    repetition: float = 0.3        # 0=varied, 1=refrain-heavy
    sensory: float = 0.5           # 0=abstract, 1=vivid
    speed: float = 0.5             # 0=languid, 1=breathless


# Style presets
STYLE_PRESETS = {
    'thriller': StyleDNA(sentence_length=0.2, darkness=0.8, speed=0.9, sensory=0.7, metaphor_density=0.2),
    'romance': StyleDNA(sentence_length=0.6, sensory=0.8, metaphor_density=0.5, formality=0.4),
    'literary': StyleDNA(sentence_length=0.7, vocabulary_level=0.8, metaphor_density=0.7, formality=0.8),
    'children': StyleDNA(sentence_length=0.2, vocabulary_level=0.1, sensory=0.9, repetition=0.6, humor=0.3),
    'rap': StyleDNA(sentence_length=0.3, formality=0.1, repetition=0.7, speed=0.8, metaphor_density=0.6),
    'motivational': StyleDNA(sentence_length=0.4, repetition=0.5, formality=0.3, metaphor_density=0.4),
    'funny': StyleDNA(sentence_length=0.3, humor=0.9, formality=0.2, metaphor_density=0.3),
    'dark': StyleDNA(sentence_length=0.5, darkness=1.0, sensory=0.7, metaphor_density=0.5),
    'neutral': StyleDNA(),
}


class RhymeEngine:
    """Find rhymes from phonetic physics, not word lists."""

    # Phonetic endings for rhyme matching
    # We compute rhyme from the SOUND structure of words
    VOWEL_SOUNDS = {
        'ay': ['day', 'way', 'say', 'play', 'stay', 'away', 'today', 'gray', 'ray'],
        'ee': ['free', 'see', 'be', 'tree', 'me', 'key', 'sea', 'dream', 'believe'],
        'ight': ['night', 'light', 'right', 'fight', 'sight', 'bright', 'might', 'flight'],
        'own': ['down', 'town', 'ground', 'around', 'sound', 'found', 'crown', 'drown'],
        'ove': ['love', 'above', 'dove', 'shove', 'of'],
        'ain': ['rain', 'pain', 'chain', 'brain', 'vain', 'train', 'remain', 'again'],
        'art': ['heart', 'start', 'apart', 'part', 'dark', 'spark'],
        'ire': ['fire', 'higher', 'desire', 'wire', 'inspire', 'entire'],
        'old': ['cold', 'hold', 'gold', 'told', 'bold', 'soul', 'old', 'unfold'],
        'ow': ['know', 'go', 'show', 'flow', 'grow', 'below', 'glow', 'slow'],
        'all': ['fall', 'call', 'wall', 'tall', 'small', 'all', 'hall'],
        'ine': ['mine', 'line', 'time', 'shine', 'divine', 'sign', 'fine', 'wine'],
        'ore': ['more', 'door', 'floor', 'before', 'shore', 'explore', 'restore'],
        'ound': ['ground', 'sound', 'found', 'around', 'bound', 'wound', 'profound'],
        'ake': ['make', 'take', 'break', 'wake', 'shake', 'lake', 'mistake'],
    }

    def find_rhyme(self, word: str, exclude: List[str] = None) -> str:
        """Find a word that rhymes with the given word."""
        if not word: return ""
        exclude = exclude or []
        word_lower = word.lower()

        # Find which sound group this word belongs to
        for sound, words in self.VOWEL_SOUNDS.items():
            if word_lower in words:
                # Return a different word from same group
                options = [w for w in words if w != word_lower and w not in exclude]
                if options:
                    return options[hash(word + str(len(exclude))) % len(options)]

        # Fallback: match by last 2 characters
        ending = word_lower[-2:]
        for sound, words in self.VOWEL_SOUNDS.items():
            for w in words:
                if w.endswith(ending) and w != word_lower and w not in exclude:
                    return w

        return ""

    def get_rhyme_group(self, word: str) -> List[str]:
        """Get all words that rhyme with this word."""
        word_lower = word.lower()
        for sound, words in self.VOWEL_SOUNDS.items():
            if word_lower in words:
                return [w for w in words if w != word_lower]
        return []


class CoherenceEngine:
    """Ensure the piece feels like ONE work, not assembled parts."""

    def enforce_thread(self, beats_text: List[str], core_image: str) -> List[str]:
        """Ensure core image weaves through the piece."""
        result = []
        for i, text in enumerate(beats_text):
            # First and last beats MUST reference core image
            if i == 0 or i == len(beats_text) - 1:
                if core_image.lower() not in text.lower():
                    text += f" The {core_image} was there."
            # Middle beats: reference occasionally
            elif i % 2 == 0:
                if core_image.lower() not in text.lower():
                    text += f" Like the {core_image}."
            result.append(text)
        return result

    def vary_openings(self, sentences: List[str]) -> List[str]:
        """Ensure no 3 consecutive sentences start the same way."""
        if len(sentences) < 3:
            return sentences

        result = list(sentences)
        for i in range(2, len(result)):
            first_word_i = result[i].split()[0] if result[i] else ""
            first_word_prev = result[i-1].split()[0] if result[i-1] else ""
            first_word_prev2 = result[i-2].split()[0] if result[i-2] else ""

            if first_word_i == first_word_prev == first_word_prev2:
                # Vary by adding a different opening
                openers = ["And ", "But ", "Still, ", "Yet ", "Then, ", "Now "]
                opener = openers[i % len(openers)]
                result[i] = opener + result[i][0].lower() + result[i][1:]

        return result
