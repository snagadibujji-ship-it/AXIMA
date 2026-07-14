"""
ACES v2 — Phase 4: Meaning Parser
Extracts semantic roles from text into a MeaningGraph.
NO word-list matching. Uses SENTENCE STRUCTURE (grammar patterns).

Extracts: subject, relation, object, cause, effect, constraint, step, transformation
"""

import re
from typing import List, Tuple, Optional
from .models import NormalizedInput, RouterDecision, MeaningGraph, MeaningNode, MeaningEdge


class MeaningParser:
    """Parse text into structured meaning using grammar patterns."""

    def __init__(self):
        self._node_counter = 0

    def parse(self, inp: NormalizedInput, decision: RouterDecision) -> MeaningGraph:
        """Extract meaning graph from normalized input."""
        graph = MeaningGraph()
        text = inp.clean

        # Split into sentences
        sentences = self._split_sentences(text)

        # Parse each sentence for semantic roles
        for sent in sentences:
            self._parse_sentence(sent, graph, decision)

        # If graph is empty, create at least a topic node
        if not graph.nodes:
            self._add_node(graph, "concept", self._extract_topic(text), text)

        return graph

    def _split_sentences(self, text: str) -> List[str]:
        """Split text into sentences."""
        # Split on sentence-ending punctuation
        sentences = re.split(r'[.!?]+', text)
        return [s.strip() for s in sentences if s.strip()]

    def _parse_sentence(self, sent: str, graph: MeaningGraph, decision: RouterDecision):
        """Parse a single sentence into the graph."""
        # Try each extraction pattern
        self._extract_definition(sent, graph)
        self._extract_causal(sent, graph)
        self._extract_process(sent, graph)
        self._extract_comparison(sent, graph)
        self._extract_condition(sent, graph)
        self._extract_purpose(sent, graph)

        # If nothing matched, extract subject-predicate at minimum
        if not graph.nodes:
            self._extract_basic_structure(sent, graph)

    # ═══════════════════════════════════════════════════════════
    # PATTERN 1: Definitions — "X is Y" / "X refers to Y"
    # ═══════════════════════════════════════════════════════════

    def _extract_definition(self, sent: str, graph: MeaningGraph):
        """Extract definitional relationships."""
        patterns = [
            # "X is Y" / "X are Y"
            r'^(.+?)\s+(?:is|are)\s+(?:a|an|the)?\s*(.+?)$',
            # "X is defined as Y"
            r'(.+?)\s+(?:is defined as|refers to|means|is called)\s+(.+?)$',
            # "X, which is Y"
            r'(.+?),?\s+which\s+(?:is|are)\s+(.+?)$',
        ]
        for pattern in patterns:
            m = re.match(pattern, sent, re.IGNORECASE)
            if m and len(m.group(1).split()) <= 6:
                subject = m.group(1).strip()
                definition = m.group(2).strip()
                subj_id = self._add_node(graph, "concept", subject)
                def_id = self._add_node(graph, "concept", definition, evidence=sent)
                self._add_edge(graph, subj_id, def_id, "is", evidence=sent)
                return

    # ═══════════════════════════════════════════════════════════
    # PATTERN 2: Causal — "X causes Y" / "because X, Y"
    # ═══════════════════════════════════════════════════════════

    def _extract_causal(self, sent: str, graph: MeaningGraph):
        """Extract cause-effect relationships."""
        patterns = [
            # "X causes/produces/leads to Y"
            (r'(.+?)\s+(?:causes?|produces?|leads?\s+to|results?\s+in|creates?)\s+(.+)', 'causes'),
            # "Y is caused by X" / "Y results from X"
            (r'(.+?)\s+(?:is caused by|results? from|is due to|comes? from)\s+(.+)', 'caused_by'),
            # "because X, Y" / "due to X, Y"
            (r'(?:because|since|due to|as)\s+(.+?),\s*(.+)', 'causes'),
            # "X, so Y" / "X, therefore Y"
            (r'(.+?),?\s+(?:so|therefore|thus|hence|consequently)\s+(.+)', 'causes'),
            # "if X then Y"
            (r'if\s+(.+?),?\s+(?:then\s+)?(.+)', 'enables'),
        ]
        for pattern, rel in patterns:
            m = re.search(pattern, sent, re.IGNORECASE)
            if m:
                if rel == 'caused_by':
                    effect, cause = m.group(1).strip(), m.group(2).strip()
                else:
                    cause, effect = m.group(1).strip(), m.group(2).strip()
                cause_id = self._add_node(graph, "concept", cause, evidence=sent)
                effect_id = self._add_node(graph, "concept", effect, evidence=sent)
                self._add_edge(graph, cause_id, effect_id, "causes", evidence=sent)
                return

    # ═══════════════════════════════════════════════════════════
    # PATTERN 3: Process — "first X, then Y" / "X → Y → Z"
    # ═══════════════════════════════════════════════════════════

    def _extract_process(self, sent: str, graph: MeaningGraph):
        """Extract sequential process steps."""
        # "first X, then Y, finally Z"
        steps = re.split(r'\b(?:first|then|next|after that|finally|lastly)\b', sent, flags=re.IGNORECASE)
        steps = [s.strip().strip(',').strip() for s in steps if s.strip()]

        if len(steps) >= 2:
            prev_id = None
            for i, step in enumerate(steps):
                step_id = self._add_node(graph, "step", f"Step {i+1}: {step}", content=step, evidence=sent)
                if prev_id:
                    self._add_edge(graph, prev_id, step_id, "enables", evidence=sent)
                prev_id = step_id
            return

        # "X, which leads to Y, which leads to Z"
        chain = re.split(r',?\s*which\s+(?:leads?\s+to|causes?|produces?)\s*', sent, flags=re.IGNORECASE)
        if len(chain) >= 2:
            prev_id = None
            for item in chain:
                item = item.strip()
                if item:
                    node_id = self._add_node(graph, "step", item, evidence=sent)
                    if prev_id:
                        self._add_edge(graph, prev_id, node_id, "transforms_into", evidence=sent)
                    prev_id = node_id

    # ═══════════════════════════════════════════════════════════
    # PATTERN 4: Comparison — "X unlike Y" / "X vs Y"
    # ═══════════════════════════════════════════════════════════

    def _extract_comparison(self, sent: str, graph: MeaningGraph):
        """Extract comparison/contrast relationships."""
        patterns = [
            r'(.+?)\s+(?:unlike|whereas|while|but|however)\s+(.+)',
            r'(.+?)\s+(?:is similar to|resembles|is like)\s+(.+)',
            r'(?:compare|difference between)\s+(.+?)\s+(?:and|vs|versus)\s+(.+)',
        ]
        for pattern in patterns:
            m = re.search(pattern, sent, re.IGNORECASE)
            if m:
                a = m.group(1).strip()
                b = m.group(2).strip()
                a_id = self._add_node(graph, "concept", a, evidence=sent)
                b_id = self._add_node(graph, "concept", b, evidence=sent)
                if 'similar' in sent.lower() or 'like' in sent.lower():
                    self._add_edge(graph, a_id, b_id, "similar_to", evidence=sent)
                else:
                    self._add_edge(graph, a_id, b_id, "contradicts", evidence=sent)
                return

    # ═══════════════════════════════════════════════════════════
    # PATTERN 5: Condition/Constraint — "X only if Y"
    # ═══════════════════════════════════════════════════════════

    def _extract_condition(self, sent: str, graph: MeaningGraph):
        """Extract conditional/constraint relationships."""
        patterns = [
            r'(.+?)\s+(?:only if|provided that|as long as|given that)\s+(.+)',
            r'(.+?)\s+(?:requires?|needs?|depends?\s+on)\s+(.+)',
            r'(?:without)\s+(.+?),\s*(.+?)(?:cannot|won\'t|can\'t)',
        ]
        for pattern in patterns:
            m = re.search(pattern, sent, re.IGNORECASE)
            if m:
                thing = m.group(1).strip()
                condition = m.group(2).strip()
                thing_id = self._add_node(graph, "concept", thing, evidence=sent)
                cond_id = self._add_node(graph, "concept", condition, evidence=sent)
                self._add_edge(graph, thing_id, cond_id, "depends_on", evidence=sent)
                return

    # ═══════════════════════════════════════════════════════════
    # PATTERN 6: Purpose — "X is used for Y" / "X enables Y"
    # ═══════════════════════════════════════════════════════════

    def _extract_purpose(self, sent: str, graph: MeaningGraph):
        """Extract purpose/function relationships."""
        patterns = [
            r'(.+?)\s+(?:is used (?:for|to)|serves? to|enables?|allows?)\s+(.+)',
            r'(.+?)\s+(?:in order to|so that|for the purpose of)\s+(.+)',
        ]
        for pattern in patterns:
            m = re.search(pattern, sent, re.IGNORECASE)
            if m:
                tool = m.group(1).strip()
                purpose = m.group(2).strip()
                tool_id = self._add_node(graph, "concept", tool, evidence=sent)
                purp_id = self._add_node(graph, "concept", purpose, evidence=sent)
                self._add_edge(graph, tool_id, purp_id, "enables", evidence=sent)
                return

    # ═══════════════════════════════════════════════════════════
    # FALLBACK: Basic subject-predicate extraction
    # ═══════════════════════════════════════════════════════════

    def _extract_basic_structure(self, sent: str, graph: MeaningGraph):
        """Fallback: extract at least a topic from the question."""
        # Remove question words
        topic = re.sub(r'^(?:what|why|how|when|where|who|which|is|are|does|do|can|will)\s+',
                      '', sent, flags=re.IGNORECASE)
        topic = re.sub(r'\?$', '', topic).strip()
        if topic:
            self._add_node(graph, "concept", topic, content=sent, evidence=sent)

    # ═══════════════════════════════════════════════════════════
    # HELPERS
    # ═══════════════════════════════════════════════════════════

    def _add_node(self, graph: MeaningGraph, node_type: str, label: str,
                  content: str = "", evidence: str = "") -> str:
        """Add a node to the graph, return its ID."""
        # Check for existing node with same label
        for n in graph.nodes:
            if n.label.lower() == label.lower():
                return n.id

        self._node_counter += 1
        node_id = f"n{self._node_counter}"
        node = MeaningNode(
            id=node_id, type=node_type, label=label,
            content=content or label, evidence=evidence
        )
        graph.add_node(node)
        return node_id

    def _add_edge(self, graph: MeaningGraph, source: str, target: str,
                  relation: str, evidence: str = ""):
        """Add an edge to the graph."""
        edge = MeaningEdge(source=source, target=target, relation=relation, evidence=evidence)
        graph.add_edge(edge)

    def _extract_topic(self, text: str) -> str:
        """Extract the main topic from a question."""
        topic = re.sub(r'^(?:what|why|how|when|where|who|explain|describe|tell me about)\s+',
                      '', text, flags=re.IGNORECASE)
        topic = re.sub(r'[?!.]$', '', topic).strip()
        return topic or text
