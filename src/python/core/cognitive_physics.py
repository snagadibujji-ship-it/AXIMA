"""
AXIMA Cognitive Physics Engine — Applies universal cognitive laws to nodes.

Responsibilities:
  - Evaluate node state
  - Apply all applicable laws
  - Update activation, confidence, decay, reinforcement
  - Spread activation through connections
  - Update priorities

Contains NO business logic. Only executes cognitive laws.

Usage:
    from core.cognitive_physics import CognitivePhysics, get_physics

    physics = get_physics()
    physics.tick()  # Apply one cycle of laws to all active nodes
    physics.tick_node(node_id)  # Apply laws to one specific node
"""

import time
from typing import Optional, List, Dict, Any

from core.reality_graph import get_reality_graph, RealityGraph
from core.cognitive_state import CognitiveState, get_state, set_state, batch_get_states, batch_set_states
from core.cognitive_laws import COGNITIVE_LAWS, CognitiveLaw


class CognitivePhysics:
    """The engine that makes cognitive laws run.
    
    This is the heartbeat of change. Every tick applies laws
    to nodes, causing the system to evolve.
    """

    def __init__(self, graph: Optional[RealityGraph] = None):
        self._graph = graph or get_reality_graph()
        self._tick_count = 0
        self._last_tick = 0.0
        self._laws = COGNITIVE_LAWS

    def tick(self, active_only: bool = True, limit: int = 50):
        """Apply one cycle of cognitive laws to nodes.
        
        Args:
            active_only: If True, only process active/important nodes (O(active) not O(N))
            limit: Max nodes to process per tick (keeps latency bounded)
        """
        self._tick_count += 1
        now = time.time()
        dt = now - self._last_tick if self._last_tick else 1.0
        self._last_tick = now

        # Get nodes to process
        node_ids = self._select_nodes(active_only, limit)
        if not node_ids:
            return

        # Batch get states
        states = batch_get_states(self._graph, node_ids)

        # Apply laws to each node
        for nid, state in states.items():
            ctx = self._build_context(nid, state, dt)
            state = self._apply_laws(state, ctx)
            states[nid] = state

        # Batch write back
        batch_set_states(self._graph, states)

    def tick_node(self, node_id: str, context: Optional[Dict] = None):
        """Apply laws to a single node with optional explicit context."""
        state = get_state(self._graph, node_id)
        ctx = context or self._build_context(node_id, state, 1.0)
        state = self._apply_laws(state, ctx)
        set_state(self._graph, node_id, state)

    def activate(self, node_id: str, amount: float = 0.3):
        """Explicitly activate a node (e.g., because it was used)."""
        state = get_state(self._graph, node_id)
        state.activation = min(1.0, state.activation + amount)
        state.usage_count += 1
        set_state(self._graph, node_id, state)

    def record_prediction(self, node_id: str, correct: bool):
        """Record whether a prediction involving this node was correct."""
        ctx = {"prediction_correct": correct, "used_successfully": correct, "used_and_failed": not correct}
        self.tick_node(node_id, context=ctx)

    def record_reflection(self, node_id: str):
        """Record that this node was reflected upon."""
        ctx = {"reflected": True}
        self.tick_node(node_id, context=ctx)

    def record_contradiction(self, node_id: str):
        """Record that a contradiction was found involving this node."""
        ctx = {"contradiction_found": True}
        self.tick_node(node_id, context=ctx)

    def mark_new(self, node_id: str):
        """Mark a node as newly created (sets novelty, activation)."""
        ctx = {"is_new": True}
        self.tick_node(node_id, context=ctx)

    def stats(self) -> Dict[str, Any]:
        """Physics engine statistics."""
        return {
            "tick_count": self._tick_count,
            "laws_count": len(self._laws),
            "last_tick": self._last_tick,
        }

    # ─── Internal ───

    def _select_nodes(self, active_only: bool, limit: int) -> List[str]:
        """Select which nodes to process this tick."""
        all_types = ["goal", "task", "fact", "concept", "theory", "memory"]
        candidates = []

        for t in all_types:
            nodes = self._graph.find_nodes(node_type=t)
            for n in nodes:
                if active_only:
                    # Only process if: active, important, or high novelty
                    activation = n.properties.get("_cs_activation", 0)
                    importance = n.properties.get("_cs_importance", 0)
                    novelty = n.properties.get("_cs_novelty", 0)
                    status = n.properties.get("status", "")
                    if activation > 0.05 or importance > 0.1 or novelty > 0.1 or status == "active":
                        candidates.append(n.id)
                else:
                    candidates.append(n.id)

        return candidates[:limit]

    def _build_context(self, node_id: str, state: CognitiveState, dt: float) -> Dict[str, Any]:
        """Build the context dict for law evaluation."""
        node = self._graph.get_node(node_id)
        if not node:
            return {}

        # Count connections
        neighbors = self._graph.neighbors(node_id, direction="both")
        active_connections = 0
        max_child_importance = 0.0
        supporting_evidence = 0

        for nid, rel, _ in neighbors:
            n = self._graph.get_node(nid)
            if n:
                n_activation = n.properties.get("_cs_activation", 0)
                if n_activation > 0.1:
                    active_connections += 1
                if rel == "contains":
                    child_imp = n.properties.get("_cs_importance", 0)
                    max_child_importance = max(max_child_importance, child_imp)
                if rel == "supports":
                    supporting_evidence += 1

        # Time since last use
        last_seen = node.properties.get("last_seen", node.updated_at)
        hours_since_use = (time.time() - last_seen) / 3600 if last_seen else 0

        return {
            "dt": dt,
            "total_connections": len(neighbors),
            "active_connections": active_connections,
            "max_child_importance": max_child_importance,
            "supporting_evidence_count": supporting_evidence,
            "hours_since_use": hours_since_use,
            "is_active_goal": node.node_type == "goal" and node.properties.get("status") == "active",
            "goal_priority": node.properties.get("priority", 0),
            "is_principle": node.properties.get("level") == "principle",
            "processed": True,
            "prev_activation": state.activation,
        }

    def _apply_laws(self, state: CognitiveState, ctx: Dict) -> CognitiveState:
        """Apply all applicable cognitive laws to a state."""
        for law in self._laws.values():
            try:
                state = law.apply(state, ctx)
            except Exception:
                continue  # Laws must never crash the system
        state.clamp()
        return state


# ═══════════════════════════════════════════════════════════════
# SINGLETON
# ═══════════════════════════════════════════════════════════════

_physics: Optional[CognitivePhysics] = None

def get_physics(graph: Optional[RealityGraph] = None) -> CognitivePhysics:
    """Get the global cognitive physics engine."""
    global _physics
    if _physics is None:
        _physics = CognitivePhysics(graph=graph)
    return _physics
