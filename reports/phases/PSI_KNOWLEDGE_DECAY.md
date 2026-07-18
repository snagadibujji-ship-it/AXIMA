# PSI_KNOWLEDGE_DECAY.md

## Overview

Knowledge decay implements graceful dormancy, allowing unused information to fade while preserving important concepts. It enables adaptive resource management.

## Decay Model

Activation decays exponentially with idle time:
```
activation(t) = activation(0) * exp(-lambda * idle_time)
```

Where `lambda` depends on node type and stability.

## Decay Rate Factors

- **Stability**: Higher stability → slower decay (lambda × (1 - stability))
- **Node type**: Theories decay at 50% rate of memories
- **Usage history**: Frequently used nodes have lower base lambda
- **Importance**: High importance slows decay slightly

## Reactivation

Dormant nodes can be reactivated:
- Activation spreading revives nearby nodes
- Meta-reasoning can target dormant high-importance nodes
- Reactivation cost: `base_cost * (1 - current_activation)`

## Categories

- **Active**: activation > 0.3
- **Dormant**: 0.01 < activation ≤ 0.3
- **Inert**: activation ≤ 0.01 (effectively removed)

## Integration

- `cognitive_physics.py` - Applies decay during tick
- `cognitive_scheduler.py` - Prioritizes reactivating dormant important nodes
- `self_metrics.py` - Tracks memory retention metrics

## Benefits

- Reduces graph size for traversal operations
- Focuses attention on relevant knowledge
- Prevents cognitive overload

---
