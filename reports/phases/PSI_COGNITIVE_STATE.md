# PSI_COGNITIVE_STATE.md

## Overview

Every cognitive node in the PSI architecture carries 12 universal state attributes that define its current condition and potential for change. These attributes form the foundation for all cognitive processes.

## Universal State Attributes

1. **activation** (0.0-1.0) - Current energy level determining visibility and influence
2. **confidence** (0.0-1.0) - Belief in accuracy; influences spreading and consolidation
3. **importance** (0.0-1.0) - Priority ranking for attention and resource allocation
4. **novelty** (0.0-1.0) -新奇度；高novelty nodes spread activation faster
5. **energy** (0.0-1.0) - Available computational resources for processing
6. **stability** (0.0-1.0) - Resistance to decay and unwanted modification
7. **age** (float) - Time since creation in seconds
8. **usage_count** (int) - Number of times node has been accessed
9. **prediction_accuracy** (0.0-1.0) - Historical accuracy of predictions made via this node
10. **reflection_count** (int) - Times node has been examined by meta-reasoning
11. **learning_value** (float) - Cumulative learning contribution
12. **entropy** (0.0-1.0) - Uncertainty or disorder measure

## Attribute Interactions

Attributes interact through the 25 cognitive laws. For example:
- High stability + high confidence → resistant to decay
- High activation + high importance → priority for scheduling
- Low confidence + high entropy → candidates for reflection

## Usage in Core Modules

All core modules read and write state attributes:
- `cognitive_laws.py` - Pure functions transforming state
- `cognitive_physics.py` - Applies laws to simulate cognition
- `memory_consolidation.py` - Uses confidence and usage_count
- `knowledge_decay.py` - Relies on stability and activation
- `self_metrics.py` - Aggregates attributes for system metrics

## Design Principle

State is immutable between ticks; updates return new state objects. This enables:
- Deterministic replay for debugging
- Parallel processing
- Temporal analysis and inspection

---
