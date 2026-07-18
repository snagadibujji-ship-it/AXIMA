"""
AXIMA Reflection Engine — Post-execution analysis creating permanent knowledge.

After every execution, reflection asks:
  - What happened?
  - Was prediction correct?
  - What failed?
  - What succeeded?
  - What surprised us?
  - What should change?

Reflection becomes permanent knowledge. Never discard lessons.

Usage:
    from core.reflection import ReflectionEngine, get_reflection

    engine = get_reflection()
    reflection = engine.reflect(observation, prediction, result)
    # reflection.lessons, reflection.surprises, reflection.prediction_accuracy
"""

import time
from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any

from core.reality_graph import get_reality_graph, RealityGraph
from core.observer import Observation
from core.prediction import Prediction


# ═══════════════════════════════════════════════════════════════
# REFLECTION DATA
# ═══════════════════════════════════════════════════════════════

@dataclass
class Lesson:
    """A lesson learned from reflection."""
    content: str
    lesson_type: str = "observation"    # observation, correction, insight, warning
    domain: str = ""
    confidence: float = 0.7
    source_interaction: str = ""


@dataclass
class Reflection:
    """Complete reflection on an interaction."""
    timestamp: float = 0.0

    # What happened
    action_taken: str = ""
    outcome: str = ""                   # success, partial, failure
    engine_used: str = ""

    # Prediction analysis
    had_prediction: bool = False
    prediction_was_correct: bool = False
    prediction_error: float = 0.0       # How far off

    # Lessons
    lessons: List[Lesson] = field(default_factory=list)
    surprises: List[str] = field(default_factory=list)
    failures: List[str] = field(default_factory=list)
    successes: List[str] = field(default_factory=list)

    # Recommendations
    should_change: List[str] = field(default_factory=list)

    def __post_init__(self):
        if not self.timestamp:
            self.timestamp = time.time()

    def summary(self) -> Dict[str, Any]:
        return {
            "outcome": self.outcome,
            "prediction_correct": self.prediction_was_correct if self.had_prediction else None,
            "lessons": len(self.lessons),
            "surprises": len(self.surprises),
            "changes_recommended": len(self.should_change),
        }


# ═══════════════════════════════════════════════════════════════
# REFLECTION ENGINE
# ═══════════════════════════════════════════════════════════════

class ReflectionEngine:
    """Post-execution analysis that creates permanent knowledge.
    
    Reflection is what turns experience into wisdom.
    Every interaction leaves a trace that improves future behavior.
    """

    def __init__(self, graph: Optional[RealityGraph] = None):
        self._graph = graph or get_reality_graph()
        self._history: List[Reflection] = []

    def reflect(self, observation: Observation,
                prediction: Optional[Prediction] = None,
                result_status: str = "success",
                result_engine: str = "",
                result_answer: str = "") -> Reflection:
        """Reflect on a completed interaction.
        
        Called after every execution to analyze what happened
        and extract lessons for the future.
        """
        ref = Reflection(
            action_taken=observation.raw_input[:200],
            outcome=result_status,
            engine_used=result_engine,
        )

        # Analyze prediction accuracy
        if prediction:
            ref.had_prediction = True
            ref.prediction_was_correct = self._check_prediction(prediction, result_status)
            ref.prediction_error = self._prediction_error(prediction, result_status)

        # Detect successes
        ref.successes = self._detect_successes(result_status, result_answer)

        # Detect failures
        ref.failures = self._detect_failures(result_status, result_answer, observation)

        # Detect surprises
        ref.surprises = self._detect_surprises(prediction, result_status, result_engine)

        # Extract lessons
        ref.lessons = self._extract_lessons(ref, observation)

        # Recommend changes
        ref.should_change = self._recommend_changes(ref)

        # Store reflection as permanent knowledge
        self._persist_reflection(ref)

        # Track history
        self._history.append(ref)
        if len(self._history) > 100:
            self._history = self._history[-100:]

        return ref

    def recent_lessons(self, n: int = 10) -> List[Lesson]:
        """Get recent lessons learned."""
        all_lessons = []
        for ref in reversed(self._history):
            all_lessons.extend(ref.lessons)
            if len(all_lessons) >= n:
                break
        return all_lessons[:n]

    def prediction_accuracy(self) -> float:
        """Overall prediction accuracy from reflection history."""
        predictions = [r for r in self._history if r.had_prediction]
        if not predictions:
            return 0.0
        correct = sum(1 for r in predictions if r.prediction_was_correct)
        return correct / len(predictions)

    def common_failures(self) -> Dict[str, int]:
        """Most common failure patterns."""
        failures = {}
        for ref in self._history:
            for f in ref.failures:
                key = f[:50]
                failures[key] = failures.get(key, 0) + 1
        return dict(sorted(failures.items(), key=lambda x: -x[1])[:10])

    def stats(self) -> Dict[str, Any]:
        """Reflection statistics."""
        total = len(self._history)
        if not total:
            return {"total_reflections": 0}
        successes = sum(1 for r in self._history if r.outcome == "success")
        return {
            "total_reflections": total,
            "success_rate": successes / total,
            "prediction_accuracy": self.prediction_accuracy(),
            "total_lessons": sum(len(r.lessons) for r in self._history),
            "total_surprises": sum(len(r.surprises) for r in self._history),
        }

    # ─── Internal ───

    def _check_prediction(self, prediction: Prediction, outcome: str) -> bool:
        """Was the prediction correct?"""
        if outcome == "success" and prediction.success_probability > 0.5:
            return True
        if outcome in ("failure", "error") and prediction.success_probability < 0.5:
            return True
        return False

    def _prediction_error(self, prediction: Prediction, outcome: str) -> float:
        """How far off was the prediction?"""
        actual = 1.0 if outcome == "success" else 0.0
        return abs(prediction.success_probability - actual)

    def _detect_successes(self, status: str, answer: str) -> List[str]:
        """What went well?"""
        successes = []
        if status == "success":
            successes.append("Query answered successfully")
            if answer and len(answer) > 50:
                successes.append("Produced detailed response")
        return successes

    def _detect_failures(self, status: str, answer: str, obs: Observation) -> List[str]:
        """What went wrong?"""
        failures = []
        if status in ("error", "no_answer"):
            failures.append(f"Failed to answer: {obs.topic or obs.raw_input[:50]}")
        if status == "partial":
            failures.append("Only partial answer produced")
        return failures

    def _detect_surprises(self, prediction: Optional[Prediction],
                          status: str, engine: str) -> List[str]:
        """What was unexpected?"""
        surprises = []
        if prediction:
            if prediction.success_probability > 0.8 and status != "success":
                surprises.append(f"Expected success ({prediction.success_probability:.0%}) but got {status}")
            if prediction.success_probability < 0.3 and status == "success":
                surprises.append(f"Unexpected success (predicted {prediction.success_probability:.0%})")
        return surprises

    def _extract_lessons(self, ref: Reflection, obs: Observation) -> List[Lesson]:
        """Extract reusable lessons from this interaction."""
        lessons = []

        # Lesson from failures
        for failure in ref.failures:
            lessons.append(Lesson(
                content=f"Failed: {failure}",
                lesson_type="warning",
                domain=obs.topic,
                confidence=0.8,
            ))

        # Lesson from surprises
        for surprise in ref.surprises:
            lessons.append(Lesson(
                content=surprise,
                lesson_type="insight",
                domain=obs.topic,
                confidence=0.6,
            ))

        # Lesson from prediction errors
        if ref.had_prediction and not ref.prediction_was_correct:
            lessons.append(Lesson(
                content=f"Prediction error ({ref.prediction_error:.0%}) for '{obs.topic}' — adjust model",
                lesson_type="correction",
                domain=obs.topic,
                confidence=0.7,
            ))

        return lessons

    def _recommend_changes(self, ref: Reflection) -> List[str]:
        """What should change based on this reflection?"""
        changes = []
        if ref.failures:
            changes.append("Investigate failure root cause")
        if ref.prediction_error > 0.5:
            changes.append("Recalibrate prediction model")
        if ref.surprises:
            changes.append("Update understanding with new evidence")
        return changes

    def _persist_reflection(self, ref: Reflection):
        """Store key lessons in the Reality Graph as permanent knowledge."""
        for lesson in ref.lessons:
            if lesson.confidence >= 0.6:
                self._graph.add_node("memory", lesson.content[:80], {
                    "memory_type": "lesson",
                    "lesson_type": lesson.lesson_type,
                    "domain": lesson.domain,
                    "confidence": lesson.confidence,
                    "source": ref.action_taken[:100],
                    "created_at": time.time(),
                })
        if ref.lessons:
            self._graph.save()


# ═══════════════════════════════════════════════════════════════
# SINGLETON
# ═══════════════════════════════════════════════════════════════

_reflection: Optional[ReflectionEngine] = None

def get_reflection(graph: Optional[RealityGraph] = None) -> ReflectionEngine:
    """Get the global reflection engine."""
    global _reflection
    if _reflection is None:
        _reflection = ReflectionEngine(graph=graph)
    return _reflection
