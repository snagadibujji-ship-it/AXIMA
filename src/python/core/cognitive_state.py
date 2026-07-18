"""
AXIMA Cognitive State — Universal dynamic state for every node.

Every node in the Reality Graph possesses these attributes.
Every subsystem reads and writes through this interface.
No exceptions.

Attributes:
    activation          — How active in current cognition (0-1)
    confidence          — How reliable (0-1)
    importance          — How critical to goals (0-1)
    novelty             — How recently discovered (0-1, decays)
    energy              — Processing invested (0-1)
    stability           — Resistance to change (0-1)
    age                 — Time since creation (seconds)
    usage_count         — Times accessed/used
    prediction_accuracy — How well predictions involving this held (0-1)
    reflection_count    — Times reflected upon
    learning_value      — How much was learned from this (0-1)
    entropy             — Uncertainty/disorder (0-1)

Usage:
    from core.cognitive_state import CognitiveState, get_state, set_state

    state = get_state(graph, node_id)
    state.activation = 0.8
    set_state(graph, node_id, state)
"""

import time
import math
from dataclasses import dataclass, field
from typing import Optional, Dict, Any, List

from core.reality_graph import RealityGraph, get_reality_graph


# ═══════════════════════════════════════════════════════════════
# COGNITIVE STATE
# ═══════════════════════════════════════════════════════════════

@dataclass
class CognitiveState:
    """Universal dynamic state for any Reality Graph node.
    
    Every node possesses these attributes. Every cognitive law
    reads and modifies them. This is the substrate of thought.
    """
    # Core dynamics
    activation: float = 0.0         # How active in current cognition (0=dormant, 1=focal)
    confidence: float = 0.5         # How reliable/trustworthy (0=unreliable, 1=certain)
    importance: float = 0.0         # How critical to active goals (0=irrelevant, 1=critical)
    novelty: float = 0.0           # How recently discovered (1=just now, decays over time)
    energy: float = 0.0            # Processing invested (0=untouched, 1=heavily processed)
    stability: float = 0.5         # Resistance to change (0=volatile, 1=immutable)

    # Temporal
    age: float = 0.0               # Seconds since creation
    usage_count: int = 0           # Times accessed/used

    # Learning
    prediction_accuracy: float = 0.5  # How well predictions involving this held
    reflection_count: int = 0         # Times reflected upon
    learning_value: float = 0.0       # How much was learned from this
    entropy: float = 0.5              # Uncertainty/disorder (0=ordered, 1=chaotic)

    def to_dict(self) -> Dict[str, Any]:
        """Serialize to dict for storage in node properties."""
        return {
            "_cs_activation": self.activation,
            "_cs_confidence": self.confidence,
            "_cs_importance": self.importance,
            "_cs_novelty": self.novelty,
            "_cs_energy": self.energy,
            "_cs_stability": self.stability,
            "_cs_age": self.age,
            "_cs_usage_count": self.usage_count,
            "_cs_prediction_accuracy": self.prediction_accuracy,
            "_cs_reflection_count": self.reflection_count,
            "_cs_learning_value": self.learning_value,
            "_cs_entropy": self.entropy,
        }

    @classmethod
    def from_dict(cls, props: Dict[str, Any]) -> 'CognitiveState':
        """Deserialize from node properties."""
        return cls(
            activation=props.get("_cs_activation", 0.0),
            confidence=props.get("_cs_confidence", props.get("confidence", 0.5)),
            importance=props.get("_cs_importance", 0.0),
            novelty=props.get("_cs_novelty", 0.0),
            energy=props.get("_cs_energy", 0.0),
            stability=props.get("_cs_stability", 0.5),
            age=props.get("_cs_age", 0.0),
            usage_count=props.get("_cs_usage_count", props.get("usage_count", 0)),
            prediction_accuracy=props.get("_cs_prediction_accuracy", 0.5),
            reflection_count=props.get("_cs_reflection_count", 0),
            learning_value=props.get("_cs_learning_value", 0.0),
            entropy=props.get("_cs_entropy", 0.5),
        )

    @property
    def is_dormant(self) -> bool:
        """Node is effectively asleep."""
        return self.activation < 0.05 and self.energy < 0.05

    @property
    def is_active(self) -> bool:
        """Node is in the cognitive foreground."""
        return self.activation > 0.3

    @property
    def is_stable(self) -> bool:
        """Node resists change."""
        return self.stability > 0.7

    @property
    def attention_score(self) -> float:
        """Composite attention score from state."""
        return (
            self.activation * 0.25 +
            self.importance * 0.25 +
            self.novelty * 0.15 +
            self.confidence * 0.10 +
            self.energy * 0.10 +
            (1.0 - self.entropy) * 0.05 +
            self.learning_value * 0.10
        )

    def clamp(self):
        """Ensure all values are within valid ranges."""
        self.activation = max(0.0, min(1.0, self.activation))
        self.confidence = max(0.0, min(1.0, self.confidence))
        self.importance = max(0.0, min(1.0, self.importance))
        self.novelty = max(0.0, min(1.0, self.novelty))
        self.energy = max(0.0, min(1.0, self.energy))
        self.stability = max(0.0, min(1.0, self.stability))
        self.prediction_accuracy = max(0.0, min(1.0, self.prediction_accuracy))
        self.learning_value = max(0.0, min(1.0, self.learning_value))
        self.entropy = max(0.0, min(1.0, self.entropy))
        self.usage_count = max(0, self.usage_count)
        self.reflection_count = max(0, self.reflection_count)


# ═══════════════════════════════════════════════════════════════
# STATE ACCESS API
# ═══════════════════════════════════════════════════════════════

def get_state(graph: RealityGraph, node_id: str) -> CognitiveState:
    """Get the cognitive state of a node. Creates default if missing."""
    node = graph.get_node(node_id)
    if not node:
        return CognitiveState()

    state = CognitiveState.from_dict(node.properties)

    # Compute age dynamically
    if node.created_at:
        state.age = time.time() - node.created_at

    return state


def set_state(graph: RealityGraph, node_id: str, state: CognitiveState):
    """Write cognitive state back to a node."""
    state.clamp()
    graph.update_node(node_id, properties=state.to_dict())


def batch_get_states(graph: RealityGraph, node_ids: List[str]) -> Dict[str, CognitiveState]:
    """Get states for multiple nodes efficiently."""
    return {nid: get_state(graph, nid) for nid in node_ids}


def batch_set_states(graph: RealityGraph, states: Dict[str, CognitiveState]):
    """Write states for multiple nodes."""
    for nid, state in states.items():
        set_state(graph, nid, state)


def initialize_state(graph: RealityGraph, node_id: str,
                     activation: float = 0.5, confidence: float = 0.5,
                     novelty: float = 1.0):
    """Initialize cognitive state for a newly created node."""
    state = CognitiveState(
        activation=activation,
        confidence=confidence,
        novelty=novelty,
        energy=0.1,
        stability=0.3,
        entropy=0.5,
    )
    set_state(graph, node_id, state)
