# PSI_COGNITIVE_LAWS.md

## Overview

The PSI architecture implements 25 cognitive laws, organized into 4 categories. Each law is a pure function `(state: State, context: Context) -> State` that transforms a node's state based on its environment.

## Law Categories

### Reinforcement Laws (8 laws)
L01: Activation boost from neighbor activation  
L03: Confidence increase from repeated exposure  
L06: Importance growth via usage  
L07: Stability increase from high confidence  
L13: Learning value accumulation  
L14: Prediction accuracy update  
L24: Energy conservation via rest  
L25: Reflection-induced confidence adjustment  

### Decay Laws (6 laws)
L02: Activation decay over time  
L04: Confidence decay for unused nodes  
L08: Stability decay under low activation  
L11: Entropy increase with inactivity  
L20: Importance decay without usage  
L23: Learning value decay  

### Meta Laws (7 laws)
L05: Metacognitive confidence calibration  
L12: Self-metric feedback integration  
L15: Budget-aware activation adjustment  
L17: Attention allocation optimization  
L18: Resource allocation based on importance  
L21: Error-driven state adjustment  
L22: Meta-reflection impact on stability  

### Spreading Laws (2 laws)
L06: Activation spreading to connected nodes  
L19: Novelty-driven spreading enhancement  

### Emergence Laws (3 laws)
L09: Pattern formation via shared activation  
L10: Contradiction generation from conflicting states  
L16: Principle emergence from repeated patterns  

## Implementation Notes

- All laws are idempotent when context is static
- Context provides graph topology, time delta, and neighbor states
- Laws compose; order matters for side-effect chains
- Each law includes validation assertions

---
