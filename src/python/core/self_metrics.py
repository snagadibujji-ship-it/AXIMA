"""
AXIMA Self Metrics — Continuous self-evaluation dashboard.

Tracks 10 key metrics about AXIMA's own cognitive performance.
Internal use only — never exposed to end users.
"""

import time
from typing import Optional, Dict, Any, List
from core.reality_graph import get_reality_graph, RealityGraph


class SelfMetrics:
    """Continuous self-evaluation of cognitive performance."""

    def __init__(self, graph: Optional[RealityGraph] = None):
        self._graph = graph or get_reality_graph()
        self._history: List[Dict[str, float]] = []

    def compute_all(self) -> Dict[str, float]:
        """Compute all 10 self-metrics."""
        m = {
            "prediction_accuracy": self._prediction_accuracy(),
            "planning_success": self._planning_success(),
            "reflection_quality": self._reflection_quality(),
            "learning_velocity": self._learning_velocity(),
            "knowledge_growth": self._knowledge_growth(),
            "contradiction_rate": self._contradiction_rate(),
            "curiosity_rate": self._curiosity_rate(),
            "goal_completion_rate": self._goal_completion_rate(),
            "understanding_depth": self._understanding_depth(),
            "reasoning_confidence": self._reasoning_confidence(),
        }
        self._history.append({**m, "time": time.time()})
        if len(self._history) > 100:
            self._history = self._history[-100:]
        return m

    def trend(self, metric: str) -> str:
        """Is a metric improving, declining, or stable?"""
        if len(self._history) < 5:
            return "insufficient_data"
        recent = [h.get(metric, 0) for h in self._history[-5:]]
        older = [h.get(metric, 0) for h in self._history[-10:-5]]
        if not older:
            return "insufficient_data"
        avg_recent = sum(recent) / len(recent)
        avg_older = sum(older) / len(older)
        if avg_recent > avg_older + 0.05:
            return "improving"
        if avg_recent < avg_older - 0.05:
            return "declining"
        return "stable"

    def _prediction_accuracy(self) -> float:
        nodes = self._graph.find_nodes(node_type="theory")
        accs = [n.properties.get("_cs_prediction_accuracy", 0.5) for n in nodes if n.properties.get("_cs_usage_count", 0) > 0]
        return sum(accs) / max(1, len(accs))

    def _planning_success(self) -> float:
        goals = self._graph.find_nodes(node_type="goal")
        completed = sum(1 for g in goals if g.properties.get("status") == "completed")
        total = max(1, len(goals))
        return completed / total

    def _reflection_quality(self) -> float:
        memories = self._graph.find_nodes(node_type="memory")
        lessons = [m for m in memories if m.properties.get("memory_type") == "lesson"]
        return min(1.0, len(lessons) / 20.0)

    def _learning_velocity(self) -> float:
        if len(self._history) < 2:
            return 0.0
        now_knowledge = self._knowledge_growth()
        prev = self._history[-2].get("knowledge_growth", 0) if len(self._history) > 1 else 0
        return max(0, now_knowledge - prev)

    def _knowledge_growth(self) -> float:
        facts = len(self._graph.find_nodes(node_type="fact"))
        concepts = len(self._graph.find_nodes(node_type="concept"))
        theories = len(self._graph.find_nodes(node_type="theory"))
        return min(1.0, (facts + concepts + theories) / 100.0)

    def _contradiction_rate(self) -> float:
        edges = self._graph.find_edges(relation="contradicts")
        facts = max(1, len(self._graph.find_nodes(node_type="fact")))
        return min(1.0, len(edges) / facts)

    def _curiosity_rate(self) -> float:
        tasks = self._graph.find_nodes(node_type="task")
        curiosity_tasks = [t for t in tasks if t.properties.get("source") == "curiosity"]
        return min(1.0, len(curiosity_tasks) / 10.0)

    def _goal_completion_rate(self) -> float:
        goals = self._graph.find_nodes(node_type="goal")
        if not goals:
            return 0.0
        completed = sum(1 for g in goals if g.properties.get("status") == "completed")
        return completed / len(goals)

    def _understanding_depth(self) -> float:
        theories = self._graph.find_nodes(node_type="theory")
        principles = sum(1 for t in theories if t.properties.get("level") == "principle")
        rules = sum(1 for t in theories if t.properties.get("level") == "rule")
        if principles > 0:
            return 1.0
        if rules > 0:
            return 0.6
        return 0.2

    def _reasoning_confidence(self) -> float:
        all_nodes = []
        for t in ["fact", "concept", "theory"]:
            all_nodes.extend(self._graph.find_nodes(node_type=t))
        confs = [n.properties.get("_cs_confidence", 0.5) for n in all_nodes]
        return sum(confs) / max(1, len(confs))


_metrics: Optional[SelfMetrics] = None
def get_self_metrics(graph: Optional[RealityGraph] = None) -> SelfMetrics:
    global _metrics
    if _metrics is None:
        _metrics = SelfMetrics(graph=graph)
    return _metrics
