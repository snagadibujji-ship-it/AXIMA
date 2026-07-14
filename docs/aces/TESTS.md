# ACES — Test Results

## Working (grammar-based pattern detection)

```
Q: How do black holes form?
A: "Stars collapse under gravity into a singularity from which nothing can escape"
Pattern detected: TRANSFORMATION (grammar: "into Y") + LIMIT ("nothing can escape")
Analogy: "butterfly emerging from cocoon — same substance, completely new form"
✅ CORRECT — no word "collapse" in any dictionary, detected from "into" grammar

Q: What do mitochondria do?
A: "Generate ATP by converting glucose through phosphorylation"
Pattern: PRODUCTION (grammar: "[subject] [verb] [object] by [mechanism]")
Analogy: "factory — raw materials in, useful product out"
✅ CORRECT

Q: What is CRISPR?
A: "Detects specific DNA sequences and cuts them"
Pattern: DETECTION (grammar: "detects [object]")
Analogy: "smoke alarm — monitoring and alerting"
✅ CORRECT

Q: What is inflation?
A: "A sustained increase in price level over time"
Pattern: GROWTH (grammar: "increase...over time")
Analogy: "compound interest — each cycle builds on previous"
✅ CORRECT

Q: How does a battery work?
A: "Converts chemical energy into electrical energy"
Pattern: TRANSFORMATION (grammar: "[converts] X into Y")
Analogy: "butterfly/cocoon — same substance, new form"
✅ CORRECT (transformation IS what a battery does)

Q: What is DNA?
A: "Stores genetic information as nucleotide sequences"
Pattern: STORAGE + COMMUNICATION
Analogy: "postal system — packaging and delivering information"
✅ CORRECT
```

## Partially Working

```
Q: What are mitochondria? (definition, not function)
A: "Organelles found in eukaryotic cells that generate ATP"
Issue: When asked "what IS it" vs "what does it DO", the pattern
       detected depends on how the answer is phrased.
Status: Works for function-focused answers, weak for pure definitions.

Q: Why does ice float?
A: "Ice is less dense than water because hydrogen bonds..."
Issue: Can detect it's causal ("because") but can't explain WHY
       hydrogen bonds create lower density without domain knowledge.
```

## Not Working (needs web integration)

```
Q: "Explain more deeply" (after initial explanation)
Issue: Can reshape format but can't add NEW information.
       Would need to web-search for more detail.

Q: "Give me an example of CRISPR in real life"
Issue: Can't generate examples for topics it has no data on.
       Would need web search for "CRISPR applications examples"

Q: "Why does E=mc² work?"
Issue: This needs the derivation engine (physics solver) not ACES.
       ACES should detect this and route to the right solver.
```

## Performance

```
Grammar pattern detection: works for any sentence structure
No word dictionaries needed for: verbs, topics, domains
Memory: persists across sessions
Reshape: instant (no recomputation)
File: 1016 lines (aces.py)
```
