"""
ACES v2 — Main Orchestrator
Runs the full pipeline: Input → Shield → Router → Parser → Graph → Skeleton → Planner → Renderer → Auditor
"""

from typing import Optional
from .models import (
    NormalizedInput, RouterDecision, MeaningGraph, ReasonChain,
    ExplanationPlan, ExplanationFrame, AuditReport, MemoryRecord
)


class ACESV2:
    """The ACES v2 Explanation Engine.
    
    Compiles meaning into a graph, derives a reason skeleton,
    and renders explanations in any human shape.
    """

    def __init__(self):
        # Pipeline stages (will be built in subsequent phases)
        self.shield = None      # Phase 2
        self.router = None      # Phase 3
        self.parser = None      # Phase 4
        self.graph_builder = None  # Phase 5
        self.reasoner = None    # Phase 6
        self.planner = None     # Phase 7
        self.renderer = None    # Phase 8
        self.auditor = None     # Phase 9
        self.memory = None      # Phase 10
        self.solver_bridge = None  # Phase 11
        self.search_bridge = None  # Phase 12

    def explain(self, question: str, mode: str = "deep",
                context: Optional[str] = None) -> ExplanationFrame:
        """Main entry point: explain anything in any shape.
        
        Args:
            question: What to explain
            mode: Explanation format (one-line/bullets/steps/deep/expert/simple/teach/exam)
            context: Optional additional context
            
        Returns:
            ExplanationFrame with the rendered explanation
        """
        # Stage 1: Shield — normalize input
        normalized = self._shield(question)

        # Stage 2: Route — decide what kind of explanation
        decision = self._route(normalized, mode)

        # Stage 3: Parse — extract meaning structure
        graph = self._parse(normalized, decision)

        # Stage 4: Reason — derive the explanation skeleton
        chain = self._reason(graph, decision)

        # Stage 5: Plan — decide how to present
        plan = self._plan(chain, decision)

        # Stage 6: Render — produce the output
        frame = self._render(plan, chain, graph, decision)

        # Stage 7: Audit — check quality
        report = self._audit(frame, graph)

        # Stage 8: Memory — store for future use
        self._remember(normalized.clean, graph, chain, frame)

        return frame

    def _shield(self, raw: str) -> NormalizedInput:
        """Stage 1: Normalize input."""
        if self.shield:
            return self.shield.process(raw)
        # Fallback: minimal normalization
        clean = raw.strip()
        return NormalizedInput(raw=raw, clean=clean, tokens=clean.split())

    def _route(self, inp: NormalizedInput, requested_mode: str) -> RouterDecision:
        """Stage 2: Decide explanation type."""
        if self.router:
            return self.router.route(inp, requested_mode)
        # Fallback: use requested mode
        return RouterDecision(format_mode=requested_mode)

    def _parse(self, inp: NormalizedInput, decision: RouterDecision) -> MeaningGraph:
        """Stage 3: Extract meaning graph."""
        if self.parser:
            return self.parser.parse(inp, decision)
        # Fallback: single-node graph
        from .models import MeaningNode
        graph = MeaningGraph()
        graph.add_node(MeaningNode(id="q", type="concept", label=inp.clean, content=inp.clean))
        return graph

    def _reason(self, graph: MeaningGraph, decision: RouterDecision) -> ReasonChain:
        """Stage 4: Derive reason skeleton."""
        if self.reasoner:
            return self.reasoner.reason(graph, decision)
        # Fallback: chain is just the node labels
        return ReasonChain(chain=[n.label for n in graph.nodes])

    def _plan(self, chain: ReasonChain, decision: RouterDecision) -> ExplanationPlan:
        """Stage 5: Plan the explanation structure."""
        if self.planner:
            return self.planner.plan(chain, decision)
        # Fallback: default plan
        return ExplanationPlan(
            opening=chain.chain[0] if chain.chain else "",
            section_order=chain.chain,
            start_with="intuition"
        )

    def _render(self, plan: ExplanationPlan, chain: ReasonChain,
                graph: MeaningGraph, decision: RouterDecision) -> ExplanationFrame:
        """Stage 6: Render into requested format."""
        if self.renderer:
            return self.renderer.render(plan, chain, graph, decision)
        # Fallback: join chain as text
        text = '\n'.join(chain.chain) if chain.chain else "(no explanation generated)"
        return ExplanationFrame(mode=decision.format_mode, text=text)

    def _audit(self, frame: ExplanationFrame, graph: MeaningGraph) -> AuditReport:
        """Stage 7: Check quality."""
        if self.auditor:
            return self.auditor.audit(frame, graph)
        return AuditReport(passed=True)

    def _remember(self, topic: str, graph: MeaningGraph,
                  chain: ReasonChain, frame: ExplanationFrame):
        """Stage 8: Store in memory."""
        if self.memory:
            self.memory.store(topic, graph, chain, frame)
