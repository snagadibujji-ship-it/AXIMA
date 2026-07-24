# AXIMA Phase 11 → Ultra-Cosmic Cognitive OS Master Plan

**Status:** Proposed authoritative engineering plan  
**Plan version:** 1.0  
**Date:** 2026-07-24  
**Scope:** Documentation and future work definition; this document does not itself change runtime behavior  
**Strategy:** Evolve the current Python architecture; do not rewrite it  
**North star:** Build the highest-assurance, highest-utility deterministic cognitive operating system per byte of memory in its declared capability domains

---

## 0. Executive mandate

AXIMA will not attempt to imitate a giant language model. It will become a compact cognitive operating system that compiles requests into typed cognitive transactions, retrieves only relevant verified structure, constructs bounded plans, executes explicit tools and symbolic rules, verifies every releasable claim, and commits only governed knowledge into versioned memory.

The system's intelligence must come from:

1. explicit semantic structure;
2. deterministic retrieval;
3. bounded multi-resolution reasoning;
4. proof-obligated planning;
5. domain tools and exact computation;
6. independent verification;
7. executable, provenance-rich memory;
8. semantic compression;
9. governed improvement;
10. reproducible state snapshots.

“Ultra-Cosmic” is a target level, not a marketing assertion. AXIMA may claim superiority only on named tasks for which independently reproducible evidence demonstrates better correctness, verification, determinism, resource efficiency, or auditability than named baselines. It must never convert architectural sophistication, test count, or internal benchmark success into an unsupported claim of general intelligence.

### 0.1 The Phase 11 thesis

> Do not store intelligence as opaque learned weights. Store it as compressed, typed, versioned, executable, and independently verified structure.

### 0.2 The Ultra-Cosmic thesis

> Treat every answer as a reproducible build artifact: compiled from a declared request, an immutable world-state snapshot, explicit rules and evidence, a bounded plan, tool results, and machine-checkable verification receipts.

### 0.3 What “king of AIs” is allowed to mean

For AXIMA, this phrase is translated into a measurable objective:

- highest verified task success per MiB on supported workloads;
- exact or proof-backed answers where probabilistic systems are unreliable;
- byte-for-byte semantic reproducibility under the same state snapshot;
- complete claim-to-evidence traceability;
- calibrated abstention outside supported boundaries;
- safe cumulative improvement without opaque retraining;
- operation within a hard 50 MiB reference runtime envelope.

It does **not** mean universal intelligence, unrestricted autonomous action, human equivalence, consciousness, or superiority without third-party evaluation.

### 0.4 Capability priorities and dependency rule

Product capability is prioritized in this order:

1. better reasoning;
2. better mathematics;
3. better coding;
4. better planning;
5. better retrieval;
6. better verification;
7. durable executable memory;
8. RAM optimization;
9. production hardening.

This is an outcome priority, not permission to violate dependencies. Contracts, snapshots, retrieval, verification, and persistence may be implemented before deeper domain features because they are prerequisites for trustworthy improvement. Intelligence drives the roadmap, but **every merged stage must remain inside its declared resource budget**; the dedicated optimization workstream comes later only because premature micro-optimization must not dictate the cognitive design.

### 0.5 Intended audiences

- **Initial:** a personal research platform for deterministic symbolic intelligence.
- **Medium term:** an open-source developer platform with stable contracts and audited domain packs.
- **Long term:** a production cognitive operating system for developers, researchers, education, scientific computing, companies, robotics, and low-resource deployments.

Each audience receives the same semantic core and constitutional guarantees. Larger deployments may add capacity, but they cannot silently weaken determinism, verification, provenance, or governance.

---

## 1. Constitutional invariants

These invariants override feature pressure, benchmark pressure, and schedule pressure.

1. **Zero learned parameters:** The reference runtime contains no trained neural weights, pretrained embeddings, hidden model calls, or remote LLM dependency.
2. **Determinism by snapshot:** Given the same normalized request, immutable state snapshot, configuration, tool versions, platform contract, and budget, AXIMA must produce the same semantic result and decision trace.
3. **Verification before release:** A claim requiring verification cannot be released at a stronger truth level than its completed verifier receipts allow.
4. **Retrieval before synthesis:** Facts, rules, prior skills, failure cases, and proof artifacts must be retrieved before an answer is composed.
5. **Planning before side effects:** No state-changing tool operation may execute without a validated plan node, authorization, budget, and rollback policy.
6. **No generator self-grading:** Verification independence must be explicit and enforceable.
7. **Canonical memory is earned:** Raw conversations, unverified outputs, and successful-looking traces cannot become canonical knowledge automatically.
8. **Uncertainty is conserved:** Rendering, aggregation, and repeated agreement from correlated sources may not increase confidence without new independent evidence.
9. **Abstention is success when warranted:** Unsupported, ambiguous, stale, or unverifiable requests must produce bounded clarification or abstention—not confident fabrication.
10. **Backward compatibility by default:** Public contracts evolve additively; replacements must reach feature and test parity before retirement of legacy paths.
11. **Resource budgets are executable:** Time, steps, recursion, disk I/O, trace size, cache size, and resident memory are enforced, not merely documented.
12. **Governance cannot self-weaken:** AXIMA cannot grant itself capabilities, alter its approval policy, erase audit history, or promote its own unreviewed system changes.
13. **Every module has measurable value:** A module without a benchmark, resource budget, failure policy, and integration path remains experimental.
14. **No benchmark theatre:** Expected outputs are not changed merely to match current behavior; public smoke tests cannot support frontier-level claims.
15. **No unbounded cognition:** Infinite logic, unrestricted recursion, unlimited graph expansion, and unconstrained self-modification are prohibited in the production runtime.

---

## 2. Precise operating definitions

### 2.1 Zero learned parameters

**Permitted:**

- deterministic parsers, grammars, finite-state machines, rewrite systems, decision tables;
- exact numerical and symbolic algorithms;
- curated facts, definitions, rules, theorems, templates, and examples;
- lexical indices, BM25/TF-IDF-style statistics computed from local corpora;
- non-learned hashes, fingerprints, sketches, and sparse signatures;
- governed rules or skills extracted from verified traces;
- local compilers, interpreters, theorem provers, SAT/SMT tools, and test runners when declared as optional tools;
- user-supplied data, provided its provenance and trust status remain explicit.

**Prohibited in the zero-parameter reference profile:**

- trained neural network weights of any size;
- pretrained sentence or token embeddings;
- external LLM/API calls hidden behind plugins;
- model-generated rules promoted without independent tests and governance;
- undeclared online services that influence answers;
- probabilistic outputs whose seed or algorithm is not captured by the state snapshot.

### 2.2 Determinism

“Same input, same output forever” is incompatible with legitimate knowledge updates. The binding definition is:

```text
semantic_result = F(
    normalized_task,
    state_snapshot_id,
    runtime_version,
    configuration_hash,
    declared_tool_versions,
    resource_budget,
    platform_contract
)
```

A learning event creates a **new immutable state version**. Replaying against the old state must reproduce the old semantic result. Replaying against the new state may produce an improved result, and the state transition must be auditable.

Wall-clock timestamps, random UUIDs, process IDs, and latency measurements are nondeterministic metadata. They must not affect semantic hashes or route selection. Stable IDs use content hashes or monotonic transaction sequence numbers scoped to a state commit.

### 2.3 The 50 MiB runtime envelope

The production reference profile must remain capable of operating under **50 MiB peak process RSS**, not merely Python heap size.

The gate includes:

- Python interpreter and loaded shared libraries attributable to the process;
- imported AXIMA modules;
- active plugin state;
- working/session memory resident in process;
- retrieval indices and mapped pages resident in RSS;
- caches, buffers, traces, and verifier state;
- one active request in the reference single-worker workload.

It excludes:

- operating-system memory outside the process;
- nonresident corpus files on disk;
- filesystem page cache not counted in process RSS;
- optional external tools running as separately budgeted processes.

The limit must be measured separately on Linux, Windows, macOS, ARM Linux/Raspberry Pi, and Android-compatible Python. The official claim is valid only for platforms passing the same workload and measurement protocol. Concurrency has a service-level budget; “50 MiB” must never be ambiguously multiplied by worker count.

### 2.4 Intelligence

AXIMA intelligence is evaluated as a vector, not one score:

```text
I = {
  supported_coverage,
  verified_correctness,
  proof_strength,
  retrieval_quality,
  plan_success,
  recovery_success,
  abstention_calibration,
  memory_reuse_gain,
  determinism,
  latency,
  memory_cost,
  audit_completeness
}
```

A release may improve one dimension only if it does not silently regress constitutional dimensions.

---

## 3. Evidence-grounded current baseline

This plan begins from the repository as audited on 2026-07-24.

### 3.1 Observed assets

- 118 Python files under `src/axima/`.
- 795 explicit `test_*` function definitions; the last full suite reported 837 executed outcomes because parametrization and collection can expand definitions.
- Nine plugins load on the exercised public API path.
- Approximately 144 MiB of corpus data under `data/`, plus approximately 2.1 MiB under `src/data/`.
- Measured Linux peak RSS in the audit environment (`ru_maxrss`, reported in KiB on Linux):
  - Python process start: 8,580 KiB (approximately 8.38 MiB);
  - after importing `axima.api`: 18,284 KiB (approximately 17.86 MiB);
  - after constructing `Axima`: 18,284 KiB (approximately 17.86 MiB);
  - after first query `solve x^2 - 4 = 0`: 18,384 KiB (approximately 17.95 MiB).
- Current first-query result was `x = ±2`, routed to `math_solver`, with nine loaded plugins.

These figures are a promising baseline, not proof of the final 50 MiB gate. Corpus retrieval, long sessions, trace growth, concurrent requests, platform variance, and external tool use were not covered by that single smoke measurement.

### 3.2 Foundations to preserve

| Existing foundation | Phase 11 role |
|---|---|
| `Axima` public API | Stable compatibility boundary and eventual cognitive transaction entry point |
| `MeaningIR` / compiler | Base semantic representation; extend rather than replace wholesale |
| `EpistemicContract` | Base answer-by-contract mechanism |
| `IntentLattice` | Initial multi-candidate routing layer |
| `PlanDAG` / `CognitivePlanner` | Base planning graph and planner contracts |
| plugin loader and capability registry | Domain execution boundary |
| `FourPlaneMemory` | Compatibility facade over persistent tiered memory |
| `KnowledgeIndex` | Base typed subject/relation/object retrieval |
| `RealityLedger`, claims, derivation, provenance | Truth-maintenance and evidence foundations |
| `VerificationConstellation` and domain verifiers | Independent claim-verification foundations |
| `SkillFoundry`, `RealityGapLoop`, `GovernanceGate` | Governed learning and executable-memory foundations |
| agency transactions and capability tokens | Side-effect safety and rollback foundations |
| benchmark manifests, judges, immune system | Evaluation and contamination-control foundations |
| lifecycle, backup, metrics, traces | Production operations foundations |
| specialist math/physics/knowledge/causal/document modules | Domain capability foundations |

### 3.3 Critical gaps that Phase 11 must close

1. `Axima.query()` initializes `CognitivePlanner` but does not call it; the documented planning stage is absent from the live path.
2. Public-path `_verify()` performs only two superficial non-empty checks, and the returned `verification_info` is discarded when the response is built.
3. The full `VerificationConstellation` exists but is not the mandatory release gate for public responses.
4. Memory is volatile, process-local, and keyword-scanned. The API attempts to bound episodic growth by checking an `_entries` attribute, while the current episodic store uses `_episodes`, so that guard does not reliably bound the live list. Memory also lacks complete confidence, verification state, version lineage, checksums on import, dependency edges, and durable transactional persistence.
5. Query recording stores truncated query/answer episodes, not reusable verified strategies or executable skills.
6. `SkillFoundry`, `RealityGapLoop`, prediction, experiments, governance, and the reality ledger are tested separately but disconnected from the public cognitive transaction.
7. The microkernel cosmic path remains basic classification plus registry dispatch and can fall back to legacy without the full semantic, planning, retrieval, and verification pipeline.
8. Confidence is largely heuristic and engine-name based rather than calibrated from claim-level evidence and verifier coverage.
9. The built-in fallback knowledge table is disconnected from the larger on-disk corpus and typed knowledge infrastructure.
10. The current default resource budget is 256 MiB, which conflicts with the Phase 11 reference envelope.
11. Existing documentation contains stale test/module counts and unproven latency or memory assertions; documentation truth must become release-gated.
12. The 45-case public evaluation is useful as a regression smoke suite but far too small and too visible to justify broad intelligence claims.

### 3.4 Explicit non-goals for Phase 11

- no ground-up Rust rewrite;
- no renaming/reorganizing modules merely to resemble a proposed directory tree;
- no replacement of stable public APIs without adapters;
- no mandatory neural or remote model component;
- no self-deployment or unrestricted autonomous code modification;
- no claim of general intelligence based on architecture alone;
- no production use of mathematically impressive constructs without a bounded use case, benchmark, and resource proof.

---

## 4. Target architecture: the cognitive transaction kernel

Every request becomes an atomic, replayable cognitive transaction.

```text
Raw Input / Attachments
        │
        ▼
[1] Input Shield + Capability Boundary
        │
        ▼
[2] State Snapshot Resolver
        │
        ▼
[3] Meaning + Intent + Contract Compiler
        │
        ▼
[4] Unknown/Ambiguity Boundary
        │
        ├── clarification / abstention when required
        ▼
[5] Deterministic Retrieval Lattice
        │
        ▼
[6] Multi-Resolution Strategy Portfolio
        │
        ▼
[7] Proof-Obligated PlanDAG
        │
        ▼
[8] Capability-Sandboxed Execution
        │
        ▼
[9] Claim Graph + Verification Constellation
        │
        ├── repair loop (bounded)
        ├── conditional release
        └── abstention/block
        ▼
[10] Constrained Answer Synthesizer
        │
        ▼
[11] Memory Candidate Extraction
        │
        ▼
[12] Governance + Atomic Commit to New State Version
        │
        ▼
Proof-Carrying Response + Snapshot/Trace References
```

### 4.1 Transaction properties

A cognitive transaction must provide:

- **Atomicity:** Canonical memory changes commit together or not at all.
- **Consistency:** Schema, graph, proof, and policy invariants hold before and after commit.
- **Isolation:** Concurrent sessions cannot observe partially promoted memory.
- **Durability:** Approved commits survive restart with checksummed persistence.
- **Replayability:** Inputs and immutable references reconstruct the semantic decision path.
- **Budgetability:** Every expansion and execution step consumes explicit resources.
- **Reversibility:** Promoted rules and skills can be revoked by versioned rollback without deleting audit history.

### 4.2 Architectural planes

The existing four planes remain and gain two cross-cutting planes:

1. **Meaning plane:** parsing, normalization, ambiguity, semantic hashes.
2. **Control plane:** routing, planning, scheduling, execution, recovery, budgets.
3. **Evidence plane:** claims, provenance, derivations, verification, confidence.
4. **Expression plane:** constrained rendering, explanation, output schemas.
5. **Memory plane (cross-cutting):** retrieval, state versions, compaction, promotion, truth maintenance.
6. **Governance plane (cross-cutting):** capability policy, approvals, audit, risk, lifecycle.

Memory and governance are not “final pipeline stages”; they constrain every stage.

### 4.3 Incremental module map

Do not create a second competing architecture. Extend current packages with focused modules only when a real contract and benchmark require them.

| Area | Preserve | Candidate additions |
|---|---|---|
| Contracts | `contracts/query.py` | `contracts/cognitive.py`, `contracts/state.py`, schema migrations |
| Kernel | `kernel/runtime.py`, scheduler, registry | `kernel/cognitive_loop.py`, `kernel/state_snapshot.py`, `kernel/budget_governor.py` |
| Semantics | `MeaningIR`, compiler, checksum | task normalization, semantic compression IR, ambiguity policies |
| Epistemics | contracts, entropy, unknowns | release policy, risk profile, claim obligations |
| Planning | planner, PlanDAG, transactions | obligations, deterministic scoring, repair executor, checkpoints |
| Memory | four-plane facade, recall | schema, SQLite store, executable DSL, compactor, promotion pipeline |
| Knowledge | corpus, index, crystals | deterministic retrieval lattice, ranking, dependency graph |
| Verification | constellation and domain verifiers | mandatory release gate, coverage policy, receipt store |
| Responses | proof-carrying response | constrained synthesizer, claim-to-text alignment, round-trip checker |
| Cognition | skills, learning, governance | integrated governed learning coordinator |
| Production | lifecycle, API, backup | migrations, snapshot manager, platform RSS monitor |
| Benchmarks | manifests, judges, immune system | Phase 11 domain suites, resource and replay harnesses |

A candidate module is added only after an ADR states: responsibility, boundary, benchmark, memory budget, failure behavior, migration path, and owner.

---

## 5. Canonical contracts

All contracts are schema-versioned, additive whenever practical, deterministically serialized, and content-addressed. Names below describe target semantics; exact Python APIs must be finalized through ADRs and contract tests.

### 5.1 CognitiveTaskEnvelope

```json
{
  "schema_version": 1,
  "task_id": "content-addressed-or-transaction-id",
  "input_text": "Solve x^2 - 5x + 6 = 0",
  "normalized_input_hash": "sha256:...",
  "session_id": "optional",
  "state_snapshot_id": "state:sha256:...",
  "domain_candidates": ["mathematics"],
  "task_type_candidates": ["solve"],
  "constraints": {
    "exact_only": true,
    "show_steps": true,
    "allowed_inference_types": ["deduction", "calculation"],
    "max_depth": 12
  },
  "risk_profile": {
    "class": "normal",
    "impact": "low",
    "freshness_required": false
  },
  "budget": {
    "wall_time_ms": 1200,
    "rss_limit_mib": 50,
    "max_steps": 100,
    "max_retrieval_candidates": 128,
    "max_trace_bytes": 65536,
    "max_disk_read_bytes": 4194304
  },
  "output_contract": {
    "schema": "structured_answer.v1",
    "truth_floor": "derived",
    "include_trace_summary": true
  }
}
```

### 5.2 StateSnapshot

```json
{
  "snapshot_id": "state:sha256:...",
  "parent_snapshot_id": "state:sha256:...",
  "runtime_version": "...",
  "code_revision": "git:...",
  "config_hash": "sha256:...",
  "rule_pack_roots": ["sha256:..."],
  "knowledge_root": "sha256:...",
  "memory_root": "sha256:...",
  "governance_policy_hash": "sha256:...",
  "tool_manifest_hash": "sha256:...",
  "locale_policy": "portable-v1",
  "numeric_policy": "exact-first-v1",
  "created_by_transaction": "txn:..."
}
```

The snapshot captures all semantic influences. It does not include volatile latency, wall-clock display time, or process-local IDs.

### 5.3 PlanNode

```json
{
  "node_id": "plan-node:sha256:...",
  "op": "retrieve|derive|compute|execute|verify|repair|synthesize|commit",
  "capability": "math.exact_algebra.v2",
  "input_refs": ["artifact:..."],
  "output_types": ["claim_set.v1"],
  "preconditions": ["expression.parsed", "domain.nonzero_denominator"],
  "postconditions": ["candidate_roots.produced"],
  "proof_obligations": ["roots.substitute_to_true", "domain.constraints_preserved"],
  "dependencies": ["node:..."],
  "fallback_nodes": ["node:..."],
  "side_effect_class": "none",
  "authorization_ref": null,
  "estimated_cost": {"time_ms": 20, "memory_kib": 64, "steps": 4},
  "deterministic": true,
  "tie_break_key": "stable-content-hash"
}
```

### 5.4 Claim and EvidenceItem

```json
{
  "claim_id": "claim:sha256:...",
  "statement_ir": {"predicate": "equals", "arguments": ["x", 2]},
  "rendered_statement": "x = 2 is a solution",
  "claim_type": "derived",
  "scope": "under declared equation domain",
  "assumptions": [],
  "evidence_refs": ["evidence:..."],
  "derivation_ref": "derivation:...",
  "dependency_claims": ["claim:..."],
  "generator": "math.exact_algebra.v2",
  "risk_class": "normal"
}
```

```json
{
  "evidence_id": "evidence:sha256:...",
  "source_type": "curated|user|tool|derived|formal",
  "source_ref": "source:...",
  "content_hash": "sha256:...",
  "valid_time": [null, null],
  "transaction_time": 184000,
  "trust_tier": "T0|T1|T2|T3|T4",
  "independence_group": "math-substitution-verifier",
  "status": "candidate|verified|rejected|revoked"
}
```

### 5.5 VerificationReceipt

```json
{
  "receipt_id": "receipt:sha256:...",
  "claim_id": "claim:sha256:...",
  "verifier": "math.substitution.v2",
  "verifier_version": "2.0.0",
  "independence_group": "substitution",
  "input_hashes": ["sha256:..."],
  "result": "pass|warn|fail|not_applicable",
  "counterexample_refs": [],
  "coverage": ["equation-satisfaction", "domain"],
  "confidence_interval": [0.999, 1.0],
  "resource_cost": {"time_ms": 2, "memory_kib": 12},
  "receipt_hash": "sha256:..."
}
```

### 5.6 TraceRecord

Trace records reference artifacts instead of duplicating large payloads:

```json
{
  "transaction_id": "txn:...",
  "sequence": 17,
  "stage": "verify",
  "module": "verification.constellation",
  "action": "claim_release_decision",
  "input_refs": ["claim:..."],
  "output_refs": ["receipt:..."],
  "decision": "pass",
  "budget_delta": {"time_ms": 4, "rss_kib": 8},
  "semantic_hash": "sha256:..."
}
```

### 5.7 Contract compatibility rules

- New fields are optional with deterministic defaults until a major schema transition.
- Readers reject unknown required semantics but preserve unknown optional fields when round-tripping.
- Every migration is pure, versioned, reversible where possible, and tested against golden fixtures.
- No mutable Python object identity may appear in serialization.
- Dictionary ordering, float rendering, Unicode normalization, line endings, and timezone handling use canonical policies.

---
## 6. Persistent, executable, governed memory

Phase 11 transforms memory from passive process-local storage into a versioned knowledge substrate. `FourPlaneMemory` remains the compatibility facade while durable storage and retrieval move behind it.

### 6.1 Target memory tiers

| Target tier | Purpose | Current mapping | Residency policy |
|---|---|---|---|
| T0 Working buffer | Current task, active goals, top-k records, live plan, verification state | Working memory | RAM only; hard bounded; cleared at transaction end |
| T1 Session state | User-approved continuity, recent task state, unresolved clarifications | Selected episodic memory | Primarily disk; tiny hot window in RAM; TTL and sensitivity enforced |
| T2 Semantic store | Verified facts, definitions, relations, canonical compressed structures | Semantic memory + knowledge index | SQLite/packs on disk; bounded summaries/index pages in RAM |
| T3 Procedural store | Verified strategies, RuleIR, SkillIR, templates, recovery recipes, failure signatures | Procedural memory + SkillFoundry | Versioned immutable packages; lazy-loaded |
| T4 Proof/invariant store | High-trust proofs, invariants, verifier artifacts, counterexamples | Evidence/derivation modules | Content-addressed, append-only, strongest promotion gate |
| T5 Episodic audit | Outcomes, rejected candidates, failures, corrections, transaction references | Episodic memory + ledgers | Append-only and compacted; raw sensitive payloads minimized |

The public four-plane vocabulary remains valid. T4 and T5 are specialized physical stores exposed through the evidence and episodic interfaces rather than breaking the existing API.

### 6.2 Canonical MemoryRecord

```json
{
  "schema_version": 1,
  "memory_id": "mem:sha256:...",
  "record_version": 3,
  "parent_versions": ["mem:sha256:..."],
  "tier": "semantic|procedural|proof|episodic",
  "kind": "fact|rule|lemma|strategy|skill|template|failure|counterexample|trace_summary",
  "canonical_key": "math.quadratic.discriminant",
  "summary": "Use the discriminant to classify real roots.",
  "payload_ref": "pack:sha256:...#offset:length",
  "symbol_keys": ["quadratic", "discriminant", "roots"],
  "type_keys": ["math.rule"],
  "relation_keys": ["classifies", "depends_on"],
  "preconditions": ["expression.degree == 2"],
  "postconditions": ["root_classification.produced"],
  "failure_modes": ["non-polynomial-input", "unsupported-coefficient-domain"],
  "provenance_refs": ["source:..."],
  "evidence_refs": ["evidence:..."],
  "dependency_refs": ["mem:..."],
  "contradiction_refs": [],
  "verification_state": "quarantined|candidate|verified|canonical|revoked",
  "verifier_receipts": ["receipt:..."],
  "confidence_interval": [0.97, 0.995],
  "valid_time": [null, null],
  "transaction_sequence": 184000,
  "retention": "session|short|long|permanent",
  "sensitivity": "public|internal|private|restricted",
  "content_hash": "sha256:...",
  "created_in_snapshot": "state:...",
  "superseded_by": null
}
```

Required corrections to the present memory model:

- preserve `created_at`, `expires_at`, and version lineage during import/export;
- checksum every record and pack;
- attach verification state, confidence interval, provenance IDs, and dependency IDs;
- distinguish transaction time from real-world valid time;
- represent deletion as a tombstone/revocation, not silent historical erasure;
- enforce sensitivity at read time, not only write time;
- cap every in-memory collection with deterministic eviction;
- reject schema-incompatible or tampered imports before they affect retrieval.

### 6.3 Executable memory: RuleIR and SkillIR

Executable memory must **not** store arbitrary Python for direct execution. It stores a small declarative DSL interpreted by a capability-restricted engine.

Minimum RuleIR vocabulary:

```text
MATCH(type/predicate/shape)
REQUIRE(predicate)
BIND(name, artifact_ref)
LOOKUP(index, typed_key, top_k)
TRANSFORM(approved_transform_id, inputs)
DERIVE(approved_rule_id, premises)
COMPUTE(approved_operator_id, inputs)
ASSERT_POSTCONDITION(predicate)
EMIT(typed_artifact)
FAIL(reason_code)
```

Minimum SkillIR structure:

```json
{
  "skill_id": "skill:sha256:...",
  "name": "solve_factorable_quadratic",
  "version": 4,
  "input_types": ["math.polynomial.degree2"],
  "output_types": ["math.solution_set"],
  "program": [
    ["REQUIRE", "leading_coefficient != 0"],
    ["TRANSFORM", "normalize_polynomial", ["input"]],
    ["COMPUTE", "factor_integer_polynomial", ["normalized"]],
    ["ASSERT_POSTCONDITION", "all_roots_substitute_true"],
    ["EMIT", "solution_set"]
  ],
  "proof_obligations": ["normalization_equivalent", "roots_complete", "domain_preserved"],
  "failure_modes": ["not-factorable-in-domain"],
  "resource_bound": {"max_steps": 40, "max_memory_kib": 256},
  "test_manifest_ref": "tests:sha256:...",
  "provenance_refs": ["trace:..."],
  "approval_ref": "approval:...",
  "status": "candidate|canary|active|revoked"
}
```

DSL safety requirements:

- no file, network, shell, reflection, import, dynamic attribute, or process opcodes;
- no unbounded loops or recursion;
- all operators registered by immutable ID and version;
- typed inputs and outputs checked at each step;
- static maximum step, depth, memory, and output-size bounds;
- deterministic iteration order and exact numeric policy;
- interpreter and verifier maintained independently;
- skill package hash included in the state snapshot.

### 6.4 Governed promotion pipeline

No memory becomes executable or canonical merely because a query succeeded.

```text
Observed transaction
  → privacy/sensitivity filter
  → reusable-pattern detector
  → anti-unification across diverse traces
  → candidate RuleIR/SkillIR
  → static schema and safety checks
  → positive tests
  → negative tests
  → adversarial tests
  → metamorphic tests
  → held-out domain tests
  → independent verifier receipts
  → governance review/approval
  → canary activation
  → monitored utility and regression checks
  → canonical promotion or revocation
```

Mandatory promotion gates:

1. At least three structurally diverse successful source traces; critical skills require more.
2. No raw secrets, private payloads, benchmark answers, or user-specific literals embedded in the generalized program.
3. Explicit preconditions, postconditions, failure modes, side-effect class, and resource bound.
4. Positive, negative, adversarial, metamorphic, and holdout coverage.
5. Zero critical security findings.
6. Improvement over baseline on a frozen evaluation set.
7. No statistically or practically significant regression on unrelated frozen suites.
8. Governance approval for canonical or executable status.
9. Reversible activation with an immutable previous snapshot.
10. Automatic revocation trigger when monitored postconditions fail.

### 6.5 Deterministic cross-session learning

Learning is modeled as state compilation, not mutable intuition.

```text
Snapshot S_n + verified candidate C + approval A
    → deterministic compiler
    → proposed snapshot S_(n+1)
    → migration/integrity/evaluation gates
    → atomic activation
```

The active state pointer changes only after all gates pass. A query that starts on `S_n` completes on `S_n` even if `S_(n+1)` activates concurrently. Every response identifies its state snapshot.

The system must support:

- replay on historical snapshots;
- semantic diff between snapshots;
- provenance from each new rule to source evidence and approval;
- rollback by switching the active pointer to a previous valid snapshot;
- deterministic rebuild from append-only events;
- garbage collection only after retention, backup, and audit policies allow it.

### 6.6 Self-healing answer and knowledge graph

The self-healing graph is a bounded truth-maintenance system, not uncontrolled graph rewriting.

Every canonical claim records:

- premises and evidence;
- derivation rules;
- dependent claims and skills;
- verification receipts;
- valid-time interval;
- source trust and independence group;
- snapshot versions in which it was active.

When evidence is corrected, expires, or is revoked:

1. append a reality-ledger event;
2. mark directly supported claims dirty;
3. traverse reverse dependencies using a bounded deterministic queue;
4. re-evaluate affected derivations against the new snapshot;
5. retain claims whose alternate valid support remains sufficient;
6. quarantine or retract unsupported descendants;
7. invalidate dependent caches and plan templates;
8. emit a semantic diff and audit event;
9. never silently rewrite past snapshots.

Safety bounds include maximum affected nodes per transaction, checkpointing, continuation tokens, cycle detection, and human review when impact exceeds policy thresholds.

### 6.7 Semantic compaction

Compaction optimizes meaning retained per byte, not merely text length.

A long artifact is compiled into typed semantic atoms:

- objective;
- invariant;
- definition;
- fact;
- relation;
- exception;
- condition;
- assumption;
- dependency;
- temporal scope;
- proof core;
- action core;
- failure mode;
- unresolved question;
- source span reference.

Compaction rules:

- retain source-span pointers so compressed claims remain auditable;
- canonicalize synonymous keys without merging distinct meanings;
- deduplicate payloads by content hash;
- store large payloads once in compressed packs;
- keep only summaries, typed keys, confidence, and pointers in hot memory;
- preserve counterexamples and failures because they constrain future plans;
- never discard an active premise required by a canonical claim;
- measure information loss with reconstruction and question-answer probes;
- quarantine ambiguous merges rather than forcing one canonical form.

---

## 7. Durable storage design

### 7.1 Reference storage stack

The Phase 11 reference implementation stays standard-library-first:

- SQLite for transactions, typed metadata, temporal records, and indices;
- SQLite FTS5 when available, with a deterministic lexical fallback when unavailable;
- compressed immutable payload packs using standard-library compression in the reference profile;
- content hashes for deduplication and integrity;
- append-only event/approval/revocation logs;
- compact hot-index snapshots loaded lazily;
- no requirement to load the 144 MiB corpus into RAM.

Optional faster codecs or native extensions must be feature-detected and cannot change semantic outcomes.

### 7.2 Logical SQLite schema

```sql
CREATE TABLE metadata (
  key TEXT PRIMARY KEY,
  value BLOB NOT NULL,
  value_hash BLOB NOT NULL
);

CREATE TABLE state_snapshots (
  snapshot_id BLOB PRIMARY KEY,
  parent_snapshot_id BLOB,
  transaction_seq INTEGER NOT NULL,
  manifest BLOB NOT NULL,
  manifest_hash BLOB NOT NULL,
  status INTEGER NOT NULL
);

CREATE TABLE memory_records (
  memory_id BLOB NOT NULL,
  version INTEGER NOT NULL,
  tier INTEGER NOT NULL,
  kind INTEGER NOT NULL,
  canonical_key TEXT NOT NULL,
  summary TEXT NOT NULL,
  payload_pack_id BLOB,
  payload_offset INTEGER,
  payload_length INTEGER,
  verification_state INTEGER NOT NULL,
  confidence_low INTEGER NOT NULL,
  confidence_high INTEGER NOT NULL,
  valid_from INTEGER,
  valid_to INTEGER,
  transaction_seq INTEGER NOT NULL,
  retention INTEGER NOT NULL,
  sensitivity INTEGER NOT NULL,
  content_hash BLOB NOT NULL,
  superseded_by BLOB,
  PRIMARY KEY(memory_id, version)
);

CREATE TABLE record_keys (
  memory_id BLOB NOT NULL,
  version INTEGER NOT NULL,
  key_type INTEGER NOT NULL,
  key_text TEXT NOT NULL,
  PRIMARY KEY(memory_id, version, key_type, key_text)
);

CREATE TABLE dependency_edges (
  source_id BLOB NOT NULL,
  target_id BLOB NOT NULL,
  relation INTEGER NOT NULL,
  snapshot_from BLOB NOT NULL,
  snapshot_to BLOB,
  PRIMARY KEY(source_id, target_id, relation, snapshot_from)
);

CREATE TABLE evidence (
  evidence_id BLOB PRIMARY KEY,
  source_type INTEGER NOT NULL,
  source_ref TEXT NOT NULL,
  content_hash BLOB NOT NULL,
  trust_tier INTEGER NOT NULL,
  independence_group TEXT NOT NULL,
  status INTEGER NOT NULL
);

CREATE TABLE verifier_receipts (
  receipt_id BLOB PRIMARY KEY,
  claim_id BLOB NOT NULL,
  verifier_id TEXT NOT NULL,
  verifier_version TEXT NOT NULL,
  result INTEGER NOT NULL,
  receipt BLOB NOT NULL,
  receipt_hash BLOB NOT NULL
);

CREATE TABLE audit_events (
  transaction_seq INTEGER NOT NULL,
  event_seq INTEGER NOT NULL,
  event_type INTEGER NOT NULL,
  actor TEXT NOT NULL,
  payload BLOB NOT NULL,
  event_hash BLOB NOT NULL,
  previous_hash BLOB,
  PRIMARY KEY(transaction_seq, event_seq)
);
```

Additional tables may cover plans, skill versions, approvals, tombstones, sessions, benchmark runs, and pack manifests. All frequently filtered columns require measured indices; speculative indices are rejected because they consume RAM and write cost.

### 7.3 Atomic commit protocol

1. Begin an immediate SQLite transaction.
2. Verify parent snapshot is still active.
3. Write payload pack to a temporary file and fsync it.
4. Verify pack checksum and deterministic manifest.
5. Insert candidate records, dependencies, receipts, approvals, and audit events.
6. Construct the new state manifest and Merkle-style root hash.
7. Run schema and graph invariants inside the transaction.
8. Atomically rename the payload pack.
9. Commit SQLite transaction.
10. Atomically switch the active snapshot pointer.
11. On failure, roll back database writes and delete orphan temporary packs.

Recovery scans incomplete transactions and orphan packs without guessing. Corruption never silently falls back to unchecked data.

### 7.4 Backup and migration

- schema migrations are numbered and checksummed;
- every migration has preflight, apply, verify, and recovery procedures;
- backups include database, payload packs, active snapshot, policy, and tool manifest;
- restore validates all hashes before activation;
- downgrade is supported while old schema semantics remain representable;
- destructive compaction requires a verified backup and governance approval;
- backup tests must restore into a clean environment and replay reference queries.

---

## 8. Deterministic retrieval lattice

Retrieval is a typed candidate-and-rank pipeline, not one substring scan and not an opaque vector similarity call.

### 8.1 Retrieval channels

1. exact canonical-key lookup;
2. lexical/FTS lookup;
3. symbol and normalized-token lookup;
4. type-compatible lookup;
5. relation and graph-neighborhood lookup;
6. temporal-validity lookup;
7. provenance/trust-tier lookup;
8. dependency and proof-premise lookup;
9. procedural precondition lookup;
10. failure/counterexample lookup;
11. recent session-state lookup when policy permits;
12. prior-plan and recovery-recipe lookup.

Domain profiles select channels and budgets. A math proof should prioritize definitions, lemmas, domain constraints, counterexamples, and proof skeletons. A repository task should prioritize symbols, tests, dependency edges, architecture constraints, and prior patch failures.

### 8.2 Retrieval algorithm

```text
compile typed retrieval request
  → resolve allowed tiers and sensitivity scope
  → generate bounded candidates per channel
  → filter invalid time, revoked state, schema mismatch, and permissions
  → compute deterministic integer features
  → rank with a versioned scoring profile
  → stable deduplication
  → diversify by source/strategy when contract requires independence
  → return top-k summaries and lazy payload references
```

### 8.3 Deterministic ranking

Use fixed-point integer features to avoid cross-platform floating-point ordering differences.

```text
score =
  3000 * lexical_relevance
+ 2500 * structural_match
+ 2200 * type_compatibility
+ 1800 * evidence_strength
+ 1500 * provenance_quality
+ 1200 * precondition_match
+ 1000 * temporal_validity
+  800 * verified_usefulness
+  500 * recency_if_relevant
- 2200 * contradiction_risk
- 1800 * staleness
- 1500 * duplication
- 1000 * estimated_load_cost
```

Each feature is an integer in a declared range. Weights are versioned configuration, not hidden magic. Stable tie-break order:

1. total score descending;
2. verification state priority;
3. trust tier;
4. kind priority for the task contract;
5. content hash ascending;
6. record ID ascending.

Every result includes a compact score explanation. Ranking changes require frozen retrieval benchmarks and a new configuration hash.

### 8.4 Retrieval correctness gates

- no unauthorized sensitivity tier can enter candidates;
- no revoked or temporally invalid fact can be returned as current;
- every returned item identifies snapshot and provenance;
- top-k is hard-bounded;
- duplicate semantics are collapsed without losing independent evidence counts;
- correlated copies do not masquerade as independent sources;
- cache keys include semantic query hash, state snapshot, policy, retrieval profile, and top-k;
- a cache hit must reproduce the same ordered record IDs as fresh retrieval.

### 8.5 Optional experimental associative methods

Hypervectors, locality-sensitive hashes, bloom filters, minhash, and other compact signatures may be researched only as candidate-generation accelerators. They must not replace exact canonical storage or verification, and they must pass memory, false-positive, recall, determinism, and explainability gates. Claims such as “O(1) retrieval across trillions of facts in 50 MiB” are prohibited without a reproducible proof and benchmark.

---

## 9. Semantic long-context engine

AXIMA will not simulate long context by retaining all raw tokens. It will maintain a versioned semantic state.

### 9.1 Context compilation pipeline

```text
stream source chunks
  → detect structure and source spans
  → compile semantic atoms
  → resolve local references
  → build entity/event/claim/dependency graphs
  → detect contradictions and uncertainty
  → create hierarchical summaries
  → retain active objectives, invariants, exceptions, and open questions
  → persist payloads and bounded indices
```

### 9.2 Multi-resolution context representation

- **L0 Source layer:** immutable source chunks and spans on disk.
- **L1 Atom layer:** facts, definitions, events, rules, conditions, exceptions.
- **L2 Structure layer:** entity, temporal, causal, argument, and dependency graphs.
- **L3 Task layer:** active goals, constraints, decisions, unresolved conflicts, state changes.
- **L4 Digest layer:** compact summaries optimized for routing and retrieval.

Reasoning descends to lower layers only when evidence or ambiguity requires it. An answer cites L0 spans even when retrieval began from L4.

### 9.3 Context retention policy

Keep in RAM only:

- current task envelope;
- active semantic digest;
- top-k retrieved atoms;
- current plan and claim graph;
- unresolved ambiguity set;
- verifier working state;
- bounded session continuity state.

Place on disk:

- raw source chunks;
- completed detailed traces;
- inactive graph regions;
- historical episodes;
- payload bodies;
- old snapshots and proof artifacts.

### 9.4 Context quality metrics

- answer accuracy as source length grows;
- source-span citation precision and recall;
- contradiction retention rate;
- objective/invariant/exception recall;
- state-update correctness across turns;
- compression ratio;
- reconstruction score on held-out questions;
- memory and latency versus source length;
- false merge and false forgetting rates.

The long-context claim is earned only when quality degrades gracefully under a fixed memory envelope.

---
## 10. Multi-resolution reasoning architecture

AXIMA reasons at several resolutions so it can reject bad strategies before spending resources on details.

### 10.1 Resolution levels

| Level | Question answered | Artifacts |
|---|---|---|
| R0 Contract | What must be answered, proven, avoided, and formatted? | Task and epistemic contracts |
| R1 Strategy | What family of solution methods is appropriate? | Ranked strategy candidates |
| R2 Skeleton | What subgoals and dependencies are necessary? | PlanDAG and proof obligations |
| R3 Exact execution | What exact transformations, computations, or tool actions solve each subgoal? | Typed artifacts and claims |
| R4 Audit | Do claims, constraints, evidence, and output survive independent checks? | Receipts, counterexamples, release decision |

A failure at a coarse level blocks finer execution. A fine-level failure may trigger a bounded local repair or strategy switch without rebuilding unrelated work.

### 10.2 Strategy portfolio

The planner selects from explicit reasoning families:

- direct lookup;
- exact deduction;
- algebraic rewrite and normalization;
- constraint propagation and finite search;
- case split and exhaustive bounded enumeration;
- proof by contradiction;
- proof by induction using declared schemas;
- counterexample search;
- causal intervention over structural models;
- temporal and bitemporal reasoning;
- analogy as candidate generation only;
- abductive hypothesis generation with explicit alternatives;
- deterministic simulation;
- tool-backed calculation, compilation, or testing;
- clarification or abstention.

Analogy, induction from examples, and heuristic search may propose candidates but cannot confer `PROVEN` or `DIRECT_FACT` status without independent evidence.

### 10.3 Typed rule engine

Every reasoning rule declares:

- stable ID and semantic version;
- accepted premise types;
- output claim type;
- side conditions;
- domain and temporal scope;
- confidence transformation;
- proof obligations;
- failure codes;
- maximum expansion cost;
- provenance and approval state;
- inverse or replay check when available.

The agenda is deterministic:

1. sort applicable rules by contract fitness, proof strength, expected information gain, cost, and stable ID;
2. apply only while budget remains;
3. memoize semantic states by content hash;
4. reject repeated states and non-progress cycles;
5. cap branch count, depth, generated claims, and artifact bytes;
6. retain why each unused strategy was rejected when explanation policy requests it.

### 10.4 Cycles and fixed points

Cyclic knowledge is permitted only under an explicit fixed-point policy. A cyclic operator must be proven monotone over a finite lattice or have a declared convergence bound. Otherwise the cycle is quarantined as unresolved. “Infinitary” or “transfinite” computation has no place in a hard-bounded production request path.

### 10.5 Reasoning tournament integration

The existing reasoning tournament becomes a high-risk or high-value verification strategy, not a decorative debate.

Roles may include:

- proposer;
- assumption hunter;
- counterexample searcher;
- evidence auditor;
- security critic;
- simplifier;
- independent judge.

Tournament output is a structured attack/defense graph. Repeated votes from correlated rules do not increase confidence. Fatal counterexamples block release. Budgets cap rounds and role invocations.

### 10.6 Unknowns and ambiguity

Before planning, the boundary mapper classifies missing information:

- essential and observable;
- essential but unavailable;
- optional;
- resolvable by retrieval;
- resolvable by deterministic computation;
- ambiguous interpretation;
- outside supported capability.

The system chooses among clarification, conditional answer, enumerated alternatives, bounded assumption, or abstention. Assumptions appear in claims and response output; they are never hidden in prose.

---

## 11. Proof-obligated planning

The existing `CognitivePlanner` and `PlanDAG` become active in the public transaction instead of remaining disconnected scaffolding.

### 11.1 Fixed plan node vocabulary

Production plans use a deliberately small set:

- `classify`;
- `clarify`;
- `retrieve`;
- `derive`;
- `compute`;
- `execute`;
- `validate`;
- `verify`;
- `repair`;
- `synthesize`;
- `commit`.

Domain-specific behavior belongs in capabilities and typed operator IDs, not an unlimited expansion of orchestration node types.

### 11.2 Planning algorithm

1. Normalize the task and freeze the state snapshot.
2. Compile the epistemic and output contracts.
3. Map unknowns, ambiguity, risk, permissions, and freshness needs.
4. Retrieve applicable facts, rules, skills, failures, tests, and prior plan skeletons.
5. Generate bounded strategy candidates.
6. Expand each candidate only to R2 skeleton resolution.
7. Attach preconditions, postconditions, proof obligations, failure branches, and cost estimates.
8. Reject infeasible plans before execution.
9. Score remaining plans deterministically.
10. Select one primary and, when justified, one independent fallback.
11. Execute topologically with checkpoints.
12. Repair locally when a postcondition fails and a bounded alternative exists.
13. Verify claim-by-claim.
14. Synthesize only releasable claims.
15. Submit reusable artifacts as memory candidates after response construction.

### 11.3 Plan scoring

Use fixed-point features and stable tie-breaking:

```text
plan_score =
  3000 * contract_coverage
+ 2500 * expected_proof_strength
+ 1800 * determinism
+ 1500 * verifier_independence
+ 1200 * expected_information_gain
+ 1000 * prior_verified_success
+  800 * rollback_quality
- 1800 * residual_risk
- 1500 * resource_cost
- 1200 * unsupported_assumptions
- 1000 * side_effect_risk
```

No historical success score is accepted without sample size, snapshot scope, and failure data. Stable plan hash resolves ties.

### 11.4 Preconditions and postconditions

Conditions are typed predicates evaluated by registered checkers. Plain strings may remain in compatibility adapters but cannot authorize production execution.

Examples:

- `artifact.type == math.polynomial`;
- `polynomial.degree == 2`;
- `capability.permission.includes(file.write:/workspace)`;
- `retrieval.coverage >= contract.minimum_coverage`;
- `all_generated_files.parse == true`;
- `all_released_claims.have_receipts == true`.

A node does not run if a required precondition is unknown. It either invokes an observation/clarification node or fails with a structured reason.

### 11.5 Recovery

Recovery order:

1. retry only deterministic transient failures with a strict count;
2. narrow or broaden retrieval according to the diagnosed failure;
3. switch to a declared alternate operator;
4. decompose the failed subgoal;
5. reduce requested scope with user-visible caveat;
6. roll back side effects;
7. abstain.

Recovery cannot weaken the task's safety, evidence, or truth contract silently.

### 11.6 Planner correctness gates

- DAG is acyclic and references only registered capabilities;
- every nontrivial node has typed pre/postconditions;
- every releasable claim path includes required verifier nodes;
- side effects have authorization and rollback;
- estimated resources fit the remaining transaction budget;
- stable serialization produces the same plan hash across repeated runs;
- a failed mandatory dependency cannot be marked skipped while dependent output is released;
- aggregation cannot precede verification required by contract.

---

## 12. Capability-safe execution

### 12.1 Capability descriptors

Descriptors must include more than accepted string types:

- input/output schemas;
- semantic version;
- deterministic status and known nondeterministic metadata;
- side-effect class;
- permission scopes;
- pre/postcondition checker IDs;
- cost envelope with observed percentiles;
- verifier independence group;
- supported platform/tool requirements;
- failure modes;
- health and degradation behavior.

### 12.2 Execution isolation

- pure symbolic operators execute in process under step and memory accounting;
- code compilation/tests execute in a restricted subprocess with time, file, and process limits;
- network is denied by default;
- files are exposed through scoped capability tokens;
- generated code never executes merely because it compiled;
- tool stdout/stderr is treated as untrusted data;
- external tool versions and command manifests enter the state snapshot;
- every side effect is transactionally staged and committed only after verification.

### 12.3 Resource admission

Before a node starts, the budget governor reserves estimated time, memory, disk read, output bytes, and process slots. A node that cannot be admitted is replanned or rejected. Actual usage updates the cost model after the transaction, but model updates become active only in a new versioned configuration.

### 12.4 Tool determinism

Tools are classified:

- **D0 Pure:** deterministic output for identical bytes and version.
- **D1 Normalizable:** volatile metadata can be stripped to a deterministic semantic result.
- **D2 Snapshot-dependent:** output depends on an explicitly captured local state.
- **D3 Nondeterministic/external:** not allowed for strict replay; results are witnessed evidence with reduced guarantees.

Strict deterministic mode permits D0-D2 only.

---

## 13. Verification as the mandatory release gate

Verification moves from an optional library to the authority that determines what can be said.

### 13.1 Claim-level verification

The response is decomposed into atomic claims. Each claim receives:

- type and risk;
- premises and assumptions;
- evidence and provenance;
- generator identity;
- applicable verifier set;
- coverage requirements;
- receipts and counterexamples;
- release decision;
- truth-level ceiling.

A global “answer passed” flag cannot hide an unverified subclaim.

### 13.2 Verifier families

**Universal:**

- schema/type checker;
- provenance integrity checker;
- temporal validity checker;
- contradiction checker;
- derivation DAG checker;
- source-independence checker;
- output-contract checker;
- resource and policy checker.

**Mathematics:**

- exact substitution/equivalence;
- domain and singularity checks;
- dimensional consistency;
- counterexample search;
- alternate derivation where independent;
- proof-step rule checker;
- numerical interval witness for approximate claims.

**Code:**

- parser/AST checker;
- compiler/type checker;
- static security analysis;
- generated unit and property tests;
- contract tests;
- sandboxed execution;
- diff scope and dependency checks;
- repository regression tests.

**Knowledge/reasoning:**

- citation-span alignment;
- source validity/freshness;
- inference-rule applicability;
- premise sufficiency;
- contradiction and counterfactual checks;
- independent source coverage;
- unsupported leap detection.

### 13.3 Release policy matrix

| Contract/risk | Minimum release condition | On failure |
|---|---|---|
| Direct deterministic computation, low risk | Applicable exact verifier passes | Repair or abstain |
| Sourced fact, low risk | Valid citation + provenance + no active contradiction | Conditional answer or abstain |
| Derived claim, normal risk | Derivation valid + required domain verifier(s) pass | Repair or abstain |
| Approximate estimate | Method valid + uncertainty interval + assumptions visible | Conditional answer |
| Generated code | Parse/compile + required tests + security policy | Return non-executable draft or block |
| High-risk claim/action | Independent quorum, all critical checks pass, explicit policy authorization | Block or require human approval |
| No applicable verifier | Never release as verified | `UNSUPPORTED` or clearly labeled unverified draft when policy allows |

A counterexample overrides positive votes. Security-critical failure blocks release. Verifier disagreement produces `CONDITIONAL` only when policy explicitly permits and the disagreement is visible.

### 13.4 Confidence calibration

Confidence derives from evidence strength, verifier coverage, independence, uncertainty propagation, historical calibration, and residual risk—not engine names.

```text
confidence ceiling = min(
  premise confidence,
  evidence trust ceiling,
  derivation rule ceiling,
  verifier coverage ceiling,
  temporal validity ceiling,
  contract-specific ceiling
)
```

Correlated verifiers share an independence group and cannot be counted as separate evidence. Calibration is measured with Brier score, expected calibration error, reliability curves, and abstention utility on frozen outcomes.

### 13.5 Repair loop

Verification may return a typed repair request:

- missing premise;
- violated domain condition;
- counterexample;
- stale citation;
- incomplete test coverage;
- schema mismatch;
- unsafe operation;
- unresolved contradiction.

The planner receives the request and may perform a bounded local repair. Repair count, changed artifacts, and new receipts remain in the trace. Verification requirements may not be removed to force a pass.

### 13.6 Response integration requirement

The public response must carry or reference:

- release decision;
- verified claim IDs;
- failed/withheld claim IDs;
- verifier receipt IDs;
- residual risk;
- state snapshot ID;
- explicit unknowns and caveats.

The current behavior of computing verification information and discarding it is a Phase 11 blocker.

---

## 14. Constrained answer synthesis

The synthesizer is not a free generator. It is a deterministic compiler from released semantic artifacts to an output schema.

### 14.1 Inputs

- released claims only;
- derivation and evidence references;
- required caveats and assumptions;
- unknowns and withheld claims;
- contract-specified format, language, register, and proof depth;
- stable rendering templates.

### 14.2 Synthesis invariants

1. Every factual sentence maps to one or more released claim IDs.
2. Rendering cannot increase truth level or confidence.
3. No citation may be attached to a claim it does not support.
4. Required assumptions and safety caveats cannot be omitted by concise mode.
5. Numeric formatting preserves exactness and declared rounding policy.
6. Code blocks map to verified artifact hashes.
7. Ordering is stable under the same output contract.
8. Round-trip parsing must recover the essential claim graph for supported output schemas.
9. If native-language realization cannot preserve meaning, technical content remains in a verified neutral form with an explicit limitation.

### 14.3 Explanation levels

- **Compact:** answer, truth level, primary evidence, critical caveat.
- **Standard:** key reasoning steps and verification summary.
- **Deep:** complete plan/derivation summary, alternatives rejected, receipts.
- **Machine:** canonical JSON/CBOR-like schema suitable for replay.

All levels refer to the same claims; detail changes must not change meaning.

---

## 15. Mathematics capability track

The goal is exact, domain-aware, proof-oriented mathematics within declared coverage—not superficial formatting success.

### 15.1 Mathematical representation

- one canonical AST across parser, specialist, plugin, verifier, and renderer;
- exact integers, rationals, algebraic numbers, symbolic constants, and intervals before binary floats;
- explicit domains, assumptions, units, branch cuts, singularities, and variable scopes;
- normalization with equivalence certificates;
- no duplicate competing parsers on the authoritative path without compatibility tests.

### 15.2 Capability progression

1. arithmetic and safe function evaluation;
2. polynomial normalization, factoring, roots, and systems;
3. rational expressions and domain exclusions;
4. symbolic differentiation and integration with rule coverage reporting;
5. limits, series, recurrence relations, and transforms in bounded supported classes;
6. linear algebra with exact and interval verification;
7. discrete mathematics, combinatorics, number theory, and finite proofs;
8. geometry and dimensional reasoning;
9. proof construction from a curated lemma library;
10. strategy selection, counterexample search, and alternate-method verification.

### 15.3 Math answer contract

A solution reports:

- normalized problem;
- domain and assumptions;
- method selected and why;
- exact result when available;
- derivation steps;
- excluded/conditional solutions;
- verifier method;
- proof status: `formal`, `machine_checked`, `verified_derivation`, `numeric_witness`, `heuristic`, or `unsupported`.

### 15.4 Math gates

- exact answer accuracy on frozen supported-domain sets;
- solution-set completeness, not just one expected number;
- domain-error and extraneous-root detection;
- proof-step validity;
- metamorphic invariance under notation and equivalent transformations;
- adversarial parser and resource-limit resistance;
- zero false `PROVEN` labels in the release corpus;
- memory and latency by problem class.

---

## 16. Coding and repository-engineering track

The goal is verified repository transformation, not text completion.

### 16.1 Pipeline

```text
requirements
  → repository model + architecture IR
  → constraints and acceptance tests
  → dependency-aware change plan
  → minimal patch candidate
  → parse/type/static checks
  → generated and existing tests
  → security and diff-scope review
  → transactional apply
  → post-apply validation
  → rollback artifact
```

### 16.2 Required capabilities

- AST- and symbol-aware navigation;
- exact reference and dependency graph;
- requirements-to-contract compilation;
- minimal diff planning;
- language-specific syntax and type validation;
- test synthesis from pre/postconditions;
- property/metamorphic tests where applicable;
- dependency and lockfile awareness;
- migration and deployment artifact validation;
- failure localization and bounded repair;
- repository-level provenance and change receipts.

### 16.3 Code safety

- default dry-run;
- explicit capability token for writes;
- workspace allowlist;
- no hidden dependency installation;
- pinned dependencies and package-name validation;
- network denied unless separately authorized;
- generated commands displayed and audited;
- no production deployment without external approval;
- rollback tested before destructive migration;
- secrets and private code excluded from reusable memory unless explicitly allowed.

### 16.4 Code gates

- parse and compile rate;
- accepted-test pass rate;
- hidden-test pass rate;
- regression rate on untouched behavior;
- patch minimality and scope accuracy;
- vulnerability and unsafe-pattern rate;
- dependency correctness;
- deterministic patch hash under a fixed repository snapshot;
- repair success without test weakening;
- rollback success.

---

## 17. General, causal, scientific, and decision reasoning

### 17.1 Structured argument engine

Represent reasoning as:

- question;
- claims;
- premises;
- warrants/rules;
- assumptions;
- alternatives;
- objections;
- counterexamples;
- evidence;
- unresolved unknowns;
- decision criteria.

This enables contradiction checks and explanations without pretending unconstrained prose is reasoning.

### 17.2 Constraint and decision reasoning

- finite-domain constraint propagation;
- deterministic search with branch-and-bound;
- Pareto-front reporting for multi-objective decisions;
- explicit utility assumptions;
- sensitivity analysis;
- scenario comparison;
- no recommendation beyond evidence and declared values.

### 17.3 Causal reasoning

Build on the existing structural causal model specialist:

- distinguish observation, intervention, and counterfactual questions;
- identify confounders and adjustment assumptions;
- retain graph provenance;
- reject causal conclusions from correlation-only evidence;
- verify interventions against model equations;
- expose model uncertainty and alternate DAGs;
- bound counterfactual branch expansion.

### 17.4 Scientific reasoning

- hypothesis as a versioned claim, not a fact;
- preregistered predictions and falsification criteria;
- experiment/simulation distinction;
- units and dimensional verification;
- uncertainty propagation;
- replication and source independence;
- theory revision through governed evidence updates;
- no benchmark or simulated result promoted as real-world discovery without external evidence.

### 17.5 General reasoning gates

- premise-to-conclusion validity;
- hidden-assumption detection;
- counterexample success;
- contradiction precision/recall;
- causal identification correctness;
- constraint satisfaction and optimality certificates;
- calibration and abstention;
- robustness to paraphrase, negation, irrelevant details, and order changes.

---

## 18. Human understanding and multilingual expression

Language detection is not equivalent to language understanding or translation. Phase 11 measures them separately.

### 18.1 Meaning-preserving interface

- parse supported language forms into shared MeaningIR;
- preserve quantities, negation, modality, conditions, and source spans;
- realize only verified claims;
- protect formulas, code, citations, and named entities;
- run round-trip semantic checks;
- abstain or use a neutral technical format when realization is not reliable.

### 18.2 Adaptive explanations

The learner model may choose examples, prerequisites, register, and detail, but it cannot alter underlying claims. Personalization memory stores user-approved learning state and misconceptions—not inferred sensitive traits.

### 18.3 Language gates

- language identification accuracy on broad, non-overfit corpora;
- intent/meaning preservation by language;
- round-trip semantic equivalence;
- formula, code, citation, and entity preservation;
- native-speaker quality review for supported languages;
- transparent separation of detection, parsing, translation, and realization capability claims.

---
## 19. Hard 50 MiB resource architecture

The resource target is a release gate with a reproducible harness. It is not a comment in a dataclass.

### 19.1 Reference budget

A provisional single-worker budget, refined by measurement:

| Component | Peak target |
|---|---:|
| Python interpreter, shared libraries, core imports | 20 MiB |
| Kernel, contracts, semantic IR, planner | 5 MiB |
| Working/session hot state | 3 MiB |
| Retrieval hot indices and top-k payloads | 6 MiB |
| Active domain capability | 4 MiB |
| Verification state | 3 MiB |
| Trace, metrics, serialization buffers | 2 MiB |
| Cache | 2 MiB |
| Emergency/headroom margin | 5 MiB |
| **Total** | **50 MiB** |

This is an envelope, not permission for each component to reserve its full amount. Measurements use peak process RSS and component-specific allocation telemetry where available.

### 19.2 Runtime profiles

- **Minimal (target ≤32 MiB):** core parser, direct math, compact knowledge lookup, limited traces.
- **Reference (hard ≤50 MiB):** one active specialist, persistent retrieval, planning, verification, executable memory.
- **Extended:** larger caches or optional tools on machines with more memory; semantic behavior must remain compatible.

AXIMA must always retain the reference profile. Extended mode cannot become the only functioning configuration.

### 19.3 Memory-saving architecture

- lazy imports and lazy plugin initialization;
- unloadable plugin caches with deterministic lifecycle;
- SQLite-backed indices rather than Python object graphs for the full corpus;
- integer IDs and enumerations in hot structures;
- frozen/slotted compact records where profiling proves benefit;
- intern only bounded controlled vocabularies;
- content-addressed payload deduplication;
- iterators and streaming parsers;
- bounded top-k retrieval;
- bounded trace and session windows;
- compact bitsets only when their false-positive and memory behavior are measured;
- one canonical representation per concept in the live pipeline;
- avoid pandas, NumPy, large ORM layers, and broad framework imports in the reference runtime;
- subprocess tools launched only on demand and charged separately.

### 19.4 Budget governor

The governor tracks:

- process RSS and peak RSS;
- Python allocations for diagnostics;
- active artifact bytes;
- cache and trace bytes;
- plan steps and branch count;
- recursion/derivation depth;
- SQLite rows/pages read;
- payload bytes decompressed;
- subprocess count and child RSS;
- wall and CPU time;
- output bytes.

`tracemalloc` alone is insufficient because it misses native/shared allocations. Platform adapters use the best available process APIs and are validated against operating-system tools.

### 19.5 Degradation ladder

When predicted or observed memory approaches thresholds:

1. stop speculative prefetch;
2. evict cold cache entries by deterministic policy;
3. flush completed trace detail to disk;
4. reduce retrieval top-k within contract limits;
5. serialize inactive plan artifacts;
6. unload inactive plugin state;
7. switch to a lower-memory verified strategy;
8. return a resource-bounded partial/conditional response if allowed;
9. abort cleanly with `RESOURCE_EXHAUSTED` before the OS kills the process.

The ladder cannot discard required evidence, safety checks, or unresolved contradictions.

### 19.6 Reference resource workloads

The 50 MiB gate includes:

- cold start and import;
- 1,000 sequential mixed-domain queries;
- a long session with maximum permitted context;
- retrieval over the full on-disk corpus;
- a deep math derivation;
- repository code analysis within declared fixture size;
- claim-level verification and repair;
- memory candidate extraction without promotion;
- snapshot switch and rollback;
- malformed and adversarial inputs;
- idle period followed by a new request.

Metrics include cold peak, warm peak, steady-state slope, retained memory after GC, p95/p99, cache hit/miss profiles, and child-process budget.

### 19.7 Cross-platform gate

At minimum:

- CPython 3.11 and supported newer versions;
- Linux x86_64;
- Windows x86_64;
- macOS on a currently supported architecture;
- Raspberry Pi/ARM Linux;
- Android through a documented supported environment.

A platform may have its own measured baseline and feature availability, but the 50 MiB claim is published only where the process passes the same semantic and resource suite. FTS5, process limits, and filesystem semantics require capability detection and deterministic fallbacks.

---

## 20. Security, privacy, and governance

Persistent executable memory introduces a larger attack surface than a stateless rule engine. Security is part of cognition, not a wrapper.

### 20.1 Threat classes

| Threat | Required control |
|---|---|
| Prompt/document injection | Treat retrieved text as data; never as policy or executable instruction |
| Memory poisoning | Quarantine, provenance, independent verification, governance, rollback |
| Skill injection | Safe DSL, static checks, test gates, signed/hashed manifests, no arbitrary Python |
| Provenance forgery | Content hashes, source identity, append-only ledger, integrity verification |
| Dependency confusion | Exact capability IDs and versions; pinned dependencies; allowlists |
| Tool abuse | Capability tokens, default-deny permissions, sandbox, transaction boundaries |
| Resource denial | Admission control, parser/graph limits, decompression limits, rate limits |
| Retrieval exfiltration | Sensitivity-aware filtering before ranking and rendering |
| Cross-session leakage | Session/tenant scopes, explicit memory consent, access checks |
| Rollback attack | Monotonic transaction sequence and trusted active-snapshot pointer |
| Audit deletion | Append-only hash chain, backups, governance prohibition |
| Benchmark poisoning | Sealed manifests, canaries, contamination checks, immutable expected semantics |
| Malicious corpus | Parser isolation, size limits, content quarantine, source trust tiers |
| Supply-chain compromise | Minimal dependencies, lock integrity, release provenance, reproducible artifacts |

### 20.2 Memory trust states

```text
UNTRUSTED_INPUT
  → QUARANTINED
  → CANDIDATE
  → VERIFIED
  → APPROVED
  → CANARY
  → CANONICAL
  → SUPERSEDED or REVOKED
```

Transitions require explicit receipts. Canonical status is never inferred merely from age, frequency, user repetition, or agreement among duplicated sources.

### 20.3 Authority separation

Separate identities and capabilities for:

- requester;
- parser/retriever;
- planner;
- executor;
- verifier;
- memory candidate extractor;
- governance approver;
- release operator.

One process may implement several roles in a small deployment, but logical permissions and audit identities remain distinct. A generator cannot issue its own verifier receipt or approval.

### 20.4 Data governance

- memory is opt-in where persistence is user-specific;
- users can inspect, export, correct, and delete eligible data;
- audit/legal retention is distinguished from semantic memory;
- private payloads are referenced minimally and never generalized into global skills by default;
- logs redact secrets and use hashes or references instead of raw content;
- deletion creates a verifiable tombstone and dependency invalidation;
- backups follow the same sensitivity policy;
- OS-level encryption is recommended; application-level encryption requires a separate key-management design before claims are made.

### 20.5 Governance gates

Human or external approval remains mandatory for:

- activating system- or module-scope rule changes;
- promoting executable skills to canonical status;
- changing verifier or release policy;
- enabling network access;
- adding a new side-effect capability;
- deleting protected history;
- deploying to production;
- publishing competitive superiority claims.

The system may autonomously quarantine, propose, test locally, measure, and revoke a failing canary under predetermined policy.

### 20.6 Security validation

- parser and serializer fuzzing;
- injection corpus across every ingestion path;
- zip/decompression bombs;
- pathological graph and expression complexity;
- sandbox escape attempts;
- path traversal and symlink races;
- capability-token misuse;
- corrupted/tampered database and pack files;
- malicious skill packages;
- cross-session and cross-tenant leakage;
- rollback and replay attacks;
- denial-of-service under the 50 MiB envelope;
- static scanning for prohibited dynamic execution paths.

No critical or high unmitigated finding is permitted at production release.

---

## 21. Observability and operations

### 21.1 Required transaction metrics

- stage latency and cost;
- peak and stage RSS;
- retrieval candidates, top-k, and cache behavior;
- plan nodes, branches, repairs, and failures;
- claims proposed/released/withheld;
- verifier coverage, disagreement, counterexamples, and residual risk;
- truth levels and abstentions;
- memory candidates, approvals, promotions, revocations;
- snapshot IDs and transitions;
- errors by structured reason;
- semantic result hash.

Metrics must not contain raw sensitive content.

### 21.2 Health checks

- database integrity and schema version;
- active snapshot availability;
- rule/knowledge/skill pack checksums;
- plugin and verifier health;
- stale or pending migrations;
- resource headroom;
- audit-chain continuity;
- backup freshness and last restore test;
- optional tool availability/version;
- reference self-check queries.

A system with corrupted evidence or policy state is unhealthy even if it can return text.

### 21.3 Failure behavior

- fail closed on policy, provenance, snapshot, or verifier corruption;
- fail bounded on resource exhaustion;
- degrade explicitly when optional tools are unavailable;
- never substitute a weaker engine without recording and enforcing its lower truth ceiling;
- preserve transaction artifacts needed for diagnosis;
- avoid exception text that leaks secrets or paths;
- surface a stable machine-readable reason code.

### 21.4 Reproducibility bundle

Any disputed response can export a bounded bundle containing:

- task envelope;
- state snapshot manifest;
- plan;
- referenced rules and evidence hashes;
- tool manifest and normalized outputs;
- claim graph;
- verification receipts;
- semantic response;
- trace summary.

Sensitive payloads may remain external with authenticated references. The bundle must state when full replay is impossible because a witnessed external source is unavailable.

---

## 22. Evaluation science

### 22.1 Test layers

1. parse/import and schema tests;
2. unit tests;
3. contract and compatibility tests;
4. property-based tests;
5. metamorphic tests;
6. differential tests between old and new paths;
7. integration tests;
8. security/adversarial tests;
9. resource and leak tests;
10. replay/determinism tests;
11. end-to-end domain evaluations;
12. sealed external evaluations.

The existing 45-case public suite remains a regression smoke suite. It cannot be the headline intelligence benchmark.

### 22.2 Dataset separation

- **Development fixtures:** visible, used during implementation.
- **Public regression suite:** visible, protects known behavior.
- **Frozen validation suite:** changes only by governed version.
- **Hidden test suite:** unavailable to implementation logic.
- **Adversarial mutation suite:** generated from semantic transformations.
- **Canary suite:** includes unanswerable and contamination-sensitive cases.
- **External suite:** independently maintained for competitive claims.

Test cases record origin, license, semantic version, expected interpretation, judge, and contamination risk.

### 22.3 Domain metrics

**Math:** exact accuracy, solution completeness, proof-step validity, domain handling, counterexample false-accept rate.  
**Code:** compile rate, test pass rate, hidden-test success, vulnerability rate, patch scope, rollback success.  
**Retrieval:** recall@k, precision@k, MRR, nDCG, citation alignment, temporal correctness, source diversity.  
**Planning:** valid-DAG rate, task success, contract coverage, recovery success, cost-estimation error, side-effect rollback.  
**Verification:** false accept/reject, applicable-verifier coverage, counterexample detection, receipt integrity, calibration.  
**Memory:** reuse benefit, bad-promotion rate, invalidation completeness, replay rate, compaction loss, poison resistance.  
**Reasoning:** validity, assumption exposure, contradiction detection, causal identification, robustness to distractors.  
**Language:** semantic preservation, negation/quantity/modality retention, round trip, native quality.  
**Operations:** peak RSS, latency percentiles, startup, long-run slope, crash recovery, backup restore.  
**Determinism:** semantic hash agreement across repeated runs, processes, and platforms.

### 22.4 Required benchmark scale

Scale grows by evidence, not vanity:

| Milestone | Minimum evaluation breadth |
|---|---|
| Foundation gate | Existing suite plus targeted new integration/resource/replay cases |
| Phase 11 alpha | ≥1,000 frozen end-to-end cases across at least six capability/risk categories |
| Phase 11 beta | ≥2,500 frozen cases plus adversarial mutations and long-run resource suite |
| Release candidate | ≥5,000 cases, hidden/external subsets, cross-platform/resource/security runs |
| Ultra-Cosmic claim | Independent domain-specific suites of sufficient statistical power; no universal score substitution |

Raw case count never replaces diversity, difficulty, judge quality, or contamination controls.

### 22.5 Provisional target thresholds

Thresholds are binding only after baseline measurement validates the metric and sample power.

| Dimension | Phase 11 production target |
|---|---:|
| Semantic determinism under same snapshot | 100% across repeated reference runs |
| Plan structural validity | 100% |
| Canonical memory promoted without required receipts | 0 |
| Critical security false releases in frozen suite | 0 |
| Verification information attached when contract requires it | 100% |
| Retrieval recall@10 on supported corpus tasks | ≥95% |
| Citation-span precision on supported tasks | ≥98% |
| Exact math accuracy on declared supported classes | ≥95% |
| Extraneous-root/domain-error detection | ≥99% |
| Code parse/compile on declared generation tasks | ≥95% |
| Code acceptance tests on supported tasks | ≥85% |
| Planner recovery on designed recoverable failures | ≥80% |
| Memory utility improvement on reuse tasks | ≥20% relative with no significant unrelated regression |
| Incorrect confident answer rate | ≤1%, with stricter per-domain gates |
| Peak RSS reference profile | ≤50 MiB on every claimed platform |
| Long-run unbounded RSS slope | none within measurement tolerance |
| Backup restore/reference replay | 100% |

### 22.6 Competitive comparison protocol

A comparison with GPT, Claude, Gemini, Wolfram, theorem provers, coding tools, or other systems must:

- name versions, dates, prompts, tools, and settings;
- use identical task semantics and allowed resources where possible;
- separate supported-domain coverage from accuracy;
- report abstentions and failures, not only wins;
- use independent judges or machine-verifiable outcomes;
- include confidence intervals and effect sizes;
- disclose benchmark visibility and development exposure;
- report latency, cost, energy/memory assumptions, and hardware;
- avoid cherry-picking;
- publish reproducible artifacts when licensing allows;
- restrict the claim to the evaluated domain.

“More deterministic than system X” may be architectural. “More capable than system X” requires measured evidence.

### 22.7 Documentation truth gate

README and architecture claims are tested release artifacts. Automated checks should verify counts, command paths, schema names, benchmark versions, supported languages/domains, and resource claims. Stale documentation blocks release when it materially overstates capability.

---

## 23. Incremental migration and compatibility

Phase 11 uses a strangler migration around the stable public API.

### 23.1 Migration sequence for each subsystem

1. define canonical contract and golden compatibility fixtures;
2. wrap existing behavior behind an adapter;
3. implement the new subsystem independently;
4. unit/property/security/resource test it;
5. run old and new in shadow mode;
6. compare semantic outputs, traces, costs, and failure behavior;
7. classify divergences as improvement, regression, or intentional contract change;
8. canary on a deterministic query partition;
9. make new path default only after gates pass;
10. retain rollback and old reader compatibility for a declared window;
11. deprecate with measured feature/test parity;
12. remove only in a separately reviewed release.

### 23.2 Public API policy

Preserve:

```python
ax = Axima()
response = ax.query(text, mode="deep", session_id=None)
```

Future options are keyword-only and additive, such as budget, state snapshot, persistence profile, or output schema. The default must remain safe and documented. Existing response fields remain readable; new verification and snapshot fields are optional until the next major contract version.

### 23.3 Pipeline migration order

1. add state snapshot and canonical trace IDs without changing answers;
2. attach real verification results to responses in shadow mode;
3. invoke planner in shadow mode and compare its selected path to current routing;
4. add persistent memory in read-only shadow mode;
5. enable retrieval results as additional context without canonical writes;
6. enable proof-obligated plans for one bounded domain, beginning with exact math;
7. make verification enforce release for that domain;
8. enable memory candidates but require manual promotion;
9. canary governed executable skills;
10. expand domain by domain;
11. converge `Axima.query` and microkernel runtime onto one authoritative cognitive loop;
12. retire duplicate routing and fallback paths only after parity.

### 23.4 Data migration

- import current memory exports as `QUARANTINED` or `EPISODIC`, never canonical by default;
- ingest corpus records with source manifest and deterministic IDs;
- map current evidence/ledger records through versioned adapters;
- preserve original bytes or hashes for audit;
- detect duplicates and contradictions before promotion;
- benchmark migration memory and time on realistic data size;
- support restart after partial migration;
- maintain a verified rollback backup.

### 23.5 Shadow comparison

Compare old and new on:

- semantic answer, not only exact text;
- truth level;
- claims and citations;
- unsupported/abstention decision;
- route and plan;
- verifier coverage;
- latency and peak RSS;
- errors and safety behavior.

The old path remains authoritative only until the new path demonstrates stronger correctness. A divergence is not automatically a new-path failure; it enters adjudication.

### 23.6 Deprecation gate

A legacy component can retire only when:

- all supported capabilities have explicit replacements;
- contract fixtures pass;
- frozen and hidden tests meet or exceed baseline;
- no critical security/resource regression exists;
- migration and rollback have been exercised;
- docs and operational tooling are updated;
- at least one release cycle has run with the replacement as default;
- repository references prove no undeclared consumers remain.

---
## 24. Phase 11 execution program

Phase 11 is organized by dependency and evidence gates, not arbitrary calendar promises. Workstreams may overlap only when their contracts are stable enough to prevent duplicate architecture.

### P11.0 — Truth lock and baseline

**Purpose:** Establish an honest, reproducible starting point.

**Deliverables:**

- machine-generated repository capability inventory;
- frozen current behavior fixtures and 45-case regression smoke suite;
- full test/eval/resource commands with environment manifest;
- platform-specific RSS measurement harness;
- documentation claim checker;
- integration map showing which declared modules are live, shadowed, disconnected, or legacy;
- initial security and data-flow review;
- no-regression baseline report with confidence intervals where applicable.

**Exit gates:**

- all current tests pass from a clean checkout;
- observed module/test/plugin/data/resource counts are reproducible;
- no known documentation claim materially overstates current capability;
- current public query path is mapped end-to-end with evidence;
- baseline artifacts are immutable and versioned.

### P11.1 — Canonical contracts and state snapshots

**Purpose:** Make semantic determinism definable and testable.

**Deliverables:**

- CognitiveTaskEnvelope compatibility extension;
- StateSnapshot manifest and content hash;
- canonical serialization policy;
- deterministic semantic IDs;
- tool/config/rule/knowledge manifest hashing;
- replay bundle schema;
- cross-platform golden serialization fixtures.

**Exit gates:**

- same request/snapshot produces identical semantic hashes over 100 repeated runs;
- volatile metadata does not influence route, plan, claims, or answer semantics;
- old API and serialized response fixtures remain readable;
- snapshot corruption is detected and fails closed.

### P11.2 — Unified cognitive transaction loop

**Purpose:** Replace parallel documented-vs-live pipelines with one authoritative orchestration path.

**Deliverables:**

- cognitive loop coordinating shield, compiler, contract, unknowns, retrieval, planner, executor, verifier, synthesizer, and memory candidate stages;
- `Axima.query` compatibility adapter;
- microkernel shadow integration;
- structured stage outcomes and reason codes;
- transaction checkpoint/rollback protocol;
- resource accounting at every stage.

**Exit gates:**

- current supported queries pass through the loop in shadow mode;
- no silent legacy fallback;
- every fallback is contract-bounded and traced;
- 100% of response paths have a state snapshot and transaction ID;
- no current frozen regression without adjudicated reason.

### P11.3 — Durable memory substrate

**Purpose:** Provide safe cross-session state without loading the corpus into RAM.

**Deliverables:**

- SQLite schema, payload packs, migrations, integrity checks;
- persistence behind `FourPlaneMemory` facade;
- complete MemoryRecord metadata;
- TTL, sensitivity, export, deletion/tombstone, and backup behavior;
- atomic snapshot commit and rollback;
- crash recovery and corruption quarantine.

**Exit gates:**

- restart preserves approved records and versions;
- tampering is detected;
- partial commits recover safely;
- deletion/invalidation propagates correctly;
- full reference workload remains within resource budget;
- restore reproduces reference semantic hashes.

### P11.4 — Deterministic retrieval lattice

**Purpose:** Turn stored structure into useful bounded context.

**Deliverables:**

- typed multi-channel candidate generation;
- fixed-point deterministic ranker;
- temporal, trust, sensitivity, and verification filters;
- provenance-aware deduplication and source diversity;
- cache keyed by state and policy;
- score explanations and retrieval traces;
- corpus ingestion adapter.

**Exit gates:**

- supported retrieval benchmark reaches target recall@10 and citation alignment;
- repeated retrieval ordering is identical under a fixed snapshot;
- revoked/private/invalid records never leak;
- full corpus remains disk-backed under 50 MiB reference profile;
- cache and fresh results are semantically identical.

### P11.5 — Proof-obligated planner and executor

**Purpose:** Make planning real rather than documented scaffolding.

**Deliverables:**

- typed pre/postcondition registry;
- proof obligations and fixed node vocabulary;
- deterministic strategy and plan scoring;
- budget admission and checkpoints;
- local repair and recovery plans;
- transactional side-effect execution;
- planner shadow comparison against existing routes.

**Exit gates:**

- 100% structural plan validity;
- mandatory verification nodes present by contract;
- deterministic plan hashes;
- designed recovery benchmark meets threshold;
- failed dependencies cannot produce released descendants;
- side-effect rollback passes all fixtures.

### P11.6 — Verification authority and proof-carrying responses

**Purpose:** Make verification determine release.

**Deliverables:**

- claim decomposition;
- mandatory constellation gate;
- verifier applicability/coverage policy;
- independence groups and confidence conservation;
- repair requests;
- receipt persistence;
- response fields/references for release decision, receipts, risk, and snapshot.

**Exit gates:**

- no claim requiring verification ships without applicable receipts;
- counterexamples block affected claims;
- no-applicable-verifier produces unsupported status;
- critical false release count is zero on frozen suite;
- calibration and abstention metrics meet domain thresholds;
- verification artifacts replay successfully.

### P11.7 — Executable memory and governed learning

**Purpose:** Allow AXIMA to improve across sessions without opaque training or self-corruption.

**Deliverables:**

- RuleIR/SkillIR interpreter;
- trace-to-candidate extraction;
- anti-unification with diversity checks;
- test synthesis and adversarial promotion harness;
- approval/canary/revocation lifecycle;
- state compiler and semantic diff;
- dependency-aware truth maintenance.

**Exit gates:**

- arbitrary code cannot enter executable memory;
- zero canonical promotions without required receipts and approval;
- frozen reuse tasks show measurable utility gain;
- unrelated tasks show no significant regression;
- revoked skills stop influencing new snapshots;
- historical snapshot replay remains exact.

### P11.8 — Exact mathematics depth

**Purpose:** Establish the first flagship specialist domain.

**Deliverables:**

- unified canonical math AST;
- exact-first numeric domains;
- expanded algebra/calculus/discrete/linear-algebra operators;
- domain and assumption handling;
- lemma/proof library;
- strategy portfolio and counterexample search;
- independent verification methods;
- comprehensive supported/unsupported capability ledger.

**Exit gates:**

- target exact accuracy and domain-error detection achieved;
- solution sets are complete on declared classes;
- no false `PROVEN` labels;
- parser metamorphic and adversarial suites pass;
- unsupported classes abstain cleanly;
- reference resource budget passes.

### P11.9 — Verified repository engineering

**Purpose:** Move from template code generation to tested transactional changes.

**Deliverables:**

- repository snapshot and symbol/dependency model;
- requirements and acceptance-test contracts;
- minimal diff planner;
- AST-aware generation/transformation;
- compile, type, static, test, and security verification;
- dependency policy;
- transactional apply and rollback;
- code change receipts.

**Exit gates:**

- target compile/test rates achieved on declared tasks;
- hidden tests demonstrate non-template generalization within supported patterns;
- no unauthorized writes/network/dependency installs;
- repair never weakens tests to pass;
- deterministic patch hashes under fixed snapshots;
- rollback succeeds.

### P11.10 — Structured reasoning and long context

**Purpose:** Expand beyond lookup while remaining evidence-bound.

**Deliverables:**

- argument and decision IR;
- constraint/finite-search engine;
- causal and temporal integration;
- multi-resolution context compiler;
- hierarchical semantic digests;
- contradiction and state-update handling;
- adaptive explanation over stable claims.

**Exit gates:**

- reasoning validity and assumption exposure targets met;
- distractor/paraphrase/negation robustness passes;
- long-context citation and invariant recall meet targets;
- compression loss stays below declared threshold;
- memory remains bounded as source length grows;
- unsupported open-ended requests abstain rather than fabricate.

### P11.11 — 50 MiB and cross-platform hardening

**Purpose:** Convert measured resource discipline into an enforceable product property.

**Deliverables:**

- lazy import/plugin lifecycle;
- RSS platform adapters and admission control;
- deterministic eviction/degradation;
- leak and long-session harness;
- minimal/reference/extended profiles;
- ARM/Android portability adapters;
- performance and resource dashboards.

**Exit gates:**

- peak ≤50 MiB on every claimed reference platform/workload;
- no unbounded retained-memory slope;
- resource exhaustion is clean and truthful;
- semantic outputs match across platform contracts;
- optional acceleration changes performance only, not meaning.

### P11.12 — Production and ecosystem release

**Purpose:** Make the cognitive kernel safe for developers and integrators.

**Deliverables:**

- stable API/SDK contracts;
- package/release provenance;
- lifecycle, health, backup, restore, migration, and observability;
- plugin/skill pack format and validation kit;
- operator and security documentation;
- contribution/governance process;
- sealed release evaluation and reproducibility bundle.

**Exit gates:**

- Phase 11 production gate in Section 26 passes;
- clean installation on supported platforms;
- backup/restore and rollback drills pass;
- no critical/high unmitigated security findings;
- documentation truth gate passes;
- at least one external reproduction of core benchmark/resource results.

---

## 25. Ultra-Cosmic horizons

These horizons begin only after the Phase 11 production foundation. They are research programs with kill criteria, not promises.

### U1 — State-addressed cognition

Every semantic artifact, rule, plan, proof, world model, and answer is addressable by content and state. AXIMA can answer not only “what is the result?” but “under which exact knowledge state, rules, assumptions, and tools was this result valid?”

**Breakthrough target:** reproducible cognition analogous to reproducible software builds.  
**Kill criterion:** if snapshot overhead or missing external state prevents reliable replay on declared tasks, restrict the claim and redesign.

### U2 — Executable knowledge civilization

Communities publish small signed/hashed domain packs containing facts, rules, proof obligations, verifiers, tests, and capability manifests—not opaque models.

A pack is accepted only after:

- schema and license validation;
- provenance and conflict analysis;
- resource profiling;
- adversarial tests;
- verifier independence review;
- local governance approval;
- canary activation.

**Breakthrough target:** intelligence grows by composing auditable domain packs.  
**Safety condition:** federation never bypasses local policy or canonical promotion gates.

### U3 — Proof economy and epistemic accounting

AXIMA treats claims as liabilities that require evidence coverage. Plans optimize not only task completion but reduction of residual uncertainty per resource unit.

Capabilities can advertise:

- expected information gain;
- proof strength;
- known failure envelope;
- verification cost;
- confidence transformation.

**Breakthrough target:** choose the cheapest plan that satisfies the evidence contract, not the shortest plausible answer.

### U4 — Self-healing world models

Versioned temporal and causal models update through evidence events. Corrections automatically identify affected predictions, plans, explanations, and skills while preserving historical states.

**Breakthrough target:** principled “changing its mind” with complete dependency impact and no silent history rewrite.  
**Boundary:** causal claims remain model-relative and expose identification assumptions.

### U5 — Machine-checkable scientific collaborator

AXIMA compiles research questions into:

- hypothesis sets;
- discriminating predictions;
- experiment/simulation plans;
- measurement and uncertainty contracts;
- analysis code;
- falsification criteria;
- evidence updates.

**Breakthrough target:** reduce scientific workflow error and improve reproducibility in bounded domains.  
**Prohibition:** simulated or generated evidence can never be labeled an empirical discovery.

### U6 — Verified embodied/robotic cognition

The cognitive transaction model extends to sensors and actuators:

- sensor readings become witnessed evidence with calibration metadata;
- plans carry physical safety invariants;
- simulation and dry-run precede action;
- capability tokens restrict actuator scope;
- runtime monitors can stop execution;
- human approval applies to high-impact actions.

**Breakthrough target:** proof-obligated robotic tasks under explicit world-model uncertainty.  
**Prerequisite:** formal safety case and hardware-specific independent review.

### U7 — Substrate optimization without semantic fork

After the Python reference stabilizes, measured hotspots may gain optional Rust/C extensions or a compact standalone kernel.

Rules:

- Python remains the executable reference specification until replacement parity is proven;
- native paths consume the same canonical contracts and fixtures;
- semantic hashes must match;
- native code expands neither authority nor truth level;
- memory/speed improvement must justify maintenance and security cost;
- pure-Python reference remains available for audit and portability where practical.

### U8 — Verified specialist frontier

AXIMA seeks independently demonstrated superiority in exact mathematics, repository transformation, evidence-grounded reasoning, or other declared domains.

A frontier claim requires:

- broad external benchmarks;
- machine-verifiable or independently judged outcomes;
- comparable tool/resource rules;
- confidence intervals;
- published failures and coverage limits;
- third-party reproduction;
- no extrapolation to unrelated domains.

This is the valid route to “king of AIs”: earn domain crowns one by one, with receipts.

---

## 26. Release gates

### 26.1 Phase 11 alpha

- canonical contracts and snapshots implemented;
- cognitive loop operational in shadow mode;
- real verification attached to responses;
- planner invoked on at least one bounded domain;
- ≥1,000 frozen end-to-end cases;
- all baseline regressions adjudicated;
- preliminary resource harness passes on primary Linux target;
- no critical security findings.

### 26.2 Phase 11 beta

- persistent memory and deterministic retrieval operational;
- governed candidate promotion functional, with canonical auto-promotion still disabled unless separately approved;
- math flagship path uses plan + verification release gate;
- ≥2,500 frozen cases plus adversarial and mutation suites;
- 50 MiB gate passes on primary reference platform;
- long-session, crash recovery, backup restore, and invalidation tests pass;
- public docs distinguish supported, partial, and unsupported capabilities.

### 26.3 Release candidate

- code and structured reasoning tracks meet declared thresholds;
- ≥5,000 diverse cases with hidden/external subsets;
- security red-team and fuzzing complete;
- 50 MiB/reference semantic gates pass across claimed desktop and ARM platforms;
- no unbounded memory growth in soak tests;
- migration/rollback rehearsed from previous release;
- verifier false-accept targets met;
- API and schema compatibility freeze.

### 26.4 Production

All of the following are mandatory:

- deterministic semantic replay 100% on reference corpus;
- zero critical false release in frozen safety suite;
- zero canonical memory promotion without required approval and receipts;
- no open critical/high security issue;
- peak reference RSS ≤50 MiB on every platform advertised with that claim;
- backup restore and snapshot rollback 100%;
- 30-day or equivalent accelerated soak with no unresolved memory/resource trend;
- published capability ledger and limitations;
- documentation truth checks pass;
- independent reproduction of installation, core tests, and reference metrics.

### 26.5 Ultra-Cosmic designation

“Ultra-Cosmic” may be used as an internal architecture maturity label only when:

- production gates hold over multiple releases;
- cumulative memory demonstrates statistically significant benefit without canonical corruption;
- self-healing dependencies handle corrections and revocations completely;
- at least two specialist domains have independent frontier comparisons;
- external developers can build audited domain packs without core modification;
- semantic replay works across at least three operating-system families and two architectures;
- no claim implies universal or human-level general intelligence without corresponding evidence.

---

## 27. Risk register

| Risk | Failure mode | Mitigation | Kill/rollback signal |
|---|---|---|---|
| Architecture without integration | More modules, unchanged intelligence | Integration-first milestones; live-path tests | New module has no benchmark/live consumer |
| Symbolic brittleness | Small phrasing changes break behavior | Meaning IR, metamorphic tests, clarification | Robustness below baseline |
| False confidence | Heuristic output labeled verified | Claim gate, confidence conservation | Any critical false `PROVEN` release |
| Memory poisoning | Bad trace becomes reusable rule | Quarantine, diverse traces, tests, approval | Poison bypasses promotion controls |
| Skill overfitting | Candidate memorizes examples | Holdout/adversarial tests, anti-leak checks | Utility disappears outside source traces |
| Non-deterministic learning | Same snapshot yields different route | Immutable manifests, stable sorting, replay | Semantic hash divergence |
| State explosion | Versions/dependencies grow without bound | Compaction, packs, retention, bounded graph work | Resource slope exceeds budget |
| 50 MiB metric gaming | Heap passes but RSS or children exceed | OS-level RSS and child accounting | Any claimed workload exceeds envelope |
| Cross-platform drift | Different float/order/tool output | Exact/fixed-point policies, canonicalization | Semantic mismatch on supported platform |
| Verification monoculture | Multiple verifiers share same bug | Independence groups, alternate methods | Correlated checks counted as quorum |
| Planner complexity | Planning costs more than task | Fast path and admission model | Net task utility/latency regression |
| Retrieval leakage | Private/stale/revoked item surfaces | Filter before rank/cache, tenant scope | Any unauthorized result in red-team suite |
| Audit growth | Logs violate 50 MiB/privacy | References, disk streaming, retention/redaction | RAM/log limits or privacy gate fail |
| Benchmark overfitting | Public score rises, hidden quality falls | Hidden suites, mutations, immune system | Significant public-hidden gap |
| Legacy lock-in | New path never becomes authoritative | Domain-by-domain canary/default dates after gates | Shadow parity stalls without root-cause plan |
| Rewrite temptation | Momentum lost in reorganizing | ADR requiring measured value | Feature parity/test coverage declines |
| Unsafe autonomy | System changes policy/deploys itself | Immutable governance, capability tokens | Any bypass of approval boundary |
| Corpus inconsistency | Conflicts produce arbitrary fact | Bitemporal claims, contradiction court | Unresolved conflict released as direct fact |
| Dependency/tool instability | Tool version changes outcomes | Tool manifests and D-classification | Replay mismatch after version drift |
| Scope inflation | “King of AIs” drives theatrical features | Measurable domain gates and kill criteria | Feature lacks user task/benchmark/resource proof |

---

## 28. Rejected or quarantined ideas

Maximum ambition requires rejecting seductive but invalid shortcuts.

### 28.1 Rejected for production

1. **Big-bang rewrite:** destroys compatibility evidence and delays real capability.
2. **Arbitrary self-written Python as memory:** creates code execution, reproducibility, and governance failures.
3. **Raw conversation as canonical knowledge:** mixes privacy, error, and context-specific content with truth.
4. **Generator self-verification:** produces circular confidence.
5. **Changing benchmark expectations to match outputs:** measures conformity to current formatting, not correctness.
6. **Loading the full corpus into Python objects:** conflicts with the 50 MiB constraint.
7. **Unbounded search or infinite reasoning:** conflicts with safety, determinism, and finite resources.
8. **Replacing MeaningIR with exotic mathematics without parity:** loses proven contracts for theoretical novelty.
9. **Topos, category, transfinite, or “multiverse” terminology as capability evidence:** mathematical vocabulary is not an implementation result.
10. **Claiming O(1) retrieval over trillions of facts in 50 MiB:** physically and informationally implausible without carefully scoped external storage and benchmarks.
11. **Universal translation from a language-independent proof graph:** requires measured language-specific semantics; category labels do not solve realization.
12. **Immediate Rust rewrite:** optimizes before semantic architecture stabilizes.
13. **Large learned embeddings hidden as retrieval infrastructure:** violates the reference zero-parameter contract.
14. **Same output forever despite state updates:** confuses determinism with immobility.
15. **More plugins as a proxy for more intelligence:** only integrated task success counts.

### 28.2 Allowed only as bounded research

- hypervector or associative signatures for candidate generation;
- formal category-theoretic representations where they simplify a concrete compiler proof;
- fixed-point semantics for finite monotone cyclic rule systems;
- alternate native kernels;
- optional external theorem provers;
- distributed domain-pack federation;
- robotic execution.

Each requires an ADR, benchmark, threat analysis, resource budget, compatibility path, and kill criterion before entering production planning.

---

## 29. How this plan strengthens the original proposals

| Original direction | Strengthened form |
|---|---|
| Intent compiler | Existing MeaningIR + contract + ambiguity/unknown boundary + state snapshot |
| Typed memory | Durable tiered records with provenance, verification, temporal scope, versions, sensitivity, and dependencies |
| Retrieval lattice | Multi-channel deterministic integer ranking with permission, time, trust, and independence filters |
| Planner contracts | Typed proof obligations, admission control, rollback, repair, and release dependencies |
| Verifier stack | Mandatory claim-level independent authority with receipts and truth ceilings |
| Answer synthesizer | Deterministic claim-to-text compiler with round-trip and citation alignment |
| Executable memory | Safe RuleIR/SkillIR—not arbitrary code—with promotion, canary, monitoring, and revocation |
| Self-healing graph | Bounded truth-maintenance system preserving historical snapshots |
| Meaning compression | Source-linked semantic atoms with measured loss and reconstruction probes |
| Multi-resolution reasoning | Contract → strategy → skeleton → exact execution → audit |
| 50 MB budget | Peak RSS protocol, component envelope, degradation ladder, cross-platform gates |
| Learning across sessions | Immutable state compilation and governed activation, deterministic by snapshot |
| Production quality | Backup, migration, security, observability, external reproduction, and honest claims |

---

## 30. Required ADRs before implementation

1. Determinism and immutable state-snapshot contract.
2. 50 MiB measurement scope and supported platform matrix.
3. Persistent memory schema and SQLite/FTS fallback.
4. Canonical serialization and content addressing.
5. RuleIR/SkillIR language and interpreter security.
6. Memory promotion, approval, canary, and revocation policy.
7. Retrieval feature set, ranking formula, and cache keys.
8. Planner pre/postcondition registry and proof obligations.
9. Claim decomposition and verification release policy.
10. Confidence calibration and independence groups.
11. Constrained synthesis and semantic round-trip.
12. Corpus ingestion, licensing, provenance, and temporal validity.
13. Public API/schema compatibility and migration.
14. Resource governor and degradation behavior.
15. External tools, sandbox, and determinism classes.
16. Competitive benchmark and claim policy.
17. Optional native extension parity requirements.

An ADR is approved only with alternatives, tradeoffs, compatibility impact, security impact, resource impact, and measurable acceptance criteria.

---

## 31. Definition of done for every Phase 11 component

A component is not done because its classes exist or unit tests pass. It is done when:

- responsibility and non-responsibilities are documented;
- typed contracts and schema versions exist;
- deterministic serialization and replay are tested;
- integration into the live/shadow transaction is demonstrated;
- unit, property, metamorphic, adversarial, integration, and failure tests appropriate to risk pass;
- performance and peak RSS are measured;
- security and privacy impact is reviewed;
- structured errors and degradation behavior exist;
- metrics and trace events are bounded and documented;
- backward compatibility and migration are tested;
- rollback or revocation is demonstrated;
- capability ledger and limitations are updated;
- benchmark improvement is shown without hidden-suite regression;
- no prohibited dependency or learned parameter enters the reference profile;
- documentation truth checks pass.

---

## 32. Program-level definition of done

Phase 11 is complete only when AXIMA can, on the reference profile:

1. accept a request through the stable public API;
2. bind it to an immutable state snapshot;
3. compile meaning, intent, unknowns, constraints, risk, and evidence contract;
4. retrieve relevant verified facts, rules, skills, failures, and proofs deterministically;
5. construct and validate a proof-obligated plan;
6. execute capabilities within permissions and budgets;
7. build a claim/evidence/derivation graph;
8. independently verify all claims required by contract;
9. repair or abstain when verification fails;
10. synthesize an answer using only releasable claims;
11. attach truth level, confidence bounds, evidence, receipts, unknowns, snapshot, and trace references;
12. extract reusable memory candidates without auto-promoting them;
13. commit approved memory atomically into a new versioned snapshot;
14. replay historical answers against historical snapshots;
15. retract/correct evidence and invalidate dependent current claims safely;
16. export/delete eligible user memory and restore backups;
17. operate at or below 50 MiB peak RSS on every platform carrying that claim;
18. pass the production evaluation, security, compatibility, and documentation gates;
19. disclose unsupported domains and abstain accurately;
20. demonstrate measurable capability improvement beyond the current pattern/lookup baseline.

---

## 33. First implementation sequence after plan approval

No implementation should begin until this plan is reviewed and the first ADRs are accepted. The lowest-risk, highest-leverage sequence is:

1. truth-lock current tests, evaluations, documentation, and RSS harness;
2. define state snapshot and canonical serialization;
3. attach state/transaction identifiers without changing behavior;
4. wire existing VerificationConstellation in shadow mode and preserve its reports;
5. wire existing CognitivePlanner in shadow mode;
6. define typed conditions and proof obligations for one exact-math slice;
7. make verification authoritative for that slice;
8. implement durable memory in read-only/import mode;
9. implement retrieval lattice and benchmark it over real corpus data;
10. enable memory candidates and manual approval;
11. implement safe SkillIR canary for one proven reusable strategy;
12. expand only after determinism, security, memory, and hidden-eval gates pass.

This order makes AXIMA more truthful and integrated before making it more autonomous.

---

## 34. Final engineering covenant

AXIMA's advantage will not come from sounding omniscient. It will come from knowing exactly:

- what task it is solving;
- which state of reality it used;
- what it retrieved;
- which assumptions it made;
- what plan it executed;
- which rules and tools produced each claim;
- what independent checks passed or failed;
- what remains unknown;
- what it learned and why that learning was allowed;
- how to reproduce, correct, revoke, or improve the result.

The Ultra-Cosmic destination is therefore not a magical chatbot. It is a compact, cumulative, self-correcting, proof-carrying cognitive operating system whose intelligence is inspectable, whose memory is executable but governed, whose uncertainty is honest, whose resource use is bounded, and whose strongest claims are earned by reproducible evidence.

**Build the blade, measure the edge, and never call it a crown until independent evidence proves the domain victory.**
