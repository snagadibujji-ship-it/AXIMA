"""
AXIMA CREATOR v3 — Grammar Physics Engine
Built by: Ghias + Kiro | 2026

PHILOSOPHY:
  Stories are CAUSAL CHAINS of EVENTS happening to ENTITIES.
  ALL content words derived from:
    1. User's topic words (direct)
    2. CATEGORY PHYSICS (what persons/places/objects CAN DO)
    3. METAPHOR STRUCTURE (abstract → concrete mapping)
    4. CAUSAL LOGIC (if X happens, then Y follows)
  
  ZERO word pools. Only structural rules.
  The inference engine is used for FACTUAL queries only, NOT for creative content.
"""

import re
import time
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass, field


# ═══════════════════════════════════════════════════════════════
# ENTITY SYSTEM — What exists in the story
# ═══════════════════════════════════════════════════════════════

@dataclass
class Entity:
    name: str
    category: str       # person/place/object/concept/force
    can_do: List[str] = field(default_factory=list)
    has: List[str] = field(default_factory=list)
    is_like: List[str] = field(default_factory=list)
    contains: List[str] = field(default_factory=list)
    opposes: str = ""   # what it's in tension with


@dataclass
class Event:
    subject: str
    action: str
    object: str
    result: str
    emotion: str


# ═══════════════════════════════════════════════════════════════
# DERIVATION ENGINE — Physics of Language Categories
# ═══════════════════════════════════════════════════════════════

class Deriver:
    """
    Derives what entities CAN DO from what they ARE.
    
    This is CATEGORY PHYSICS:
      - A person can: think, move, speak, feel, choose, remember, forget
      - A place can: hold, reveal, hide, surround, transform, echo
      - An object can: break, remain, fall, be given, be lost, carry meaning
      - A concept can: grow, fade, consume, transform, demand, haunt
      - A force can: push, pull, crush, lift, shake, shatter
    
    These aren't vocabulary — they're what categories of things DO in reality.
    """

    def derive(self, word: str, all_topic_words: List[str]) -> Entity:
        """Derive full entity from a word + its topic context."""
        cat = self._categorize(word)
        entity = Entity(name=word, category=cat)

        # Derive what it can DO (from category physics)
        if cat == "person":
            entity.can_do = ["reached out", "turned away", "watched",
                           "held on", "let go", "remembered", "whispered",
                           "stood still", "searched", "stepped back",
                           "chose", "refused", "waited", "spoke"]
            entity.has = ["hands", "voice", "shadow", "breath", "name", "past"]
            entity.contains = ["doubt", "want", "what came before"]
            entity.opposes = self._find_opposition(word, all_topic_words)

        elif cat == "place":
            entity.can_do = ["held", "opened", "closed", "swallowed", "revealed",
                           "surrounded", "echoed", "waited"]
            entity.has = ["walls", "edges", "air", "light", "silence", "history"]
            entity.contains = ["echoes", "what was left behind", "the shape of absence"]

        elif cat == "object":
            entity.can_do = ["shattered", "remained", "fell", "rested",
                           "carried the weight of", "held the shape of"]
            entity.has = ["weight", "surface", "cracks", "warmth", "coldness"]
            entity.is_like = [f"the last proof of {word}", f"what {word} left behind"]

        elif cat == "concept":
            entity.can_do = ["grew", "faded", "shifted", "consumed",
                           "demanded", "refused to leave", "transformed",
                           "hollowed out", "filled", "returned"]
            entity.has = ["weight", "edges", "beginning", "end"]
            entity.is_like = self._metaphor_map(word)
            entity.contains = ["contradiction", "what nobody says", "the truth"]
            entity.opposes = self._concept_opposition(word)

        elif cat == "force":
            entity.can_do = ["pushed", "pulled", "shattered", "lifted",
                           "carried away", "pressed down on", "tore through"]
            entity.has = ["direction", "origin", "consequence"]
            entity.is_like = [f"{word} made physical"]

        return entity

    def _categorize(self, word: str) -> str:
        """Categorize by STRUCTURAL RULES."""
        # Person: role words, names
        if re.search(r'(ist|ier|eer|ent|ant|man|woman|boy|girl|child|ther|ther|tive)$', word):
            return "person"
        if word[0:1].isupper():
            return "person"
        # Place
        if re.search(r'(room|house|city|land|world|field|street|forest|ocean|sky|space|sea|lab)$', word):
            return "place"
        # Force (natural phenomena)
        if re.search(r'(wind|storm|rain|fire|flood|wave|quake|thunder|gravity)$', word):
            return "force"
        # Concept (abstract)
        if re.search(r'(ness|ity|ment|tion|sion|ence|ance|ship|dom)$', word):
            return "concept"
        if word in ('love','hate','fear','time','life','death','hope','loss','pain',
                    'grief','rage','joy','peace','war','truth','trust','faith',
                    'doubt','shame','pride','guilt','freedom','silence',
                    'heartbreak','loneliness','betrayal','redemption'):
            return "concept"
        # Default: object
        return "object"

    def _metaphor_map(self, concept: str) -> List[str]:
        """
        Map abstract → concrete through structural metaphor.
        
        Metaphor rule: abstract concepts are experienced PHYSICALLY.
        Map to the PHYSICAL SENSATION of that concept.
        """
        # Metaphor physics: concept → how it feels in the body
        if re.search(r'(love|heart|passion|desire)', concept):
            return ["fire that won't go out", "weight in the chest", "open wound"]
        if re.search(r'(time|age|moment|past|future)', concept):
            return ["water through fingers", "door that won't reopen", "thing already gone"]
        if re.search(r'(fear|dread|terror|anxiety)', concept):
            return ["cold that starts inside", "walls closing in", "ground giving way"]
        if re.search(r'(loss|grief|death|gone|miss)', concept):
            return ["empty room that echoes", "shape of what was there", "silence after sound"]
        if re.search(r'(hope|dream|wish|future)', concept):
            return ["light under door", "seed in concrete", "voice from far away"]
        if re.search(r'(anger|rage|fury|hate)', concept):
            return ["heat with nowhere to go", "thing that eats itself", "storm without sky"]
        if re.search(r'(break|hurt|pain|wound)', concept):
            return ["glass that knows it will shatter", "line that can't un-cross", "sound that stays"]
        if re.search(r'(free|escape|release)', concept):
            return ["sky after ceiling", "first breath after water", "weight lifting"]
        if re.search(r'(alone|lonely|solitude)', concept):
            return ["room with one chair", "echo answering itself", "clock in empty house"]
        # Default: any concept → physical experience
        return [f"the shape {concept} takes when no one watches",
                f"what {concept} sounds like at 3am",
                f"the weight of {concept} in the hands"]

    def _find_opposition(self, word: str, all_words: List[str]) -> str:
        """Find what a character opposes (narrative tension)."""
        # If there are concepts in the topic, the person opposes them
        for w in all_words:
            if w != word and self._categorize(w) == "concept":
                return w
        return "what cannot be undone"

    def _concept_opposition(self, concept: str) -> str:
        """Find what opposes a concept (dialectic tension)."""
        oppositions = {
            'love': 'loss', 'loss': 'presence', 'fear': 'truth',
            'time': 'memory', 'death': 'meaning', 'hope': 'evidence',
            'pain': 'numbness', 'freedom': 'belonging', 'silence': 'the need to speak',
            'heartbreak': 'the desire to feel again', 'loneliness': 'vulnerability',
            'betrayal': 'trust that remains', 'rage': 'the thing that caused it',
        }
        for key, val in oppositions.items():
            if key in concept:
                return val
        return "what came before"


# ═══════════════════════════════════════════════════════════════
# SENTENCE PHYSICS — How events become language
# ═══════════════════════════════════════════════════════════════

class SentencePhysics:
    """
    Sentence physics:
      MOMENTUM — short speeds up, long slows down
      GRAVITY — important words at edges (start or end)
      CONTRAST — meaning from DIFFERENCE between sentences
      RHYTHM — alternating creates music
      SPECIFICITY — concrete > abstract
    """

    def render(self, event: Event, tension: float, position: int,
              total_in_beat: int, form: str, all_entities: List[Entity]) -> str:
        """Turn event into sentence based on tension + form."""
        # Ensure action completeness
        action = event.action
        obj = event.object
        
        # If action ends with preposition, merge object INTO action
        if re.search(r'\b(for|from|to|with|at|on|of)$', action):
            action = f"{action} {obj}"
            obj = event.result  # shift result into object slot

        # For lyrics, use action as-is (past tense works: "I faded", "I consumed")
        action_base = action

        # Create cleaned event
        clean = Event(event.subject, action_base if form == "song" else action, obj, event.result, event.emotion)

        if form == "poem":
            return self._poetic(clean, tension, position)
        elif form == "song":
            return self._lyric(clean, tension, position, total_in_beat)
        else:
            return self._prose(clean, tension, position, total_in_beat, all_entities)

    def _prose(self, event: Event, tension: float, pos: int,
              total: int, entities: List[Entity]) -> str:
        s, a, o, r = event.subject, event.action, event.object, event.result

        # Add articles where needed (structural grammar rule)
        if s[0].islower() and not s.startswith(('I ','the ','a ')):
            s_full = f"the {s}"
        else:
            s_full = s
        s_cap = s_full[0].upper() + s_full[1:]

        if o and o[0].islower() and not o.startswith(('the ','a ','what ','something')):
            o_full = f"the {o}"
        else:
            o_full = o

        # Build "subject action object" phrase naturally
        # Some actions are intransitive (watched, refused) — don't need object after them
        intransitive = ('watched', 'refused', 'waited', 'spoke', 'let go',
                       'stood still', 'stepped back', 'turned away', 'reached out')
        if a in intransitive:
            s_a_o = f"{s_full} {a}"
        else:
            s_a_o = f"{s_full} {a} {o_full}"

        # Use content-hash for variety (never same pattern twice in a row)
        h = (hash(f"{s}{a}{o}{r}{pos}{tension}") % 997) + pos * 3

        # Position within beat determines micro-rhythm
        is_first = (pos == 0)
        is_last = (pos >= total - 1)
        phase = pos / max(1, total - 1)  # 0.0 to 1.0 within beat

        if tension > 0.85:
            # CLIMAX: fragments, single images, maximum impact
            options = [
                f"{s_cap}.",
                f"And then — {a}.",
                f"{o_full.capitalize()}. {r.capitalize()}.",
                f"No. {s_a_o.capitalize()}.",
                f"{r.capitalize()}.",
                f"It was done. {s_a_o.capitalize()}.",
                f"Everything after this would be different.",
            ]
        elif tension > 0.6:
            # RISING: compound, building, urgency
            options = [
                f"{s_a_o.capitalize()}, and for a moment — {r}.",
                f"Something about {o_full} told {s_full} everything.",
                f"There was no going back. {s_cap} {a}.",
                f"{s_a_o.capitalize()}. Not because it was right. Because it was time.",
                f"{o_full.capitalize()} changed, and {s_full} knew.",
                f"Before thinking, before choosing — {s_full} {a}.",
                f"It was happening. {s_cap} could feel it.",
            ]
        elif tension > 0.3:
            # MIDDLE: observation, building detail
            options = [
                f"{s_a_o.capitalize()}, the way one does when nothing else remains.",
                f"There was something about {o_full} that made {s_full} pause.",
                f"{o_full.capitalize()} had always been there. {s_cap} just hadn't noticed before.",
                f"{s_cap} thought about {o_full}. About what it meant.",
                f"In the quiet, {s_full} {a}. And {o_full} waited.",
                f"It was the kind of {o_full} that demanded attention. And {s_full} gave it.",
            ]
        else:
            # OPENING / STILLNESS: atmospheric, establishing
            options = [
                f"In the space where {o_full} meets silence, {s_full} {a}.",
                f"{s_cap} sat with {o_full} for what felt like hours.",
                f"There was nothing urgent about it. {s_a_o.capitalize()}, slowly.",
                f"The world was quiet here. {s_cap} {a}, and {o_full} remained.",
                f"It began like this: {s_full} and {o_full}, together in the stillness.",
                f"Nobody would have noticed. {s_a_o.capitalize()}, and the day continued.",
                f"Outside, the world moved. Here, {s_full} {a}.",
            ]

        return options[h % len(options)]

    def _poetic(self, event: Event, tension: float, pos: int) -> str:
        s, a, o, r = event.subject, event.action, event.object, event.result

        if tension > 0.7:
            options = [
                f"{s} {a}",
                f"and {o} — {r}",
                f"{a}. {a}. {a}.",
                f"the {o} where {s} ends",
            ]
        else:
            options = [
                f"the {o} where {s} once {a}",
                f"{s} in the shape of {o}",
                f"what {a} leaves behind:",
                f"{o} — and {r}",
                f"if {s} were {o}",
            ]
        return options[pos % len(options)]

    def _lyric(self, event: Event, tension: float, pos: int, total: int) -> str:
        s, a, o, r = event.subject, event.action, event.object, event.result

        # For lyrics, create base form for "could X" / "would never X" patterns
        # Only strip -ed/-ing if the result is still 4+ chars
        a_base = a
        if len(a) > 6 and a.endswith('ed'):
            candidate = a[:-2]
            if len(candidate) >= 4:
                a_base = candidate
        elif len(a) > 6 and a.endswith('ing'):
            candidate = a[:-3]
            if len(candidate) >= 4:
                a_base = candidate

        if tension > 0.7:
            # Chorus energy: repetition, hook
            options = [
                f"I {a} {o}",
                f"and {r}",
                f"tell me why {s} {a}",
                f"tell me why {r}",
                f"no more {o}",
                f"I {a_base}, I {a_base}, I {a_base}",
            ]
        elif tension > 0.4:
            # Verse: narrative, specificity
            options = [
                f"there was a time when {s} could {a_base}",
                f"before {o} became {r}",
                f"I held {o} like it was everything",
                f"you said {s} would never {a_base}",
                f"but {o} — {o} was always there",
            ]
        else:
            # Intro/outro: sparse, atmospheric
            options = [
                f"in the {o}",
                f"where {s} used to be",
                f"I remember {o}",
                f"before everything changed",
            ]
        return options[pos % len(options)]


# ═══════════════════════════════════════════════════════════════
# NARRATIVE INTELLIGENCE — Story Logic
# ═══════════════════════════════════════════════════════════════

class NarrativeEngine:
    """
    Plans WHAT HAPPENS using causal logic:
      - Each beat CAUSES the next (not random sequence)
      - Characters have WANTS that drive action
      - Tension follows physics (builds, releases, builds higher)
      - Ending transforms the beginning (circular structure)
    """

    def plan(self, form: str, target_words: int, entities: List[Entity]) -> List[Dict]:
        if form == "song":
            return self._song(target_words, entities)
        elif form == "poem":
            return self._poem(target_words, entities)
        else:
            return self._story(target_words, entities)

    def _story(self, target: int, entities: List[Entity]) -> List[Dict]:
        # Find protagonist and their opposition
        person = next((e for e in entities if e.category == "person"), None)
        concept = next((e for e in entities if e.category == "concept"), None)
        force = next((e for e in entities if e.category == "force"), None)

        subj = person.name if person else (entities[0].name if entities else "they")
        opp = concept or force or (entities[-1] if len(entities) > 1 else None)
        opp_name = opp.name if opp else "what cannot be undone"

        return [
            {"tension": 0.1, "words": target // 5,
             "focus": subj, "against": opp_name,
             "purpose": "establish world and character"},
            {"tension": 0.4, "words": target // 5,
             "focus": subj, "against": opp_name,
             "purpose": "something changes — character must respond"},
            {"tension": 0.7, "words": target // 5,
             "focus": subj, "against": opp_name,
             "purpose": "action and unexpected consequence"},
            {"tension": 1.0, "words": target // 5,
             "focus": subj, "against": opp_name,
             "purpose": "confrontation with core truth"},
            {"tension": 0.2, "words": target // 5,
             "focus": subj, "against": opp_name,
             "purpose": "world same but character changed"},
        ]

    def _song(self, target: int, entities: List[Entity]) -> List[Dict]:
        concept = next((e for e in entities if e.category == "concept"),
                      entities[0] if entities else Entity("this", "concept"))
        # Different focus per section for variety
        alt_focus = entities[-1].name if len(entities) > 1 else "you"
        return [
            {"tension": 0.3, "words": target // 5, "focus": "I", "against": concept.name,
             "purpose": "scene before"},
            {"tension": 0.8, "words": target // 5, "focus": concept.name, "against": "",
             "purpose": "emotional truth"},
            {"tension": 0.5, "words": target // 5, "focus": alt_focus, "against": concept.name,
             "purpose": "story deepens"},
            {"tension": 0.85, "words": target // 5, "focus": concept.name, "against": "I",
             "purpose": "truth hits harder"},
            {"tension": 0.9, "words": target // 5, "focus": "I", "against": concept.name,
             "purpose": "final revelation"},
        ]

    def _poem(self, target: int, entities: List[Entity]) -> List[Dict]:
        e = entities[0] if entities else Entity("silence", "concept")
        return [
            {"tension": 0.2, "words": target // 3, "focus": e.name, "against": "",
             "purpose": "single image"},
            {"tension": 0.6, "words": target // 3, "focus": e.name, "against": "",
             "purpose": "image expands"},
            {"tension": 0.85, "words": target // 3, "focus": e.name, "against": "",
             "purpose": "inversion — means opposite"},
        ]

    def generate_events(self, beat: Dict, entities: List[Entity], deriver: Deriver) -> List[Event]:
        """Generate events for a beat from entities + causal logic."""
        events = []
        tension = beat["tension"]
        word_budget = beat["words"]
        focus = beat["focus"]
        against = beat["against"]

        # Estimate events needed (~12 words per rendered event, overshoot for dedup)
        num_events = max(6, (word_budget // 10) + 4)

        # Track used action+object combos to prevent repetition
        used_combos = set()

        for i in range(num_events):
            # Alternate between focus entity and opposition
            if i % 3 == 0 and against:
                opp_entity = next((e for e in entities if e.name == against), None)
                if opp_entity:
                    ev = self._derive_unique_event(opp_entity, tension, beat.get("purpose", ""), i, used_combos)
                    events.append(ev)
                    continue

            # Focus entity acts
            focus_entity = next((e for e in entities if e.name == focus), None)
            if not focus_entity:
                focus_entity = entities[i % len(entities)] if entities else Entity("it", "object")

            # Vary tension within beat (builds toward end)
            local_t = tension * (0.6 + 0.4 * (i / max(1, num_events - 1)))
            ev = self._derive_unique_event(focus_entity, local_t, beat.get("purpose", ""), i, used_combos)
            events.append(ev)

        return events

    def _derive_unique_event(self, entity: Entity, tension: float, purpose: str, iteration: int, used: set) -> Event:
        """Derive event ensuring no repeated action+object combo."""
        n_actions = len(entity.can_do)
        n_has = len(entity.has)
        n_like = len(entity.is_like)
        n_contains = len(entity.contains)

        # Try different action indices until we find unused combo
        for attempt in range(n_actions + 3):
            idx = (int(tension * (n_actions - 1)) + iteration + attempt) % max(1, n_actions)
            action = entity.can_do[idx] if entity.can_do else "moved"

            # Pick object — cycle through ALL available material
            obj_pool = entity.has + entity.is_like + entity.contains
            if not obj_pool:
                obj_pool = [entity.name]
            obj_idx = (iteration + attempt * 3) % len(obj_pool)
            obj = obj_pool[obj_idx]

            combo = f"{entity.name}:{action}:{obj}"
            if combo not in used:
                used.add(combo)
                break

        # Result — also varied
        result_pool = entity.contains + [entity.opposes] if entity.opposes else entity.contains
        if not result_pool:
            result_pool = ["something changed"]
        result = result_pool[(iteration + int(tension * 10)) % len(result_pool)]

        return Event(entity.name, action, obj, result, purpose)


# ═══════════════════════════════════════════════════════════════
# MAIN ENGINE
# ═══════════════════════════════════════════════════════════════

class CreatorV3:
    def __init__(self):
        self.deriver = Deriver()
        self.physics = SentencePhysics()
        self.narrative = NarrativeEngine()

    def create(self, request: str) -> str:
        """Create content. All words from topic + category physics."""
        form, topic, target = self._parse(request)
        topic_words = self._extract_words(topic)

        # Derive entities from topic
        entities = [self.deriver.derive(w, topic_words) for w in topic_words]

        # Plan arc
        arc = self.narrative.plan(form, target, entities)

        # Generate beat by beat
        sections = []
        for beat_idx, beat in enumerate(arc):
            events = self.narrative.generate_events(beat, entities, self.narrative)
            sentences = []
            used_patterns = set()
            for ev_idx, event in enumerate(events):
                sent = self.physics.render(event, beat["tension"], ev_idx,
                                          len(events), form, entities)
                # Deduplicate: skip if first 5 words already used
                key = ' '.join(sent.split()[:5])
                if key in used_patterns:
                    continue
                used_patterns.add(key)
                sentences.append(sent)

            if form in ("poem", "song"):
                sections.append('\n'.join(sentences))
            else:
                sections.append(' '.join(sentences))

        # Assemble
        text = self._assemble(sections, form, entities)
        title = f"— {topic.strip().title()} —\n\n" if topic.strip() else ""
        return title + text

    def _parse(self, request: str) -> Tuple[str, str, int]:
        req = request.lower()
        form = "story"
        if re.search(r'\b(song|lyrics|sing)\b', req): form = "song"
        elif re.search(r'\b(poem|poetry|haiku)\b', req): form = "poem"
        elif re.search(r'\b(rap|bars)\b', req): form = "rap"

        m = re.search(r'(\d+)\s*word', req)
        target = int(m.group(1)) if m else {"story": 500, "song": 200, "poem": 80}.get(form, 500)

        topic = re.sub(r'\b(write|create|make|generate|give|me|a|an|the|please)\b', '', req)
        topic = re.sub(r'\b(story|song|poem|rap|lyrics|about|on|word[s]?)\b', '', topic)
        topic = re.sub(r'\d+', '', topic).strip()
        return form, topic, target

    def _extract_words(self, topic: str) -> List[str]:
        """Extract entity-worthy words from topic."""
        words = re.findall(r'\b[a-z]{3,}\b', topic.lower())
        result = []
        for w in words:
            # Skip verb-form words (structural: -ing/-ed/-es endings on long words)
            if re.search(r'(ing|ied|ies|izes|ates|ving|ting|ning)$', w) and len(w) > 5:
                continue
            if len(w) == 3 and w not in ('war','art','sky','sea','sun','man','god','ice'):
                continue
            result.append(w)
        return result if result else ["something"]

    def _assemble(self, sections: List[str], form: str, entities: List[Entity]) -> str:
        """Final assembly with connectors."""
        if form in ("poem", "song"):
            return '\n\n'.join(sections)

        # Prose: add paragraph breaks and minimal connectors
        result = []
        connectors = ["", "\n\n", "\n\nAnd then —\n\n", "\n\nBut —\n\n", "\n\n"]
        for i, section in enumerate(sections):
            if i == 0:
                result.append(section)
            else:
                result.append(connectors[i % len(connectors)] + section)

        return ''.join(result)


def get_creator_v3():
    return CreatorV3()
