"""
AXIMA Knowledge Decay — Graceful dormancy, never instant deletion.

Knowledge is never instantly forgotten:
  - Activation decreases over time
  - Importance shifts based on goal relevance
  - Confidence adjusts with new evidence
  - Nodes become dormant (not deleted)
  - Dormant knowledge can be reactivated by spreading

No permanent deletion unless explicitly requested by user.
"""

import time
import math
from typing import Optional, Dict, Any, List

from core.reality_graph import get_reality_graph, RealityGraph
from core.cognitive_state import get_state, set_state


class KnowledgeDecay:
    """Manages graceful knowledge decay and dormancy."""

    def __init__(self, graph: Optional[RealityGraph] = None):
        self._graph = graph or get_reality_graph()

    def decay_tick(self, max_nodes: int = 100):
        """Apply one cycle of decay to all nodes.
        
        Incremental: processes at most max_nodes per call.
        """
        now = time.time()
        processed = 0

        for node_type in ["fact", "concept", "theory", "memory", "task"]:
            if processed >= max_nodes:
                break
            nodes = self._graph.find_nodes(node_type=node_type)
            for node in nodes:
                if processed >= max_nodes:
                    break
                state = get_state(self._graph, node.id)
                if state.is_dormant:
                    continue  # Skip already dormant nodes

                # Compute time-based decay
                hours_old = state.age / 3600
                last_used = node.properties.get("last_seen", node.updated_at)
                hours_idle = (now - last_used) / 3600 if last_used else hours_old

                # Apply decay rates
                state = self._apply_decay(state, hours_idle, node.node_type)
                set_state(self._graph, node.id, state)
                processed += 1

    def reactivate(self, node_id: str, strength: float = 0.5):
        """Reactivate a dormant node."""
        state = get_state(self._graph, node_id)
        state.activation = max(state.activation, strength)
        state.energy = max(state.energy, 0.2)
        state.usage_count += 1
        self._graph.update_node(node_id, properties={"last_seen": time.time()})
        set_state(self._graph, node_id, state)

    def dormant_nodes(self) -> List[str]:
        """Get all dormant node IDs."""
        dormant = []
        for node_type in ["fact", "concept", "theory", "memory"]:
            nodes = self._graph.find_nodes(node_type=node_type)
            for n in nodes:
                if n.properties.get("_cs_activation", 0) < 0.02:
                    dormant.append(n.id)
        return dormant

    def _apply_decay(self, state, hours_idle: float, node_type: str):
        """Apply type-appropriate decay."""
        # Base decay rates (per hour idle)
        base_rate = 0.005
        if node_type == "theory":
            base_rate = 0.002  # Theories decay slower
        elif node_type == "memory":
            base_rate = 0.008  # Memories decay faster
        elif node_type == "task":
            base_rate = 0.003

        # Stability reduces decay
        effective_rate = base_rate * (1.0 - state.stability * 0.8)

        # Apply
        decay_factor = math.exp(-effective_rate * hours_idle)
        state.activation *= decay_factor
        state.novelty *= decay_factor
        state.energy *= (1.0 - effective_rate * 0.5)

        # Importance decays very slowly
        if hours_idle > 24:
            state.importance *= 0.999

        return state

    def stats(self) -> Dict[str, Any]:
        return {"dormant_count": len(self.dormant_nodes())}


_decay: Optional[KnowledgeDecay] = None
def get_decay(graph: Optional[RealityGraph] = None) -> KnowledgeDecay:
    global _decay
    if _decay is None:
        _decay = KnowledgeDecay(graph=graph)
    return _decay
