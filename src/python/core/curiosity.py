"""
AXIMA Curiosity Engine — Autonomous gap-finding and research task generation.

When idle, the system:
  - Finds knowledge gaps
  - Finds unanswered questions
  - Finds weak theories (low confidence)
  - Finds disconnected graph regions
  - Generates research tasks automatically

Curiosity increases understanding without user requests.

Usage:
    from core.curiosity import CuriosityEngine, get_curiosity

    curiosity = get_curiosity()
    gaps = curiosity.find_gaps()
    tasks = curiosity.generate_research_tasks(limit=5)
"""

import time
from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any, Set

from core.reality_graph import get_reality_graph, RealityGraph


# ═══════════════════════════════════════════════════════════════
# GAP TYPES
# ═══════════════════════════════════════════════════════════════

@dataclass
class KnowledgeGap:
    """A gap in the system's knowledge."""
    description: str
    gap_type: str = "unknown"       # unknown, weak, disconnected, incomplete, stale
    domain: str = ""
    importance: float = 0.5         # How important to fill
    related_nodes: List[str] = field(default_factory=list)  # Node IDs
    suggested_action: str = ""      # What to do about it


@dataclass
class ResearchTask:
    """An automatically generated research task."""
    question: str
    priority: float = 0.5
    domain: str = ""
    gap_type: str = ""
    reason: str = ""                # Why this is worth investigating
    related_to: List[str] = field(default_factory=list)


# ═══════════════════════════════════════════════════════════════
# CURIOSITY ENGINE
# ═══════════════════════════════════════════════════════════════

class CuriosityEngine:
    """Autonomous knowledge gap detection and research generation.
    
    This is the beginning of autonomous cognition.
    The system becomes self-improving without user prompting.
    """

    def __init__(self, graph: Optional[RealityGraph] = None):
        self._graph = graph or get_reality_graph()

    def find_gaps(self) -> List[KnowledgeGap]:
        """Find all knowledge gaps in the Reality Graph."""
        gaps = []
        gaps.extend(self._find_weak_knowledge())
        gaps.extend(self._find_disconnected_regions())
        gaps.extend(self._find_incomplete_goals())
        gaps.extend(self._find_unresolved_contradictions())
        gaps.extend(self._find_stale_knowledge())

        # Sort by importance
        gaps.sort(key=lambda g: -g.importance)
        return gaps

    def generate_research_tasks(self, limit: int = 10) -> List[ResearchTask]:
        """Generate research tasks from identified gaps."""
        gaps = self.find_gaps()
        tasks = []

        for gap in gaps[:limit * 2]:  # Generate more than needed, then filter
            task = self._gap_to_task(gap)
            if task:
                tasks.append(task)

        # Deduplicate and sort
        seen = set()
        unique_tasks = []
        for t in tasks:
            key = t.question[:50].lower()
            if key not in seen:
                seen.add(key)
                unique_tasks.append(t)

        unique_tasks.sort(key=lambda t: -t.priority)
        return unique_tasks[:limit]

    def curiosity_score(self) -> float:
        """How curious should the system be right now?
        
        High score = many gaps, system should be exploring.
        Low score = knowledge is well-connected and confident.
        """
        gaps = self.find_gaps()
        if not gaps:
            return 0.0

        # Weight by importance
        total_importance = sum(g.importance for g in gaps)
        # Normalize against graph size
        total_nodes = len(self._graph.find_nodes())
        if total_nodes == 0:
            return 1.0

        return min(1.0, total_importance / max(total_nodes, 1))

    def stats(self) -> Dict[str, Any]:
        """Curiosity statistics."""
        gaps = self.find_gaps()
        gap_types = {}
        for g in gaps:
            gap_types[g.gap_type] = gap_types.get(g.gap_type, 0) + 1
        return {
            "total_gaps": len(gaps),
            "gap_types": gap_types,
            "curiosity_score": self.curiosity_score(),
            "avg_importance": sum(g.importance for g in gaps) / max(1, len(gaps)),
        }

    # ─── Gap Finders ───

    def _find_weak_knowledge(self) -> List[KnowledgeGap]:
        """Find facts/theories with low confidence."""
        gaps = []
        for node_type in ["fact", "theory"]:
            nodes = self._graph.find_nodes(node_type=node_type)
            for node in nodes:
                confidence = node.properties.get("confidence", 0.5)
                if confidence < 0.4:
                    gaps.append(KnowledgeGap(
                        description=f"Low confidence ({confidence:.0%}): {node.label}",
                        gap_type="weak",
                        domain=node.properties.get("domain", ""),
                        importance=0.6 * (1 - confidence),
                        related_nodes=[node.id],
                        suggested_action=f"Verify or find supporting evidence for: {node.label}",
                    ))
        return gaps

    def _find_disconnected_regions(self) -> List[KnowledgeGap]:
        """Find nodes with no connections (isolated knowledge)."""
        gaps = []
        all_nodes = []
        for t in ["fact", "concept", "theory"]:
            all_nodes.extend(self._graph.find_nodes(node_type=t))

        for node in all_nodes:
            connections = self._graph.neighbors(node.id, direction="both")
            if len(connections) == 0:
                gaps.append(KnowledgeGap(
                    description=f"Isolated: {node.label}",
                    gap_type="disconnected",
                    domain=node.properties.get("domain", ""),
                    importance=0.4,
                    related_nodes=[node.id],
                    suggested_action=f"Find relationships for: {node.label}",
                ))
        return gaps

    def _find_incomplete_goals(self) -> List[KnowledgeGap]:
        """Find goals with no tasks (need decomposition)."""
        gaps = []
        goals = self._graph.find_nodes(node_type="goal")

        for goal in goals:
            if goal.properties.get("status") != "active":
                continue
            children = self._graph.neighbors(goal.id, relation="contains")
            if not children:
                gaps.append(KnowledgeGap(
                    description=f"Goal has no tasks: {goal.label}",
                    gap_type="incomplete",
                    importance=0.8,
                    related_nodes=[goal.id],
                    suggested_action=f"Decompose goal '{goal.label}' into tasks",
                ))
        return gaps

    def _find_unresolved_contradictions(self) -> List[KnowledgeGap]:
        """Find unresolved contradictions in the graph."""
        gaps = []
        edges = self._graph.find_edges(relation="contradicts")

        # Group contradictions
        seen_pairs: Set[tuple] = set()
        for edge in edges:
            pair = tuple(sorted([edge.source_id, edge.target_id]))
            if pair in seen_pairs:
                continue
            seen_pairs.add(pair)

            src = self._graph.get_node(edge.source_id)
            tgt = self._graph.get_node(edge.target_id)
            if src and tgt:
                # Check if already resolved
                src_status = src.properties.get("status", "")
                tgt_status = tgt.properties.get("status", "")
                if src_status != "disputed" and tgt_status != "disputed":
                    gaps.append(KnowledgeGap(
                        description=f"Contradiction: '{src.label}' vs '{tgt.label}'",
                        gap_type="contradiction",
                        importance=0.7,
                        related_nodes=[src.id, tgt.id],
                        suggested_action="Resolve which fact is correct",
                    ))
        return gaps

    def _find_stale_knowledge(self) -> List[KnowledgeGap]:
        """Find knowledge that hasn't been accessed in a long time."""
        gaps = []
        now = time.time()
        stale_threshold = 7 * 24 * 3600  # 7 days

        for node_type in ["fact", "concept"]:
            nodes = self._graph.find_nodes(node_type=node_type)
            for node in nodes:
                last_seen = node.properties.get("last_seen", node.updated_at)
                if last_seen and (now - last_seen) > stale_threshold:
                    age_days = (now - last_seen) / 86400
                    gaps.append(KnowledgeGap(
                        description=f"Stale ({age_days:.0f} days): {node.label}",
                        gap_type="stale",
                        importance=0.3,
                        related_nodes=[node.id],
                        suggested_action=f"Verify if still current: {node.label}",
                    ))
        return gaps[:20]  # Cap stale findings

    # ─── Task Generation ───

    def _gap_to_task(self, gap: KnowledgeGap) -> Optional[ResearchTask]:
        """Convert a knowledge gap into a research task."""
        if gap.gap_type == "weak":
            return ResearchTask(
                question=f"What evidence supports: {gap.description.split(': ', 1)[-1]}?",
                priority=gap.importance,
                domain=gap.domain,
                gap_type=gap.gap_type,
                reason="Low confidence knowledge needs verification",
                related_to=gap.related_nodes,
            )
        elif gap.gap_type == "disconnected":
            return ResearchTask(
                question=f"What relates to: {gap.description.split(': ', 1)[-1]}?",
                priority=gap.importance,
                domain=gap.domain,
                gap_type=gap.gap_type,
                reason="Isolated knowledge should be connected",
                related_to=gap.related_nodes,
            )
        elif gap.gap_type == "incomplete":
            return ResearchTask(
                question=f"What tasks are needed for: {gap.description.split(': ', 1)[-1]}?",
                priority=gap.importance,
                gap_type=gap.gap_type,
                reason="Goal needs task decomposition",
                related_to=gap.related_nodes,
            )
        elif gap.gap_type == "contradiction":
            return ResearchTask(
                question=f"Which is correct: {gap.description}?",
                priority=gap.importance,
                gap_type=gap.gap_type,
                reason="Contradictory knowledge needs resolution",
                related_to=gap.related_nodes,
            )
        elif gap.gap_type == "stale":
            return ResearchTask(
                question=f"Is this still true: {gap.description.split(': ', 1)[-1]}?",
                priority=gap.importance,
                domain=gap.domain,
                gap_type=gap.gap_type,
                reason="Knowledge may be outdated",
                related_to=gap.related_nodes,
            )
        return None


# ═══════════════════════════════════════════════════════════════
# SINGLETON
# ═══════════════════════════════════════════════════════════════

_curiosity: Optional[CuriosityEngine] = None

def get_curiosity(graph: Optional[RealityGraph] = None) -> CuriosityEngine:
    """Get the global curiosity engine."""
    global _curiosity
    if _curiosity is None:
        _curiosity = CuriosityEngine(graph=graph)
    return _curiosity
