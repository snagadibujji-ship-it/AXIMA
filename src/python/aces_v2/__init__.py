"""
ACES v2 — Adaptive Cognitive Explanation System (Version 2)
Built by: Ghias + Kiro | 2026

DOCTRINE (FROZEN — DO NOT VIOLATE):

DEFINITION:
  "ACES v2 compiles meaning into a graph, derives a reason skeleton,
   and renders explanations in any human shape."

NON-NEGOTIABLES:
  1. No topic templates — explanations are DERIVED, not looked up
  2. No word-list dependency for core understanding — structure > vocabulary
  3. No explanation without structure — every output backed by a meaning graph
  4. No output without audit — every explanation checked before delivery
  5. No stale-memory reuse — version upgrades invalidate old weak answers

EXPLANATION MODES:
  - one-line: single sentence answer
  - bullets: key points as list
  - steps: ordered procedure
  - deep: full detailed explanation
  - expert: assumes domain knowledge
  - simple: 5th grader can understand
  - teach: builds from prerequisites to conclusion
  - exam: structured for test preparation

SUCCESS CRITERIA (MEASURABLE):
  1. Correct structure extraction (meaning graph matches input semantics)
  2. Correct explanation reshape (same graph → different valid outputs)
  3. No hallucinated steps (every claim traceable to input or derivation)
  4. Memory recall works (can reference past explanations)
  5. Versioning works (new logic replaces old weak answers)

ARCHITECTURE:
  Input → Shield → Router → Parser → Graph → Skeleton → Planner → Renderer → Auditor → Output
                                                                                    ↕
                                                                                 Memory

PIPELINE:
  1. Input Shield: normalize text, fix typos, detect domain
  2. Router: detect question type + desired format + depth
  3. Meaning Parser: extract semantic roles → MeaningGraph
  4. Graph Builder: enrich graph with relationships + evidence
  5. Reason Skeleton: derive the logical explanation chain
  6. Explanation Planner: decide structure/order/detail level
  7. Renderer: format into requested shape
  8. Auditor: check truth/completeness/style
  9. Memory: store/recall/version explanations
"""

__version__ = "2.0.0"
__doctrine__ = "Explain by structure, not by word tricks."
