"""
AXIMA Planner — Converts predictions into actions via graph state.

Responsibilities:
  - Create tasks from goal analysis
  - Prioritize tasks using attention scores
  - Detect blockers from graph relationships
  - Recommend next action

Planning emerges from graph state — no hardcoded workflows.

Usage:
    from core.planner import Planner, get_planner

    planner = get_planner()
    plan = planner.plan_next()
    # plan.recommended_action, plan.priority_tasks, plan.blockers
"""

import time
from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any

from core.reality_graph import get_reality_graph, RealityGraph
from core.attention import get_attention, AttentionSystem
from core.prediction import get_predictions, PredictionEngine


# ═══════════════════════════════════════════════════════════════
# PLAN OUTPUT
# ═══════════════════════════════════════════════════════════════

@dataclass
class Action:
    """A recommended action."""
    description: str
    action_type: str = "execute"    # execute, investigate, unblock, create, wait
    target_id: str = ""             # Node this action targets
    priority: float = 0.5           # 0=low, 1=critical
    reason: str = ""                # Why this action


@dataclass
class Plan:
    """The planner's output — what to do next."""
    recommended_action: Optional[Action] = None
    priority_tasks: List[Action] = field(default_factory=list)
    blockers: List[Dict[str, str]] = field(default_factory=list)
    observations: List[str] = field(default_factory=list)    # Planning notes
    timestamp: float = 0.0

    def __post_init__(self):
        if not self.timestamp:
            self.timestamp = time.time()

    @property
    def has_blockers(self) -> bool:
        return len(self.blockers) > 0

    def summary(self) -> Dict[str, Any]:
        return {
            "recommended": self.recommended_action.description if self.recommended_action else None,
            "priority_tasks": len(self.priority_tasks),
            "blockers": len(self.blockers),
            "observations": self.observations,
        }


# ═══════════════════════════════════════════════════════════════
# PLANNER
# ═══════════════════════════════════════════════════════════════

class Planner:
    """Converts graph state + predictions into actionable plans.
    
    Planning emerges from the current state of:
    - Reality Graph (what we know)
    - Attention System (what matters)
    - Prediction Engine (what we expect)
    """

    def __init__(self, graph: Optional[RealityGraph] = None,
                 attention: Optional[AttentionSystem] = None,
                 predictions: Optional[PredictionEngine] = None):
        self._graph = graph or get_reality_graph()
        self._attention = attention or get_attention(self._graph)
        self._predictions = predictions or get_predictions(self._graph)

    def plan_next(self) -> Plan:
        """Generate a plan based on current state.
        
        This is the primary planning function.
        Returns what AXIMA should focus on next.
        """
        plan = Plan()

        # Refresh state
        self._attention.update_scores()
        self._predictions.update_all()

        # Find blockers
        plan.blockers = self._find_all_blockers()

        # Generate priority tasks
        plan.priority_tasks = self._prioritize_tasks()

        # Determine recommended action
        plan.recommended_action = self._recommend_action(plan)

        # Add observations
        plan.observations = self._generate_observations(plan)

        return plan

    def plan_for_goal(self, goal_id: str) -> Plan:
        """Generate a plan specific to a goal."""
        plan = Plan()
        goal = self._graph.get_node(goal_id)
        if not goal:
            plan.observations.append(f"Goal {goal_id} not found")
            return plan

        # Get children
        children = self._get_children(goal_id)
        active = [c for c in children if c.properties.get("status") == "active"]
        blocked = [c for c in children if c.properties.get("status") == "blocked"]

        # Blockers
        for b in blocked:
            reason = b.properties.get("block_reason", "Unknown")
            plan.blockers.append({"task": b.label, "reason": reason, "id": b.id})

        # Priority tasks from active children
        for task in active:
            plan.priority_tasks.append(Action(
                description=task.label,
                action_type="execute",
                target_id=task.id,
                priority=0.7,
                reason=f"Active task under '{goal.label}'",
            ))

        # If there are blockers, recommend unblocking
        if blocked:
            plan.recommended_action = Action(
                description=f"Unblock: {blocked[0].label}",
                action_type="unblock",
                target_id=blocked[0].id,
                priority=0.9,
                reason=blocked[0].properties.get("block_reason", "Task is blocked"),
            )
        elif active:
            plan.recommended_action = Action(
                description=active[0].label,
                action_type="execute",
                target_id=active[0].id,
                priority=0.7,
                reason="Next active task",
            )

        # Prediction insight
        pred = self._predictions.predict_goal(goal_id)
        if pred:
            plan.observations.append(
                f"Success probability: {pred.success_probability:.0%}, "
                f"Risk: {pred.risk_level:.0%}, "
                f"Est. {pred.estimated_turns} turns remaining"
            )

        return plan

    def create_tasks_for_goal(self, goal_id: str, task_descriptions: List[str]) -> List[str]:
        """Create tasks under a goal from descriptions. Returns task IDs."""
        task_ids = []
        for desc in task_descriptions:
            tid = self._graph.add_node("task", desc, {
                "status": "active",
                "detected_at": time.time(),
                "confidence": 0.8,
            })
            self._graph.add_edge(goal_id, tid, "contains")
            task_ids.append(tid)
        self._graph.save()
        return task_ids

    def detect_completed_goals(self) -> List[str]:
        """Find goals where all tasks are completed."""
        completed = []
        goals = self._graph.find_nodes(node_type="goal")
        for goal in goals:
            if goal.properties.get("status") != "active":
                continue
            children = self._get_children(goal.id)
            if children and all(c.properties.get("status") == "completed" for c in children):
                self._graph.update_node(goal.id, properties={
                    "status": "completed",
                    "progress": 1.0,
                    "completed_at": time.time(),
                })
                completed.append(goal.id)
        if completed:
            self._graph.save()
        return completed

    # ─── Internal ───

    def _find_all_blockers(self) -> List[Dict[str, str]]:
        """Find all blocked tasks across all goals."""
        blockers = []
        tasks = self._graph.find_nodes(node_type="task")
        for task in tasks:
            if task.properties.get("status") == "blocked":
                blockers.append({
                    "task": task.label,
                    "reason": task.properties.get("block_reason", "Unknown"),
                    "id": task.id,
                })
        return blockers

    def _prioritize_tasks(self) -> List[Action]:
        """Get prioritized list of actionable tasks."""
        actions = []
        active_nodes = self._attention.active_nodes(limit=15)

        for score in active_nodes:
            if score.node_type == "task":
                node = self._graph.get_node(score.node_id)
                if node and node.properties.get("status") == "active":
                    actions.append(Action(
                        description=node.label,
                        action_type="execute",
                        target_id=node.id,
                        priority=score.total,
                        reason=f"Attention score: {score.total:.2f}",
                    ))
            elif score.node_type == "goal":
                node = self._graph.get_node(score.node_id)
                if node and node.properties.get("status") == "active":
                    actions.append(Action(
                        description=f"Progress goal: {node.label}",
                        action_type="investigate",
                        target_id=node.id,
                        priority=score.total * 0.8,
                        reason=f"Active goal, attention: {score.total:.2f}",
                    ))

        actions.sort(key=lambda a: -a.priority)
        return actions[:10]

    def _recommend_action(self, plan: Plan) -> Optional[Action]:
        """Determine the single best next action."""
        # Priority: unblock > execute high-priority > investigate
        if plan.blockers:
            b = plan.blockers[0]
            return Action(
                description=f"Unblock: {b['task']}",
                action_type="unblock",
                target_id=b.get("id", ""),
                priority=0.95,
                reason=b["reason"],
            )
        if plan.priority_tasks:
            return plan.priority_tasks[0]
        return None

    def _generate_observations(self, plan: Plan) -> List[str]:
        """Generate planning observations/notes."""
        obs = []
        if plan.blockers:
            obs.append(f"{len(plan.blockers)} task(s) blocked")

        # Check high-risk predictions
        high_risk = self._predictions.high_risk()
        if high_risk:
            obs.append(f"{len(high_risk)} goal(s) at high risk")

        # Check for goals with no tasks
        goals = self._graph.find_nodes(node_type="goal")
        for goal in goals:
            if goal.properties.get("status") == "active":
                children = self._get_children(goal.id)
                if not children:
                    obs.append(f"Goal '{goal.label}' has no tasks — needs decomposition")

        return obs

    def _get_children(self, node_id: str) -> List:
        """Get child nodes via 'contains' edges."""
        children = []
        for child_id, rel, _ in self._graph.neighbors(node_id, relation="contains"):
            child = self._graph.get_node(child_id)
            if child:
                children.append(child)
        return children


# ═══════════════════════════════════════════════════════════════
# SINGLETON
# ═══════════════════════════════════════════════════════════════

_planner: Optional[Planner] = None

def get_planner(graph: Optional[RealityGraph] = None) -> Planner:
    """Get the global planner."""
    global _planner
    if _planner is None:
        _planner = Planner(graph=graph)
    return _planner
