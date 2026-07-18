"""
AXIMA Understanding Evolution — Makes understanding improve over time.

Extends the Understanding Pipeline with:
  - Confidence updates (evidence accumulates)
  - Principle refinement (sharpen with new data)
  - Principle merging (combine related principles)
  - Principle retirement (remove disproven)
  - Cross-domain links (find analogies)

Usage:
    from core.evolution import UnderstandingEvolution, get_evolution

    evo = get_evolution()
    evo.update_confidence(fact_id, new_evidence=True)
    evo.find_cross_domain_links()
    evo.retire_weak_principles(threshold=0.2)
"""

import time
from typing import Optional, List, Dict, Any

from core.reality_graph import get_reality_graph, RealityGraph
from core.understanding import get_understanding_pipeline, UnderstandingPipeline, AbstractionLevel


class UnderstandingEvolution:
    """Makes AXIMA's understanding evolve over time.
    
    This system ensures the knowledge graph doesn't just accumulate — 
    it IMPROVES. Weak knowledge fades, strong knowledge strengthens,
    and cross-domain connections emerge.
    """

    def __init__(self, graph: Optional[RealityGraph] = None,
                 pipeline: Optional[UnderstandingPipeline] = None):
        self._graph = graph or get_reality_graph()
        self._pipeline = pipeline or get_understanding_pipeline(self._graph)

    # ─── Confidence Updates ───

    def update_confidence(self, node_id: str, supporting: bool = True,
                          amount: float = 0.1) -> float:
        """Update confidence based on new evidence.
        
        supporting=True → confidence increases
        supporting=False → confidence decreases
        """
        node = self._graph.get_node(node_id)
        if not node:
            return 0.0

        current = node.properties.get("confidence", 0.5)
        if supporting:
            new_conf = min(1.0, current + amount * (1 - current))  # Diminishing returns
        else:
            new_conf = max(0.0, current - amount * current)  # Proportional decrease

        self._graph.update_node(node_id, properties={
            "confidence": new_conf,
            "last_evidence_at": time.time(),
            "evidence_count": node.properties.get("evidence_count", 0) + 1,
        })
        self._graph.save()
        return new_conf

    def strengthen_with_evidence(self, node_id: str, evidence_ids: List[str]):
        """Strengthen a node by linking new supporting evidence."""
        for eid in evidence_ids:
            self._graph.add_edge(eid, node_id, "supports")
        self.update_confidence(node_id, supporting=True,
                             amount=0.05 * len(evidence_ids))

    # ─── Principle Refinement ───

    def refine_principle(self, principle_id: str, new_statement: str,
                         reason: str = "") -> bool:
        """Refine a principle's statement based on new understanding."""
        node = self._graph.get_node(principle_id)
        if not node:
            return False

        # Store old version
        old_statement = node.properties.get("statement", node.label)
        history = node.properties.get("refinement_history", [])
        history.append({
            "old": old_statement,
            "new": new_statement,
            "reason": reason,
            "time": time.time(),
        })

        self._graph.update_node(principle_id, label=new_statement[:80], properties={
            "statement": new_statement,
            "refinement_history": history[-10:],  # Keep last 10
            "last_refined": time.time(),
            "refinement_count": len(history),
        })
        self._graph.save()
        return True

    # ─── Principle Merging ───

    def merge_principles(self, principle_ids: List[str],
                         merged_statement: str) -> Optional[str]:
        """Merge multiple related principles into one stronger principle.
        
        Returns the new merged principle's node ID.
        """
        if len(principle_ids) < 2:
            return None

        # Collect all supporting rules/evidence
        all_supports = []
        avg_confidence = 0.0
        for pid in principle_ids:
            node = self._graph.get_node(pid)
            if node:
                avg_confidence += node.properties.get("confidence", 0.5)
                # Get supporting edges
                for nid, rel, _ in self._graph.neighbors(pid, direction="in"):
                    if rel == "supports":
                        all_supports.append(nid)

        avg_confidence /= len(principle_ids)

        # Create merged principle with higher confidence
        merged_id = self._graph.add_node("theory", merged_statement[:80], {
            "statement": merged_statement,
            "level": AbstractionLevel.PRINCIPLE.value,
            "confidence": min(0.95, avg_confidence + 0.1),
            "merged_from": principle_ids,
            "created_at": time.time(),
        })

        # Link supports
        for sid in all_supports:
            self._graph.add_edge(sid, merged_id, "supports")

        # Link old principles as derived_from
        for pid in principle_ids:
            self._graph.add_edge(merged_id, pid, "derived_from")
            # Mark old as merged
            self._graph.update_node(pid, properties={
                "status": "merged",
                "merged_into": merged_id,
            })

        self._graph.save()
        return merged_id

    # ─── Principle Retirement ───

    def retire_weak_principles(self, threshold: float = 0.2) -> List[str]:
        """Retire principles below confidence threshold.
        
        Retired principles aren't deleted — they're marked inactive.
        """
        retired = []
        theories = self._graph.find_nodes(node_type="theory")

        for theory in theories:
            if theory.properties.get("level") != AbstractionLevel.PRINCIPLE.value:
                continue
            if theory.properties.get("status") in ("merged", "retired"):
                continue

            confidence = theory.properties.get("confidence", 0.5)
            if confidence < threshold:
                self._graph.update_node(theory.id, properties={
                    "status": "retired",
                    "retired_at": time.time(),
                    "retired_reason": f"Confidence dropped below {threshold}",
                })
                retired.append(theory.id)

        if retired:
            self._graph.save()
        return retired

    # ─── Cross-Domain Links ───

    def find_cross_domain_links(self) -> List[Dict[str, Any]]:
        """Find potential analogies between different domains.
        
        Looks for structural similarities in different domain subgraphs.
        """
        links = []

        # Get all concepts grouped by domain
        concepts = self._graph.find_nodes(node_type="concept")
        by_domain: Dict[str, List] = {}
        for c in concepts:
            domain = c.properties.get("domain", "general")
            by_domain.setdefault(domain, []).append(c)

        domains = list(by_domain.keys())

        # Compare concepts across domains
        for i, domain1 in enumerate(domains):
            for domain2 in domains[i+1:]:
                for c1 in by_domain[domain1]:
                    for c2 in by_domain[domain2]:
                        # Check if they share structural properties
                        sim = self._structural_similarity(c1, c2)
                        if sim > 0.3:
                            # Check if edge already exists
                            existing = self._graph.neighbors(c1.id, direction="both")
                            already_linked = any(nid == c2.id for nid, _, _ in existing)
                            if not already_linked:
                                links.append({
                                    "concept1": {"id": c1.id, "label": c1.label, "domain": domain1},
                                    "concept2": {"id": c2.id, "label": c2.label, "domain": domain2},
                                    "similarity": sim,
                                    "link_type": "analogy",
                                })

        return links[:20]

    def create_cross_domain_edge(self, node1_id: str, node2_id: str,
                                  reason: str = ""):
        """Create a cross-domain relationship edge."""
        self._graph.add_edge(node1_id, node2_id, "relates_to",
                            properties={"cross_domain": True, "reason": reason})
        self._graph.save()

    # ─── Evolution Metrics ───

    def evolution_report(self) -> Dict[str, Any]:
        """Report on how understanding has evolved."""
        facts = self._graph.find_nodes(node_type="fact")
        theories = self._graph.find_nodes(node_type="theory")
        concepts = self._graph.find_nodes(node_type="concept")

        avg_fact_conf = sum(f.properties.get("confidence", 0.5) for f in facts) / max(1, len(facts))
        avg_theory_conf = sum(t.properties.get("confidence", 0.5) for t in theories) / max(1, len(theories))

        retired = sum(1 for t in theories if t.properties.get("status") == "retired")
        merged = sum(1 for t in theories if t.properties.get("status") == "merged")
        refined = sum(1 for t in theories if t.properties.get("refinement_count", 0) > 0)

        return {
            "total_facts": len(facts),
            "total_theories": len(theories),
            "total_concepts": len(concepts),
            "avg_fact_confidence": round(avg_fact_conf, 3),
            "avg_theory_confidence": round(avg_theory_conf, 3),
            "retired_theories": retired,
            "merged_theories": merged,
            "refined_theories": refined,
            "cross_domain_edges": len(self._graph.find_edges(relation="relates_to")),
        }

    # ─── Helpers ───

    def _structural_similarity(self, node1, node2) -> float:
        """Compare structural role of two nodes (number of relations of each type)."""
        n1_neighbors = self._graph.neighbors(node1.id, direction="both")
        n2_neighbors = self._graph.neighbors(node2.id, direction="both")

        # Compare relation types
        n1_rels = set(rel for _, rel, _ in n1_neighbors)
        n2_rels = set(rel for _, rel, _ in n2_neighbors)

        if not n1_rels and not n2_rels:
            return 0.0
        if not n1_rels or not n2_rels:
            return 0.0

        overlap = len(n1_rels & n2_rels)
        union = len(n1_rels | n2_rels)
        return overlap / max(union, 1)


# ═══════════════════════════════════════════════════════════════
# SINGLETON
# ═══════════════════════════════════════════════════════════════

_evolution: Optional[UnderstandingEvolution] = None

def get_evolution(graph: Optional[RealityGraph] = None) -> UnderstandingEvolution:
    """Get the global understanding evolution instance."""
    global _evolution
    if _evolution is None:
        _evolution = UnderstandingEvolution(graph=graph)
    return _evolution
