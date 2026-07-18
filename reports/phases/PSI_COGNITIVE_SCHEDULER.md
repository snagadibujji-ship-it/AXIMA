# PSI_COGNITIVE_SCHEDULER.md

## Overview

The cognitive scheduler manages computational budget allocation across 7 task types, ensuring efficient resource utilization while prioritizing high-impact activities.

## Tasks

| Task | Priority | Interval | Cost (ms) |
|------|----------|----------|-----------|
| Physics tick | 1 | Every | 10 |
| Spreading | 2 | Every 3 | 5 |
| Consolidation | 3 | Every 5 | 8 |
| Decay | 2 | Every | 3 |
| Evolution | 3 | Every 10 | 12 |
| Metrics | 4 | Every 5 | 2 |
| Meta-reasoning | 5 | Optional | 15 |

## Algorithm

`what_runs_now(budget=50ms)` returns tasks within budget:

1. Sort tasks by priority
2. Iterate, accumulating cost
3. Stop when budget exhausted
4. Return list of scheduled tasks

## Dynamic Adjustment

- Low activity → reduce intervals
- High contradiction → boost evolution priority
- High entropy → increase meta-reasoning

## Integration

- Called by `cognitive_runtime.py` each tick
- Used by `cognitive_physics.py` for selective updates
- Feeds into performance monitoring

## Benefits

- Adapts to system state
- Prevents overload
- Prioritizes high-impact operations

---
