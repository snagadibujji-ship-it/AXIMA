"""
ACES v2 — Core Data Models
All structures that flow through the pipeline.
Tiny, deterministic, no logic — just shape.
"""

from typing import List, Dict, Optional, Tuple, Any
from dataclasses import dataclass, field


# ═══════════════════════════════════════════════════════════════
# STAGE 1: Input
# ═══════════════════════════════════════════════════════════════

@dataclass
class NormalizedInput:
    """Cleaned, normalized input ready for processing."""
    raw: str                          # Original user input
    clean: str                        # Normalized text
    tokens: List[str] = field(default_factory=list)  # Token spans
    domain_hint: str = ""             # Detected domain (math/physics/bio/etc)
    language: str = "en"              # Detected language
    has_formula: bool = False         # Contains mathematical expression
    has_code: bool = False            # Contains code
    confidence: float = 1.0           # How confident in normalization


# ═══════════════════════════════════════════════════════════════
# STAGE 2: Routing
# ═══════════════════════════════════════════════════════════════

@dataclass
class RouterDecision:
    """What kind of explanation is needed."""
    question_type: str = "fact"       # fact/why/how/compare/calculation/derivation/process/teach
    format_mode: str = "deep"         # one-line/bullets/steps/deep/expert/simple/teach/exam
    depth: int = 2                    # 1=surface, 2=standard, 3=thorough, 4=exhaustive
    domain: str = "general"           # math/physics/bio/cs/general/etc
    confidence: float = 0.8
    needs_solver: bool = False        # Route to math/physics solver?
    needs_search: bool = False        # Need external knowledge?


# ═══════════════════════════════════════════════════════════════
# STAGE 3: Meaning Graph
# ═══════════════════════════════════════════════════════════════

@dataclass
class MeaningNode:
    """A concept/entity/step in the meaning graph."""
    id: str                           # Unique identifier
    type: str                         # concept/entity/rule/formula/step/example/warning/insight
    label: str                        # Human-readable name
    content: str = ""                 # Full content/definition
    evidence: str = ""                # Where this came from (span reference)
    confidence: float = 1.0
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class MeaningEdge:
    """A relationship between two nodes."""
    source: str                       # Source node ID
    target: str                       # Target node ID
    relation: str                     # causes/depends_on/enables/transforms_into/part_of/similar_to/contradicts/limits
    confidence: float = 1.0
    evidence: str = ""                # What supports this edge


@dataclass
class MeaningGraph:
    """The complete meaning structure of an explanation."""
    nodes: List[MeaningNode] = field(default_factory=list)
    edges: List[MeaningEdge] = field(default_factory=list)
    root_node: str = ""               # Main topic node ID
    
    def add_node(self, node: MeaningNode):
        self.nodes.append(node)
        if not self.root_node:
            self.root_node = node.id
    
    def add_edge(self, edge: MeaningEdge):
        self.edges.append(edge)
    
    def get_node(self, node_id: str) -> Optional[MeaningNode]:
        for n in self.nodes:
            if n.id == node_id:
                return n
        return None
    
    def get_children(self, node_id: str) -> List[MeaningNode]:
        child_ids = [e.target for e in self.edges if e.source == node_id]
        return [n for n in self.nodes if n.id in child_ids]
    
    def get_parents(self, node_id: str) -> List[MeaningNode]:
        parent_ids = [e.source for e in self.edges if e.target == node_id]
        return [n for n in self.nodes if n.id in parent_ids]


# ═══════════════════════════════════════════════════════════════
# STAGE 4: Reason Chain
# ═══════════════════════════════════════════════════════════════

@dataclass
class ReasonChain:
    """The logical skeleton of an explanation."""
    prerequisites: List[str] = field(default_factory=list)    # What must be known first
    chain: List[str] = field(default_factory=list)            # Step-by-step reasoning
    analogies: List[str] = field(default_factory=list)        # Helpful comparisons
    misconceptions: List[str] = field(default_factory=list)   # Common wrong ideas
    enables: List[str] = field(default_factory=list)          # What this knowledge unlocks
    rules_out: List[str] = field(default_factory=list)        # What this eliminates
    shortest_path: List[str] = field(default_factory=list)    # Minimal explanation


# ═══════════════════════════════════════════════════════════════
# STAGE 5: Explanation Plan + Frame
# ═══════════════════════════════════════════════════════════════

@dataclass
class ExplanationPlan:
    """How to structure the explanation."""
    opening: str = ""                 # First sentence strategy
    section_order: List[str] = field(default_factory=list)  # Order of topics
    detail_level: Dict[str, int] = field(default_factory=dict)  # Per-section detail
    hidden: List[str] = field(default_factory=list)  # What to omit (too complex for level)
    analogy_choice: str = ""          # Best analogy to use
    start_with: str = "intuition"     # intuition/formula/steps/example
    adaptation: str = "standard"      # beginner/exam/technical/proof/teacher


@dataclass
class ExplanationFrame:
    """A single rendered explanation output."""
    mode: str                         # Which render mode was used
    title: str = ""                   # Optional title
    sections: List[Dict[str, str]] = field(default_factory=list)  # [{type, content}]
    text: str = ""                    # Final rendered text
    formulas: List[str] = field(default_factory=list)  # Preserved formulas
    source_graph: Optional[MeaningGraph] = None  # Link back to structure


# ═══════════════════════════════════════════════════════════════
# STAGE 6: Audit + Memory
# ═══════════════════════════════════════════════════════════════

@dataclass
class AuditReport:
    """Quality check on an explanation."""
    passed: bool = True
    issues: List[str] = field(default_factory=list)
    truth_score: float = 1.0          # 0-1: how truthful
    completeness_score: float = 1.0   # 0-1: how complete
    style_score: float = 1.0          # 0-1: how well-formatted
    has_contradiction: bool = False
    has_unsupported_claim: bool = False
    has_missing_step: bool = False
    repair_suggestions: List[str] = field(default_factory=list)


@dataclass
class MemoryRecord:
    """Stored explanation for future reference."""
    topic: str                        # What was explained
    version: int = 1                  # Explanation version (for upgrades)
    graph: Optional[MeaningGraph] = None
    chain: Optional[ReasonChain] = None
    best_mode: str = "deep"           # Which mode worked best
    confidence: float = 0.8
    times_used: int = 0
    last_used: float = 0.0            # Timestamp
    superseded: bool = False          # Replaced by newer version?
