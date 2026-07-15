# AXIMA CREATOR v3 — Final Plan (All Weak Points Fixed)

## Current State: BROKEN

```
OUTPUT: "In the grow, Losing everything and rising again everything, with"
THIS IS GARBAGE. Unusable. Must be completely rewritten.

ROOT CAUSES:
  1. Generic word pools don't match topic
  2. Grammar skeletons filled with random words
  3. No actual content/narrative generation
  4. Too short (170 words when 1000 requested)
  5. No character/event persistence between beats
  6. No sentence-level quality check
```

## Weak Points in Previous Plans (FIXED)

```
WEAK POINT 1: "Words from knowledge base" — but knowledge has FACTS not STORY words
  Problem: Knowledge says "gravity is a force" — that doesn't help write a love story
  FIX: Knowledge provides ASSOCIATED CONCEPTS, not direct text.
       "scientist" → [lab, experiment, discovery, late nights, equations, failure, breakthrough]
       These associations are the VOCABULARY POOL for this specific story.
       If no knowledge match → derive from INPUT words only.

WEAK POINT 2: "Grammar skeletons" still produce robotic output
  Problem: Even with right words, "The scientist {verb} the {noun}" sounds mechanical
  FIX: Don't use fill-in-the-blank templates.
       Instead: SENTENCE TYPES that vary structure:
       - Simple: "He worked late."
       - Compound: "He worked late, and the lab grew cold."
       - Complex: "When the data finally aligned, he understood."
       - Fragment: "Gone. All of it."
       - Dialogue: "'It works,' he whispered."
       Each type is a GRAMMAR RULE, not a template with blanks.

WEAK POINT 3: "Tension physics" sounds nice but HOW does it produce SENTENCES?
  Problem: "tension_rising" is abstract — what actual words does it generate?
  FIX: Tension level controls SENTENCE PROPERTIES:
       Low tension → longer sentences, more description, slower pace
       High tension → short sentences, action words, fragments
       Peak → single words, exclamations, reversals
       This is CONCRETE: tension=0.8 → max sentence length = 6 words.

WEAK POINT 4: No way to generate SPECIFIC content
  Problem: Can't produce "The scientist adjusted his glasses and looked at the screen"
           because "glasses" and "screen" aren't in any system
  FIX: SCENE BUILDING from topic.
       Topic: "scientist discovers time travel"
       → Scene elements: scientist(person), lab(place), time machine(object)
       → Actions: researches, builds, tests, fails, discovers
       → Details: late night, flickering screens, coffee gone cold, equations on whiteboard
       These are DERIVED from the topic LOGICALLY, not from word lists.
       "scientist works in" → logically "lab"
       "lab has" → logically "equipment, screens, whiteboards"
       "late work means" → logically "coffee, tired eyes, dim lights"

WEAK POINT 5: Length control doesn't exist
  Problem: Always produces ~170 words regardless of request
  FIX: EXPLICIT word budget system.
       User wants 1000 words → budget = 1000
       Split across beats: 6 beats × ~166 words each
       Each beat generates sentences UNTIL its word budget is reached.
       More beats for longer content, fewer for shorter.

WEAK POINT 6: No dialogue
  Problem: Stories without dialogue feel like summaries, not stories
  FIX: DIALOGUE GENERATION:
       - Characters get names (derived from topic or generated: "the scientist" → "Dr. Karev")
       - Dialogue lines alternate between characters
       - Dialogue reveals conflict/emotion (not just information)
       - Format: "text," character said. (standard fiction format)

WEAK POINT 7: Everything sounds the same
  Problem: Sad story and happy story use same sentence structures
  FIX: MOOD → SENTENCE STYLE mapping:
       Happy: open vowels, rising rhythm, longer sentences, light words
       Sad: closed sounds, falling rhythm, trailing sentences...
       Tense: short. Punchy. Fragments. Questions.
       Peaceful: flowing sentences with commas, and gentle descriptions, like water.
       THIS is real sentence physics — mood shapes HOW you write, not just WHAT.

WEAK POINT 8: Songs don't rhyme properly  
  Problem: Current rhyme engine picks random words from sound groups
  FIX: Rhyme is CONSTRAINED by meaning.
       End of line 1 → identifies rhyme-possible endings
       Line 2 is CONSTRUCTED to end with a meaningful rhyme
       Not: find rhyme word then force it in
       But: write line 2 knowing it MUST end with X, build toward X

WEAK POINT 9: No sense of "this was written by one mind"
  Problem: Each sentence feels disconnected from the last
  FIX: CONNECTIVE TISSUE between sentences:
       - Pronouns referring back ("He", "This", "That moment")
       - Cause-effect links ("Because of this... the next thing")
       - Time progression ("Then", "Later", "By morning")
       - Repeated motifs (same image returning transformed)
       Without these, output reads like random sentences. With them, it flows.
```

## Architecture (Clean)

```
INPUT: "Write a 1000-word story about a scientist who discovers time travel"
       ↓
┌─── STEP 1: PARSE REQUEST ──────────────────────────────────┐
│  Form: story                                                │
│  Length: 1000 words                                         │
│  Topic words: [scientist, discovers, time travel]           │
│  Emotion: wonder → fear → acceptance                        │
│  Tension: curiosity vs consequences                         │
└─────────────────────────────────────────────────────────────┘
       ↓
┌─── STEP 2: BUILD WORLD (from topic, not from word lists) ──┐
│                                                             │
│  CHARACTERS:                                                │
│    - protagonist: "the scientist" / "Dr. Karev"            │
│    - traits: obsessive, brilliant, lonely                   │
│    (derived from: scientist + discovers = driven person)    │
│                                                             │
│  SETTING:                                                   │
│    - primary: laboratory (logically: scientist → lab)       │
│    - details: screens, equations, coffee, dim lights        │
│    (derived from: lab → what labs contain)                  │
│                                                             │
│  OBJECTS:                                                   │
│    - the machine (time travel → needs a device)            │
│    - the notebook (scientist → records findings)           │
│    - the photograph (time travel → memory of past)         │
│    (derived from: what a time travel story needs)          │
│                                                             │
│  VOCABULARY (all from world-building, nothing stored):      │
│    [lab, machine, notebook, data, screen, equations,        │
│     late night, coffee, flickering, discovery, portal,      │
│     past, future, consequences, change, regret, return]    │
│                                                             │
└─────────────────────────────────────────────────────────────┘
       ↓
┌─── STEP 3: PLOT ARC (beats with word budgets) ─────────────┐
│                                                             │
│  Beat 1 (166 words): SETUP — scientist in lab, obsession   │
│  Beat 2 (166 words): DISCOVERY — it works, wonder          │
│  Beat 3 (166 words): FIRST USE — goes back, changes thing  │
│  Beat 4 (166 words): CONSEQUENCE — returns, world changed  │
│  Beat 5 (166 words): CRISIS — can't fix it, despair       │
│  Beat 6 (170 words): RESOLUTION — acceptance, learns       │
│                                                             │
│  Each beat has: tension_level, emotion, key_event, setting  │
│                                                             │
└─────────────────────────────────────────────────────────────┘
       ↓
┌─── STEP 4: GENERATE SENTENCES (per beat, until budget) ────┐
│                                                             │
│  For each beat:                                             │
│    while word_count < budget:                               │
│      1. Pick sentence TYPE based on tension level:          │
│         low → description/compound                         │
│         mid → simple/action                                │
│         high → fragment/dialogue                           │
│      2. Pick CONTENT from world vocabulary + beat context   │
│      3. Add CONNECTIVE to previous sentence                │
│      4. Check: does this advance the beat's event?         │
│      5. Vary: don't repeat same structure twice in a row   │
│                                                             │
│  SENTENCE TYPES (grammar rules, not templates):             │
│    DESCRIPTION: [Character] [verb-ed] [at/in] [detail].   │
│    ACTION: [Character] [verb-ed] [object].                 │
│    COMPOUND: [Clause], and [clause].                       │
│    COMPLEX: When [event], [character] [realized/felt].     │
│    FRAGMENT: [Noun]. [Noun]. [Emotion].                    │
│    DIALOGUE: "[Speech]," [character] [said-variant].       │
│    REFLECTION: [Character] [thought-verb] about [concept]. │
│                                                             │
└─────────────────────────────────────────────────────────────┘
       ↓
┌─── STEP 5: CONNECT & POLISH ───────────────────────────────┐
│                                                             │
│  - Add pronouns (replace repeated character names)         │
│  - Add time markers between beats ("Later that night...")  │
│  - Add motif callbacks (opening image returns at end)      │
│  - Verify word count ±10% of target                        │
│  - Vary sentence openings (no 3 in a row same start)       │
│                                                             │
└─────────────────────────────────────────────────────────────┘
       ↓
OUTPUT: 1000-word story that reads like SOMEONE WROTE IT
```

## For Songs

```
Same architecture but:
  - Beats = verse/chorus/bridge (not plot arc)
  - Chorus REPEATS (generated once, reused)
  - Lines limited to ~8 words (song phrasing)
  - RHYME CONSTRAINT: line endings must rhyme (AABB or ABAB)
  - Build line 2 KNOWING it must end with rhyme of line 1
  - 100 lines = ~12 sections × 8 lines each
```

## For Poems

```
Same architecture but:
  - Short lines (max 8 words)
  - IMAGERY focused (sensory details over narrative)
  - Form constraints: haiku(5-7-5), sonnet(14 lines), free verse
  - More metaphor, less literal
```

## What We Need to Build

```
FILE: src/python/creator/engine_v3.py

class CreatorV3:
    def create(self, request: str) -> str:
        seed = self.parse_request(request)      # Step 1
        world = self.build_world(seed)          # Step 2
        arc = self.plan_arc(seed, world)        # Step 3
        text = self.generate(arc, world, seed)  # Step 4
        polished = self.polish(text)            # Step 5
        return polished

class WorldBuilder:
    """Derives characters, settings, objects, vocabulary from topic."""
    def build(self, topic_words, knowledge_engine) -> World

class SentenceGenerator:
    """Generates sentences from type + world vocabulary + beat context."""
    def generate(self, sentence_type, vocabulary, context) -> str

class Connector:
    """Adds pronouns, time markers, motif callbacks."""
    def connect(self, paragraphs) -> str
```

## Success Criteria

```
- [ ] "1000 word story about scientist" → produces 900-1100 words
- [ ] Every sentence grammatically correct
- [ ] Characters persist (scientist mentioned throughout, not just once)
- [ ] Events connect (cause → effect across beats)
- [ ] NO generic words (no "hollow", "shattered" unless topic is about destruction)
- [ ] ALL content words traceable to topic or logical derivation
- [ ] Song produces actual rhyming lines
- [ ] Different topics produce DIFFERENT vocabulary and feel
- [ ] Output reads like a PERSON wrote it, not a template engine
```

## What Makes This Different From Previous Plans

```
PREVIOUS: "Harvest words then fill grammar skeletons"
THIS:     "Build a WORLD from the topic, then NARRATE events in that world"

The difference:
  Previous: picks random verbs from pools → garbage
  This: derives SPECIFIC actions from SPECIFIC characters in SPECIFIC settings

  "The scientist adjusted his glasses and stared at the screen.
   The numbers didn't lie. It had worked."

  Every word here is DERIVED:
    scientist → wears glasses (logical)
    scientist in lab → has screens (logical)
    discovers something → checks data → numbers (logical)
    time travel works → "it had worked" (plot logic)

  NO word pool. Just LOGICAL DERIVATION from the world model.
```

---

## BEYOND COSMIC: What Nobody Has Done

### 1. RECURSIVE WORLD EXPANSION

```
Current thinking: Build world ONCE from topic, then write.
Beyond: World GROWS as the story progresses.

Beat 1 introduces: scientist, lab
  → World expands: what does lab contain? (screens, coffee, whiteboard)
Beat 2 introduces: discovery
  → World expands: what does discovery create? (machine, portal, danger)
Beat 3 introduces: consequence
  → World expands: what changes? (people missing, buildings different)

The world is NOT static. It EVOLVES with the narrative.
Each beat can ADD new elements that weren't in the original topic.

HOW: After each beat, run inference:
  "if scientist discovers time travel, what logically follows?"
  → needs to test it → needs a subject → goes back → changes something
  → comes back → world is different

This is PLOT DERIVATION FROM LOGIC, not from templates.
```

### 2. CHARACTER PSYCHOLOGY ENGINE

```
Characters aren't just names. They have DRIVES:

DRIVE MODEL:
  want: what they desire (scientist wants → knowledge/truth)
  fear: what they avoid (scientist fears → losing control)
  flaw: what holds them back (scientist's flaw → obsession over balance)
  arc: how they change (obsessed → humbled → wiser)

Every DECISION a character makes comes from drive vs fear vs flaw:
  "Should he use the machine again?"
  want(knowledge) says YES
  fear(consequences) says NO
  flaw(obsession) wins → he uses it again

This produces BELIEVABLE character behavior.
Not random actions. PSYCHOLOGICALLY DERIVED actions.
```

### 3. SENSORY LAYER (Show Don't Tell)

```
Current: "He was scared"  (TELLING — bad writing)
Beyond: "His hands shook. The coffee cup rattled against the saucer." (SHOWING)

RULE: Never state an emotion directly.
Instead: describe PHYSICAL MANIFESTATIONS.

EMOTION → PHYSICAL MAPPING (computed, not listed):
  fear → body: trembling, cold sweat, tight chest, wide eyes
  joy → body: warmth spreading, involuntary smile, lightness
  anger → body: jaw clenching, fists, heat rising, narrowed eyes
  sadness → body: heaviness, slow movement, unfocused eyes, silence

For each emotion in a beat:
  1. Identify the emotion (from tension curve)
  2. Map to 2-3 physical manifestations
  3. Weave INTO the action (not as separate sentences)

  "He reached for the switch — his hand hovering,
   trembling an inch away from everything changing."

  Fear is SHOWN through the trembling hand, not STATED.
```

### 4. MICRO-RHYTHM ENGINE

```
Every paragraph has an INTERNAL RHYTHM that matches emotion:

CALM SCENE:
  Long sentence with commas, flowing description, unhurried pacing.
  Another long one, perhaps with a gentle observation about the light.
  Then a medium one, settling into the moment.

TENSE SCENE:
  Short. Direct.
  He ran.
  The door — locked.
  Something behind him. Getting closer.
  No time.

REVELATION SCENE:
  Build up with medium sentences, each adding a detail.
  The picture becoming clearer, piece by piece.
  Until one short sentence changes everything:
  "It was him."

The RHYTHM is the story. Not just words — the SHAPE of text on page.

HOW: Sentence length sequence follows a PATTERN per emotion:
  calm = [15, 18, 12, 16, 14] (all medium-long, gentle variation)
  tense = [3, 4, 2, 6, 2, 1] (short bursts, decreasing)
  reveal = [10, 12, 14, 16, 3] (building then snap)
```

### 5. SUBTEXT ENGINE

```
Great writing says two things at once:
  Surface: what's literally happening
  Subtext: what it MEANS emotionally

Example:
  Surface: "She rearranged the books on the shelf for the third time."
  Subtext: She's avoiding the conversation. She's anxious. She needs control.

HOW TO GENERATE SUBTEXT:
  1. Identify the REAL emotion of the moment (anxiety)
  2. Find a DISPLACEMENT ACTIVITY (something physical that expresses it indirectly)
     anxiety → organizing, cleaning, fidgeting, checking phone
  3. Write the ACTIVITY, let reader infer the EMOTION

  The reader feels smarter because they "figured it out."
  This is what makes writing feel LITERARY vs JUVENILE.
```

### 6. VOICE CONSISTENCY (Writing Style DNA)

```
Each story has ONE narrative voice that stays consistent:

FIRST PERSON PAST: "I walked into the lab that night knowing something was different."
THIRD PERSON CLOSE: "He walked into the lab that night. Something was different."
OMNISCIENT: "The scientist walked into his lab, unaware that this night would change everything."

Voice parameters (set ONCE, maintained throughout):
  person: first/third
  tense: past/present
  distance: close/omniscient
  formality: casual/literary
  sentence_length_mean: varies by style

ONCE SET, every sentence generated MUST match these parameters.
No accidental tense switches. No POV breaks. CONSISTENCY.
```

### 7. SURPRISE THROUGH LOGICAL INVERSION

```
Predictable writing: setup → expected outcome
Great writing: setup → LOGICAL BUT UNEXPECTED outcome

HOW:
  1. Build expectation (scientist will succeed)
  2. At the beat before climax, ask: "What would be logical BUT unexpected?"
  3. The INFERENCE ENGINE can find this:
     "time travel + success → what could go wrong LOGICALLY?"
     → "he succeeds but discovers HE was the one who caused the problem in the first place"

  This is a TWIST that's both surprising AND logical.
  Derived from inference, not random.
```

### 8. PARAGRAPH ARCHITECTURE

```
Each paragraph has a PURPOSE and an internal arc:

PARAGRAPH TYPES:
  SCENE: Set the visual (where, when, what it looks like)
  ACTION: Something happens (events, movement, change)
  REFLECTION: Character processes what happened (thoughts, realizations)
  DIALOGUE: Characters interact (reveals conflict/emotion)
  TRANSITION: Move between scenes (time skip, location change)

A good story ALTERNATES these:
  Scene → Action → Dialogue → Reflection → Transition → Scene → Action...

Never two REFLECTIONS in a row (boring).
Never three ACTIONS in a row (exhausting).
The RHYTHM of paragraph types creates PACING.
```

### 9. ENDING = TRANSFORMED BEGINNING

```
The most satisfying endings ECHO the opening but CHANGED:

Opening: "The lab was quiet. The kind of quiet that comes before everything changes."
Ending: "The lab was quiet again. But this time, he didn't need it to change."

SAME IMAGE. DIFFERENT MEANING.
The reader feels the CHARACTER'S GROWTH through the REPETITION.

HOW:
  1. Store the opening image/phrase
  2. At final beat: bring it back
  3. Change ONE key word that shows the transformation
  4. This creates circular structure = completeness feeling
```

### 10. MULTI-THREADED NARRATIVE

```
For longer pieces (1000+ words), ONE thread is boring.
Add a SECONDARY thread:

MAIN: Scientist builds time machine
SECONDARY: His daughter is growing up without him (he's always in the lab)

These INTERSECT at the climax:
  He uses the machine to go back — not to change science — but to be at her recital.

The SECONDARY thread gives EMOTIONAL STAKES to the MAIN thread.

HOW TO DERIVE SECONDARY THREAD:
  Look at character's FLAW: "obsession over balance"
  What does obsession COST? → relationships, health, presence
  WHO pays the cost? → someone who loves them (family, friend)
  This becomes the secondary thread — AUTOMATICALLY DERIVED from character psychology.
```

## Final Architecture (Complete)

```
Parse Request
  ↓
Build World (characters + setting + objects + vocabulary)
  ↓
Derive Character Psychology (want + fear + flaw + arc)
  ↓
Plan Arc (beats with word budgets)
  ↓
For each beat:
  ├── Expand World (new elements from inference)
  ├── Pick Paragraph Types (scene/action/dialogue/reflection)
  ├── For each paragraph:
  │     ├── Pick Sentence Type based on tension + mood
  │     ├── Generate from world vocabulary + beat context
  │     ├── Apply Sensory Layer (show don't tell)
  │     ├── Apply Micro-Rhythm (sentence length pattern)
  │     └── Add Subtext (displacement activities)
  ├── Connect paragraphs (transitions, pronouns, time)
  └── Check word budget
  ↓
Apply Surprise (logical inversion at climax)
  ↓
Apply Ending Echo (transformed beginning)
  ↓
Final Polish (voice consistency, vary openings, motif callbacks)
  ↓
OUTPUT
```
