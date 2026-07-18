"""
AXIMA Memory Consolidation — Knowledge organizes itself incrementally.

Pipeline: Observations → Facts → Patterns → Rules → Principles → Long-term

The process is incremental — no massive rebuilds. Each tick, a small
amount of consolidation work promotes knowledge up the abstraction ladder.

Usage:
    from core.memory_consolidation import MemoryConsolidation, get_consolidation

    consolidation = get_consolidation()
    consolidation.consolidate_step()  # One incremental step
"""

import time
from typing import Optional, List, Dict, Any

from core.reality_graph import get_reality_graph, RealityGraph
from core.cognitive_state import get_state, set_state


class MemoryConsolidation:
    """Incremental knowledge organization.
    
    Each call to consolidate_step() does a small amount of work:
    - Promotes high-confidence facts to patterns (if cluster detected)
    - Promotes strong patterns to rules
    - Promotes validated rules to principles
    
    Never processes the entire graph at once.
    """

    def __init__(self, graph: Optional[RealityGraph] = None):
        self._graph = graph or get_reality_graph()
        self._consolidation_count = 0

    def consolidate_step(self, max_work: int = 5) -> Dict[str, int]:
        """One incremental consolidation step.
        
        Args:
            max_work: Maximum promotions per step (keeps latency bounded)
        Returns:
            {promoted_to_pattern, promoted_to_rule, promoted_to_principle}
        """
        self._consolidation_count += 1
        result = {"promoted_to_pattern": 0, "promoted_to_rule": 0, "promoted_to_principle": 0}
        work_done = 0

        # Stage 1: Facts → Patterns (cluster similar high-confidence facts)
        if work_done < max_work:
            promoted = self._consolidate_facts_to_patterns(max_work - work_done)
            result["promoted_to_pattern"] = promoted
            work_done += promoted

        # Stage 2: Patterns → Rules (patterns with consistent behavior)
        if work_done < max_work:
            promoted = self._consolidate_patterns_to_rules(max_work - work_done)
            result["promoted_to_rule"] = promoted
            work_done += promoted

        # Stage 3: Rules → Principles (validated cross-domain rules)
        if work_done < max_work:
            promoted = self._consolidate_rules_to_principles(max_work - work_done)
            result["promoted_to_principle"] = promoted

        return result

    def _consolidate_facts_to_patterns(self, limit: int) -> int:
        """Find clusters of related high-confidence facts and promote to patterns."""
        facts = self._graph.find_nodes(node_type="fact")
        high_conf = [f for f in facts if f.properties.get("_cs_confidence", f.properties.get("confidence", 0)) > 0.7]

        promoted = 0
        # Group by subject
        by_subject: Dict[str, List] = {}
        for f in high_conf:
            subj = f.properties.get("subject", "")
            if subj:
                by_subject.setdefault(subj.lower()[:30], []).append(f)

        for subj, cluster in by_subject.items():
            if len(cluster) >= 3 and promoted < limit:
                # Check if pattern already exists
                existing = self._graph.find_nodes(node_type="concept", label_contains=subj[:15])
                pattern_exists = any(n.properties.get("level") == "pattern" for n in existing)
                if not pattern_exists:
                    # Create pattern
                    pattern_desc = f"Pattern: multiple facts about {subj}"
                    pid = self._graph.add_node("concept", pattern_desc[:80], {
                        "level": "pattern",
                        "source_count": len(cluster),
                        "confidence": 0.6,
                        "_cs_confidence": 0.6,
                        "_cs_novelty": 0.5,
                        "_cs_activation": 0.3,
                        "created_at": time.time(),
                    })
                    for fact in cluster[:5]:
                        self._graph.add_edge(fact.id, pid, "supports")
                    promoted += 1

        if promoted:
            self._graph.save()
        return promoted

    def _consolidate_patterns_to_rules(self, limit: int) -> int:
        """Promote strong patterns to rules."""
        concepts = self._graph.find_nodes(node_type="concept")
        patterns = [c for c in concepts if c.properties.get("level") == "pattern"]

        promoted = 0
        for pattern in patterns:
            if promoted >= limit:
                break
            conf = pattern.properties.get("_cs_confidence", pattern.properties.get("confidence", 0))
            usage = pattern.properties.get("_cs_usage_count", 0)
            # Promote if high confidence and used
            if conf > 0.7 and usage > 3:
                # Check if rule already exists
                existing = self._graph.find_nodes(node_type="theory", label_contains=pattern.label[:20])
                rule_exists = any(n.properties.get("level") == "rule" for n in existing)
                if not rule_exists:
                    rid = self._graph.add_node("theory", f"Rule: {pattern.label[:60]}", {
                        "level": "rule",
                        "confidence": conf * 0.9,
                        "_cs_confidence": conf * 0.9,
                        "_cs_stability": 0.5,
                        "derived_from_pattern": pattern.id,
                        "created_at": time.time(),
                    })
                    self._graph.add_edge(pattern.id, rid, "supports")
                    promoted += 1

        if promoted:
            self._graph.save()
        return promoted

    def _consolidate_rules_to_principles(self, limit: int) -> int:
        """Promote validated rules to principles."""
        theories = self._graph.find_nodes(node_type="theory")
        rules = [t for t in theories if t.properties.get("level") == "rule"]

        promoted = 0
        for rule in rules:
            if promoted >= limit:
                break
            conf = rule.properties.get("_cs_confidence", rule.properties.get("confidence", 0))
            pred_acc = rule.properties.get("_cs_prediction_accuracy", 0.5)
            stability = rule.properties.get("_cs_stability", 0)
            # Promote if very confident, accurate, and stable
            if conf > 0.8 and pred_acc > 0.7 and stability > 0.6:
                existing = self._graph.find_nodes(node_type="theory", label_contains=rule.label[:20])
                principle_exists = any(n.properties.get("level") == "principle" for n in existing)
                if not principle_exists:
                    pid = self._graph.add_node("theory", f"Principle: {rule.label[:55]}", {
                        "level": "principle",
                        "confidence": conf * 0.95,
                        "_cs_confidence": conf * 0.95,
                        "_cs_stability": 0.7,
                        "_cs_importance": 0.5,
                        "derived_from_rule": rule.id,
                        "created_at": time.time(),
                    })
                    self._graph.add_edge(rule.id, pid, "supports")
                    promoted += 1

        if promoted:
            self._graph.save()
        return promoted

    def stats(self) -> Dict[str, Any]:
        """Consolidation statistics."""
        theories = self._graph.find_nodes(node_type="theory")
        concepts = self._graph.find_nodes(node_type="concept")
        return {
            "consolidation_cycles": self._consolidation_count,
            "patterns": sum(1 for c in concepts if c.properties.get("level") == "pattern"),
            "rules": sum(1 for t in theories if t.properties.get("level") == "rule"),
            "principles": sum(1 for t in theories if t.properties.get("level") == "principle"),
        }


_consolidation: Optional[MemoryConsolidation] = None
def get_consolidation(graph: Optional[RealityGraph] = None) -> MemoryConsolidation:
    global _consolidation
    if _consolidation is None:
        _consolidation = MemoryConsolidation(graph=graph)
    return _consolidation
