"""
AXIMA Activation Spreading — Thinking spreads through the graph.

When one node activates:
  - Related concepts receive partial activation
  - Important relationships amplify spreading
  - Weak relationships reduce spreading
  - Activation fades with distance

This creates "ripples of thought" through the knowledge graph.

Usage:
    from core.activation_spreading import ActivationSpreading, get_spreading

    spreading = get_spreading()
    spreading.spread_from(node_id, strength=0.5)
    spreading.spread_all()  # Spread from all currently active nodes
"""

import math
from typing import Optional, List, Dict, Set

from core.reality_graph import get_reality_graph, RealityGraph
from core.cognitive_state import CognitiveState, get_state, set_state


# Relationship weights: how much activation passes through each type
RELATION_WEIGHTS = {
    "contains": 0.7,       # Parent-child: strong
    "supports": 0.6,       # Evidence: strong
    "depends_on": 0.5,     # Dependency: medium
    "extends": 0.5,        # Extension: medium
    "relates_to": 0.3,     # General: weak
    "contradicts": 0.1,    # Contradiction: minimal (awareness, not support)
    "derived_from": 0.4,   # Derivation: medium
    "owns": 0.2,           # Ownership: weak
    "created": 0.2,        # Creation: weak
    "blocked_by": 0.3,     # Blocker: medium (draws attention to block)
}

# Distance decay: activation × decay_factor^distance
DISTANCE_DECAY = 0.5  # Each hop halves the activation


class ActivationSpreading:
    """Spreading activation through the Reality Graph.
    
    Models how thinking in one area naturally activates related areas.
    """

    def __init__(self, graph: Optional[RealityGraph] = None,
                 max_depth: int = 3, min_activation: float = 0.02):
        self._graph = graph or get_reality_graph()
        self._max_depth = max_depth
        self._min_activation = min_activation

    def spread_from(self, source_id: str, strength: float = 0.5,
                    max_depth: Optional[int] = None):
        """Spread activation from a single source node.
        
        Activation ripples outward, decaying with distance and
        modulated by relationship strength.
        """
        depth = max_depth or self._max_depth
        visited: Set[str] = {source_id}
        frontier: List[tuple] = [(source_id, strength)]  # (node_id, activation_to_spread)

        for d in range(depth):
            next_frontier = []
            for node_id, current_strength in frontier:
                if current_strength < self._min_activation:
                    continue

                # Get neighbors
                neighbors = self._graph.neighbors(node_id, direction="both")
                for neighbor_id, relation, edge in neighbors:
                    if neighbor_id in visited:
                        continue
                    visited.add(neighbor_id)

                    # Calculate spread amount
                    rel_weight = RELATION_WEIGHTS.get(relation, 0.2)
                    edge_weight = edge.weight if edge else 1.0
                    spread_amount = current_strength * rel_weight * edge_weight * DISTANCE_DECAY

                    if spread_amount < self._min_activation:
                        continue

                    # Apply to neighbor
                    neighbor_state = get_state(self._graph, neighbor_id)
                    neighbor_state.activation = min(1.0, neighbor_state.activation + spread_amount)
                    # Small energy boost from being activated by spreading
                    neighbor_state.energy = min(1.0, neighbor_state.energy + spread_amount * 0.1)
                    set_state(self._graph, neighbor_id, neighbor_state)

                    next_frontier.append((neighbor_id, spread_amount))

            frontier = next_frontier

    def spread_all(self, threshold: float = 0.3):
        """Spread from all currently active nodes above threshold."""
        # Find all active nodes
        active_nodes = []
        for node_type in ["goal", "task", "fact", "concept", "theory"]:
            nodes = self._graph.find_nodes(node_type=node_type)
            for n in nodes:
                activation = n.properties.get("_cs_activation", 0)
                if activation > threshold:
                    active_nodes.append((n.id, activation))

        # Spread from each (limited to top 10 to keep O(N) bounded)
        active_nodes.sort(key=lambda x: -x[1])
        for node_id, activation in active_nodes[:10]:
            spread_strength = activation * 0.3  # Only spread 30% of activation
            self.spread_from(node_id, strength=spread_strength, max_depth=2)

    def focused_spread(self, source_id: str, target_type: Optional[str] = None):
        """Spread activation but only to nodes of a specific type.
        
        Useful for: "activate all facts related to this goal"
        """
        visited: Set[str] = {source_id}
        source_state = get_state(self._graph, source_id)
        strength = source_state.activation * 0.4

        neighbors = self._graph.neighbors(source_id, direction="both")
        for neighbor_id, relation, edge in neighbors:
            if neighbor_id in visited:
                continue
            visited.add(neighbor_id)

            node = self._graph.get_node(neighbor_id)
            if not node:
                continue
            if target_type and node.node_type != target_type:
                continue

            rel_weight = RELATION_WEIGHTS.get(relation, 0.2)
            spread_amount = strength * rel_weight

            if spread_amount >= self._min_activation:
                state = get_state(self._graph, neighbor_id)
                state.activation = min(1.0, state.activation + spread_amount)
                set_state(self._graph, neighbor_id, state)

    def decay_all(self, rate: float = 0.05):
        """Apply global activation decay to all nodes.
        
        Called each tick to let activation naturally fade.
        """
        for node_type in ["goal", "task", "fact", "concept", "theory", "memory"]:
            nodes = self._graph.find_nodes(node_type=node_type)
            for n in nodes:
                activation = n.properties.get("_cs_activation", 0)
                if activation > 0.01:
                    new_activation = activation * (1.0 - rate)
                    self._graph.update_node(n.id, properties={"_cs_activation": new_activation})

    def stats(self) -> Dict:
        """Spreading statistics."""
        active = 0
        total = 0
        for node_type in ["goal", "task", "fact", "concept", "theory"]:
            nodes = self._graph.find_nodes(node_type=node_type)
            for n in nodes:
                total += 1
                if n.properties.get("_cs_activation", 0) > 0.1:
                    active += 1
        return {
            "total_nodes": total,
            "active_nodes": active,
            "active_ratio": active / max(1, total),
        }


# ═══════════════════════════════════════════════════════════════
# SINGLETON
# ═══════════════════════════════════════════════════════════════

_spreading: Optional[ActivationSpreading] = None

def get_spreading(graph: Optional[RealityGraph] = None) -> ActivationSpreading:
    """Get the global activation spreading instance."""
    global _spreading
    if _spreading is None:
        _spreading = ActivationSpreading(graph=graph)
    return _spreading
