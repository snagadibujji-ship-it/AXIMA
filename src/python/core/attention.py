"""
AXIMA Attention System — Cognitive focus through dynamic node scoring.

Every node in the Reality Graph receives an attention score based on:
  - importance: how critical to active goals
  - urgency: time pressure
  - novelty: how recently discovered
  - confidence: how reliable
  - recency: how recently accessed
  - energy: how much processing it has received

Only top-scoring nodes are "active" — the cognitive foreground.
Everything else remains stored but doesn't consume reasoning.

Usage:
    from core.attention import AttentionSystem, get_attention

    attention = get_attention()
    attention.update_scores()
    
    active = attention.active_nodes(limit=10)
    focus = attention.current_focus()
"""

import time
import math
from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any, Tuple

from core.reality_graph import get_reality_graph, RealityGraph, Node


# ═══════════════════════════════════════════════════════════════
# ATTENTION SCORE
# ═══════════════════════════════════════════════════════════════

@dataclass
class AttentionScore:
    """Attention score components for a single node."""
    node_id: str
    node_type: str = ""
    label: str = ""

    # Components (each 0.0 to 1.0)
    importance: float = 0.0     # How critical to active goals
    urgency: float = 0.0       # Time pressure
    novelty: float = 0.0       # How recently discovered
    confidence: float = 0.0    # How reliable the information is
    recency: float = 0.0       # How recently accessed/updated
    energy: float = 0.0        # How much processing invested

    # Computed
    total: float = 0.0         # Weighted composite score

    def compute_total(self, weights: Dict[str, float] = None) -> float:
        """Compute weighted total attention score."""
        w = weights or {
            'importance': 0.30,
            'urgency': 0.25,
            'novelty': 0.15,
            'confidence': 0.10,
            'recency': 0.10,
            'energy': 0.10,
        }
        self.total = (
            self.importance * w.get('importance', 0.3) +
            self.urgency * w.get('urgency', 0.25) +
            self.novelty * w.get('novelty', 0.15) +
            self.confidence * w.get('confidence', 0.1) +
            self.recency * w.get('recency', 0.1) +
            self.energy * w.get('energy', 0.1)
        )
        return self.total


# ═══════════════════════════════════════════════════════════════
# ATTENTION SYSTEM
# ═══════════════════════════════════════════════════════════════

class AttentionSystem:
    """Dynamic attention scoring for Reality Graph nodes.
    
    Determines what AXIMA is "thinking about" at any moment.
    """

    def __init__(self, graph: Optional[RealityGraph] = None,
                 active_limit: int = 20):
        self._graph = graph or get_reality_graph()
        self._scores: Dict[str, AttentionScore] = {}
        self._active_limit = active_limit
        self._weights = {
            'importance': 0.30,
            'urgency': 0.25,
            'novelty': 0.15,
            'confidence': 0.10,
            'recency': 0.10,
            'energy': 0.10,
        }

    def update_scores(self):
        """Recompute attention scores for all nodes."""
        self._scores.clear()
        now = time.time()

        for node in self._all_nodes():
            score = AttentionScore(
                node_id=node.id,
                node_type=node.node_type,
                label=node.label,
            )

            score.importance = self._compute_importance(node)
            score.urgency = self._compute_urgency(node, now)
            score.novelty = self._compute_novelty(node, now)
            score.confidence = self._compute_confidence(node)
            score.recency = self._compute_recency(node, now)
            score.energy = self._compute_energy(node)

            score.compute_total(self._weights)
            self._scores[node.id] = score

    def active_nodes(self, limit: Optional[int] = None) -> List[AttentionScore]:
        """Get the highest-scoring nodes (the cognitive foreground)."""
        if not self._scores:
            self.update_scores()
        ranked = sorted(self._scores.values(), key=lambda s: -s.total)
        n = limit or self._active_limit
        return ranked[:n]

    def current_focus(self) -> Optional[AttentionScore]:
        """The single highest-attention node."""
        active = self.active_nodes(limit=1)
        return active[0] if active else None

    def get_score(self, node_id: str) -> Optional[AttentionScore]:
        """Get attention score for a specific node."""
        return self._scores.get(node_id)

    def boost(self, node_id: str, component: str, amount: float = 0.2):
        """Manually boost a component of a node's attention.
        
        Used when the system wants to draw attention to something.
        """
        if node_id in self._scores:
            score = self._scores[node_id]
            current = getattr(score, component, 0)
            setattr(score, component, min(1.0, current + amount))
            score.compute_total(self._weights)

    def decay(self, rate: float = 0.05):
        """Apply time-based decay to all scores.
        
        Called periodically to let attention naturally fade
        from things that aren't being reinforced.
        """
        for score in self._scores.values():
            score.urgency = max(0, score.urgency - rate)
            score.novelty = max(0, score.novelty - rate * 0.5)
            score.energy = max(0, score.energy - rate * 0.3)
            score.compute_total(self._weights)

    def set_weights(self, **kwargs):
        """Adjust attention weights (what matters most right now)."""
        for key, value in kwargs.items():
            if key in self._weights:
                self._weights[key] = value

    def stats(self) -> Dict[str, Any]:
        """Attention system statistics."""
        if not self._scores:
            return {"nodes_scored": 0}
        scores = list(self._scores.values())
        active = [s for s in scores if s.total > 0.3]
        return {
            "nodes_scored": len(scores),
            "active_nodes": len(active),
            "top_focus": scores[0].label if scores else "",
            "avg_attention": sum(s.total for s in scores) / max(1, len(scores)),
            "max_attention": max(s.total for s in scores) if scores else 0,
        }

    # ─── Component Calculators ───

    def _compute_importance(self, node: Node) -> float:
        """How critical is this node to active goals?"""
        # Goals with high priority are important
        if node.node_type == "goal":
            priority = node.properties.get("priority", 0)
            status = node.properties.get("status", "")
            if status == "active":
                return min(1.0, priority / 10.0)
            return 0.1

        # Tasks under active goals inherit importance
        if node.node_type == "task":
            status = node.properties.get("status", "")
            if status == "active":
                return 0.7
            if status == "blocked":
                return 0.8  # Blocked tasks need attention
            return 0.1

        # Facts supporting active goals
        if node.node_type == "fact":
            # Check if connected to active goals
            neighbors = self._graph.neighbors(node.id, direction="both")
            for nid, rel, _ in neighbors:
                n = self._graph.get_node(nid)
                if n and n.node_type == "goal" and n.properties.get("status") == "active":
                    return 0.6
            return 0.2

        # Concepts connected to many things
        if node.node_type == "concept":
            connections = len(self._graph.neighbors(node.id, direction="both"))
            return min(1.0, connections / 10.0)

        return 0.3

    def _compute_urgency(self, node: Node, now: float) -> float:
        """Time pressure on this node."""
        urgency = node.properties.get("urgency", 0)
        if urgency:
            return min(1.0, float(urgency))

        # Blocked tasks have urgency
        if node.properties.get("status") == "blocked":
            return 0.7

        # Active goals with no progress are urgent
        if node.node_type == "goal" and node.properties.get("status") == "active":
            progress = node.properties.get("progress", 0)
            if progress < 0.1:
                return 0.5
        return 0.0

    def _compute_novelty(self, node: Node, now: float) -> float:
        """How recently was this discovered/created?"""
        created = node.properties.get("detected_at", node.created_at)
        if not created:
            return 0.0
        age_hours = (now - created) / 3600
        # Exponential decay: new = 1.0, 1 hour = 0.6, 24 hours = 0.1
        return math.exp(-age_hours / 10.0)

    def _compute_confidence(self, node: Node) -> float:
        """How reliable is this information?"""
        conf = node.properties.get("confidence", 0.5)
        return float(conf)

    def _compute_recency(self, node: Node, now: float) -> float:
        """How recently was this accessed/updated?"""
        updated = node.updated_at or node.created_at
        if not updated:
            return 0.0
        age_hours = (now - updated) / 3600
        return math.exp(-age_hours / 24.0)

    def _compute_energy(self, node: Node) -> float:
        """How much processing has been invested in this node?"""
        mentions = node.properties.get("mention_count", 0)
        used = node.properties.get("used_count", 0)
        return min(1.0, (mentions + used) / 10.0)

    def _all_nodes(self) -> List[Node]:
        """Get all nodes from the graph."""
        all_types = ["goal", "task", "fact", "concept", "theory", "user", "project"]
        nodes = []
        for t in all_types:
            nodes.extend(self._graph.find_nodes(node_type=t))
        return nodes


# ═══════════════════════════════════════════════════════════════
# SINGLETON
# ═══════════════════════════════════════════════════════════════

_attention: Optional[AttentionSystem] = None

def get_attention(graph: Optional[RealityGraph] = None) -> AttentionSystem:
    """Get the global attention system."""
    global _attention
    if _attention is None:
        _attention = AttentionSystem(graph=graph)
    return _attention
