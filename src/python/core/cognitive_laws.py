"""
AXIMA Cognitive Laws — Universal rules governing all cognition.

Every law is:
  - Predictable: given state, output is deterministic
  - Composable: laws combine without conflict
  - Independent: no law depends on another law's implementation
  - Testable: can verify with unit tests
  - Explainable: can describe in one sentence

Laws operate on CognitiveState. They are pure functions:
    (CognitiveState, context) → CognitiveState

The Cognitive Physics Engine applies these laws to nodes.
"""

from dataclasses import dataclass
from typing import Callable, Dict, Any, Optional
import math

from core.cognitive_state import CognitiveState


# ═══════════════════════════════════════════════════════════════
# LAW DEFINITION
# ═══════════════════════════════════════════════════════════════

@dataclass
class CognitiveLaw:
    """A single universal cognitive law."""
    id: str                     # Unique identifier (e.g., "L01")
    name: str                   # Human-readable name
    description: str            # One-sentence explanation
    category: str               # reinforcement, decay, spreading, meta, emergence
    apply: Callable             # (state, context) → state


# ═══════════════════════════════════════════════════════════════
# THE 25 COGNITIVE LAWS
# ═══════════════════════════════════════════════════════════════

def _L01_prediction_success(state: CognitiveState, ctx: Dict) -> CognitiveState:
    """Successful predictions increase confidence."""
    if ctx.get("prediction_correct"):
        boost = 0.05 * (1.0 - state.confidence)  # Diminishing returns
        state.confidence += boost
        state.prediction_accuracy += 0.03
        state.stability += 0.02
    return state


def _L02_contradiction_weakens(state: CognitiveState, ctx: Dict) -> CognitiveState:
    """Contradictions decrease confidence."""
    if ctx.get("contradiction_found"):
        loss = 0.08 * state.confidence  # Proportional loss
        state.confidence -= loss
        state.entropy += 0.05
        state.stability -= 0.03
    return state


def _L03_usage_activates(state: CognitiveState, ctx: Dict) -> CognitiveState:
    """Frequently used knowledge gains activation."""
    if ctx.get("used"):
        state.usage_count += 1
        state.activation += 0.1 * (1.0 - state.activation)
        state.energy += 0.05
    return state


def _L04_unused_decays(state: CognitiveState, ctx: Dict) -> CognitiveState:
    """Unused knowledge slowly decays activation."""
    hours_idle = ctx.get("hours_since_use", 0)
    if hours_idle > 1:
        decay_rate = 0.02 * math.log1p(hours_idle)
        state.activation -= decay_rate * state.activation
        state.novelty -= 0.01
    return state


def _L05_reflection_deepens(state: CognitiveState, ctx: Dict) -> CognitiveState:
    """Reflection increases understanding and learning value."""
    if ctx.get("reflected"):
        state.reflection_count += 1
        state.learning_value += 0.08 * (1.0 - state.learning_value)
        state.stability += 0.02
        state.entropy -= 0.03
    return state


def _L06_connection_reinforces(state: CognitiveState, ctx: Dict) -> CognitiveState:
    """Connected ideas reinforce one another."""
    connections = ctx.get("active_connections", 0)
    if connections > 0:
        reinforcement = 0.02 * min(connections, 5)
        state.activation += reinforcement
        state.importance += 0.01 * connections
    return state


def _L07_goals_attract_attention(state: CognitiveState, ctx: Dict) -> CognitiveState:
    """Important goals naturally gain attention/activation."""
    if ctx.get("is_active_goal"):
        priority = ctx.get("goal_priority", 0)
        state.importance = max(state.importance, priority / 10.0)
        state.activation = max(state.activation, 0.3 + priority * 0.05)
    return state


def _L08_weak_retires(state: CognitiveState, ctx: Dict) -> CognitiveState:
    """Weak principles gradually retire."""
    if ctx.get("is_principle") and state.confidence < 0.2:
        state.activation *= 0.9
        state.importance *= 0.9
        if state.confidence < 0.1:
            state.stability = 0.0  # Ready for retirement
    return state


def _L09_novelty_sparks_curiosity(state: CognitiveState, ctx: Dict) -> CognitiveState:
    """New observations increase curiosity (activation + novelty)."""
    if ctx.get("is_new"):
        state.novelty = 1.0
        state.activation += 0.3
        state.entropy += 0.1  # New things add uncertainty
    return state


def _L10_curiosity_creates_goals(state: CognitiveState, ctx: Dict) -> CognitiveState:
    """High curiosity (novelty + entropy) promotes to importance."""
    curiosity = state.novelty * 0.5 + state.entropy * 0.3
    if curiosity > 0.5 and state.importance < 0.3:
        state.importance += 0.05
    return state


def _L11_energy_conservation(state: CognitiveState, ctx: Dict) -> CognitiveState:
    """Total energy dissipates — processing costs energy."""
    if ctx.get("processed"):
        state.energy -= 0.02  # Processing costs
    # Natural energy recovery
    state.energy += 0.005
    return state


def _L12_stability_resists_change(state: CognitiveState, ctx: Dict) -> CognitiveState:
    """Stable nodes resist state changes (inertia)."""
    # Applied as a modifier to other laws' effects
    # High stability = slower changes
    if state.stability > 0.8:
        # Dampen any recent changes
        state.activation = state.activation * 0.95 + ctx.get("prev_activation", state.activation) * 0.05
    return state


def _L13_age_stabilizes(state: CognitiveState, ctx: Dict) -> CognitiveState:
    """Older knowledge gains stability (unless contradicted)."""
    age_days = state.age / 86400
    if age_days > 7 and state.confidence > 0.5:
        state.stability = min(0.9, state.stability + 0.001 * age_days)
    return state


def _L14_success_energizes(state: CognitiveState, ctx: Dict) -> CognitiveState:
    """Successful use of knowledge adds energy."""
    if ctx.get("used_successfully"):
        state.energy += 0.1
        state.confidence += 0.02
    return state


def _L15_failure_teaches(state: CognitiveState, ctx: Dict) -> CognitiveState:
    """Failures increase learning value but decrease confidence."""
    if ctx.get("used_and_failed"):
        state.learning_value += 0.15
        state.confidence -= 0.05
        state.entropy += 0.1
    return state


def _L16_entropy_seeks_resolution(state: CognitiveState, ctx: Dict) -> CognitiveState:
    """High entropy nodes attract attention (need resolution)."""
    if state.entropy > 0.7:
        state.importance += 0.05
        state.activation += 0.03
    return state


def _L17_learning_reduces_entropy(state: CognitiveState, ctx: Dict) -> CognitiveState:
    """Learning value accumulated reduces entropy."""
    if state.learning_value > 0.3:
        reduction = state.learning_value * 0.02
        state.entropy -= reduction
    return state


def _L18_reflection_accuracy_improves(state: CognitiveState, ctx: Dict) -> CognitiveState:
    """Multiple reflections improve prediction accuracy."""
    if state.reflection_count > 3:
        improvement = 0.01 * min(state.reflection_count, 10)
        state.prediction_accuracy += improvement * (1.0 - state.prediction_accuracy)
    return state


def _L19_importance_propagates_up(state: CognitiveState, ctx: Dict) -> CognitiveState:
    """Child importance propagates to parent nodes."""
    child_importance = ctx.get("max_child_importance", 0)
    if child_importance > state.importance:
        state.importance = state.importance * 0.7 + child_importance * 0.3
    return state


def _L20_dormancy_threshold(state: CognitiveState, ctx: Dict) -> CognitiveState:
    """Nodes below activation threshold enter dormancy."""
    if state.activation < 0.02 and state.importance < 0.1:
        state.activation = 0.0
        state.energy = max(0.0, state.energy - 0.01)
    return state


def _L21_activation_ceiling(state: CognitiveState, ctx: Dict) -> CognitiveState:
    """No node can exceed activation of 1.0 (conservation)."""
    if state.activation > 1.0:
        overflow = state.activation - 1.0
        state.activation = 1.0
        state.energy += overflow * 0.5  # Overflow converts to energy
    return state


def _L22_confidence_requires_evidence(state: CognitiveState, ctx: Dict) -> CognitiveState:
    """Confidence cannot exceed evidence level."""
    evidence = ctx.get("supporting_evidence_count", 0)
    max_conf = min(1.0, 0.3 + evidence * 0.1)
    if state.confidence > max_conf and state.stability < 0.9:
        state.confidence = state.confidence * 0.95 + max_conf * 0.05
    return state


def _L23_novelty_decays_naturally(state: CognitiveState, ctx: Dict) -> CognitiveState:
    """Novelty always decays toward zero over time."""
    decay_rate = 0.01  # Per cycle
    state.novelty *= (1.0 - decay_rate)
    return state


def _L24_usage_builds_stability(state: CognitiveState, ctx: Dict) -> CognitiveState:
    """Repeated successful usage builds stability."""
    if state.usage_count > 5 and state.prediction_accuracy > 0.6:
        state.stability = min(0.9, state.stability + 0.005)
    return state


def _L25_connected_knowledge_survives(state: CognitiveState, ctx: Dict) -> CognitiveState:
    """Well-connected knowledge resists decay better."""
    connections = ctx.get("total_connections", 0)
    if connections > 3:
        # Connected nodes decay slower
        state.stability += 0.002 * min(connections, 10)
    return state


# ═══════════════════════════════════════════════════════════════
# LAW REGISTRY
# ═══════════════════════════════════════════════════════════════

COGNITIVE_LAWS: Dict[str, CognitiveLaw] = {
    "L01": CognitiveLaw("L01", "Prediction Success", "Successful predictions increase confidence", "reinforcement", _L01_prediction_success),
    "L02": CognitiveLaw("L02", "Contradiction Weakens", "Contradictions decrease confidence", "decay", _L02_contradiction_weakens),
    "L03": CognitiveLaw("L03", "Usage Activates", "Frequently used knowledge gains activation", "reinforcement", _L03_usage_activates),
    "L04": CognitiveLaw("L04", "Unused Decays", "Unused knowledge slowly decays", "decay", _L04_unused_decays),
    "L05": CognitiveLaw("L05", "Reflection Deepens", "Reflection increases understanding", "meta", _L05_reflection_deepens),
    "L06": CognitiveLaw("L06", "Connection Reinforces", "Connected ideas reinforce one another", "spreading", _L06_connection_reinforces),
    "L07": CognitiveLaw("L07", "Goals Attract", "Important goals naturally gain attention", "reinforcement", _L07_goals_attract_attention),
    "L08": CognitiveLaw("L08", "Weak Retires", "Weak principles gradually retire", "decay", _L08_weak_retires),
    "L09": CognitiveLaw("L09", "Novelty Sparks", "New observations increase curiosity", "emergence", _L09_novelty_sparks_curiosity),
    "L10": CognitiveLaw("L10", "Curiosity Creates Goals", "Curiosity promotes to importance", "emergence", _L10_curiosity_creates_goals),
    "L11": CognitiveLaw("L11", "Energy Conservation", "Processing costs energy", "decay", _L11_energy_conservation),
    "L12": CognitiveLaw("L12", "Stability Resists", "Stable nodes resist state changes", "meta", _L12_stability_resists_change),
    "L13": CognitiveLaw("L13", "Age Stabilizes", "Older knowledge gains stability", "reinforcement", _L13_age_stabilizes),
    "L14": CognitiveLaw("L14", "Success Energizes", "Successful use adds energy", "reinforcement", _L14_success_energizes),
    "L15": CognitiveLaw("L15", "Failure Teaches", "Failures increase learning value", "meta", _L15_failure_teaches),
    "L16": CognitiveLaw("L16", "Entropy Seeks Resolution", "High entropy attracts attention", "emergence", _L16_entropy_seeks_resolution),
    "L17": CognitiveLaw("L17", "Learning Reduces Entropy", "Learning accumulated reduces entropy", "meta", _L17_learning_reduces_entropy),
    "L18": CognitiveLaw("L18", "Reflection Improves Accuracy", "Multiple reflections improve predictions", "meta", _L18_reflection_accuracy_improves),
    "L19": CognitiveLaw("L19", "Importance Propagates Up", "Child importance propagates to parents", "spreading", _L19_importance_propagates_up),
    "L20": CognitiveLaw("L20", "Dormancy Threshold", "Low activation + low importance = dormant", "decay", _L20_dormancy_threshold),
    "L21": CognitiveLaw("L21", "Activation Ceiling", "Activation cannot exceed 1.0", "meta", _L21_activation_ceiling),
    "L22": CognitiveLaw("L22", "Confidence Requires Evidence", "Confidence bounded by evidence", "meta", _L22_confidence_requires_evidence),
    "L23": CognitiveLaw("L23", "Novelty Decays", "Novelty always fades toward zero", "decay", _L23_novelty_decays_naturally),
    "L24": CognitiveLaw("L24", "Usage Builds Stability", "Repeated success builds stability", "reinforcement", _L24_usage_builds_stability),
    "L25": CognitiveLaw("L25", "Connected Survives", "Well-connected knowledge resists decay", "reinforcement", _L25_connected_knowledge_survives),
}


def get_laws_by_category(category: str) -> Dict[str, CognitiveLaw]:
    """Get all laws in a category."""
    return {k: v for k, v in COGNITIVE_LAWS.items() if v.category == category}


def get_all_laws() -> Dict[str, CognitiveLaw]:
    """Get all cognitive laws."""
    return COGNITIVE_LAWS
