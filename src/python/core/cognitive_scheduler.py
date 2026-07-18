"""
AXIMA Cognitive Scheduler — Optimize what thinks when.

Decides:
  - What should think now? (high activation + importance)
  - What can wait? (low urgency, stable)
  - What deserves immediate attention? (contradictions, blockers)
  - What should consolidate later? (dormant but valuable)

Optimizes: latency, memory, energy, reasoning quality.
"""

import time
from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any

from core.reality_graph import get_reality_graph, RealityGraph
from core.cognitive_state import get_state


@dataclass
class ScheduleEntry:
    """A scheduled cognitive task."""
    task_type: str          # physics_tick, spreading, consolidation, decay, reflection, curiosity
    priority: float = 0.5
    last_run: float = 0.0
    interval_seconds: float = 1.0   # Minimum time between runs
    estimated_cost_ms: float = 10.0  # Expected latency


class CognitiveScheduler:
    """Decides what cognitive processes run and when."""

    def __init__(self, graph: Optional[RealityGraph] = None,
                 budget_ms: float = 50.0):
        self._graph = graph or get_reality_graph()
        self._budget_ms = budget_ms  # Max time per scheduling cycle
        self._schedule: Dict[str, ScheduleEntry] = {
            "physics_tick": ScheduleEntry("physics_tick", priority=0.9, interval_seconds=0.5, estimated_cost_ms=15),
            "activation_spreading": ScheduleEntry("activation_spreading", priority=0.7, interval_seconds=1.0, estimated_cost_ms=10),
            "memory_consolidation": ScheduleEntry("memory_consolidation", priority=0.4, interval_seconds=5.0, estimated_cost_ms=20),
            "knowledge_decay": ScheduleEntry("knowledge_decay", priority=0.3, interval_seconds=10.0, estimated_cost_ms=10),
            "principle_evolution": ScheduleEntry("principle_evolution", priority=0.3, interval_seconds=10.0, estimated_cost_ms=15),
            "self_metrics": ScheduleEntry("self_metrics", priority=0.2, interval_seconds=30.0, estimated_cost_ms=10),
            "curiosity": ScheduleEntry("curiosity", priority=0.2, interval_seconds=30.0, estimated_cost_ms=20),
        }

    def what_runs_now(self) -> List[str]:
        """Determine which cognitive processes should run this cycle.
        
        Returns list of task_types to execute, sorted by priority,
        constrained by budget.
        """
        now = time.time()
        ready = []

        for name, entry in self._schedule.items():
            time_since = now - entry.last_run
            if time_since >= entry.interval_seconds:
                # Urgency increases with overdue time
                overdue_factor = min(2.0, time_since / entry.interval_seconds)
                effective_priority = entry.priority * overdue_factor
                ready.append((name, effective_priority, entry.estimated_cost_ms))

        # Sort by priority descending
        ready.sort(key=lambda x: -x[1])

        # Fill budget
        selected = []
        remaining_budget = self._budget_ms
        for name, priority, cost in ready:
            if cost <= remaining_budget:
                selected.append(name)
                remaining_budget -= cost

        return selected

    def mark_completed(self, task_type: str, actual_ms: float = 0.0):
        """Mark a scheduled task as completed."""
        if task_type in self._schedule:
            entry = self._schedule[task_type]
            entry.last_run = time.time()
            # Adapt cost estimate with exponential moving average
            if actual_ms > 0:
                entry.estimated_cost_ms = entry.estimated_cost_ms * 0.8 + actual_ms * 0.2

    def set_budget(self, budget_ms: float):
        """Adjust the scheduling budget."""
        self._budget_ms = budget_ms

    def boost_priority(self, task_type: str, amount: float = 0.2):
        """Temporarily boost a task's priority."""
        if task_type in self._schedule:
            self._schedule[task_type].priority = min(1.0, self._schedule[task_type].priority + amount)

    def stats(self) -> Dict[str, Any]:
        """Scheduler statistics."""
        now = time.time()
        return {
            "budget_ms": self._budget_ms,
            "tasks": {
                name: {
                    "priority": entry.priority,
                    "overdue_s": round(now - entry.last_run - entry.interval_seconds, 1),
                    "cost_ms": round(entry.estimated_cost_ms, 1),
                }
                for name, entry in self._schedule.items()
            }
        }


_scheduler: Optional[CognitiveScheduler] = None
def get_scheduler(graph: Optional[RealityGraph] = None) -> CognitiveScheduler:
    global _scheduler
    if _scheduler is None:
        _scheduler = CognitiveScheduler(graph=graph)
    return _scheduler
