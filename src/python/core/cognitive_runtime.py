"""
AXIMA Cognitive Runtime — The heartbeat of the cognitive operating system.

This is not a request/response system. This is a continuously thinking mind.

The Cognitive Loop:
    Observe → Understand → Update Reality → Select Attention → Predict →
    Plan → Execute → Reflect → Learn → Update Understanding → Repeat

Every interaction flows through this loop. The system's internal state
evolves with every interaction.

Usage:
    from core.cognitive_runtime import CognitiveRuntime, get_runtime

    runtime = get_runtime()
    response = runtime.think("fix the math router")
    
    # The runtime has:
    # - Observed the input
    # - Updated the reality graph
    # - Focused attention
    # - Made predictions
    # - Planned actions
    # - Executed via plugins
    # - Reflected on the outcome
    # - Learned from the experience
"""

import time
from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any

from core.reality_graph import get_reality_graph, RealityGraph
from core.observer import Observer, Observation
from core.reality_sync import RealitySynchronizer, SyncResult
from core.attention import AttentionSystem, AttentionScore
from core.prediction import PredictionEngine, Prediction
from core.planner import Planner, Plan
from core.reflection import ReflectionEngine, Reflection
from core.evolution import UnderstandingEvolution
from core.contradiction import ContradictionEngine
from core.curiosity import CuriosityEngine


# ═══════════════════════════════════════════════════════════════
# COGNITIVE STATE
# ═══════════════════════════════════════════════════════════════

@dataclass
class CognitiveState:
    """Snapshot of the runtime's cognitive state after one cycle."""
    timestamp: float = 0.0
    cycle_number: int = 0

    # What was perceived
    observation: Optional[Observation] = None

    # What changed in reality
    sync_result: Optional[SyncResult] = None

    # What has attention
    focus: Optional[AttentionScore] = None
    active_count: int = 0

    # What we predict
    predictions: List[Dict[str, Any]] = field(default_factory=list)

    # What we plan
    plan: Optional[Plan] = None

    # What we produced
    response: str = ""
    response_engine: str = ""
    response_status: str = ""

    # What we learned
    reflection: Optional[Reflection] = None

    # Meta
    total_latency_ms: float = 0.0

    def summary(self) -> Dict[str, Any]:
        return {
            "cycle": self.cycle_number,
            "intent": self.observation.intent if self.observation else "",
            "topic": self.observation.topic if self.observation else "",
            "reality_changes": self.sync_result.total_changes if self.sync_result else 0,
            "focus": self.focus.label if self.focus else "",
            "response_engine": self.response_engine,
            "outcome": self.response_status,
            "lessons_learned": len(self.reflection.lessons) if self.reflection else 0,
            "latency_ms": round(self.total_latency_ms, 1),
        }


# ═══════════════════════════════════════════════════════════════
# COGNITIVE RUNTIME
# ═══════════════════════════════════════════════════════════════

class CognitiveRuntime:
    """The AXIMA Cognitive Runtime — orchestrates all subsystems.
    
    This replaces the simple request → route → respond pattern.
    Every interaction flows through a full cognitive loop that
    perceives, reasons, acts, and learns.
    """

    def __init__(self, graph: Optional[RealityGraph] = None):
        # Foundation
        self._graph = graph or get_reality_graph()

        # Cognitive subsystems
        self._observer = Observer()
        self._sync = RealitySynchronizer(self._graph)
        self._attention = AttentionSystem(self._graph)
        self._predictions = PredictionEngine(self._graph)
        self._planner = Planner(self._graph, self._attention, self._predictions)
        self._reflection = ReflectionEngine(self._graph)
        self._evolution = UnderstandingEvolution(self._graph)
        self._contradiction = ContradictionEngine(self._graph)
        self._curiosity = CuriosityEngine(self._graph)

        # State
        self._cycle_count = 0
        self._history: List[CognitiveState] = []
        self._started_at = time.time()

    def think(self, input_text: str, execute_fn=None) -> CognitiveState:
        """Run one full cognitive cycle.
        
        This is the heartbeat. Every interaction passes through here.
        
        Args:
            input_text: User input or system trigger
            execute_fn: Optional function(query, intent) → (answer, engine, status)
                        If not provided, execution step is skipped.
        
        Returns:
            CognitiveState — complete snapshot of what happened
        """
        start = time.time()
        self._cycle_count += 1
        state = CognitiveState(
            timestamp=start,
            cycle_number=self._cycle_count,
        )

        # ── STAGE 1: OBSERVE ──
        state.observation = self._observe(input_text)

        # ── STAGE 2: UPDATE REALITY ──
        state.sync_result = self._update_reality(state.observation)

        # ── STAGE 3: SELECT ATTENTION ──
        state.focus, state.active_count = self._select_attention()

        # ── STAGE 4: PREDICT ──
        state.predictions = self._predict()

        # ── STAGE 5: PLAN ──
        state.plan = self._plan()

        # ── STAGE 6: EXECUTE ──
        if execute_fn:
            state.response, state.response_engine, state.response_status = (
                self._execute(input_text, state.observation, execute_fn)
            )
        else:
            state.response_status = "skipped"

        # ── STAGE 7: REFLECT ──
        # Find relevant prediction for this interaction
        relevant_pred = None
        if state.predictions:
            relevant_pred = Prediction(
                target_id="interaction",
                success_probability=0.7,  # Default expectation
            )

        state.reflection = self._reflect(
            state.observation,
            relevant_pred,
            state.response_status,
            state.response_engine,
            state.response,
        )

        # ── STAGE 8: EVOLVE UNDERSTANDING ──
        self._evolve(state)

        # Finalize
        state.total_latency_ms = (time.time() - start) * 1000

        # Store in history
        self._history.append(state)
        if len(self._history) > 100:
            self._history = self._history[-100:]

        return state

    def idle_think(self) -> Dict[str, Any]:
        """Idle cognition — what the system does when not processing a request.
        
        This is autonomous background thinking:
        - Curiosity finds gaps
        - Evolution strengthens knowledge
        - Contradictions get flagged
        """
        results = {
            "gaps_found": 0,
            "research_tasks": 0,
            "weak_retired": 0,
            "cross_links": 0,
        }

        # Curiosity: find knowledge gaps
        gaps = self._curiosity.find_gaps()
        results["gaps_found"] = len(gaps)

        # Generate research tasks from gaps
        tasks = self._curiosity.generate_research_tasks(limit=3)
        results["research_tasks"] = len(tasks)

        # For each task, create it in the goal system
        for task in tasks:
            # Check if similar task already exists
            existing = self._graph.find_nodes(node_type="task", label_contains=task.question[:30])
            if not existing:
                self._graph.add_node("task", task.question[:80], {
                    "status": "active",
                    "source": "curiosity",
                    "priority": int(task.priority * 5),
                    "gap_type": task.gap_type,
                    "created_at": time.time(),
                })

        # Retire weak principles
        retired = self._evolution.retire_weak_principles(threshold=0.15)
        results["weak_retired"] = len(retired)

        # Find cross-domain links
        links = self._evolution.find_cross_domain_links()
        results["cross_links"] = len(links)
        for link in links[:5]:  # Create top 5 links
            self._evolution.create_cross_domain_edge(
                link["concept1"]["id"],
                link["concept2"]["id"],
                reason=f"Structural analogy (sim={link['similarity']:.2f})"
            )

        # Decay attention (natural forgetting of focus)
        self._attention.decay(rate=0.02)

        self._graph.save()
        return results

    # ─── Cognitive Stages ───

    def _observe(self, text: str) -> Observation:
        """Stage 1: Perceive and understand input."""
        return self._observer.observe(text)

    def _update_reality(self, observation: Observation) -> SyncResult:
        """Stage 2: Synchronize observations into Reality Graph."""
        return self._sync.synchronize(observation)

    def _select_attention(self) -> tuple:
        """Stage 3: Determine cognitive focus."""
        self._attention.update_scores()
        focus = self._attention.current_focus()
        active = self._attention.active_nodes(limit=10)
        return focus, len(active)

    def _predict(self) -> List[Dict[str, Any]]:
        """Stage 4: Update predictions."""
        self._predictions.update_all()
        preds = self._predictions.all_predictions()
        return [
            {
                "goal": p.target_label,
                "success": round(p.success_probability, 2),
                "risk": round(p.risk_level, 2),
                "trend": p.trend,
            }
            for p in preds[:5]
        ]

    def _plan(self) -> Plan:
        """Stage 5: Determine what to do next."""
        return self._planner.plan_next()

    def _execute(self, text: str, observation: Observation, execute_fn) -> tuple:
        """Stage 6: Execute using provided function."""
        try:
            answer, engine, status = execute_fn(text, observation.intent)
            return (answer or "", engine or "unknown", status or "success")
        except Exception as e:
            return ("", "error", f"error: {e}")

    def _reflect(self, observation: Observation,
                 prediction: Optional[Prediction],
                 status: str, engine: str, answer: str) -> Reflection:
        """Stage 7: Reflect on what happened."""
        return self._reflection.reflect(
            observation=observation,
            prediction=prediction,
            result_status=status,
            result_engine=engine,
            result_answer=answer,
        )

    def _evolve(self, state: CognitiveState):
        """Stage 8: Evolve understanding based on this cycle."""
        # If contradictions were found, flag them
        if state.sync_result and state.sync_result.has_contradictions:
            for c in state.sync_result.contradictions:
                self._attention.boost(c.get("existing_id", ""), "urgency", 0.3)

        # If we learned something new, boost novelty
        if state.sync_result and state.sync_result.created_nodes:
            for node_info in state.sync_result.created_nodes:
                self._attention.boost(node_info["id"], "novelty", 0.5)

    # ─── Query State ───

    @property
    def cycle_count(self) -> int:
        return self._cycle_count

    def current_state(self) -> Dict[str, Any]:
        """Get current cognitive state summary."""
        focus = self._attention.current_focus()
        return {
            "cycles": self._cycle_count,
            "uptime_seconds": time.time() - self._started_at,
            "focus": focus.label if focus else "none",
            "active_nodes": len(self._attention.active_nodes()),
            "predictions": len(self._predictions.all_predictions()),
            "reflection_accuracy": self._reflection.prediction_accuracy(),
            "curiosity_score": self._curiosity.curiosity_score(),
            "graph_nodes": self._graph.stats()["nodes"],
            "graph_edges": self._graph.stats()["edges"],
        }

    def recent_history(self, n: int = 5) -> List[Dict[str, Any]]:
        """Get summaries of recent cognitive cycles."""
        return [s.summary() for s in self._history[-n:]]


# ═══════════════════════════════════════════════════════════════
# SINGLETON
# ═══════════════════════════════════════════════════════════════

_runtime: Optional[CognitiveRuntime] = None

def get_runtime(graph: Optional[RealityGraph] = None) -> CognitiveRuntime:
    """Get the global cognitive runtime."""
    global _runtime
    if _runtime is None:
        _runtime = CognitiveRuntime(graph=graph)
    return _runtime
