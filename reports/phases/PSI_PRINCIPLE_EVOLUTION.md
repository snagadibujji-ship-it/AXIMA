# PSI_PRINCIPLE_EVOLUTION.md

## Overview

Living principles evolve through their lifecycle: strengthen when predictive, weaken when contradicted, merge when redundant, or retire when obsolete.

## Principle Attributes

- **confidence** - Current belief level
- **prediction_accuracy** - Historical predictive success
- **supports** - Number of supporting evidence nodes
- **contradictions** - Number of conflicting observations
- **usage** - Times applied in reasoning

## Evolution Operators

`evolve_tick()` applies these operators:

1. **Strengthen**: If accuracy > 0.8 and usage > 2, confidence += 0.05
2. **Weaken**: If contradictions > 2, confidence -= 0.1 per contradiction
3. **Merge**: If two principles have > 0.9 overlap and similar accuracy, merge
4. **Retire**: If confidence < 0.2 after 3 weakening cycles, mark retired

## Lifecycle

1. **Emergence** - From memory consolidation
2. **Testing** - Applied in prediction contexts
3. **Strengthening/Weakening** - Based on outcomes
4. **Maturity** - Stable, high-confidence principles
5. **Retirement** - Obsolete or contradicted

## Integration

- Called by `cognitive_scheduler.py` periodically
- Used by `self_metrics.py` for principle health tracking
- Feeds `meta_reasoning.py` for principle justification

## Benefits

- Adapts to new evidence
- Eliminates outdated beliefs
- Reduces redundancy through merging

---
