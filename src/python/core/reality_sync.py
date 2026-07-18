"""
AXIMA Reality Synchronizer — Automatically updates Reality Graph from observations.

No manual synchronization required. The graph is always current.

Every observation flows through here:
  - New goals → create goal nodes
  - New facts → create fact nodes (with contradiction check)
  - New entities → create/update entity nodes
  - Task progress → update task status
  - New relationships → create edges

Usage:
    from core.reality_sync import RealitySynchronizer, get_reality_sync

    sync = get_reality_sync()
    changes = sync.synchronize(observation)
    # changes.created_nodes, changes.updated_nodes, changes.created_edges
"""

import time
from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any, Tuple

from core.reality_graph import get_reality_graph, RealityGraph
from core.observer import Observation, Entity, DetectedGoal, DetectedTask, DetectedFact, DetectedConcept


# ═══════════════════════════════════════════════════════════════
# SYNC RESULT
# ═══════════════════════════════════════════════════════════════

@dataclass
class SyncResult:
    """What changed in the Reality Graph after synchronization."""
    created_nodes: List[Dict[str, str]] = field(default_factory=list)   # [{id, type, label}]
    updated_nodes: List[Dict[str, str]] = field(default_factory=list)   # [{id, field, old, new}]
    created_edges: List[Dict[str, str]] = field(default_factory=list)   # [{source, target, relation}]
    contradictions: List[Dict[str, str]] = field(default_factory=list)  # [{existing, new, issue}]
    duplicates_merged: int = 0
    timestamp: float = 0.0

    def __post_init__(self):
        if not self.timestamp:
            self.timestamp = time.time()

    @property
    def total_changes(self) -> int:
        return len(self.created_nodes) + len(self.updated_nodes) + len(self.created_edges)

    @property
    def has_contradictions(self) -> bool:
        return len(self.contradictions) > 0

    def summary(self) -> Dict[str, Any]:
        return {
            "created": len(self.created_nodes),
            "updated": len(self.updated_nodes),
            "edges": len(self.created_edges),
            "contradictions": len(self.contradictions),
            "duplicates_merged": self.duplicates_merged,
        }


# ═══════════════════════════════════════════════════════════════
# REALITY SYNCHRONIZER
# ═══════════════════════════════════════════════════════════════

class RealitySynchronizer:
    """Automatically updates the Reality Graph from observations.
    
    This is the bridge between perception (Observer) and memory (Reality Graph).
    It ensures the graph always reflects current reality.
    """

    def __init__(self, graph: Optional[RealityGraph] = None):
        self._graph = graph or get_reality_graph()

    def synchronize(self, observation: Observation) -> SyncResult:
        """Synchronize an observation into the Reality Graph.
        
        This is the primary function. It processes all extracted
        elements and updates the graph accordingly.
        """
        result = SyncResult()

        # Record the observation itself as a session event
        self._record_session(observation, result)

        # Sync entities
        for entity in observation.entities:
            self._sync_entity(entity, result)

        # Sync goals
        for goal in observation.goals:
            self._sync_goal(goal, observation, result)

        # Sync tasks
        for task in observation.tasks:
            self._sync_task(task, result)

        # Sync facts (with duplicate/contradiction detection)
        for fact in observation.facts:
            self._sync_fact(fact, result)

        # Sync concepts
        for concept in observation.concepts:
            self._sync_concept(concept, result)

        # Create cross-references
        self._create_cross_references(observation, result)

        # Persist
        self._graph.save()

        return result

    def _record_session(self, obs: Observation, result: SyncResult):
        """Record this interaction as a session node."""
        # Create or update session node
        sessions = self._graph.find_nodes(node_type="session", label_contains="current")
        if sessions:
            self._graph.update_node(sessions[0].id, properties={
                "last_input": obs.raw_input[:200],
                "last_intent": obs.intent,
                "last_topic": obs.topic,
                "turn_count": sessions[0].properties.get("turn_count", 0) + 1,
                "last_active": time.time(),
            })
        else:
            self._graph.add_node("session", "current session", {
                "last_input": obs.raw_input[:200],
                "last_intent": obs.intent,
                "last_topic": obs.topic,
                "turn_count": 1,
                "started_at": time.time(),
                "last_active": time.time(),
            })

    def _sync_entity(self, entity: Entity, result: SyncResult):
        """Sync an entity — create if new, update if exists."""
        # Check for existing entity with same name
        existing = self._find_similar_node(entity.name, "concept")
        if existing:
            # Update properties
            self._graph.update_node(existing.id, properties={
                "entity_type": entity.entity_type,
                "last_seen": time.time(),
                "mention_count": existing.properties.get("mention_count", 0) + 1,
            })
            result.updated_nodes.append({
                "id": existing.id, "type": "concept", "label": entity.name
            })
        else:
            # Create new
            nid = self._graph.add_node("concept", entity.name, {
                "entity_type": entity.entity_type,
                "confidence": entity.confidence,
                "mention_count": 1,
                "first_seen": time.time(),
                "last_seen": time.time(),
            })
            result.created_nodes.append({"id": nid, "type": "concept", "label": entity.name})

    def _sync_goal(self, goal: DetectedGoal, obs: Observation, result: SyncResult):
        """Sync a goal — create if new, update if similar exists."""
        # Check for existing similar goal
        existing_goals = self._graph.find_nodes(node_type="goal")
        for eg in existing_goals:
            if self._is_similar(goal.description, eg.label):
                # Update urgency if higher
                if goal.urgency > eg.properties.get("urgency", 0):
                    self._graph.update_node(eg.id, properties={"urgency": goal.urgency})
                result.updated_nodes.append({
                    "id": eg.id, "type": "goal", "label": eg.label
                })
                return

        # Create new goal
        nid = self._graph.add_node("goal", goal.description, {
            "status": "active",
            "verb": goal.verb,
            "target": goal.target,
            "urgency": goal.urgency,
            "confidence": goal.confidence,
            "priority": int(goal.urgency * 10),
            "progress": 0.0,
            "detected_at": time.time(),
        })
        result.created_nodes.append({"id": nid, "type": "goal", "label": goal.description})

    def _sync_task(self, task: DetectedTask, result: SyncResult):
        """Sync a task — create under parent goal if identified."""
        # Find parent goal
        parent_id = None
        if task.parent_goal:
            goals = self._graph.find_nodes(node_type="goal")
            for g in goals:
                if self._is_similar(task.parent_goal, g.label):
                    parent_id = g.id
                    break

        # Check for existing similar task
        existing_tasks = self._graph.find_nodes(node_type="task")
        for et in existing_tasks:
            if self._is_similar(task.description, et.label):
                result.duplicates_merged += 1
                return

        # Create new task
        nid = self._graph.add_node("task", task.description, {
            "status": "active",
            "is_explicit": task.is_explicit,
            "confidence": task.confidence,
            "detected_at": time.time(),
        })
        result.created_nodes.append({"id": nid, "type": "task", "label": task.description})

        # Link to parent goal
        if parent_id:
            self._graph.add_edge(parent_id, nid, "contains")
            result.created_edges.append({
                "source": parent_id, "target": nid, "relation": "contains"
            })

    def _sync_fact(self, fact: DetectedFact, result: SyncResult):
        """Sync a fact — create with contradiction detection."""
        # Check for contradictions with existing facts
        existing_facts = self._graph.find_nodes(node_type="fact")
        for ef in existing_facts:
            existing_subject = ef.properties.get("subject", "")
            if existing_subject and self._is_similar(fact.subject, existing_subject):
                existing_object = ef.properties.get("object", "")
                # Same subject but different assertion → potential contradiction
                if existing_object and not self._is_similar(fact.object, existing_object):
                    if fact.fact_type == ef.properties.get("fact_type"):
                        result.contradictions.append({
                            "existing_id": ef.id,
                            "existing": ef.label,
                            "new": fact.statement,
                            "issue": f"Conflicting info about '{fact.subject}'",
                        })
                        # Create the fact but mark the contradiction
                        nid = self._graph.add_node("fact", fact.statement[:80], {
                            "subject": fact.subject,
                            "object": fact.object,
                            "fact_type": fact.fact_type,
                            "is_negation": fact.is_negation,
                            "confidence": fact.confidence,
                            "contradicts": ef.id,
                            "detected_at": time.time(),
                        })
                        self._graph.add_edge(nid, ef.id, "contradicts")
                        result.created_nodes.append({"id": nid, "type": "fact", "label": fact.statement[:80]})
                        result.created_edges.append({"source": nid, "target": ef.id, "relation": "contradicts"})
                        return

                # Same subject and same assertion → duplicate, skip
                if self._is_similar(fact.statement, ef.label):
                    result.duplicates_merged += 1
                    return

        # No contradiction — create new fact
        nid = self._graph.add_node("fact", fact.statement[:80], {
            "subject": fact.subject,
            "object": fact.object,
            "fact_type": fact.fact_type,
            "is_negation": fact.is_negation,
            "confidence": fact.confidence,
            "detected_at": time.time(),
        })
        result.created_nodes.append({"id": nid, "type": "fact", "label": fact.statement[:80]})

    def _sync_concept(self, concept: DetectedConcept, result: SyncResult):
        """Sync a concept — create or merge."""
        existing = self._find_similar_node(concept.name, "concept")
        if existing:
            # Update domain if provided
            props = {"last_seen": time.time()}
            if concept.domain:
                props["domain"] = concept.domain
            props["mention_count"] = existing.properties.get("mention_count", 0) + 1
            self._graph.update_node(existing.id, properties=props)
        else:
            nid = self._graph.add_node("concept", concept.name, {
                "domain": concept.domain,
                "confidence": concept.confidence,
                "mention_count": 1,
                "first_seen": time.time(),
                "last_seen": time.time(),
            })
            result.created_nodes.append({"id": nid, "type": "concept", "label": concept.name})

    def _create_cross_references(self, obs: Observation, result: SyncResult):
        """Create edges between related items from the same observation."""
        # Link concepts that appear together (co-occurrence)
        concept_nodes = []
        for c in obs.concepts:
            node = self._find_similar_node(c.name, "concept")
            if node:
                concept_nodes.append(node.id)

        for i, nid1 in enumerate(concept_nodes):
            for nid2 in concept_nodes[i+1:]:
                # Check if edge already exists
                neighbors = self._graph.neighbors(nid1, relation="relates_to")
                if not any(n_id == nid2 for n_id, _, _ in neighbors):
                    self._graph.add_edge(nid1, nid2, "relates_to")
                    result.created_edges.append({
                        "source": nid1, "target": nid2, "relation": "relates_to"
                    })

    # ─── Helpers ───

    def _find_similar_node(self, label: str, node_type: str):
        """Find a node with a similar label."""
        nodes = self._graph.find_nodes(node_type=node_type)
        for n in nodes:
            if self._is_similar(label, n.label):
                return n
        return None

    def _is_similar(self, a: str, b: str, threshold: float = 0.7) -> bool:
        """Simple similarity check (word overlap ratio)."""
        if not a or not b:
            return False
        words_a = set(a.lower().split())
        words_b = set(b.lower().split())
        if not words_a or not words_b:
            return False
        overlap = len(words_a & words_b)
        min_len = min(len(words_a), len(words_b))
        return (overlap / max(min_len, 1)) >= threshold


# ═══════════════════════════════════════════════════════════════
# SINGLETON
# ═══════════════════════════════════════════════════════════════

_sync: Optional[RealitySynchronizer] = None

def get_reality_sync(graph: Optional[RealityGraph] = None) -> RealitySynchronizer:
    """Get the global reality synchronizer."""
    global _sync
    if _sync is None:
        _sync = RealitySynchronizer(graph=graph)
    return _sync
