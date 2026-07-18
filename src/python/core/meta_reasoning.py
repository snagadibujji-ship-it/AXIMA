"""
AXIMA Meta Reasoning — Reason about own cognition.

Questions this system answers:
  - Why did I choose this?
  - What evidence supports this?
  - What assumptions exist?
  - Could another explanation fit better?
  - What should I investigate next?

Reusable service — any subsystem can ask for meta-reasoning.
"""

from typing import Optional, List, Dict, Any
from core.reality_graph import get_reality_graph, RealityGraph
from core.cognitive_state import get_state


class MetaReasoning:
    """Reasons about AXIMA's own cognitive decisions."""

    def __init__(self, graph: Optional[RealityGraph] = None):
        self._graph = graph or get_reality_graph()

    def why_chosen(self, node_id: str) -> Dict[str, Any]:
        """Why was this node activated/chosen?"""
        node = self._graph.get_node(node_id)
        if not node:
            return {"reason": "Node not found"}
        state = get_state(self._graph, node_id)
        reasons = []
        if state.importance > 0.5:
            reasons.append(f"High importance ({state.importance:.2f})")
        if state.activation > 0.5:
            reasons.append(f"High activation ({state.activation:.2f})")
        if state.novelty > 0.3:
            reasons.append(f"Novel ({state.novelty:.2f})")
        if state.usage_count > 5:
            reasons.append(f"Frequently used ({state.usage_count} times)")
        # Check connections to active goals
        neighbors = self._graph.neighbors(node_id, direction="both")
        goal_connections = [(nid, r) for nid, r, _ in neighbors
                          if self._graph.get_node(nid) and self._graph.get_node(nid).node_type == "goal"]
        if goal_connections:
            reasons.append(f"Connected to {len(goal_connections)} goal(s)")
        return {
            "node": node.label,
            "reasons": reasons or ["No strong reason identified — may be default behavior"],
            "confidence_in_choice": state.confidence,
            "alternatives_considered": self._find_alternatives(node_id, node.node_type),
        }

    def what_evidence(self, node_id: str) -> Dict[str, Any]:
        """What evidence supports this node?"""
        neighbors = self._graph.neighbors(node_id, direction="in")
        supporting = []
        contradicting = []
        for nid, rel, edge in neighbors:
            n = self._graph.get_node(nid)
            if not n:
                continue
            if rel == "supports":
                supporting.append({"id": nid, "label": n.label, "type": n.node_type})
            elif rel == "contradicts":
                contradicting.append({"id": nid, "label": n.label})
        state = get_state(self._graph, node_id)
        return {
            "supporting_evidence": supporting,
            "contradicting_evidence": contradicting,
            "evidence_ratio": len(supporting) / max(1, len(supporting) + len(contradicting)),
            "confidence": state.confidence,
            "prediction_accuracy": state.prediction_accuracy,
        }

    def what_assumptions(self, node_id: str) -> List[str]:
        """What assumptions underlie this node?"""
        assumptions = []
        state = get_state(self._graph, node_id)
        node = self._graph.get_node(node_id)
        if not node:
            return ["Node not found"]
        if state.confidence > 0.8 and state.usage_count < 3:
            assumptions.append("High confidence assumed without extensive testing")
        neighbors = self._graph.neighbors(node_id, direction="in")
        if len([n for n, r, _ in neighbors if r == "supports"]) == 0:
            assumptions.append("No supporting evidence — confidence may be unjustified")
        if state.prediction_accuracy == 0.5 and state.usage_count == 0:
            assumptions.append("Default prediction accuracy — never tested")
        if node.node_type == "theory" and state.stability > 0.7:
            assumptions.append("Assumed stable — may need re-evaluation")
        return assumptions or ["No obvious assumptions identified"]

    def better_explanation(self, node_id: str) -> Optional[Dict[str, Any]]:
        """Could another explanation fit better?"""
        alternatives = self._find_alternatives(node_id, None)
        if not alternatives:
            return None
        # Find the best alternative
        best = max(alternatives, key=lambda a: a.get("score", 0))
        node = self._graph.get_node(node_id)
        current_state = get_state(self._graph, node_id)
        if best["score"] > current_state.confidence:
            return {
                "current": node.label if node else "",
                "current_confidence": current_state.confidence,
                "alternative": best["label"],
                "alternative_score": best["score"],
                "recommendation": "Consider alternative — higher confidence",
            }
        return None

    def what_to_investigate(self, node_id: str) -> List[str]:
        """What should be investigated next about this node?"""
        investigations = []
        state = get_state(self._graph, node_id)
        if state.entropy > 0.6:
            investigations.append("High uncertainty — gather more evidence")
        if state.prediction_accuracy < 0.5:
            investigations.append("Low prediction accuracy — test against new cases")
        evidence = self.what_evidence(node_id)
        if evidence["contradicting_evidence"]:
            investigations.append(f"Resolve {len(evidence['contradicting_evidence'])} contradiction(s)")
        if not evidence["supporting_evidence"]:
            investigations.append("Find supporting evidence")
        if state.confidence > 0.8 and state.usage_count < 3:
            investigations.append("Stress-test: use in more scenarios")
        return investigations or ["No immediate investigation needed"]

    def _find_alternatives(self, node_id: str, node_type: Optional[str]) -> List[Dict]:
        """Find alternative nodes that could serve same purpose."""
        node = self._graph.get_node(node_id)
        if not node:
            return []
        ntype = node_type or node.node_type
        similar = self._graph.find_nodes(node_type=ntype)
        alternatives = []
        for s in similar:
            if s.id == node_id:
                continue
            s_state = get_state(self._graph, s.id)
            if s_state.confidence > 0.3:
                alternatives.append({
                    "id": s.id, "label": s.label,
                    "score": s_state.confidence * (1 + s_state.prediction_accuracy) / 2
                })
        return sorted(alternatives, key=lambda a: -a["score"])[:5]


_meta: Optional[MetaReasoning] = None
def get_meta_reasoning(graph: Optional[RealityGraph] = None) -> MetaReasoning:
    global _meta
    if _meta is None:
        _meta = MetaReasoning(graph=graph)
    return _meta
