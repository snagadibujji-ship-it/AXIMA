"""
AXIMA Contradiction Engine — Detects conflicts in knowledge automatically.

When knowledge enters the Reality Graph, automatically detect:
  - Duplicates (same fact, different wording)
  - Support (new fact strengthens existing)
  - Contradictions (new fact conflicts with existing)
  - Extensions (new fact extends existing)
  - Obsolete information (old fact superseded)

Never silently overwrite knowledge. Always create contradiction relationships.

Usage:
    from core.contradiction import ContradictionEngine, get_contradiction_engine

    engine = get_contradiction_engine()
    analysis = engine.analyze_new_fact("Water boils at 90°C at sea level")
    # analysis.contradicts, analysis.supports, analysis.duplicates
"""

import re
import time
from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any, Tuple

from core.reality_graph import get_reality_graph, RealityGraph


# ═══════════════════════════════════════════════════════════════
# ANALYSIS RESULT
# ═══════════════════════════════════════════════════════════════

class Relationship:
    DUPLICATE = "duplicate"
    SUPPORTS = "supports"
    CONTRADICTS = "contradicts"
    EXTENDS = "extends"
    OBSOLETES = "obsoletes"


@dataclass
class ConflictAnalysis:
    """Result of analyzing a new piece of knowledge against existing."""
    new_content: str
    relationships: List[Dict[str, Any]] = field(default_factory=list)
    # Each: {type, existing_id, existing_label, confidence, reason}

    @property
    def has_contradictions(self) -> bool:
        return any(r["type"] == Relationship.CONTRADICTS for r in self.relationships)

    @property
    def has_duplicates(self) -> bool:
        return any(r["type"] == Relationship.DUPLICATE for r in self.relationships)

    @property
    def contradicts(self) -> List[Dict]:
        return [r for r in self.relationships if r["type"] == Relationship.CONTRADICTS]

    @property
    def supports(self) -> List[Dict]:
        return [r for r in self.relationships if r["type"] == Relationship.SUPPORTS]

    @property
    def duplicates(self) -> List[Dict]:
        return [r for r in self.relationships if r["type"] == Relationship.DUPLICATE]

    @property
    def extensions(self) -> List[Dict]:
        return [r for r in self.relationships if r["type"] == Relationship.EXTENDS]

    def summary(self) -> Dict[str, int]:
        counts = {}
        for r in self.relationships:
            counts[r["type"]] = counts.get(r["type"], 0) + 1
        return counts


# ═══════════════════════════════════════════════════════════════
# CONTRADICTION ENGINE
# ═══════════════════════════════════════════════════════════════

class ContradictionEngine:
    """Automatically detects conflicts, duplicates, and support in knowledge.
    
    Ensures knowledge is never silently overwritten.
    Every conflict creates an explicit relationship.
    """

    def __init__(self, graph: Optional[RealityGraph] = None):
        self._graph = graph or get_reality_graph()

    def analyze_new_fact(self, content: str, subject: str = "",
                         predicate: str = "", obj: str = "") -> ConflictAnalysis:
        """Analyze a new fact against all existing knowledge.
        
        Returns a ConflictAnalysis showing all relationships found.
        """
        analysis = ConflictAnalysis(new_content=content)

        # Get all existing facts
        existing_facts = self._graph.find_nodes(node_type="fact")

        for fact_node in existing_facts:
            rel = self._compare(content, subject, obj, fact_node)
            if rel:
                analysis.relationships.append(rel)

        # Also check theories/concepts
        existing_theories = self._graph.find_nodes(node_type="theory")
        for theory in existing_theories:
            rel = self._compare_theory(content, theory)
            if rel:
                analysis.relationships.append(rel)

        return analysis

    def record_relationships(self, new_node_id: str, analysis: ConflictAnalysis):
        """Record found relationships as edges in the Reality Graph."""
        for rel in analysis.relationships:
            existing_id = rel["existing_id"]
            rel_type = rel["type"]

            if rel_type == Relationship.CONTRADICTS:
                self._graph.add_edge(new_node_id, existing_id, "contradicts",
                                    properties={"reason": rel.get("reason", "")})
                self._graph.add_edge(existing_id, new_node_id, "contradicts")
            elif rel_type == Relationship.SUPPORTS:
                self._graph.add_edge(new_node_id, existing_id, "supports",
                                    properties={"confidence": rel.get("confidence", 0.5)})
            elif rel_type == Relationship.EXTENDS:
                self._graph.add_edge(new_node_id, existing_id, "extends")
            elif rel_type == Relationship.OBSOLETES:
                self._graph.add_edge(new_node_id, existing_id, "extends",
                                    properties={"obsoletes": True})
                # Mark old fact as lower confidence
                old_node = self._graph.get_node(existing_id)
                if old_node:
                    old_conf = old_node.properties.get("confidence", 1.0)
                    self._graph.update_node(existing_id,
                                           properties={"confidence": old_conf * 0.5})

        if analysis.relationships:
            self._graph.save()

    def scan_all(self) -> List[ConflictAnalysis]:
        """Scan entire graph for contradictions between existing facts."""
        facts = self._graph.find_nodes(node_type="fact")
        contradictions = []

        checked = set()
        for i, fact1 in enumerate(facts):
            for fact2 in facts[i+1:]:
                pair_key = tuple(sorted([fact1.id, fact2.id]))
                if pair_key in checked:
                    continue
                checked.add(pair_key)

                rel = self._compare(
                    fact1.label,
                    fact1.properties.get("subject", ""),
                    fact1.properties.get("object", ""),
                    fact2
                )
                if rel and rel["type"] == Relationship.CONTRADICTS:
                    analysis = ConflictAnalysis(new_content=fact1.label)
                    analysis.relationships.append(rel)
                    contradictions.append(analysis)

        return contradictions

    def resolve_contradiction(self, keep_id: str, discard_id: str,
                              reason: str = "") -> bool:
        """Resolve a contradiction by choosing which fact to trust."""
        keep = self._graph.get_node(keep_id)
        discard = self._graph.get_node(discard_id)
        if not keep or not discard:
            return False

        # Boost confidence of kept fact
        self._graph.update_node(keep_id, properties={
            "confidence": min(1.0, keep.properties.get("confidence", 0.5) + 0.2),
            "validated": True,
        })

        # Mark discarded as low confidence
        self._graph.update_node(discard_id, properties={
            "confidence": 0.1,
            "status": "disputed",
            "dispute_reason": reason,
        })

        self._graph.save()
        return True

    # ─── Internal comparison ───

    def _compare(self, new_content: str, new_subject: str, new_object: str,
                 existing_node) -> Optional[Dict]:
        """Compare new content with an existing fact node."""
        existing_label = existing_node.label
        existing_subject = existing_node.properties.get("subject", "")
        existing_object = existing_node.properties.get("object", "")

        # Check for duplicate (high word overlap)
        similarity = self._text_similarity(new_content, existing_label)
        if similarity > 0.85:
            return {
                "type": Relationship.DUPLICATE,
                "existing_id": existing_node.id,
                "existing_label": existing_label,
                "confidence": similarity,
                "reason": "Very similar content",
            }

        # Check for contradiction (same subject, conflicting object)
        if new_subject and existing_subject:
            subj_sim = self._text_similarity(new_subject, existing_subject)
            if subj_sim > 0.7:
                # Same subject — check if objects conflict
                if new_object and existing_object:
                    obj_sim = self._text_similarity(new_object, existing_object)
                    if obj_sim < 0.3:  # Very different objects = contradiction
                        # Check for negation
                        new_neg = self._has_negation(new_content)
                        exist_neg = existing_node.properties.get("is_negation", False)
                        if new_neg != exist_neg or obj_sim < 0.2:
                            return {
                                "type": Relationship.CONTRADICTS,
                                "existing_id": existing_node.id,
                                "existing_label": existing_label,
                                "confidence": subj_sim,
                                "reason": f"Same subject '{new_subject}' but conflicting assertions",
                            }
                    elif 0.3 <= obj_sim <= 0.7:  # Partially overlapping = extends
                        return {
                            "type": Relationship.EXTENDS,
                            "existing_id": existing_node.id,
                            "existing_label": existing_label,
                            "confidence": subj_sim * obj_sim,
                            "reason": f"Extends knowledge about '{new_subject}'",
                        }

        # Check for support (similar topic, aligned assertion)
        if similarity > 0.4 and similarity <= 0.85:
            # Determine if supporting or extending
            if new_subject and existing_subject:
                if self._text_similarity(new_subject, existing_subject) > 0.5:
                    return {
                        "type": Relationship.SUPPORTS,
                        "existing_id": existing_node.id,
                        "existing_label": existing_label,
                        "confidence": similarity,
                        "reason": "Related assertion on same topic",
                    }

        return None

    def _compare_theory(self, new_content: str, theory_node) -> Optional[Dict]:
        """Compare new content with an existing theory."""
        statement = theory_node.properties.get("statement", theory_node.label)
        similarity = self._text_similarity(new_content, statement)

        if similarity > 0.6:
            return {
                "type": Relationship.SUPPORTS,
                "existing_id": theory_node.id,
                "existing_label": theory_node.label,
                "confidence": similarity,
                "reason": "Supports existing theory",
            }
        return None

    def _text_similarity(self, a: str, b: str) -> float:
        """Word-level Jaccard similarity."""
        if not a or not b:
            return 0.0
        words_a = set(re.findall(r'\b\w{3,}\b', a.lower()))
        words_b = set(re.findall(r'\b\w{3,}\b', b.lower()))
        if not words_a or not words_b:
            return 0.0
        intersection = len(words_a & words_b)
        union = len(words_a | words_b)
        return intersection / max(union, 1)

    def _has_negation(self, text: str) -> bool:
        """Check if text contains negation."""
        return bool(re.search(r"\b(?:not|n't|never|no|cannot|can't|won't|doesn't|isn't)\b", text, re.I))


# ═══════════════════════════════════════════════════════════════
# SINGLETON
# ═══════════════════════════════════════════════════════════════

_engine: Optional[ContradictionEngine] = None

def get_contradiction_engine(graph: Optional[RealityGraph] = None) -> ContradictionEngine:
    """Get the global contradiction engine."""
    global _engine
    if _engine is None:
        _engine = ContradictionEngine(graph=graph)
    return _engine
