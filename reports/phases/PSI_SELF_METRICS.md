# PSI_SELF_METRICS.md

## Overview

Self-metrics compute 10 system-wide measures from graph state, tracking trends over time for metacognitive insight.

## Metrics

1. **total_nodes** - Graph size
2. **avg_activation** - Average activation across nodes
3. **avg_confidence** - Knowledge reliability
4. **knowledge_growth_rate** - New principles per tick
5. **memory_retention** - Active vs total facts
6. **contradiction_count** - Conflicting beliefs
7. **avg_stability** - Knowledge resilience
8. **entropy_level** - System uncertainty
9. **principle_diversity** - Unique principles count
10. **evolution_rate** - Principle changes per tick

## History Tracking

Each metric maintains:
- Current value
- Last N values (default: 100)
- Trend (up/down/stable)
- Slope for rate of change

## Uses

- Input to meta-reasoning ("why is entropy high?")
- Scheduler priority adjustment
- Emergency alerts (contradictions > threshold)
- Debugging and monitoring

## Performance

- O(n) computation per tick
- Rolling window for history
- Caching between ticks

## Integration

- `meta_reasoning.py` - Explains metric changes
- `cognitive_scheduler.py` - Adjusts budget based on trends
- `emergent_validation.py` - Validates emergent properties

---
