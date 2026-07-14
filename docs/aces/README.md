# A.C.E.S — Adaptive Cognitive Explanation System

## The Problem

AXIMA can compute answers but can't EXPLAIN them deeply.
Current approach: hardcoded explanations per topic → doesn't scale.
We can't add keyword templates for infinite topics.

## The Invention

ACES doesn't know WHAT it's explaining.
It understands the SHAPE of knowledge and transforms it into any form.

## How It Works (Current State)

### Grammar-Based Pattern Detection

Instead of matching words like "generate", "produce", "create" (infinite list),
ACES reads the SENTENCE STRUCTURE:

```
"X [verb] INTO Y"          → transformation pattern
"X [verb] Y BY [process]"  → production pattern
"X [verb] FROM A TO B"     → movement pattern
"X [verb] AGAINST Y"       → protection pattern
"nothing can [verb]"       → limit pattern
```

This works for ANY verb — even invented words — because it reads
grammar not vocabulary.

### Pattern → Analogy Mapping

```
transformation → "butterfly emerging from cocoon"
production     → "factory — raw materials in, product out"
movement       → "river carrying things downstream"
regulation     → "thermostat maintaining temperature"
detection      → "smoke alarm monitoring and alerting"
growth         → "compound interest accelerating"
limit          → "wall you cannot climb over"
storage        → "library preserving until needed"
protection     → "armor deflecting damage"
connection     → "bridge enabling interaction"
breakdown      → "digestion breaking into pieces"
communication  → "postal system delivering information"
oscillation    → "heartbeat keeping rhythm"
```

### Knowledge Dimensions (reshape on command)

Same knowledge, user controls the shape:
- "shorter" → one line
- "deeper" → full derivation
- "in points" → bullet list
- "simply" → child-level analogy
- "technically" → expert precision
- "example" → concrete instance
- "why" → causal chain
- "teach me" → build from prerequisites

### Memory

Once explained, NEVER forgotten. Stored to disk.
Next time → instant recall + go to new angle.

## What Works

- ✅ Correct analogies for ANY topic using grammar patterns
- ✅ Works for topics never seen (mitochondria, CRISPR, inflation, blockchain)
- ✅ Reshape on command (points/paragraph/simple/deep/steps)
- ✅ Persistent memory across sessions
- ✅ Structured data path (from solvers) gives GPT-level explanations
- ✅ No keyword dictionaries for topic-specific content

## What's Broken / Needs Fixing

### Problem 1: Intuition is shallow for unknown topics
When ACES only has raw text from web, it can only rephrase.
It can't generate DEEP intuition without understanding the domain.

**Possible fix:** Auto-search web for "why [topic] is important" or
"[topic] explained simply" and extract the intuition from THAT.

### Problem 2: Some grammar patterns overlap
"converts X into Y" matches both production AND transformation.
Currently picks by priority, but sometimes gets wrong one.

**Possible fix:** Use the QUESTION type to disambiguate.
"How does X work?" → prefer transformation/process
"What does X produce?" → prefer production

### Problem 3: Can't go DEEP without domain knowledge
For math/physics (where we have solvers), ACES is amazing.
For web-learned topics, it can't derivate or show steps.

**Possible fix:** Wire ACES into web search — when user says
"go deeper", auto-search for more detail and incorporate.

### Problem 4: Example generation is weak
Can only extract examples FROM the answer text.
Can't generate novel examples for unknown topics.

**Possible fix:** Search web for "examples of [topic]" and use those.

## Architecture

```
src/python/aces.py (1016 lines)

Classes:
  KnowledgeNode      — atomic unit of understanding (all dimensions)
  AnatomyDetector    — what TYPE of answer is this?
  ConceptDecomposer  — break any answer into a node
  ShapeTransformer   — reshape knowledge into any format
  ExplanationMemory  — persistent never-forget storage
  ACES              — main engine (entry point)

Key methods:
  aces.explain(question, answer, structured=None) → full explanation
  aces.reshape(topic, "in points") → different format of same knowledge
```

## The Real Next Step

The system needs to be WIRED INTO:
1. `hybrid_ai.py` pipeline — every answer passes through ACES
2. `online_search.py` — when ACES needs more depth, it searches
3. Solver structured output — math/physics solvers feed ACES rich data

When those connections are made, ACES becomes the universal
explanation layer that makes AXIMA teach like a brilliant tutor.
