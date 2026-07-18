# PSI_MEMORY_CONSOLIDATION.md

## Overview

Memory consolidation transforms raw facts into progressively abstract knowledge structures through incremental processing. It implements a hierarchical abstraction pipeline.

## Abstraction Levels

1. **Facts** - Atomic propositions with confidence scores
2. **Patterns** - Repeated fact sequences grouped by similarity
3. **Rules** - Generalized patterns with conditions and consequences
4. **Principles** - High-level, stable abstractions guiding reasoning

## Algorithm

`consolidate_step(max_work=5)` processes up to 5 consolidation steps per tick:

1. Identify high-confidence facts (confidence > 0.8, usage_count > 3)
2. Cluster facts by subject/relation
3. Detect repeated patterns within clusters
4. Generate rule candidates from patterns
5. Promote rules to principles when stable

## Clustering

Uses normalized semantic similarity:
- Fact similarity via shared predicates/objects
- Temporal proximity for sequential patterns
- Activation overlap for associative grouping

## Stability Requirements

Principles require:
- High confidence (> 0.9)
- High stability (> 0.7)
- Multiple supporting facts (> 5)
- Low entropy (< 0.3)

## Integration

- Called by `cognitive_scheduler.py` during low-priority cycles
- Used by `principle_evolution.py` for principle lifecycle
- Feeds `self_metrics.py` for knowledge quality metrics

## Benefits

- Reduces cognitive load by compressing facts
- Enables hierarchical reasoning
- Improves prediction accuracy through abstraction

---
