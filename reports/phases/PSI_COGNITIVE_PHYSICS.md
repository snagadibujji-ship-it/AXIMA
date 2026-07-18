# PSI_COGNITIVE_PHYSICS.md

## Overview

The cognitive physics engine applies all 25 cognitive laws to simulate mental processes. It operates in discrete time steps, updating node states based on their graph context.

## Core Functions

### tick(delta_t)
Process all active nodes for time step `delta_t`. Returns updated graph state.

1. Iterate over active nodes
2. Build context for each node
3. Apply all laws sequentially
4. Collect new states
5. Update graph

### tick_node(node_id, delta_t)
Process a single node. Used for targeted updates or debugging.

1. Retrieve node state and neighbors
2. Build context: connections, time delta, neighbor activations
3. Apply each law: `state = law(state, context)`
4. Return updated state

## Context Construction

Context includes:
- Node's current state
- Graph connections (incoming/outgoing edges)
- Neighbor states with weights
- Time delta since last tick
- Global system time
- Budget constraints

## Physics Properties

- **Conservation**: Total activation not conserved (open system)
- **Locality**: Laws depend only on local neighborhood
- **Determinism**: Same state + context → same output
- **Composability**: Laws can be chained or reordered

## Integration

Used by:
- `cognitive_scheduler.py` - Determines which nodes tick when
- `cognitive_runtime.py` - Main simulation loop
- `emergent_validation.py` - Validates emergent behaviors

## Performance

- Linear complexity in node count
- Parallelizable per-node operations
- Incremental updates via `tick_node`

---
