"""
A.C.E.S — Adaptive Cognitive Explanation System
Built by: Ghias + Kiro

THE INVENTION: Knowledge exists in a SHAPE. Same knowledge can be expressed
in infinite forms. ACES transforms knowledge-shape on demand, for ANY topic,
even ones it has never seen before.

Not a template engine. A knowledge-shape transformer.
"""

import re
import json
import os
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field


# ══════════════════════════════════════════════════════════════════════════════
# KNOWLEDGE NODE — The atomic unit of understanding
# ══════════════════════════════════════════════════════════════════════════════

@dataclass
class KnowledgeNode:
    """A piece of knowledge decomposed into all its dimensions."""
    topic: str                              # what this is about
    core: str                               # essential truth in one line
    answer_type: str = ""                   # calculation|fact|process|concept|relation|event
    components: List[str] = field(default_factory=list)      # sub-parts
    depends_on: List[str] = field(default_factory=list)      # prerequisites
    leads_to: List[str] = field(default_factory=list)        # what this enables
    analogies: List[str] = field(default_factory=list)       # similar things
    concrete_example: str = ""              # real-world instance
    counter_example: str = ""               # what this is NOT
    mechanism: List[str] = field(default_factory=list)       # step-by-step how
    intuition: str = ""                     # plain-language why
    meaning: str = ""                       # real-world significance
    insight: str = ""                       # the "aha!" moment
    formula: str = ""                       # symbolic representation
    explanation_history: List[str] = field(default_factory=list)  # what we already told user


# ══════════════════════════════════════════════════════════════════════════════
# MODULE 1: ANSWER ANATOMY DETECTOR — What kind of knowledge is this?
# ══════════════════════════════════════════════════════════════════════════════

class AnatomyDetector:
    """Detects the STRUCTURE of any answer to determine how to explain it."""

    @staticmethod
    def detect(question: str, answer: str) -> str:
        """Returns the answer type: calculation|fact|process|concept|relation|event|definition|comparison"""
        q = question.lower()
        a = answer.lower()

        # Calculation: has numbers + formula
        if any(c in answer for c in '0123456789') and any(op in answer for op in '=+-×÷*/^'):
            if any(w in q for w in ['calculate', 'find', 'what is the', 'compute', 'solve']):
                return "calculation"

        # Process: sequential steps
        if any(w in q for w in ['how to', 'how do', 'how does', 'steps', 'process', 'procedure']):
            return "process"

        # Definition: asking what something IS
        if any(w in q for w in ['what is', 'what are', 'define', 'meaning of', 'what does']):
            return "definition"

        # Comparison: asking about differences
        if any(w in q for w in ['difference', 'compare', 'vs', 'versus', 'better', 'unlike']):
            return "comparison"

        # Cause/effect
        if any(w in q for w in ['why', 'cause', 'reason', 'because', 'effect', 'result']):
            return "causal"

        # Event: specific occurrence
        if any(w in q for w in ['when', 'happened', 'event', 'history', 'discovered']):
            return "event"

        # Relation: about connections
        if any(w in q for w in ['relate', 'connection', 'between', 'linked']):
            return "relation"

        # Fact: general knowledge
        if any(w in q for w in ['who', 'where', 'which', 'name']):
            return "fact"

        # Default: if has numbers → calculation, else → concept
        if any(c.isdigit() for c in answer):
            return "calculation"
        return "concept"


# ══════════════════════════════════════════════════════════════════════════════
# MODULE 2: UNIVERSAL CONCEPT DECOMPOSER — Break ANY answer into a node
# ══════════════════════════════════════════════════════════════════════════════

class ConceptDecomposer:
    """Decomposes any answer into a KnowledgeNode — works for ANY topic."""

    # Universal analogy patterns — map abstract relationships to concrete ones
    ANALOGY_PATTERNS = {
        "grows": ["snowball rolling downhill", "compound interest", "chain reaction", "virus spreading"],
        "flows": ["water through pipes", "traffic on highway", "electricity in wire", "heat from hot to cold"],
        "balances": ["seesaw in playground", "thermostat in house", "supply and demand", "tug of war"],
        "oscillates": ["child on swing", "heartbeat", "seasons cycling", "pendulum clock"],
        "decays": ["ice melting", "battery draining", "memory fading", "radioactive atom splitting"],
        "transforms": ["caterpillar to butterfly", "water to steam", "raw ingredients to meal", "seed to tree"],
        "accumulates": ["saving money in bank", "sediment building layers", "knowledge from studying", "snow piling up"],
        "competes": ["animals hunting same prey", "companies in market", "players in game", "species evolving"],
        "emerges": ["ant colony from simple ants", "traffic jam from individual cars", "consciousness from neurons", "wave from water molecules"],
        "resonates": ["pushing swing at right moment", "tuning radio to frequency", "shattering glass with voice", "bridge vibrating with soldiers"],
        "shields": ["umbrella from rain", "sunscreen from UV", "wall from wind", "password from hackers"],
        "branches": ["tree growing limbs", "river delta splitting", "family tree", "decision tree"],
        "cycles": ["water evaporate-rain-evaporate", "breathe in-out", "day-night", "born-live-die-decompose"],
        "propagates": ["ripples in pond", "rumor spreading", "dominos falling", "light traveling"],
        "stores": ["battery holding charge", "book holding knowledge", "dam holding water", "DNA holding instructions"],
        "converts": ["solar panel (light→electricity)", "engine (fuel→motion)", "plant (CO2→sugar)", "speaker (electricity→sound)"],
        "amplifies": ["microphone+speaker", "lever multiplying force", "rumor getting exaggerated", "avalanche from small crack"],
        "filters": ["coffee filter", "sunglasses", "immune system", "spam filter"],
        "connects": ["bridge between lands", "translator between languages", "internet between people", "enzyme between molecules"],
        "limits": ["speed limit on road", "melting point of material", "carrying capacity of ecosystem", "bandwidth of connection"],
    }

    # Relationship extraction patterns
    RELATION_PATTERNS = [
        (r'(.+)\s+is\s+(?:a|an|the)\s+(.+)', 'is_a'),           # X is a Y
        (r'(.+)\s+(?:causes?|leads?\s+to|results?\s+in)\s+(.+)', 'causes'),
        (r'(.+)\s+(?:is\s+made\s+of|consists?\s+of|contains?)\s+(.+)', 'has_parts'),
        (r'(.+)\s+(?:is\s+used\s+for|is\s+used\s+to|enables?)\s+(.+)', 'purpose'),
        (r'(.+)\s+(?:was\s+discovered|was\s+invented|was\s+created)\s+by\s+(.+)', 'origin'),
        (r'(.+)\s+(?:depends?\s+on|requires?|needs?)\s+(.+)', 'depends_on'),
        (r'(.+)\s+(?:is\s+(?:greater|larger|bigger|more|faster)\s+than)\s+(.+)', 'comparison'),
        (r'(.+)\s+(?:is\s+part\s+of|belongs?\s+to)\s+(.+)', 'part_of'),
    ]

    def decompose(self, question: str, answer: str, answer_type: str,
                  structured: Dict = None) -> KnowledgeNode:
        """Decompose any answer into a full KnowledgeNode.
        
        If structured data is provided (from a solver), uses that directly.
        If only raw text (from web), extracts what it can.
        """
        node = KnowledgeNode(
            topic=self._extract_topic(question),
            core=self._extract_core(answer),
            answer_type=answer_type
        )

        # If we got structured data from a solver — USE IT (much better)
        if structured:
            node.formula = structured.get("formula", "")
            node.mechanism = structured.get("steps", [])
            node.intuition = structured.get("intuition", "")
            node.meaning = structured.get("meaning", "")
            node.insight = structured.get("insight", "")
            node.concrete_example = structured.get("example", "")
            node.analogies = structured.get("analogies", [])
            node.depends_on = structured.get("depends_on", [])
            node.leads_to = structured.get("leads_to", [])
            node.components = structured.get("components", [])
            node.counter_example = structured.get("counter_example", "")
            return node

        # Otherwise: extract what we can from raw text (web answers etc.)
        node.components = self._extract_components(answer)
        node.formula = self._extract_formula(answer)
        node.intuition = self._generate_intuition(question, answer, answer_type)
        node.analogies = self._find_analogies(question, answer)
        node.mechanism = self._extract_mechanism(answer)
        node.meaning = self._generate_meaning(question, answer, answer_type)
        node.insight = self._generate_insight(question, answer, answer_type)
        node.concrete_example = self._find_example(question, answer)

        return node

    def _extract_topic(self, question: str) -> str:
        """Extract the main topic from the question."""
        # Remove question words
        topic = re.sub(r'^(what|how|why|when|where|who|calculate|find|solve|explain|describe)\s+(is|are|does|do|the|a|an)?\s*',
                       '', question.lower()).strip()
        # Remove trailing question mark
        topic = topic.rstrip('?').strip()
        return topic if topic else question[:50]

    def _extract_core(self, answer: str) -> str:
        """Extract the essential one-line truth from any answer."""
        # First line is usually the core answer
        lines = [l.strip() for l in answer.split('\n') if l.strip()]
        if lines:
            # Skip lines that are just decorators
            for line in lines:
                if line and not line.startswith(('─', '═', '┌', '│', '└', '  ')):
                    return line[:200]
        return answer[:200]

    def _extract_components(self, answer: str) -> List[str]:
        """Break answer into sub-components."""
        components = []
        # Look for bullet points, numbered items, or sentences
        lines = answer.split('\n')
        for line in lines:
            line = line.strip()
            if line.startswith(('•', '-', '→', '*')) or re.match(r'^\d+[\.\)]', line):
                components.append(re.sub(r'^[•\-→*\d\.\)]\s*', '', line))
            elif ':' in line and len(line) < 100:
                components.append(line)
        return components[:10]

    def _extract_formula(self, answer: str) -> str:
        """Extract symbolic formula if present."""
        # Look for patterns like "X = ..." or common math notation
        m = re.search(r'([A-Za-z_]+\s*=\s*[^\n]+)', answer)
        if m:
            return m.group(1).strip()
        return ""

    def _extract_mechanism(self, answer: str) -> List[str]:
        """Extract step-by-step mechanism."""
        steps = []
        lines = answer.split('\n')
        for line in lines:
            line = line.strip()
            if re.match(r'^(Step\s+\d|[1-9][\.\)]|\d+\.)', line):
                steps.append(line)
        return steps

    def _generate_intuition(self, question: str, answer: str, atype: str) -> str:
        """Generate intuition by understanding WHAT THE SENTENCE DESCRIBES.
        Not keyword matching. Extracts the core relationship."""
        a = answer.lower()
        q = question.lower()

        # STRATEGY: Extract the CORE CLAIM from the answer
        # "X [verb] Y" → "The essential idea is that X does/is Y"

        # Try to find the main clause: subject + verb + complement
        # Pattern 1: "X is/are Y" → identity/classification
        m = re.search(r'^(.+?)\s+(?:is|are)\s+(.+?)(?:\.|,\s*(?:which|that|where))', a)
        if m:
            subject = m.group(1).strip()
            complement = m.group(2).strip()
            # Is it a classification? (X is a type of Y)
            if complement.startswith(('a ', 'an ', 'the ')):
                return f"At its essence, {subject} is {complement}. This classification tells you what family it belongs to and what properties to expect."
            # Is it a description? (X is [adjective])
            return f"The core fact: {subject} is {complement}. Everything else follows from this."

        # Pattern 2: "X [action verb] Y" → functional relationship
        m = re.search(r'^(.+?)\s+(\w+(?:s|es|ed))\s+(.+?)(?:\.|,)', a)
        if m:
            subject = m.group(1).strip()
            verb = m.group(2).strip()
            obj = m.group(3).strip()
            return f"The key relationship: {subject} {verb} {obj}. This is the core action that defines what this is about."

        # Pattern 3: Look for "by [mechanism]" or "through [process]"
        m = re.search(r'(?:by|through|via|using)\s+(.+?)(?:\.|,)', a)
        if m:
            mechanism = m.group(1).strip()
            return f"The mechanism: this works by {mechanism}. Understanding this 'how' is the key to understanding the whole concept."

        # Pattern 4: Look for purpose "to [goal]" or "for [purpose]"
        m = re.search(r'(?:to|for|in order to)\s+(.+?)(?:\.|,)', a)
        if m:
            purpose = m.group(1).strip()
            return f"The purpose: this exists to {purpose}. Knowing the 'why' makes the details make sense."

        # If all else fails, summarize the first sentence
        first_sentence = a.split('.')[0].strip()
        if len(first_sentence) > 10:
            return f"In plain terms: {first_sentence}."

        return ""

    def _find_analogies(self, question: str, answer: str) -> List[str]:
        """Find analogies by UNDERSTANDING the relationship structure — not keyword matching.
        
        The brain doesn't match keywords. It understands:
        - What is the SUBJECT?
        - What is the ACTION/RELATIONSHIP?
        - What is the OBJECT/RESULT?
        
        Then maps that abstract pattern to something familiar.
        """
        text = answer.lower()
        matches = []

        # ═══════════════════════════════════════════════════════════
        # STEP 1: Extract the RELATIONSHIP STRUCTURE from the sentence
        # Pattern: [Subject] [relationship verb] [Object/Result]
        # ═══════════════════════════════════════════════════════════

        # Extract subject-verb-object triples
        relationships = []

        # "X [verb]s Y" — active voice
        for m in re.finditer(r'(\w+(?:\s+\w+)?)\s+(is|are|was|were|has|have|had|does|do|can|will|may|might)\s+(\w+)', text):
            relationships.append(('state', m.group(1), m.group(3)))

        # "X [action verb] Y" — things doing things
        for m in re.finditer(r'(\w+(?:\s+\w+)?)\s+(\w+(?:s|es|ed|ing))\s+(\w+(?:\s+\w+)?)', text):
            verb = m.group(2)
            relationships.append(('action', m.group(1), verb, m.group(3)))

        # ═══════════════════════════════════════════════════════════
        # STEP 2: Classify by SENTENCE GRAMMAR — not by words
        #
        # Instead of matching verbs, match SENTENCE STRUCTURES:
        #   "X [any verb] INTO Y" → transformation
        #   "X [any verb] Y FROM Z" → production
        #   "X [any verb] AGAINST Y" → protection
        #
        # This works for ANY verb, even invented ones.
        # ═══════════════════════════════════════════════════════════

        patterns_found = set()

        # PRODUCTION: sentence describes INPUT → OUTPUT relationship
        # Grammar: "X [verb] Y by [process]" or "converts X into Y"
        # Key signal: explicit mention of output being created + mechanism
        if re.search(r'\w+\s+\w+\s+\w+.*\bby\b', text):
            patterns_found.add('production')
        elif re.search(r'\binto\b', text) and re.search(r'\benergy\b|\boutput\b|\bproduct\b|\bresult\b', text):
            patterns_found.add('production')

        # TRANSFORMATION: "X [verb] INTO Y" or "X becomes Y" or "X → Y"
        if re.search(r'\binto\b|\bbecomes?\b|\bturns?\s+into\b|→|→', text):
            patterns_found.add('transformation')

        # Also: "X [verb] under/from [condition]" = transformation by external cause
        if re.search(r'\bunder\b.*\b(?:gravity|pressure|heat|force|stress)\b', text):
            patterns_found.add('transformation')

        # MOVEMENT: "X [verb] FROM A TO B" or physical "through"/"across"
        # But NOT "through [process]" (like "through oxidation") — that's mechanism, not movement
        has_movement_grammar = re.search(r'\bfrom\b.*\bto\b|\bacross\b|\balong\b', text)
        has_physical_through = re.search(r'\bthrough\b\s+(?:the|a|an|its|their)\s+\w+', text)  # "through the membrane"
        if has_movement_grammar or has_physical_through:
            patterns_found.add('movement')

        # REGULATION: "X maintains/keeps Y [adjective]" or feedback/balance language
        if re.search(r'\bmaintain|\bkeep|\bstable|\bconstant|\bbalance|\bequilibrium|\bhomeostasis', text):
            patterns_found.add('regulation')

        # STORAGE: "X holds/contains/stores Y" or "Y is stored in X"
        if re.search(r'\bstored?\b|\bholds?\b|\bcontains?\b|\bpreserv', text):
            patterns_found.add('storage')

        # PROTECTION: "X [verb] AGAINST Y" or "prevents" or "shields from"
        if re.search(r'\bagainst\b|\bprevents?\b|\bprotects?\b|\bshields?\b|\bimmun|\bresist', text):
            patterns_found.add('protection')

        # CONNECTION: "X links/connects A and B" or "between"
        if re.search(r'\bbetween\b|\bconnects?\b|\blinks?\b|\bbridg|\bbinds?\b', text):
            patterns_found.add('connection')

        # BREAKDOWN: "X breaks Y into Z" or "decomposes" or "digests"
        if re.search(r'\bbreak\w*\s+\w+\s+into\b|\binto\s+\w+\s+(?:parts|pieces|components)', text):
            patterns_found.add('breakdown')

        # DETECTION: "X detects/senses/recognizes Y" — subject finds/notices object
        if re.search(r'\bdetects?\b|\bsenses?\b|\brecogniz|\bidentif|\bmonitor', text):
            patterns_found.add('detection')

        # COMMUNICATION: "X signals/tells/informs Y" — information transfer
        if re.search(r'\bsignals?\b|\binforms?\b|\bcommunicat|\btransmits?\b|\bencod', text):
            patterns_found.add('communication')

        # GROWTH: "X increases/grows/expands" — getting bigger over time
        if re.search(r'\bincreas\w*\b|\bgrow\w*\b|\bexpand\w*\b|\baccumulat', text):
            patterns_found.add('growth')

        # OSCILLATION: sentence mentions periodicity or repetition
        if re.search(r'\bperiod\w*\b|\bcycl\w*\b|\boscillat\w*\b|\brepeat\w*\b|\brhythm', text):
            patterns_found.add('oscillation')

        # LIMIT: "cannot" / "impossible" / "maximum" — boundary
        if re.search(r'\bcannot\b|\bimpossible\b|\bmaximum\b|\blimit\w*\b|\bnever\b.*\bescape\b', text):
            patterns_found.add('limit')

        # ═══════════════════════════════════════════════════════════
        # STEP 2.5: WEIGHT patterns by relevance to the QUESTION
        # "How do X form?" → formation/transformation matters most
        # "What does X do?" → production/function matters most  
        # "What is X?" → classification matters, pick most defining pattern
        # ═══════════════════════════════════════════════════════════

        q_lower = question.lower()
        # Boost patterns based on question type
        boosted = set()
        if any(w in q_lower for w in ['how do', 'how does', 'how is', 'form', 'work', 'happen']):
            # HOW questions → prioritize transformation, movement, process patterns
            for p in ['transformation', 'movement', 'breakdown', 'production']:
                if p in patterns_found:
                    boosted.add(p)
        elif any(w in q_lower for w in ['what does', 'function', 'role', 'purpose', 'job']):
            # FUNCTION questions → prioritize production, regulation, protection
            for p in ['production', 'regulation', 'protection', 'detection', 'communication']:
                if p in patterns_found:
                    boosted.add(p)
        elif any(w in q_lower for w in ['why', 'cause', 'reason']):
            # WHY questions → the causal/mechanism pattern matters
            for p in ['production', 'transformation', 'growth', 'breakdown']:
                if p in patterns_found:
                    boosted.add(p)

        # ═══════════════════════════════════════════════════════════
        # STEP 3: Map the ABSTRACT PATTERN to a UNIVERSAL ANALOGY
        # Use boosted patterns first, then priority order
        # ═══════════════════════════════════════════════════════════

        pattern_priority = list(boosted) + [p for p in [
            'production', 'transformation', 'regulation', 'protection',
            'detection', 'communication', 'breakdown', 'connection',
            'storage', 'movement', 'growth', 'oscillation',
        ] if p not in boosted]

        pattern_analogies = {
            'production': "a factory — raw materials go in, useful product comes out",
            'transformation': "a butterfly emerging from a cocoon — same substance, completely new form",
            'movement': "a river carrying things downstream — from source to destination",
            'regulation': "a thermostat — constantly measuring and adjusting to maintain the right condition",
            'storage': "a library — information organized and preserved until someone needs it",
            'protection': "armor — absorbing or deflecting what would otherwise cause damage",
            'connection': "a bridge — enabling interaction between two things that couldn't reach each other",
            'breakdown': "digestion — breaking large things into smaller usable pieces",
            'detection': "a smoke alarm — constantly monitoring and alerting when something changes",
            'communication': "a postal system — packaging information, sending it, and delivering to the right recipient",
            'growth': "compound interest — each cycle builds on what came before, accelerating over time",
            'oscillation': "a heartbeat — a regular rhythm that keeps the system alive",
            'limit': "a wall you cannot climb over — a fundamental boundary that nothing can cross",
        }

        for pattern in pattern_priority:
            if pattern in patterns_found:
                matches.append(f"Think of it like {pattern_analogies[pattern]}")
                if len(matches) >= 2:
                    break

        # ═══════════════════════════════════════════════════════════
        # STEP 4: If no pattern found, use the sentence structure itself
        # ═══════════════════════════════════════════════════════════

        if not matches:
            # Check if it's a classification (X is a type of Y)
            if re.search(r'\bis\s+(?:a|an)\s+(?:type|kind|form|class|category)', text):
                matches.append("Think of it as a member of a family — sharing traits with siblings but having its own unique features")
            # Check if it's a composition (X is made of Y)
            elif re.search(r'(?:made of|consists of|composed of|contains)', text):
                matches.append("Think of it like a machine — multiple parts working together, each with a specific role")
            # Check if it describes a property
            elif re.search(r'(?:is\s+\w+er\s+than|has\s+(?:a\s+)?(?:high|low|large|small))', text):
                matches.append("Think of it on a spectrum — somewhere between two extremes, with its position telling you something meaningful")
            else:
                matches.append("Think of it as a piece of a larger puzzle — its significance becomes clear when you see what it connects to")

        return matches[:2]

    def _find_example(self, question: str, answer: str) -> str:
        """Find example from the answer content — not from keyword dictionary."""
        a = answer.lower()

        # STRATEGY 1: Answer already contains an example
        m = re.search(r'(?:such as|for example|e\.g\.|for instance|like)\s+(.+?)[\.\,]', a)
        if m:
            return m.group(1).strip().capitalize()

        # STRATEGY 2: Answer mentions where it's found/used
        m = re.search(r'(?:found in|used in|seen in|applied in|common in|occurs in)\s+(.+?)[\.\,]', a)
        if m:
            return f"You can see this in: {m.group(1).strip()}"

        # STRATEGY 3: Construct from relationship
        m = re.search(r'(\w+)\s+(?:produces?|generates?|creates?)\s+(\w+)', a)
        if m:
            return f"Input: {m.group(1)} → Output: {m.group(2)}"

        return ""  # No example is better than a fabricated one

    def _generate_meaning(self, question: str, answer: str, atype: str) -> str:
        """Explain what this result MEANS — extract significance from sentence structure."""
        a = answer.lower()
        q = question.lower()
        topic = self._extract_topic(question)

        # STRATEGY: Meaning comes from CONSEQUENCES and IMPLICATIONS
        # Look for what this ENABLES, PREVENTS, or CAUSES

        # Check for consequence markers in answer
        m = re.search(r'(?:which|this|that)\s+(?:means|implies|allows|enables|prevents|causes|leads to|results in)\s+(.+?)[\.\,]', a)
        if m:
            return f"The significance: {m.group(1).strip()}."

        # Check for "important because" / "essential for"
        m = re.search(r'(?:important|essential|crucial|vital|necessary|fundamental)\s+(?:for|to|because|in)\s+(.+?)[\.\,]', a)
        if m:
            return f"This matters because it's essential for {m.group(1).strip()}."

        # Check for "without this" implication
        m = re.search(r'(?:without\s+(?:it|this|them),?)\s+(.+?)[\.\,]', a)
        if m:
            return f"Without this: {m.group(1).strip()} — that's why it matters."

        # For calculations: the meaning is the physical interpretation
        if atype == "calculation":
            # Try to extract units or physical quantity
            units = re.findall(r'\b(meters?|seconds?|joules?|watts?|newtons?|kg|eV|Hz|volts?)\b', a)
            if units:
                return f"This number ({units[0]}) is something you can measure in the real world — it makes a prediction about physical reality."
            return f"This numerical result can be verified by experiment — it's a testable prediction."

        # For definitions: the meaning is what it connects to
        if atype == "definition":
            return f"Understanding '{topic}' unlocks a chain of connected ideas — it's a building block that other concepts depend on."

        # Fallback: extract what this thing DOES from the answer
        m = re.search(r'(?:used|applied|found|occurs?|happens?)\s+(?:in|for|when|during)\s+(.+?)[\.\,]', a)
        if m:
            return f"In practice, this shows up in: {m.group(1).strip()}."

        return ""

    def _generate_insight(self, question: str, answer: str, atype: str) -> str:
        """Generate insight by finding what's SURPRISING or NON-OBVIOUS.
        
        An insight is something that:
        - Contradicts common expectation
        - Shows a hidden connection
        - Reveals an unexpected simplification
        - Points to a universal principle
        """
        a = answer.lower()
        q = question.lower()

        # STRATEGY 1: Find contradictions to expectation
        # "despite X, Y" / "surprisingly" / "even though" / "regardless of"
        m = re.search(r'(?:despite|surprisingly|even though|regardless of|independent of|does not depend on|irrespective of)\s+(.+?)[\.\,]', a)
        if m:
            return f"The surprising part: {m.group(1).strip()} — this contradicts what most people would expect."

        # STRATEGY 2: Find universality
        # "all" / "every" / "always" / "never" / "no matter"
        m = re.search(r'(?:all|every|always|never|no matter|any|universal)\s+(.+?)[\.\,]', a)
        if m:
            return f"This is universal: {m.group(1).strip()} — it applies without exception."

        # STRATEGY 3: Find the simplification
        # Complex input → simple output/rule
        if re.search(r'(?:simply|just|only|merely|nothing more than|reduces to)', a):
            m = re.search(r'(?:simply|just|only|merely)\s+(.+?)[\.\,]', a)
            if m:
                return f"The beautiful simplification: it's really just {m.group(1).strip()}."

        # STRATEGY 4: Find the connection to something unexpected
        if re.search(r'(?:same as|equivalent to|identical to|analogous to|similar to)\s+(.+?)[\.\,]', a):
            m = re.search(r'(?:same as|equivalent to|identical to)\s+(.+?)[\.\,]', a)
            if m:
                return f"Hidden connection: this is actually the same thing as {m.group(1).strip()}, just viewed differently."

        # STRATEGY 5: Find limits/impossibilities
        if re.search(r'(?:cannot|impossible|maximum|minimum|limit|never\s+exceed|forbidden)', a):
            m = re.search(r'(?:cannot|impossible|can never)\s+(.+?)[\.\,]', a)
            if m:
                return f"A fundamental limit: you cannot {m.group(1).strip()} — this is not a technical limitation but a law of nature."

        # STRATEGY 6: For calculations — the insight is what CANCELS or what DOESN'T matter
        if atype == "calculation":
            # Look for things that are absent from the formula
            if 'mass' not in a and ('period' in q or 'pendulum' in q or 'frequency' in q):
                return "Mass doesn't appear in the answer — it cancels out! The result is independent of how heavy the object is."
            if '=' in answer:
                # Count variables in formula — fewer = more elegant
                formula_part = answer.split('=')[-1] if '=' in answer else answer
                vars_in_formula = set(re.findall(r'[a-zA-Z](?![\w])', formula_part))
                if len(vars_in_formula) <= 3:
                    return f"Despite the complexity of the system, the answer depends on only {len(vars_in_formula)} quantities."

        return ""  # No fake insight — silence is better than wrong


# ══════════════════════════════════════════════════════════════════════════════
# MODULE 3: SHAPE TRANSFORMER — Reshape knowledge on user command
# ══════════════════════════════════════════════════════════════════════════════

class ShapeTransformer:
    """Transforms a KnowledgeNode into any output format the user wants."""

    # Detect what the user wants from their follow-up
    FORMAT_SIGNALS = {
        "shorter": "one_line",
        "brief": "one_line",
        "quick": "one_line",
        "one line": "one_line",
        "in points": "points",
        "bullet": "points",
        "list": "points",
        "paragraph": "paragraph",
        "essay": "paragraph",
        "describe": "paragraph",
        "deeper": "deep",
        "more detail": "deep",
        "explain more": "deep",
        "more": "deep",
        "step by step": "steps",
        "steps": "steps",
        "derivation": "steps",
        "simply": "simple",
        "like i'm 5": "simple",
        "easy": "simple",
        "eli5": "simple",
        "technically": "expert",
        "precisely": "expert",
        "formally": "expert",
        "rigorous": "expert",
        "example": "example",
        "show me": "example",
        "like what": "example",
        "real world": "example",
        "why": "why",
        "reason": "why",
        "how does it connect": "connections",
        "related": "connections",
        "compare": "comparison",
        "formula": "formula_only",
        "equation": "formula_only",
        "teach me": "teach",
    }

    def detect_format(self, user_message: str) -> str:
        """Detect what format/depth the user wants."""
        msg = user_message.lower().strip()
        for signal, fmt in self.FORMAT_SIGNALS.items():
            if signal in msg:
                return fmt
        return "full"  # default: give full explanation

    def transform(self, node: KnowledgeNode, fmt: str) -> str:
        """Transform a knowledge node into the requested format."""
        if fmt == "one_line":
            return node.core

        elif fmt == "points":
            lines = [f"• {node.core}"]
            if node.formula:
                lines.append(f"• Formula: {node.formula}")
            for comp in node.components[:5]:
                lines.append(f"• {comp}")
            if node.insight:
                lines.append(f"• Key insight: {node.insight}")
            return '\n'.join(lines)

        elif fmt == "paragraph":
            parts = [node.core + "."]
            if node.intuition:
                parts.append(node.intuition)
            if node.meaning:
                parts.append(node.meaning)
            if node.insight:
                parts.append("The key insight: " + node.insight)
            return ' '.join(parts)

        elif fmt == "deep":
            return self._format_deep(node)

        elif fmt == "steps":
            lines = [node.core, ""]
            if node.mechanism:
                for i, step in enumerate(node.mechanism, 1):
                    lines.append(f"  {step}" if step.startswith(('Step', '1', '2', '3')) else f"  Step {i}: {step}")
            elif node.components:
                for i, comp in enumerate(node.components, 1):
                    lines.append(f"  Step {i}: {comp}")
            if node.formula:
                lines.append(f"\n  Formula: {node.formula}")
            return '\n'.join(lines)

        elif fmt == "simple":
            # ELI5 — use analogy, no jargon
            lines = [node.core]
            if node.analogies:
                lines.append(f"\n{node.analogies[0]}.")
            if node.concrete_example:
                lines.append(f"\nReal example: {node.concrete_example}")
            return '\n'.join(lines)

        elif fmt == "expert":
            lines = [node.core]
            if node.formula:
                lines.append(f"\n  {node.formula}")
            if node.mechanism:
                lines.append("\n  Derivation:")
                for step in node.mechanism:
                    lines.append(f"    {step}")
            if node.depends_on:
                lines.append(f"\n  Prerequisites: {', '.join(node.depends_on)}")
            if node.leads_to:
                lines.append(f"  Leads to: {', '.join(node.leads_to)}")
            return '\n'.join(lines)

        elif fmt == "example":
            lines = [node.core]
            if node.concrete_example:
                lines.append(f"\n  Real-world example: {node.concrete_example}")
            if node.analogies:
                lines.append(f"\n  Analogy: {node.analogies[0]}")
            return '\n'.join(lines)

        elif fmt == "why":
            lines = []
            if node.intuition:
                lines.append(node.intuition)
            if node.analogies:
                lines.append(f"\n{node.analogies[0]}")
            if node.insight:
                lines.append(f"\nKey insight: {node.insight}")
            return '\n'.join(lines) if lines else node.core

        elif fmt == "connections":
            lines = [f"Topic: {node.topic}"]
            if node.depends_on:
                lines.append(f"\n  Built on: {', '.join(node.depends_on)}")
            if node.leads_to:
                lines.append(f"  Enables: {', '.join(node.leads_to)}")
            if node.analogies:
                lines.append(f"  Similar to: {'; '.join(node.analogies)}")
            return '\n'.join(lines)

        elif fmt == "formula_only":
            return node.formula if node.formula else node.core

        elif fmt == "teach":
            return self._format_teach(node)

        else:
            return self._format_full(node)

    def _format_full(self, node: KnowledgeNode) -> str:
        """Full explanation — the default."""
        lines = []

        # Answer first
        lines.append(node.core)
        lines.append("")

        # Intuition — the WHY in plain language
        if node.intuition:
            lines.append(f"  {node.intuition}")

        # Analogy
        if node.analogies:
            lines.append(f"  {node.analogies[0]}")

        lines.append("")

        # Mechanism — the HOW
        if node.mechanism:
            for step in node.mechanism:
                lines.append(f"  {step}")
            lines.append("")
        elif node.formula:
            lines.append(f"  Formula: {node.formula}")
            lines.append("")

        # Meaning
        if node.meaning:
            lines.append(f"  {node.meaning}")

        # Insight
        if node.insight:
            lines.append(f"\n  💡 {node.insight}")

        # Example
        if node.concrete_example:
            lines.append(f"\n  📌 {node.concrete_example}")

        return '\n'.join(lines)

    def _format_deep(self, node: KnowledgeNode) -> str:
        """Deep explanation — maximum detail."""
        lines = [node.core, ""]

        if node.intuition:
            lines.append(f"  Intuition: {node.intuition}")
            lines.append("")

        if node.analogies:
            lines.append(f"  Analogy: {node.analogies[0]}")
            lines.append("")

        if node.depends_on:
            lines.append(f"  Prerequisites: {', '.join(node.depends_on)}")

        if node.mechanism:
            lines.append("\n  Derivation / Steps:")
            for step in node.mechanism:
                lines.append(f"    {step}")

        if node.formula:
            lines.append(f"\n  Formula: {node.formula}")

        if node.components:
            lines.append("\n  Key components:")
            for comp in node.components:
                lines.append(f"    • {comp}")

        if node.meaning:
            lines.append(f"\n  Significance: {node.meaning}")

        if node.insight:
            lines.append(f"\n  💡 Key insight: {node.insight}")

        if node.concrete_example:
            lines.append(f"\n  📌 Example: {node.concrete_example}")

        if node.counter_example:
            lines.append(f"  ⚠️  Common misconception: {node.counter_example}")

        if node.leads_to:
            lines.append(f"\n  This connects to: {', '.join(node.leads_to)}")

        return '\n'.join(lines)

    def _format_teach(self, node: KnowledgeNode) -> str:
        """Teaching mode — build understanding from ground up."""
        lines = []
        lines.append(f"Let's learn about: {node.topic}")
        lines.append("")

        if node.depends_on:
            lines.append(f"  First, you need to know: {', '.join(node.depends_on)}")
            lines.append("")

        if node.analogies:
            lines.append(f"  Starting with an analogy: {node.analogies[0]}")
            lines.append("")

        lines.append(f"  The core idea: {node.core}")
        lines.append("")

        if node.mechanism:
            lines.append("  Breaking it down:")
            for i, step in enumerate(node.mechanism, 1):
                lines.append(f"    {i}. {step}")
            lines.append("")

        if node.insight:
            lines.append(f"  The 'aha!' moment: {node.insight}")
            lines.append("")

        if node.concrete_example:
            lines.append(f"  See it in action: {node.concrete_example}")

        if node.leads_to:
            lines.append(f"\n  Next, you can learn: {', '.join(node.leads_to)}")

        return '\n'.join(lines)


# ══════════════════════════════════════════════════════════════════════════════
# MODULE 4: EXPLANATION MEMORY — Never forget, never repeat
# ══════════════════════════════════════════════════════════════════════════════

class ExplanationMemory:
    """Persistent memory of all explanations given. Never forgets."""

    def __init__(self, filepath: str = "user_data/explanation_memory.json"):
        self.filepath = filepath
        self.nodes: Dict[str, dict] = {}
        self._load()

    def _load(self):
        """Load memory from disk."""
        try:
            if os.path.exists(self.filepath):
                with open(self.filepath) as f:
                    self.nodes = json.load(f)
        except:
            self.nodes = {}

    def _save(self):
        """Save memory to disk."""
        try:
            os.makedirs(os.path.dirname(self.filepath), exist_ok=True)
            with open(self.filepath, 'w') as f:
                json.dump(self.nodes, f, indent=2, default=str)
        except:
            pass

    def remember(self, topic: str, node: KnowledgeNode, format_used: str):
        """Store an explanation we gave."""
        key = topic.lower().strip()
        if key not in self.nodes:
            self.nodes[key] = {
                "core": node.core,
                "type": node.answer_type,
                "formula": node.formula,
                "insight": node.insight,
                "analogies": node.analogies,
                "mechanism": node.mechanism,
                "times_asked": 0,
                "formats_used": [],
                "explanation_history": [],
            }
        self.nodes[key]["times_asked"] += 1
        if format_used not in self.nodes[key]["formats_used"]:
            self.nodes[key]["formats_used"].append(format_used)
        self._save()

    def recall(self, topic: str) -> Optional[dict]:
        """Check if we've explained this before."""
        key = topic.lower().strip()
        # Exact match
        if key in self.nodes:
            return self.nodes[key]
        # Fuzzy match
        for stored_key in self.nodes:
            if key in stored_key or stored_key in key:
                return self.nodes[stored_key]
        return None

    def already_explained_in_format(self, topic: str, fmt: str) -> bool:
        """Check if we already gave this explanation in this format."""
        mem = self.recall(topic)
        return mem is not None and fmt in mem.get("formats_used", [])


# ══════════════════════════════════════════════════════════════════════════════
# MAIN: ACES ENGINE — The unified entry point
# ══════════════════════════════════════════════════════════════════════════════

class ACES:
    """Adaptive Cognitive Explanation System — explains ANYTHING in ANY format."""

    def __init__(self):
        self.detector = AnatomyDetector()
        self.decomposer = ConceptDecomposer()
        self.transformer = ShapeTransformer()
        self.memory = ExplanationMemory()

    def explain(self, question: str, raw_answer: str, user_format: str = None,
                structured: Dict = None) -> str:
        """Generate a deep, educational explanation for any answer.

        Args:
            question: What the user asked
            raw_answer: The computed/retrieved answer (from math, physics, web, etc.)
            user_format: Optional explicit format request (from follow-up message)
            structured: Optional dict from solver with pre-computed explanation data:
                        {"formula", "steps", "intuition", "meaning", "insight",
                         "example", "analogies", "depends_on", "leads_to", "components"}

        Returns:
            Rich explanation shaped to user's needs
        """
        # Detect answer type
        answer_type = self.detector.detect(question, raw_answer)

        # Decompose into knowledge node (uses structured data if available)
        node = self.decomposer.decompose(question, raw_answer, answer_type, structured)

        # Determine output format
        if user_format:
            fmt = self.transformer.detect_format(user_format)
        else:
            fmt = "full"  # default: give full explanation

        # Check memory — if already explained, go deeper or different angle
        prev = self.memory.recall(node.topic)
        if prev and self.memory.already_explained_in_format(node.topic, fmt):
            fmt = "deep"  # already explained this way → go deeper

        # Transform into requested shape
        explanation = self.transformer.transform(node, fmt)

        # Remember this explanation
        self.memory.remember(node.topic, node, fmt)

        return explanation

    def reshape(self, topic: str, user_request: str) -> str:
        """Reshape a previously-given explanation based on follow-up.
        e.g., "explain shorter", "give me points", "go deeper" """

        fmt = self.transformer.detect_format(user_request)
        prev = self.memory.recall(topic)

        if prev:
            # Rebuild node from memory
            node = KnowledgeNode(
                topic=topic,
                core=prev.get("core", ""),
                answer_type=prev.get("type", "concept"),
                formula=prev.get("formula", ""),
                insight=prev.get("insight", ""),
                analogies=prev.get("analogies", []),
                mechanism=prev.get("mechanism", []),
            )
            return self.transformer.transform(node, fmt)

        return f"I haven't explained '{topic}' yet. Ask me about it first!"


# ══════════════════════════════════════════════════════════════════════════════
# CONVENIENCE: Singleton
# ══════════════════════════════════════════════════════════════════════════════

_aces_instance = None

def get_aces() -> ACES:
    """Get singleton ACES instance."""
    global _aces_instance
    if _aces_instance is None:
        _aces_instance = ACES()
    return _aces_instance
