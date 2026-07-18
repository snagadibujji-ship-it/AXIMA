"""
AXIMA Principle Evolution — Principles as living objects.

Each principle maintains: confidence, prediction_accuracy, supporting facts,
contradictions, domains, usage, reflection_history, version_history.

Successful principles strengthen. Weak merge. Incorrect retire.
"""

import time
from typing import Optional, List, Dict, Any
from core.reality_graph import get_reality_graph, RealityGraph
from core.cognitive_state import get_state, set_state


class PrincipleEvolution:
    """Manages the lifecycle of principles as living objects."""

    def __init__(self, graph: Optional[RealityGraph] = None):
        self._graph = graph or get_reality_graph()

    def evolve_tick(self):
        """One evolution cycle: strengthen, merge, retire."""
        theories = self._graph.find_nodes(node_type="theory")
        principles = [t for t in theories if t.properties.get("level") == "principle"
                     and t.properties.get("status") not in ("retired", "merged")]

        for p in principles:
            state = get_state(self._graph, p.id)
            # Strengthen if high accuracy + usage
            if state.prediction_accuracy > 0.7 and state.usage_count > 5:
                state.confidence = min(0.95, state.confidence + 0.01)
                state.stability = min(0.9, state.stability + 0.005)
            # Weaken if low accuracy
            if state.prediction_accuracy < 0.3 and state.usage_count > 3:
                state.confidence -= 0.02
            set_state(self._graph, p.id, state)

        # Retire weak principles
        self._retire_weak(principles)
        # Merge similar principles
        self._merge_similar(principles)
        self._graph.save()

    def record_prediction_result(self, principle_id: str, correct: bool):
        """Record whether a prediction based on this principle was correct."""
        state = get_state(self._graph, principle_id)
        state.usage_count += 1
        # Exponential moving average
        alpha = 0.1
        actual = 1.0 if correct else 0.0
        state.prediction_accuracy = state.prediction_accuracy * (1 - alpha) + actual * alpha
        if correct:
            state.confidence = min(1.0, state.confidence + 0.02)
        else:
            state.confidence = max(0.0, state.confidence - 0.03)
            state.entropy += 0.05
        set_state(self._graph, principle_id, state)

    def add_supporting_fact(self, principle_id: str, fact_id: str):
        """Link a supporting fact to a principle."""
        self._graph.add_edge(fact_id, principle_id, "supports")
        state = get_state(self._graph, principle_id)
        state.confidence = min(1.0, state.confidence + 0.01)
        state.stability += 0.005
        set_state(self._graph, principle_id, state)

    def add_contradiction(self, principle_id: str, fact_id: str):
        """Link a contradicting fact to a principle."""
        self._graph.add_edge(fact_id, principle_id, "contradicts")
        state = get_state(self._graph, principle_id)
        state.confidence -= 0.05
        state.entropy += 0.1
        state.stability -= 0.02
        set_state(self._graph, principle_id, state)

    def get_principle_health(self, principle_id: str) -> Dict[str, Any]:
        """Get health report for a principle."""
        node = self._graph.get_node(principle_id)
        state = get_state(self._graph, principle_id)
        supports = len([n for n, r, _ in self._graph.neighbors(principle_id, direction="in") if r == "supports"])
        contradictions = len([n for n, r, _ in self._graph.neighbors(principle_id, direction="in") if r == "contradicts"])
        return {
            "label": node.label if node else "",
            "confidence": state.confidence,
            "prediction_accuracy": state.prediction_accuracy,
            "stability": state.stability,
            "usage_count": state.usage_count,
            "supports": supports,
            "contradictions": contradictions,
            "health": "strong" if state.confidence > 0.7 else "weak" if state.confidence < 0.3 else "moderate",
        }

    def _retire_weak(self, principles: List):
        """Retire principles below threshold."""
        for p in principles:
            state = get_state(self._graph, p.id)
            if state.confidence < 0.15 and state.usage_count > 5:
                self._graph.update_node(p.id, properties={
                    "status": "retired", "retired_at": time.time(),
                    "retired_reason": f"Confidence dropped to {state.confidence:.2f}"
                })
                state.activation = 0.0
                state.importance = 0.0
                set_state(self._graph, p.id, state)

    def _merge_similar(self, principles: List):
        """Merge principles with high overlap."""
        # Simple: find pairs with same domain and similar labels
        for i, p1 in enumerate(principles):
            for p2 in principles[i+1:]:
                if p1.properties.get("status") == "merged" or p2.properties.get("status") == "merged":
                    continue
                d1 = p1.properties.get("domain", "")
                d2 = p2.properties.get("domain", "")
                if d1 and d1 == d2:
                    # Check label similarity
                    words1 = set(p1.label.lower().split())
                    words2 = set(p2.label.lower().split())
                    overlap = len(words1 & words2) / max(len(words1 | words2), 1)
                    if overlap > 0.6:
                        # Merge: keep stronger, mark weaker
                        s1 = get_state(self._graph, p1.id)
                        s2 = get_state(self._graph, p2.id)
                        if s1.confidence >= s2.confidence:
                            self._graph.update_node(p2.id, properties={"status": "merged", "merged_into": p1.id})
                            s1.confidence = min(1.0, s1.confidence + 0.05)
                            set_state(self._graph, p1.id, s1)
                        else:
                            self._graph.update_node(p1.id, properties={"status": "merged", "merged_into": p2.id})
                            s2.confidence = min(1.0, s2.confidence + 0.05)
                            set_state(self._graph, p2.id, s2)
                        return  # One merge per tick


_evolution: Optional[PrincipleEvolution] = None
def get_principle_evolution(graph: Optional[RealityGraph] = None) -> PrincipleEvolution:
    global _evolution
    if _evolution is None:
        _evolution = PrincipleEvolution(graph=graph)
    return _evolution
