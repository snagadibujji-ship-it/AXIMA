# PSI_ACTIVATION_SPREADING.md

## Overview

Activation spreading simulates attention and associative recall by propagating activation through the knowledge graph. It implements the spreading activation theory of memory.

## Mechanism

Activation ripples from source nodes through edges. Each hop reduces activation by a decay factor, simulating limited attention span.

## Parameters

- **Relation weights**: Determines spreading strength
  - `contains`: 0.7 (strong hierarchical links)
  - `supports`: 0.6 (evidence/justification links)
  - `relates_to`: 0.3 (weak associative links)
- **Distance decay**: 0.5 per hop (exponential decay)
- **Max depth**: 3 hops (shallow spread for focus)
- **Threshold**: 0.1 (cutoff for negligible activation)

## Algorithm

```python
def spread_activation(graph, source_ids, max_depth=3):
    queue = [(id, 1.0, 0) for id in source_ids]
    visited = {}
    while queue:
        node_id, act, depth = queue.pop(0)
        if depth >= max_depth:
            continue
        for neighbor, edge_weight in graph.get_neighbors(node_id):
            new_act = act * edge_weight * 0.5
            if new_act > 0.1:
                queue.append((neighbor, new_act, depth + 1))
    return accumulated activations
```

## Use Cases

- Triggering related concepts
- Priming effects in reasoning
- Attention allocation to relevant knowledge
- Pattern completion from partial cues

## Integration

- Called by `cognitive_physics.py` during tick
- Used by `cognitive_scheduler.py` to prioritize nodes
- Feeds into `memory_consolidation.py` for pattern detection

---
