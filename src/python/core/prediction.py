"""
AXIMA Prediction Engine — Maintains predictions on active goals.

Every active goal maintains:
  - Probability of success
  - Estimated completion
  - Risk level
  - Confidence in prediction
  - Prediction history (for tracking accuracy)

Predictions update whenever reality changes.

Usage:
    from core.prediction import PredictionEngine, get_predictions

    engine = get_predictions()
    engine.update_all()
    
    pred = engine.predict_goal(goal_id)
    # pred.success_probability, pred.risk_level, pred.estimated_turns
"""

import time
import math
from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any

from core.reality_graph import get_reality_graph, RealityGraph


# ═══════════════════════════════════════════════════════════════
# PREDICTION DATA
# ═══════════════════════════════════════════════════════════════

@dataclass
class Prediction:
    """A prediction about a goal or task."""
    target_id: str                      # What this predicts about
    target_label: str = ""

    # Core predictions
    success_probability: float = 0.5    # 0.0 to 1.0
    estimated_turns: int = 0            # Estimated interactions to complete
    risk_level: float = 0.0             # 0=safe, 1=high risk
    confidence: float = 0.5             # How confident in this prediction

    # Risk factors
    blockers: List[str] = field(default_factory=list)
    risks: List[str] = field(default_factory=list)

    # History
    created_at: float = 0.0
    updated_at: float = 0.0
    history: List[Dict[str, float]] = field(default_factory=list)  # [{time, success_prob, confidence}]

    def record_snapshot(self):
        """Record current state in history."""
        self.history.append({
            "time": time.time(),
            "success_probability": self.success_probability,
            "confidence": self.confidence,
            "risk_level": self.risk_level,
        })
        # Keep last 50 snapshots
        if len(self.history) > 50:
            self.history = self.history[-50:]

    @property
    def trend(self) -> str:
        """Is the prediction improving or declining?"""
        if len(self.history) < 2:
            return "stable"
        recent = self.history[-3:]
        if len(recent) < 2:
            return "stable"
        avg_recent = sum(h["success_probability"] for h in recent) / len(recent)
        avg_prev = sum(h["success_probability"] for h in self.history[:-3][:3]) / max(1, min(3, len(self.history) - 3))
        if avg_recent > avg_prev + 0.1:
            return "improving"
        if avg_recent < avg_prev - 0.1:
            return "declining"
        return "stable"


# ═══════════════════════════════════════════════════════════════
# PREDICTION ENGINE
# ═══════════════════════════════════════════════════════════════

class PredictionEngine:
    """Maintains and updates predictions on active goals.
    
    Predictions emerge from graph state — not from simulation.
    """

    def __init__(self, graph: Optional[RealityGraph] = None):
        self._graph = graph or get_reality_graph()
        self._predictions: Dict[str, Prediction] = {}

    def update_all(self):
        """Update predictions for all active goals."""
        goals = self._graph.find_nodes(node_type="goal")
        active_goals = [g for g in goals if g.properties.get("status") == "active"]

        for goal in active_goals:
            self._update_prediction(goal)

    def predict_goal(self, goal_id: str) -> Optional[Prediction]:
        """Get prediction for a specific goal."""
        if goal_id not in self._predictions:
            node = self._graph.get_node(goal_id)
            if node:
                self._update_prediction(node)
        return self._predictions.get(goal_id)

    def all_predictions(self) -> List[Prediction]:
        """Get all current predictions."""
        return list(self._predictions.values())

    def high_risk(self) -> List[Prediction]:
        """Get predictions with high risk level."""
        return [p for p in self._predictions.values() if p.risk_level > 0.6]

    def accuracy_report(self) -> Dict[str, Any]:
        """How accurate have predictions been?"""
        completed_goals = self._graph.find_nodes(node_type="goal")
        completed = [g for g in completed_goals if g.properties.get("status") == "completed"]

        correct = 0
        total = 0
        for goal in completed:
            if goal.id in self._predictions:
                pred = self._predictions[goal.id]
                # If we predicted high success and it completed → correct
                if pred.history:
                    first_pred = pred.history[0]["success_probability"]
                    if first_pred > 0.5:
                        correct += 1
                    total += 1

        return {
            "total_predictions": len(self._predictions),
            "completed_goals": len(completed),
            "tracked_completions": total,
            "correct_predictions": correct,
            "accuracy": correct / max(1, total),
        }

    def _update_prediction(self, goal_node):
        """Compute/update prediction for a goal."""
        goal_id = goal_node.id

        # Get or create prediction
        if goal_id not in self._predictions:
            self._predictions[goal_id] = Prediction(
                target_id=goal_id,
                target_label=goal_node.label,
                created_at=time.time(),
            )
        pred = self._predictions[goal_id]

        # Compute components
        pred.success_probability = self._estimate_success(goal_node)
        pred.risk_level = self._estimate_risk(goal_node)
        pred.estimated_turns = self._estimate_completion(goal_node)
        pred.confidence = self._estimate_confidence(goal_node)
        pred.blockers = self._find_blockers(goal_node)
        pred.risks = self._identify_risks(goal_node)
        pred.updated_at = time.time()

        # Record in history
        pred.record_snapshot()

    def _estimate_success(self, goal_node) -> float:
        """Estimate probability of goal success."""
        progress = goal_node.properties.get("progress", 0.0)
        # Progress directly contributes
        base = progress * 0.5

        # Children status
        children = self._get_children(goal_node.id)
        if children:
            completed = sum(1 for c in children if c.properties.get("status") == "completed")
            blocked = sum(1 for c in children if c.properties.get("status") == "blocked")
            total = len(children)

            completion_ratio = completed / max(1, total)
            block_ratio = blocked / max(1, total)

            base += completion_ratio * 0.4
            base -= block_ratio * 0.2

        # Cap between 0.1 and 0.95
        return max(0.1, min(0.95, base))

    def _estimate_risk(self, goal_node) -> float:
        """Estimate risk level (what could go wrong)."""
        risk = 0.0

        children = self._get_children(goal_node.id)
        if children:
            blocked = sum(1 for c in children if c.properties.get("status") == "blocked")
            if blocked > 0:
                risk += 0.3

            # Many incomplete tasks = risk
            active = sum(1 for c in children if c.properties.get("status") == "active")
            if active > 5:
                risk += 0.2

        # Low confidence = risk
        confidence = goal_node.properties.get("confidence", 0.5)
        if confidence < 0.5:
            risk += 0.2

        # Contradictions connected = risk
        neighbors = self._graph.neighbors(goal_node.id, direction="both")
        contradictions = sum(1 for _, rel, _ in neighbors if rel == "contradicts")
        if contradictions > 0:
            risk += 0.2

        return min(1.0, risk)

    def _estimate_completion(self, goal_node) -> int:
        """Estimate turns/interactions to completion."""
        children = self._get_children(goal_node.id)
        if not children:
            return 1

        active = sum(1 for c in children if c.properties.get("status") == "active")
        blocked = sum(1 for c in children if c.properties.get("status") == "blocked")

        # Each active task ~ 1-2 turns, blocked tasks ~ 3+ turns
        return active * 2 + blocked * 4

    def _estimate_confidence(self, goal_node) -> float:
        """How confident are we in this prediction?"""
        children = self._get_children(goal_node.id)
        if not children:
            return 0.3  # No info → low confidence

        # More data = more confidence
        total = len(children)
        return min(0.9, 0.4 + total * 0.05)

    def _find_blockers(self, goal_node) -> List[str]:
        """Find what's blocking a goal."""
        blockers = []
        children = self._get_children(goal_node.id)
        for child in children:
            if child.properties.get("status") == "blocked":
                reason = child.properties.get("block_reason", "")
                blockers.append(f"{child.label}: {reason}" if reason else child.label)
        return blockers

    def _identify_risks(self, goal_node) -> List[str]:
        """Identify risk factors."""
        risks = []
        children = self._get_children(goal_node.id)

        blocked_count = sum(1 for c in children if c.properties.get("status") == "blocked")
        if blocked_count > 0:
            risks.append(f"{blocked_count} blocked task(s)")

        # Check for contradictions
        neighbors = self._graph.neighbors(goal_node.id, direction="both")
        for nid, rel, _ in neighbors:
            if rel == "contradicts":
                node = self._graph.get_node(nid)
                if node:
                    risks.append(f"Contradicts: {node.label}")

        return risks

    def _get_children(self, node_id: str) -> List:
        """Get child nodes (via 'contains' edges)."""
        children = []
        for child_id, rel, _ in self._graph.neighbors(node_id, relation="contains"):
            child = self._graph.get_node(child_id)
            if child:
                children.append(child)
        return children


# ═══════════════════════════════════════════════════════════════
# SINGLETON
# ═══════════════════════════════════════════════════════════════

_engine: Optional[PredictionEngine] = None

def get_predictions(graph: Optional[RealityGraph] = None) -> PredictionEngine:
    """Get the global prediction engine."""
    global _engine
    if _engine is None:
        _engine = PredictionEngine(graph=graph)
    return _engine
