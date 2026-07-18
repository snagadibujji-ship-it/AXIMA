"""
AXIMA Observer — Cognitive perception layer.

The Observer NEVER answers questions. It only understands.

Responsibilities:
  • Extract entities (people, things, places, systems)
  • Detect goals (what the user wants to achieve)
  • Detect tasks (specific actions needed)
  • Detect facts (assertions about reality)
  • Detect concepts (abstract ideas being discussed)
  • Detect unknowns (what we don't know yet)
  • Estimate confidence in each extraction

Usage:
    from core.observer import Observer, Observation

    observer = Observer()
    obs = observer.observe("I need to fix the math router because it's dropping results")
    
    obs.goals       → [Goal("fix the math router")]
    obs.facts       → [Fact("math router is dropping results")]
    obs.entities    → [Entity("math router")]
    obs.unknowns    → [Unknown("why results are dropped")]
"""

import re
import time
from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any, Tuple


# ═══════════════════════════════════════════════════════════════
# OBSERVATION DATA STRUCTURES
# ═══════════════════════════════════════════════════════════════

@dataclass
class Entity:
    """A thing that exists in the world."""
    name: str
    entity_type: str = "unknown"    # person, system, concept, place, organization
    confidence: float = 0.8
    properties: Dict[str, Any] = field(default_factory=dict)


@dataclass
class DetectedGoal:
    """A goal detected in the input."""
    description: str
    verb: str = ""                  # The action verb (fix, build, create, improve)
    target: str = ""               # What it acts on
    urgency: float = 0.5           # 0=low, 1=critical
    confidence: float = 0.7


@dataclass
class DetectedTask:
    """A specific actionable task detected."""
    description: str
    parent_goal: str = ""           # Which goal this serves
    is_explicit: bool = True        # Explicitly stated vs inferred
    confidence: float = 0.7


@dataclass
class DetectedFact:
    """An assertion about reality."""
    statement: str
    fact_type: str = "assertion"    # assertion, measurement, definition, relationship
    subject: str = ""
    predicate: str = ""
    object: str = ""
    confidence: float = 0.8
    is_negation: bool = False


@dataclass
class DetectedConcept:
    """An abstract concept being discussed."""
    name: str
    domain: str = ""                # math, physics, programming, etc.
    relations: List[str] = field(default_factory=list)  # Related concepts
    confidence: float = 0.7


@dataclass
class DetectedUnknown:
    """Something we don't know yet."""
    question: str                   # What we don't know
    importance: float = 0.5         # How important to resolve
    related_to: str = ""            # Related entity/goal
    confidence: float = 0.6


@dataclass
class Observation:
    """Complete observation from a single input.
    
    This is what the Observer produces. It NEVER contains an answer,
    only an understanding of what was said.
    """
    raw_input: str
    timestamp: float = 0.0

    # Extracted elements
    entities: List[Entity] = field(default_factory=list)
    goals: List[DetectedGoal] = field(default_factory=list)
    tasks: List[DetectedTask] = field(default_factory=list)
    facts: List[DetectedFact] = field(default_factory=list)
    concepts: List[DetectedConcept] = field(default_factory=list)
    unknowns: List[DetectedUnknown] = field(default_factory=list)

    # Meta
    intent: str = "unknown"         # question, command, statement, request
    topic: str = ""                 # Primary topic
    mood: str = "neutral"           # neutral, urgent, frustrated, curious
    complexity: float = 0.5         # 0=simple, 1=complex
    confidence: float = 0.0         # Overall confidence in observation

    def __post_init__(self):
        if not self.timestamp:
            self.timestamp = time.time()

    @property
    def is_empty(self) -> bool:
        return not any([self.entities, self.goals, self.tasks,
                       self.facts, self.concepts, self.unknowns])

    def summary(self) -> Dict[str, Any]:
        return {
            "intent": self.intent,
            "topic": self.topic,
            "entities": len(self.entities),
            "goals": len(self.goals),
            "tasks": len(self.tasks),
            "facts": len(self.facts),
            "concepts": len(self.concepts),
            "unknowns": len(self.unknowns),
            "confidence": round(self.confidence, 2),
        }


# ═══════════════════════════════════════════════════════════════
# OBSERVER
# ═══════════════════════════════════════════════════════════════

class Observer:
    """The cognitive perception layer.
    
    Observes input and produces structured understanding.
    Never answers. Only perceives.
    """

    # Intent patterns
    _INTENT_PATTERNS = {
        'command': re.compile(
            r'^(?:fix|build|create|add|remove|delete|update|change|make|set|'
            r'implement|write|generate|deploy|run|start|stop|restart)\b', re.I),
        'question': re.compile(
            r'^(?:what|why|how|when|where|who|which|is|are|does|do|can|could|'
            r'would|should|will)\b|\?\s*$', re.I),
        'request': re.compile(
            r'^(?:please|can you|could you|I need|I want|help me|show me|'
            r'tell me|give me|explain)\b', re.I),
        'statement': re.compile(
            r'^(?:the|this|that|it|I|we|there|here)\b', re.I),
    }

    # Goal verb patterns
    _GOAL_VERBS = re.compile(
        r'\b(fix|solve|build|create|implement|improve|optimize|upgrade|'
        r'add|remove|redesign|refactor|deploy|configure|setup|'
        r'migrate|integrate|automate|test|debug|analyze)\b', re.I)

    # Fact patterns (X is Y, X has Y, X causes Y)
    _FACT_PATTERNS = [
        (re.compile(r'(.+?)\s+(?:is|are|was|were)\s+(.+?)(?:\.|$)', re.I), 'assertion'),
        (re.compile(r'(.+?)\s+(?:has|have|had)\s+(.+?)(?:\.|$)', re.I), 'assertion'),
        (re.compile(r'(.+?)\s+(?:causes?|produces?|leads?\s+to|results?\s+in)\s+(.+?)(?:\.|$)', re.I), 'relationship'),
        (re.compile(r'(.+?)\s+(?:depends?\s+on|requires?|needs?)\s+(.+?)(?:\.|$)', re.I), 'relationship'),
        (re.compile(r'(.+?)\s+(?:contains?|includes?|consists?\s+of)\s+(.+?)(?:\.|$)', re.I), 'relationship'),
    ]

    # Negation
    _NEGATION = re.compile(r"\b(?:not|n't|never|no|cannot|can't|won't|doesn't|isn't|aren't)\b", re.I)

    # Urgency markers
    _URGENCY_MARKERS = re.compile(
        r'\b(urgent|critical|asap|immediately|broken|crash|down|emergency|'
        r'blocking|stuck|deadline|priority|important)\b', re.I)

    # Domain detection
    _DOMAINS = {
        'math': re.compile(r'\b(equation|solve|derivative|integral|algebra|calculus|formula|math)\b', re.I),
        'physics': re.compile(r'\b(force|energy|velocity|momentum|quantum|gravity|wave)\b', re.I),
        'programming': re.compile(r'\b(code|function|class|api|bug|error|compile|deploy|git|database)\b', re.I),
        'architecture': re.compile(r'\b(system|module|engine|pipeline|router|plugin|graph|runtime)\b', re.I),
        'language': re.compile(r'\b(grammar|word|sentence|translate|language|speak|text)\b', re.I),
    }

    def observe(self, text: str) -> Observation:
        """Observe input and produce structured understanding.
        
        This is the primary cognitive perception function.
        It extracts everything meaningful from the input
        without attempting to answer or solve anything.
        """
        obs = Observation(raw_input=text)

        # Detect intent
        obs.intent = self._detect_intent(text)

        # Detect mood/urgency
        obs.mood = self._detect_mood(text)

        # Extract entities
        obs.entities = self._extract_entities(text)

        # Detect goals
        obs.goals = self._detect_goals(text)

        # Detect tasks
        obs.tasks = self._detect_tasks(text, obs.goals)

        # Detect facts
        obs.facts = self._detect_facts(text)

        # Detect concepts
        obs.concepts = self._detect_concepts(text)

        # Detect unknowns
        obs.unknowns = self._detect_unknowns(text, obs.intent)

        # Set topic
        obs.topic = self._determine_topic(obs)

        # Estimate complexity
        obs.complexity = self._estimate_complexity(text, obs)

        # Overall confidence
        obs.confidence = self._compute_confidence(obs)

        return obs

    def _detect_intent(self, text: str) -> str:
        """Classify the primary intent of the input."""
        for intent, pattern in self._INTENT_PATTERNS.items():
            if pattern.search(text):
                return intent
        return "statement"

    def _detect_mood(self, text: str) -> str:
        """Detect urgency/mood from markers."""
        if self._URGENCY_MARKERS.search(text):
            return "urgent"
        if '!' in text or text.isupper():
            return "emphatic"
        if '?' in text:
            return "curious"
        return "neutral"

    def _extract_entities(self, text: str) -> List[Entity]:
        """Extract named entities from text."""
        entities = []
        # Technical entities (capitalized or compound words)
        tech_pattern = re.compile(r'\b([A-Z][a-zA-Z]*(?:\s+[A-Z][a-zA-Z]*)*)\b')
        for m in tech_pattern.finditer(text):
            name = m.group(1)
            if len(name) > 2 and name not in ('The', 'This', 'That', 'What', 'How', 'Why',
                                                'When', 'Where', 'Who', 'Which', 'Please',
                                                'Can', 'Could', 'Would', 'Should', 'Will'):
                entities.append(Entity(name=name, entity_type="system", confidence=0.7))

        # Quoted entities
        for m in re.finditer(r'"([^"]+)"|\'([^\']+)\'|`([^`]+)`', text):
            name = m.group(1) or m.group(2) or m.group(3)
            entities.append(Entity(name=name, entity_type="reference", confidence=0.9))

        # Technical terms (snake_case, camelCase, paths)
        for m in re.finditer(r'\b([a-z]+_[a-z_]+|[a-z]+[A-Z][a-zA-Z]+|[\w/]+\.(?:py|js|ts|md|json))\b', text):
            entities.append(Entity(name=m.group(1), entity_type="code", confidence=0.9))

        return entities

    def _detect_goals(self, text: str) -> List[DetectedGoal]:
        """Detect goals (desired outcomes) in the text."""
        goals = []
        sentences = re.split(r'[.!;]|\n', text)

        for sent in sentences:
            sent = sent.strip()
            if not sent:
                continue

            # Look for goal verbs
            verb_match = self._GOAL_VERBS.search(sent)
            if verb_match:
                verb = verb_match.group(1).lower()
                # Target is what comes after the verb
                after_verb = sent[verb_match.end():].strip()
                target = re.sub(r'\s*(?:because|since|so that|to|for).*$', '', after_verb, flags=re.I)
                target = target.strip(' .,;')

                if target and len(target) > 3:
                    urgency = 0.8 if self._URGENCY_MARKERS.search(sent) else 0.5
                    goals.append(DetectedGoal(
                        description=f"{verb} {target}",
                        verb=verb,
                        target=target,
                        urgency=urgency,
                        confidence=0.75,
                    ))

            # "I need X", "I want X" patterns
            need_match = re.match(r'(?:I|we)\s+(?:need|want|must|should|have to)\s+(?:to\s+)?(.+)', sent, re.I)
            if need_match and not verb_match:
                desc = need_match.group(1).strip(' .,;')
                if desc and len(desc) > 3:
                    goals.append(DetectedGoal(
                        description=desc,
                        verb="achieve",
                        target=desc,
                        urgency=0.6,
                        confidence=0.7,
                    ))

        return goals

    def _detect_tasks(self, text: str, goals: List[DetectedGoal]) -> List[DetectedTask]:
        """Detect specific actionable tasks."""
        tasks = []

        # Numbered/bulleted items are almost always tasks
        for m in re.finditer(r'(?:^|\n)\s*(?:\d+[.)]\s*|[-•*]\s+)(.+)', text):
            item = m.group(1).strip()
            if item and len(item) > 5:
                parent = goals[0].description if goals else ""
                tasks.append(DetectedTask(
                    description=item,
                    parent_goal=parent,
                    is_explicit=True,
                    confidence=0.85,
                ))

        # Imperative sentences (start with verb)
        for sent in re.split(r'[.!;]|\n', text):
            sent = sent.strip()
            if sent and re.match(r'^(?:Add|Remove|Fix|Update|Create|Delete|Set|Move|Copy|Run|Test|Check)\b', sent, re.I):
                if not any(t.description == sent for t in tasks):
                    tasks.append(DetectedTask(
                        description=sent,
                        parent_goal=goals[0].description if goals else "",
                        is_explicit=True,
                        confidence=0.8,
                    ))

        return tasks

    def _detect_facts(self, text: str) -> List[DetectedFact]:
        """Detect factual assertions in the text."""
        facts = []

        for pattern, fact_type in self._FACT_PATTERNS:
            for m in pattern.finditer(text):
                subject = m.group(1).strip()
                obj = m.group(2).strip()[:100]
                # Skip if too short or too long
                if len(subject) < 2 or len(subject) > 80:
                    continue
                is_neg = bool(self._NEGATION.search(m.group(0)))
                facts.append(DetectedFact(
                    statement=m.group(0).strip()[:150],
                    fact_type=fact_type,
                    subject=subject,
                    object=obj,
                    is_negation=is_neg,
                    confidence=0.7,
                ))

        return facts[:10]  # Cap at 10 to avoid noise

    def _detect_concepts(self, text: str) -> List[DetectedConcept]:
        """Detect abstract concepts being discussed."""
        concepts = []
        seen = set()

        for domain, pattern in self._DOMAINS.items():
            for m in pattern.finditer(text):
                name = m.group(1).lower()
                if name not in seen:
                    seen.add(name)
                    concepts.append(DetectedConcept(
                        name=name,
                        domain=domain,
                        confidence=0.75,
                    ))

        return concepts

    def _detect_unknowns(self, text: str, intent: str) -> List[DetectedUnknown]:
        """Detect things we don't know / questions being asked."""
        unknowns = []

        # Direct questions
        if intent == "question":
            # Extract the question itself
            q = text.strip().rstrip('?')
            unknowns.append(DetectedUnknown(
                question=q,
                importance=0.8,
                confidence=0.9,
            ))

        # "I don't know", "not sure", "unclear" signals
        unsure_matches = re.finditer(
            r"(?:don't know|not sure|unclear|uncertain|no idea)\s+(?:about|why|how|what|if|whether)\s+(.+?)(?:\.|$)",
            text, re.I)
        for m in unsure_matches:
            unknowns.append(DetectedUnknown(
                question=m.group(1).strip(),
                importance=0.6,
                confidence=0.7,
            ))

        # "why" embedded in statements
        why_matches = re.finditer(r'\b(?:because|since|reason)\b', text, re.I)
        if not list(why_matches) and 'why' not in text.lower() and intent != 'question':
            # No causal explanation given for problems → unknown
            for fact in re.finditer(r'(.+?)\s+(?:is broken|fails|crashes|doesn\'t work)', text, re.I):
                unknowns.append(DetectedUnknown(
                    question=f"why does {fact.group(1)} fail",
                    importance=0.7,
                    related_to=fact.group(1),
                    confidence=0.5,
                ))

        return unknowns

    def _determine_topic(self, obs: Observation) -> str:
        """Determine the primary topic from extracted data."""
        if obs.goals:
            return obs.goals[0].target or obs.goals[0].description
        if obs.concepts:
            return obs.concepts[0].name
        if obs.entities:
            return obs.entities[0].name
        if obs.facts:
            return obs.facts[0].subject
        return ""

    def _estimate_complexity(self, text: str, obs: Observation) -> float:
        """Estimate cognitive complexity of the input."""
        score = 0.0
        # Length contributes
        score += min(0.3, len(text) / 500)
        # Multiple goals = complex
        score += min(0.3, len(obs.goals) * 0.15)
        # Multiple concepts = complex
        score += min(0.2, len(obs.concepts) * 0.1)
        # Unknowns = complex
        score += min(0.2, len(obs.unknowns) * 0.1)
        return min(1.0, score)

    def _compute_confidence(self, obs: Observation) -> float:
        """Overall confidence in the observation."""
        if obs.is_empty:
            return 0.2
        # Average confidence of all extractions
        confidences = []
        for e in obs.entities: confidences.append(e.confidence)
        for g in obs.goals: confidences.append(g.confidence)
        for t in obs.tasks: confidences.append(t.confidence)
        for f in obs.facts: confidences.append(f.confidence)
        for c in obs.concepts: confidences.append(c.confidence)
        if confidences:
            return sum(confidences) / len(confidences)
        return 0.3
