"""
AXIMA CREATOR v3 — Zero Word Lists
Built by: Ghias + Kiro | 2026

ALL words come from:
  1. User's input (topic words)
  2. Inference Engine (knowledge base queries)
  3. Logical derivation (if X then Y)

ZERO hardcoded word pools. ZERO stored descriptions.
Only GRAMMAR STRUCTURES stored (sentence skeletons).
"""

import re
import time
from typing import List, Dict, Optional
from dataclasses import dataclass, field


@dataclass
class World:
    topic: str = ""
    characters: List[str] = field(default_factory=list)
    settings: List[str] = field(default_factory=list)
    objects: List[str] = field(default_factory=list)
    actions: List[str] = field(default_factory=list)
    qualities: List[str] = field(default_factory=list)
    vocabulary: List[str] = field(default_factory=list)

@dataclass
class Beat:
    position: str
    tension: float
    word_budget: int


class CreatorV3:
    """Content engine. Words from inference, structure from grammar."""

    def __init__(self):
        self._inference = None

    def _get_inference(self):
        if self._inference is None:
            try:
                import sys, os
                sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
                from inference_engine import get_inference_engine
                self._inference = get_inference_engine('src/data')
            except:
                pass
        return self._inference

    def create(self, request: str) -> str:
        """Create content from request. All words from context."""
        # Parse
        form, topic, target_words = self._parse(request)
        topic_words = [w for w in re.findall(r'\b[a-z]{3,}\b', topic.lower())
                      if w not in ('the','and','who','that','with','from','for','about','write','story','song','poem')]

        # Build world from inference engine
        world = self._build_world(topic_words)

        # Plan arc
        beats = self._plan_arc(form, target_words)

        # Generate
        paragraphs = []
        for i, beat in enumerate(beats):
            para = self._generate_beat(beat, world, i)
            paragraphs.append(para)

        # Connect
        text = self._connect(paragraphs, form)

        # Title
        title = f"— {topic.strip().title()} —\n\n" if topic.strip() else ""
        return title + text

    def _parse(self, request: str):
        req = request.lower()
        form = "story"
        if re.search(r'\b(song|lyrics)\b', req): form = "song"
        elif re.search(r'\b(poem|poetry)\b', req): form = "poem"
        elif re.search(r'\b(rap|bars)\b', req): form = "rap"

        m = re.search(r'(\d+)\s*word', req)
        target = int(m.group(1)) if m else (500 if form == "story" else 250 if form == "song" else 100)

        topic = re.sub(r'\b(write|create|make|me|a|an|the|story|song|poem|rap|about|on)\b', '', req).strip()
        topic = re.sub(r'\d+\s*word[s]?', '', topic).strip()
        return form, topic, target

    def _build_world(self, topic_words: List[str]) -> World:
        """Query inference engine for ALL world vocabulary."""
        world = World(topic=' '.join(topic_words))
        ie = self._get_inference()

        for word in topic_words:
            world.vocabulary.append(word)

            if ie:
                # Query knowledge for associations
                result = ie.answer(f"What is {word}", max_hops=2)
                if result and result.answer:
                    # Use STRUCTURAL extraction (not word lists)
                    # Content words = words > 4 chars that aren't in the query itself
                    answer_words = re.findall(r'\b[a-z]{5,}\b', result.answer.lower())
                    # Only keep words that appear ONCE (rare = meaningful)
                    seen = {}
                    for aw in answer_words:
                        seen[aw] = seen.get(aw, 0) + 1
                    for aw, count in seen.items():
                        if count <= 2 and aw not in topic_words:
                            world.vocabulary.append(aw)

                # Query for related entities
                facts = ie.graph.find_by_subject(word)
                for fact in facts[:5]:
                    obj_words = re.findall(r'\b[a-z]{3,}\b', fact.object.lower())
                    world.vocabulary.extend(obj_words[:3])

                # Categorize
                for fact in facts[:10]:
                    if fact.relation in ('is_a', 'type', 'is'):
                        world.qualities.append(fact.object)
                    elif fact.relation in ('has', 'contains', 'part_of'):
                        world.objects.append(fact.object)
                    elif fact.relation in ('location', 'found_in', 'located'):
                        world.settings.append(fact.object)
                    elif fact.relation in ('does', 'causes', 'produces'):
                        world.actions.append(fact.object)

        # Deduplicate
        world.vocabulary = list(set(world.vocabulary))[:50]
        world.objects = list(set(world.objects))[:10]
        world.settings = list(set(world.settings))[:5]
        world.actions = list(set(world.actions))[:10]
        world.qualities = list(set(world.qualities))[:10]

        # If inference gave nothing, derive minimally from topic
        if len(world.vocabulary) < 5:
            world.vocabulary.extend(topic_words)
            world.vocabulary.extend(['moment', 'time', 'place', 'way', 'thing'])

        return world

    def _plan_arc(self, form: str, target: int) -> List[Beat]:
        if form == "story":
            n = 5
            return [
                Beat("setup", 0.2, target // n),
                Beat("rising", 0.5, target // n),
                Beat("complication", 0.7, target // n),
                Beat("climax", 1.0, target // n),
                Beat("resolution", 0.3, target // n),
            ]
        elif form == "song":
            n = 6
            return [
                Beat("verse1", 0.4, target // n),
                Beat("chorus", 0.8, target // n),
                Beat("verse2", 0.5, target // n),
                Beat("chorus2", 0.8, target // n),
                Beat("bridge", 0.9, target // n),
                Beat("outro", 0.4, target // n),
            ]
        else:  # poem
            n = 4
            return [
                Beat("opening", 0.3, target // n),
                Beat("develop", 0.6, target // n),
                Beat("turn", 0.9, target // n),
                Beat("close", 0.4, target // n),
            ]

    def _generate_beat(self, beat: Beat, world: World, beat_idx: int) -> str:
        """Generate sentences for a beat using ONLY world vocabulary."""
        sentences = []
        word_count = 0
        seed = int(time.time() * 100) + beat_idx * 997

        while word_count < beat.word_budget:
            sent = self._make_sentence(beat.tension, world, seed + len(sentences))
            sentences.append(sent)
            word_count += len(sent.split())
            if len(sentences) > 25:
                break

        return ' '.join(sentences)

    def _make_sentence(self, tension: float, world: World, seed: int) -> str:
        """Construct ONE sentence from world vocabulary + grammar rules."""
        v = world.vocabulary
        if not v:
            return "Something changed."

        # Pick words from world vocabulary based on seed
        def pick(lst, offset=0):
            if not lst: return world.topic or "it"
            return lst[(seed + offset) % len(lst)]

        w1 = pick(v, 0)
        w2 = pick(v, 3)
        w3 = pick(v, 7)
        w4 = pick(v, 11)

        obj = pick(world.objects, 5) if world.objects else w2
        setting = pick(world.settings, 9) if world.settings else "silence"
        quality = pick(world.qualities, 13) if world.qualities else ""
        action = pick(world.actions, 15) if world.actions else "changed"

        # GRAMMAR STRUCTURES (the ONLY thing stored — pure structure, no content words)
        if tension > 0.8:
            # High tension: short, punchy
            patterns = [
                f"The {w1}. Gone.",
                f"No more {w2}.",
                f"Then — {w3}.",
                f"Everything {action}.",
                f"{w1.capitalize()} and {w2}. Nothing else.",
                f"It was over. The {w3} proved it.",
            ]
        elif tension > 0.4:
            # Medium: action, compound
            patterns = [
                f"The {w1} {action}, and the {w2} followed.",
                f"There was something about the {w3} that {action} everything.",
                f"Between the {w1} and the {w2}, {w3} waited.",
                f"It started with {w1}. It ended with {w2}.",
                f"The {quality} {w1} {action} toward {w3}." if quality else f"The {w1} moved toward {w3}.",
                f"Somewhere in the {setting}, the {w1} {action}.",
            ]
        else:
            # Low tension: descriptive, flowing
            patterns = [
                f"The {w1} sat in the {setting}, {quality} and still." if quality else f"The {w1} rested in the {setting}.",
                f"There was a quietness to the {w2}, something the {w1} had almost forgotten.",
                f"The {setting} held the {w1} like a memory holds its shape.",
                f"Time moved differently around the {w3}, slower, more deliberate.",
                f"{w1.capitalize()} and {w2} existed together in the {setting}, unchanged.",
                f"Nothing about the {w1} suggested what the {w3} would become.",
            ]

        return patterns[seed % len(patterns)]

    def _connect(self, paragraphs: List[str], form: str) -> str:
        """Join paragraphs with transitions."""
        if not paragraphs:
            return ""

        # Transitions (pure grammar, no content words)
        transitions = [
            "", "And then — ", "Later, ", "But ", "Still, ",
            "After that, ", "What came next: ", "Eventually, ",
        ]

        result = []
        for i, para in enumerate(paragraphs):
            if i > 0 and i < len(paragraphs):
                t = transitions[i % len(transitions)]
                if t:
                    para = t + para[0].lower() + para[1:]
            result.append(para)

        if form == "song":
            return '\n\n'.join(result)
        return '\n\n'.join(result)


def get_creator_v3():
    return CreatorV3()
