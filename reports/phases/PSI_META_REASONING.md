# PSI_META_REASONING.md

## Overview

Meta-reasoning provides 5 introspective services that explain and justify cognitive processes. It enables the system to reason about its own reasoning.

## Services

### why_chosen(node_id)
Explains why a node was selected for processing. Returns: activation, importance, recent usage, novelty, and predicted contribution.

### what_evidence(node_id)
Lists evidence supporting a node's state. Returns: supporting nodes with confidence weights, recent validations, and prediction history.

### what_assumptions(node_id)
Identifies implicit assumptions enabling a node. Returns: unstated premises, required conditions, and dependency chains.

### better_explanation(node_id)
Proposes improved reasoning paths. Returns: alternative explanations with confidence scores, evidence gaps, and testable predictions.

### what_to_investigate()
Suggests investigation targets. Returns: high-entropy nodes, contradictory patterns, under-supported principles, and novelty opportunities.

## Implementation

- Uses graph traversal for evidence paths
- Computes explanation quality via prediction accuracy
- Maintains a reason trace for reproducibility

## Uses

- Debugging and auditing
- Explainability to users
- Self-improvement via reflection
- Error diagnosis

## Integration

- Called by `self_metrics.py` for trend explanation
- Used by `cognitive_scheduler.py` for priority adjustment
- Feeds `emergent_validation.py` for behavior justification

---
