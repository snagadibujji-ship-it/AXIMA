# ACES — Gaps & Fix Ideas

## Gap 1: Still uses some word-matching

**Where:** Pattern detection still has a few word-based checks like
`\bdetects?\b` for detection, `\bstored?\b` for storage.

**Why it's a problem:** If a sentence uses a synonym we didn't list,
it won't match.

**Fix idea:** Instead of checking for specific verbs, check for
sentence ROLES:
- Subject + transitive verb + object = some kind of action
- The PREPOSITION after the verb tells you the pattern:
  - "into" = transformation
  - "from...to" = movement
  - "against" = protection
  - "by" = production (input→output via mechanism)
  
Pure preposition-based detection would need ZERO word lists.

## Gap 2: Can't generate deep intuition for unknown topics

**Where:** `_generate_intuition()` for web-learned answers just
rephrases the sentence.

**Why:** Without domain knowledge, it can't explain WHY something
is true — only THAT it's true.

**Fix idea:** 
- When user asks "why", auto-search: "why [core fact]" 
- Extract explanation from top result
- Feed that as a second-level answer to ACES
- Now ACES has BOTH the fact AND the reason

## Gap 3: Can't generate examples for unknown topics

**Where:** `_find_example()` returns empty for topics where the
answer text doesn't contain "such as" or "found in".

**Fix idea:**
- Auto-search: "[topic] real world example"
- Or: construct from analogy — if pattern is "production",
  example is "like how [analogy subject] produces [analogy output]"

## Gap 4: Memory recall sometimes uses stale data

**Where:** `ExplanationMemory.recall()` pulls from first time
a topic was explained, even if we've improved since.

**Fix idea:** Version the memory — when ACES code changes,
invalidate old nodes and regenerate on next ask.

## Gap 5: Analogy sometimes picks wrong pattern

**Where:** "converts X into Y" matches both production and
transformation. Battery = production (makes electricity) but
ACES says transformation (changes form).

**Both are correct!** This is actually not a bug — batteries
DO transform energy. The "problem" is that the user might
expect one over the other.

**Fix idea:** Show BOTH patterns when multiple match:
"Think of it as both a transformation (one form → another)
AND a production (input → useful output)"

## Gap 6: No way to handle MULTI-STEP processes

**Where:** "How does photosynthesis work?" has 6+ steps but
ACES can only detect one pattern for the whole sentence.

**Fix idea:** Split answer into sentences. Detect pattern for
EACH sentence. Chain them: "First [pattern1], then [pattern2]..."

## Gap 7: Universal — still can't explain "why" from first principles

**The hard truth:** Without either:
1. A domain-specific solver (like we have for physics/math)
2. Web search for deeper information
3. A causal knowledge graph

ACES cannot generate WHY something is true. It can only
restructure WHAT it already has.

**This is the fundamental limit of rule-based explanation
without external knowledge.** The fix is integration:
- For math/physics: use solver structured data ← DONE
- For everything else: auto-search web for depth ← TODO
