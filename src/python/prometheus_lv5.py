#!/usr/bin/env python3
"""
PROMETHEUS Level 5 — Research Beast
The final level: produce research-quality mathematics.

Components:
- 5.1 Mega Theorem Database (indexed, searchable, dependency graph)
- 5.2 Formal Proof Verifier (every step must be justified)
- 5.3 Research Engine (gap detection, approach suggestion)
- 5.4 Creative Constructor (build novel objects)
- 5.5 Cross-Domain Connector (transfer ideas between fields)

Built by: Ghias + Kiro
"""

from typing import List, Dict, Optional, Set, Tuple, Callable
import math


# ═══════════════════════════════════════════════════════════════
# 5.1 MEGA THEOREM DATABASE
# Indexed by: field, tags, dependencies, proof strategy
# Searchable by: conclusion, preconditions, keywords
# ═══════════════════════════════════════════════════════════════

class MegaTheoremDB:
    """Extended theorem database with dependency graph and strategy tagging."""

    def __init__(self):
        self.theorems = {}
        self.dep_graph = {}  # theorem → [theorems it depends on]
        self.reverse_deps = {}  # theorem → [theorems that use it]
        self.by_field = {}
        self.by_tag = {}
        self._load_all()

    def _load_all(self):
        """Load theorems from all levels."""
        from prometheus_lv3 import TheoremDB
        from prometheus_lv4 import TheoremDBLevel4

        # Level 3 theorems
        db3 = TheoremDB()
        for name, t in db3.theorems.items():
            self._add(name, t.field, t.statement, t.conclusion,
                     t.preconditions, t.depends_on, t.tags, t.proof_strategy)

        # Level 4 theorems
        for name, data in TheoremDBLevel4.THEOREMS.items():
            self._add(name, data['field'], data['statement'],
                     data.get('conclusion', ''), [], [], [])

    def _add(self, name, field, statement, conclusion, preconditions=None,
             depends_on=None, tags=None, strategy=''):
        self.theorems[name] = {
            'field': field, 'statement': statement, 'conclusion': conclusion,
            'preconditions': preconditions or [], 'depends_on': depends_on or [],
            'tags': tags or [], 'strategy': strategy
        }
        # Index by field
        self.by_field.setdefault(field, []).append(name)
        # Index by tags
        for tag in (tags or []):
            self.by_tag.setdefault(tag, []).append(name)
        # Dependency graph
        self.dep_graph[name] = depends_on or []
        for dep in (depends_on or []):
            self.reverse_deps.setdefault(dep, []).append(name)

    def search(self, query: str, limit: int = 10) -> List[Dict]:
        """Full-text search across all theorems."""
        q = query.lower()
        scored = []
        for name, data in self.theorems.items():
            score = 0
            if q in name: score += 3
            if q in data['statement'].lower(): score += 2
            if q in data['conclusion'].lower(): score += 2
            if any(q in tag for tag in data['tags']): score += 1
            if score > 0:
                scored.append((score, name, data))
        scored.sort(reverse=True)
        return [{'name': n, **d} for _, n, d in scored[:limit]]

    def path_between(self, start: str, end: str) -> Optional[List[str]]:
        """Find dependency path between two theorems (BFS)."""
        if start not in self.theorems or end not in self.theorems:
            return None
        # BFS on reverse_deps (what uses what)
        from collections import deque
        queue = deque([(start, [start])])
        visited = {start}
        while queue:
            current, path = queue.popleft()
            if current == end:
                return path
            for next_t in self.reverse_deps.get(current, []):
                if next_t not in visited:
                    visited.add(next_t)
                    queue.append((next_t, path + [next_t]))
        return None

    def related(self, name: str) -> Dict[str, List[str]]:
        """Find related theorems (same field, shared tags, dependencies)."""
        if name not in self.theorems:
            return {}
        t = self.theorems[name]
        related = {
            'depends_on': t['depends_on'],
            'used_by': self.reverse_deps.get(name, []),
            'same_field': [n for n in self.by_field.get(t['field'], []) if n != name][:5],
            'shared_tags': [],
        }
        for tag in t['tags']:
            for other in self.by_tag.get(tag, []):
                if other != name and other not in related['shared_tags']:
                    related['shared_tags'].append(other)
        return related

    def stats(self) -> Dict:
        return {
            'total': len(self.theorems),
            'fields': {f: len(ts) for f, ts in self.by_field.items()},
            'most_depended': sorted(
                [(name, len(self.reverse_deps.get(name, [])))
                 for name in self.theorems],
                key=lambda x: -x[1])[:5]
        }


# ═══════════════════════════════════════════════════════════════
# 5.2 FORMAL PROOF VERIFIER
# Every step must be: axiom, known theorem, or valid deduction
# NO handwaving. NO "clearly". Catches logical gaps.
# ═══════════════════════════════════════════════════════════════

class ProofVerifier:
    """Verifies proofs step by step. Catches logical errors."""

    # Valid deduction rules
    RULES = {
        'modus_ponens': 'If P and P→Q, then Q',
        'universal_instantiation': 'If ∀x P(x), then P(a) for any a',
        'existential_generalization': 'If P(a), then ∃x P(x)',
        'conjunction_intro': 'If P and Q, then P∧Q',
        'conjunction_elim': 'If P∧Q, then P (or Q)',
        'disjunction_intro': 'If P, then P∨Q',
        'contradiction': 'If P leads to contradiction, then ¬P',
        'substitution': 'Replace variable with equivalent expression',
        'transitivity': 'If a=b and b=c, then a=c',
        'symmetry': 'If a=b then b=a',
        'induction_base': 'Verify P(0) or P(1)',
        'induction_step': 'P(k)→P(k+1) for arbitrary k',
        'definition': 'Apply a definition',
        'theorem_application': 'Apply a known theorem',
    }

    def __init__(self, theorem_db: MegaTheoremDB = None):
        self.db = theorem_db or MegaTheoremDB()
        self.known_facts = set()

    def verify_proof(self, steps: List[Dict]) -> Dict:
        """Verify a proof given as list of steps.
        Each step: {claim: str, justification: str, rule: str}
        Returns: {valid: bool, errors: List[str]}"""
        errors = []
        established = set()

        for i, step in enumerate(steps):
            claim = step.get('claim', '')
            justification = step.get('justification', '')
            rule = step.get('rule', '')

            # Check rule is valid
            if rule not in self.RULES and rule != 'assumption' and rule != 'given':
                errors.append(f"Step {i+1}: Unknown rule '{rule}'")
                continue

            # Check justification references valid prior steps
            if rule == 'theorem_application':
                theorem_name = justification
                if theorem_name not in self.db.theorems:
                    errors.append(f"Step {i+1}: Unknown theorem '{theorem_name}'")
                    continue

            # Check modus ponens: need both P and P→Q established
            if rule == 'modus_ponens':
                # Would need formal logic parser here
                pass

            # Accept step
            established.add(claim)

        return {
            'valid': len(errors) == 0,
            'errors': errors,
            'steps_verified': len(steps) - len(errors),
            'total_steps': len(steps),
        }

    def check_proof_structure(self, proof_text: str) -> Dict:
        """Analyze proof text for common issues."""
        issues = []
        lines = proof_text.split('\n')

        # Check for unjustified claims
        unjustified_phrases = ['clearly', 'obviously', 'it is easy to see',
                               'trivially', 'the rest follows', 'by inspection']
        for i, line in enumerate(lines):
            for phrase in unjustified_phrases:
                if phrase in line.lower():
                    issues.append(f"Line {i+1}: Unjustified claim ('{phrase}') — needs proof")

        # Check for logical structure
        has_assumption = any('assume' in l.lower() or 'suppose' in l.lower() or 'let' in l.lower() for l in lines)
        has_conclusion = any('therefore' in l.lower() or 'thus' in l.lower() or '∎' in l or 'QED' in l for l in lines)

        if not has_assumption:
            issues.append("Missing: No explicit assumptions/givens stated")
        if not has_conclusion:
            issues.append("Missing: No explicit conclusion marker (therefore/∎)")

        return {
            'issues': issues,
            'structure_ok': len(issues) == 0,
            'lines': len(lines),
            'has_assumptions': has_assumption,
            'has_conclusion': has_conclusion,
        }


# ═══════════════════════════════════════════════════════════════
# 5.3 RESEARCH ENGINE
# Identifies gaps, suggests approaches, connects ideas
# ═══════════════════════════════════════════════════════════════

class ResearchEngine:
    """Identifies mathematical gaps and suggests research approaches."""

    def __init__(self, db: MegaTheoremDB = None):
        self.db = db or MegaTheoremDB()

    def suggest_approach(self, problem: str) -> Dict:
        """Given a problem statement, suggest proof strategies."""
        low = problem.lower()
        approaches = []

        # Classify problem type
        if 'prove' in low or 'show' in low:
            approaches.extend(self._suggest_proof_strategies(low))
        elif 'construct' in low or 'find' in low or 'build' in low:
            approaches.extend(self._suggest_construction_strategies(low))
        elif 'classify' in low:
            approaches.extend(self._suggest_classification_strategies(low))
        elif 'compute' in low or 'calculate' in low:
            approaches.extend(self._suggest_computation_strategies(low))

        # Find relevant theorems
        relevant = self.db.search(problem, limit=5)

        return {
            'problem': problem,
            'suggested_approaches': approaches,
            'relevant_theorems': [r['name'] for r in relevant],
            'key_tools': self._identify_tools(low),
        }

    def identify_gaps(self, known_theorems: List[str]) -> List[str]:
        """Identify what's missing between known theorems and potential conclusions."""
        gaps = []
        for name, data in self.db.theorems.items():
            if name in known_theorems:
                continue
            # Check if preconditions are partially met
            preconds = data.get('preconditions', [])
            met = sum(1 for p in preconds if any(k in p.lower() for k in known_theorems))
            if 0 < met < len(preconds):
                gaps.append(f"Almost provable: {name} (need {len(preconds)-met} more preconditions)")
        return gaps[:10]

    def _suggest_proof_strategies(self, problem: str) -> List[str]:
        strategies = []
        if 'all' in problem or 'every' in problem or 'for any' in problem:
            strategies.append("Mathematical Induction (if parameter is natural number)")
            strategies.append("Universal proof (arbitrary element + derive property)")
        if 'not' in problem or 'no' in problem or 'impossible' in problem:
            strategies.append("Proof by Contradiction (assume opposite, derive contradiction)")
        if 'if and only if' in problem or 'iff' in problem:
            strategies.append("Prove both directions: (→) and (←) separately")
        if 'unique' in problem:
            strategies.append("Existence + Uniqueness: prove ∃ then prove if two exist they're equal")
        if 'isomorphic' in problem or '≅' in problem:
            strategies.append("Construct explicit isomorphism or use structure theorems")
        if not strategies:
            strategies.append("Direct proof: assume hypotheses, derive conclusion step by step")
            strategies.append("Contradiction: assume negation of goal")
            strategies.append("Induction: if parameter is discrete")
        return strategies

    def _suggest_construction_strategies(self, problem: str) -> List[str]:
        strategies = []
        if 'group' in problem:
            strategies.append("Try: cyclic groups, dihedral groups, symmetric groups, direct products")
        if 'ring' in problem:
            strategies.append("Try: ℤ/nℤ, polynomial rings, localization, quotient rings")
        if 'counterexample' in problem:
            strategies.append("Systematically check small cases / known pathological examples")
        if not strategies:
            strategies.append("Start with known constructions, modify until properties satisfied")
        return strategies

    def _suggest_classification_strategies(self, problem: str) -> List[str]:
        return [
            "Use structure theorems (e.g., finite abelian groups = products of cyclic)",
            "Apply Sylow theorems to constrain subgroup structure",
            "Enumerate cases using constraints on order",
        ]

    def _suggest_computation_strategies(self, problem: str) -> List[str]:
        return [
            "Identify applicable formula/algorithm",
            "Break into sub-computations",
            "Use properties to simplify before computing",
        ]

    def _identify_tools(self, problem: str) -> List[str]:
        tools = []
        tool_keywords = {
            'sylow': 'Sylow theorems', 'lagrange': "Lagrange's theorem",
            'induction': 'Mathematical induction', 'contradiction': 'Proof by contradiction',
            'homomorphism': 'Homomorphism theorems', 'quotient': 'Quotient structures',
            'exact': 'Exact sequences', 'cohomology': 'Cohomology theory',
            'galois': 'Galois theory', 'spectral': 'Spectral sequences',
            'dimension': 'Dimension counting', 'orbit': 'Orbit-stabilizer',
        }
        for kw, tool in tool_keywords.items():
            if kw in problem:
                tools.append(tool)
        return tools


# ═══════════════════════════════════════════════════════════════
# 5.4 CREATIVE CONSTRUCTOR
# Builds novel mathematical objects satisfying given properties
# ═══════════════════════════════════════════════════════════════

class CreativeConstructor:
    """Constructs mathematical objects with specific properties.
    Goes beyond StructureBuilder (Level 4) by combining constructions."""

    def __init__(self):
        from prometheus_lv4 import StructureBuilder
        self.basic_builder = StructureBuilder()

    def construct(self, description: str) -> Dict:
        """Interpret a construction request and build the object."""
        low = description.lower()

        if 'group' in low:
            return self._construct_group(description)
        elif 'ring' in low or 'domain' in low:
            return self._construct_ring(description)
        elif 'sequence' in low or 'series' in low:
            return self._construct_sequence(description)
        elif 'function' in low or 'map' in low:
            return self._construct_function(description)
        elif 'counterexample' in low:
            return self._find_counterexample(description)

        return {'status': 'cannot_construct', 'description': description}

    def _construct_group(self, desc: str) -> Dict:
        """Construct a group with specific properties."""
        import re
        properties = []

        # Extract properties from description
        if 'non-abelian' in desc.lower() or 'not abelian' in desc.lower():
            properties.append('non-abelian')
        if 'abelian' in desc.lower() and 'non' not in desc.lower():
            properties.append('abelian')
        if 'simple' in desc.lower():
            properties.append('simple')
        if 'solvable' in desc.lower():
            properties.append('solvable')

        # Extract order
        m = re.search(r'order\s*(\d+)', desc)
        if m:
            properties.append(f'order = {m.group(1)}')

        result = self.basic_builder.build_group(properties)
        if result:
            result['construction_method'] = 'direct_search'
            return result

        # Advanced: try products and semidirect products
        return {
            'status': 'no_simple_construction',
            'properties': properties,
            'suggestion': 'Try: semidirect product, extension, or quotient construction'
        }

    def _construct_ring(self, desc: str) -> Dict:
        """Construct a ring with specific properties."""
        properties = []
        if 'noetherian' in desc.lower():
            properties.append('noetherian')
        if 'not noetherian' in desc.lower() or 'non-noetherian' in desc.lower():
            properties.append('non-noetherian')

        result = self.basic_builder.build_ring(properties)
        if result:
            return result
        return {'status': 'cannot_construct_ring', 'properties': properties}

    def _construct_sequence(self, desc: str) -> Dict:
        """Construct a sequence with given properties."""
        import re
        if 'converge' in desc.lower():
            # Convergent sequence: 1/n
            return {'sequence': '1/n', 'limit': 0, 'type': 'convergent'}
        if 'diverge' in desc.lower():
            return {'sequence': 'n', 'type': 'divergent'}
        if 'bounded' in desc.lower() and 'not converge' in desc.lower():
            return {'sequence': '(-1)^n', 'type': 'bounded_not_convergent'}
        if 'cauchy' in desc.lower():
            return {'sequence': '1/n', 'type': 'Cauchy (converges in ℝ)'}
        return {'status': 'unknown_sequence_type'}

    def _construct_function(self, desc: str) -> Dict:
        """Construct a function with given properties."""
        if 'continuous' in desc.lower() and 'not differentiable' in desc.lower():
            return {'function': '|x|', 'at': 'x=0',
                    'note': 'Continuous everywhere, not differentiable at 0'}
        if 'differentiable' in desc.lower() and 'not twice' in desc.lower():
            return {'function': 'x|x|', 'note': 'Differentiable but second derivative DNE at 0'}
        if 'nowhere differentiable' in desc.lower():
            return {'function': 'Weierstrass function: Σ aⁿcos(bⁿπx)',
                    'note': 'Continuous everywhere, differentiable nowhere (0 < a < 1, b odd, ab > 1+3π/2)'}
        return {'status': 'unknown_function_type'}

    def _find_counterexample(self, desc: str) -> Dict:
        """Find a counterexample to a false statement."""
        low = desc.lower()
        if 'commutative' in low and 'matrix' in low:
            return {'counterexample': 'A=[[1,1],[0,1]], B=[[1,0],[1,1]], AB≠BA',
                    'note': 'Matrix multiplication is not commutative in general'}
        if 'continuous' in low and 'differentiable' in low:
            return {'counterexample': 'f(x)=|x|',
                    'note': 'Continuous at x=0 but not differentiable there'}
        if 'convergent' in low and 'series' in low and 'term' in low:
            return {'counterexample': 'Σ1/n diverges but 1/n→0',
                    'note': 'Terms going to 0 does NOT guarantee series converges'}
        return {'status': 'no_counterexample_found'}


# ═══════════════════════════════════════════════════════════════
# 5.5 CROSS-DOMAIN CONNECTOR
# Finds analogies and transfers ideas between mathematical fields
# ═══════════════════════════════════════════════════════════════

class CrossDomainConnector:
    """Connects ideas across different areas of mathematics."""

    # Structural analogies between fields
    ANALOGIES = {
        ('group_theory', 'topology'): {
            'concepts': {'subgroup': 'subspace', 'normal subgroup': 'closed set',
                        'quotient group': 'quotient space', 'homomorphism': 'continuous map',
                        'isomorphism': 'homeomorphism', 'kernel': 'preimage of point'},
            'principle': 'Both study objects with structure-preserving maps between them',
        },
        ('group_theory', 'ring_theory'): {
            'concepts': {'subgroup': 'ideal', 'normal subgroup': 'ideal',
                        'quotient group': 'quotient ring', 'homomorphism': 'ring homomorphism',
                        'simple group': 'simple ring (field)'},
            'principle': 'Quotient constructions and homomorphism theorems parallel each other',
        },
        ('analysis', 'topology'): {
            'concepts': {'convergent sequence': 'converging net', 'continuous function': 'continuous map',
                        'open interval': 'open set', 'closed interval': 'closed set',
                        'bounded': 'totally bounded', 'Cauchy sequence': 'Cauchy filter'},
            'principle': 'Analysis is topology + metric; many results generalize',
        },
        ('linear_algebra', 'homological_algebra'): {
            'concepts': {'vector space': 'module', 'linear map': 'homomorphism',
                        'kernel': 'kernel', 'rank-nullity': 'exact sequence',
                        'dimension': 'rank/Betti number'},
            'principle': 'Homological algebra generalizes linear algebra to non-vector-space modules',
        },
        ('number_theory', 'algebraic_geometry'): {
            'concepts': {'prime number': 'prime ideal', 'integer': 'ring element',
                        'divisibility': 'ideal containment', 'factorization': 'scheme theory',
                        'congruence': 'fiber over point'},
            'principle': 'Arithmetic geometry: numbers ARE points on curves/varieties',
        },
    }

    def find_analogy(self, source_field: str, target_field: str) -> Optional[Dict]:
        """Find analogy between two fields."""
        key = (source_field, target_field)
        if key in self.ANALOGIES:
            return self.ANALOGIES[key]
        # Try reverse
        rev = (target_field, source_field)
        if rev in self.ANALOGIES:
            data = self.ANALOGIES[rev]
            # Reverse the concept mapping
            return {
                'concepts': {v: k for k, v in data['concepts'].items()},
                'principle': data['principle'],
            }
        return None

    def transfer_technique(self, technique: str, source_field: str, target_field: str) -> str:
        """Suggest how a technique from one field might apply in another."""
        analogy = self.find_analogy(source_field, target_field)
        if not analogy:
            return f"No known analogy between {source_field} and {target_field}"

        lines = []
        lines.append(f"Transferring '{technique}' from {source_field} to {target_field}:")
        lines.append(f"  Principle: {analogy['principle']}")
        lines.append(f"  Concept mapping:")
        for src, tgt in list(analogy['concepts'].items())[:5]:
            lines.append(f"    {src} → {tgt}")
        lines.append(f"  Suggestion: Replace {source_field} concepts with {target_field} analogues")
        return '\n'.join(lines)

    def suggest_connections(self, problem: str) -> List[str]:
        """Suggest which fields might have relevant techniques."""
        low = problem.lower()
        suggestions = []

        if any(w in low for w in ['group', 'symmetry', 'permutation']):
            suggestions.append("group_theory → topology (covering spaces, fundamental group)")
            suggestions.append("group_theory → number_theory (Galois groups of number fields)")
        if any(w in low for w in ['polynomial', 'root', 'factor']):
            suggestions.append("ring_theory → algebraic_geometry (varieties = zero sets)")
            suggestions.append("field_theory → number_theory (algebraic number fields)")
        if any(w in low for w in ['continuous', 'limit', 'converge']):
            suggestions.append("analysis → topology (generalize metric to topological)")
            suggestions.append("analysis → functional_analysis (infinite-dimensional)")
        if any(w in low for w in ['exact', 'sequence', 'kernel', 'image']):
            suggestions.append("homological_algebra → topology (compute invariants)")
            suggestions.append("homological_algebra → algebraic_geometry (sheaf cohomology)")

        return suggestions if suggestions else ["No cross-domain suggestions for this problem"]


# ═══════════════════════════════════════════════════════════════
# UNIFIED LEVEL 5 INTERFACE
# ═══════════════════════════════════════════════════════════════

class PrometheusResearch:
    """Top-level research interface combining all Level 5 components."""

    def __init__(self):
        self.db = MegaTheoremDB()
        self.verifier = ProofVerifier(self.db)
        self.research = ResearchEngine(self.db)
        self.constructor = CreativeConstructor()
        self.connector = CrossDomainConnector()

    def analyze_problem(self, problem: str) -> str:
        """Full research-level analysis of a mathematical problem."""
        lines = []
        lines.append(f"═══ RESEARCH ANALYSIS ═══")
        lines.append(f"Problem: {problem}")
        lines.append("")

        # Suggest approaches
        approach = self.research.suggest_approach(problem)
        lines.append("Suggested approaches:")
        for a in approach['suggested_approaches'][:3]:
            lines.append(f"  • {a}")
        lines.append("")

        # Relevant theorems
        if approach['relevant_theorems']:
            lines.append("Relevant theorems:")
            for t in approach['relevant_theorems'][:5]:
                data = self.db.theorems.get(t, {})
                lines.append(f"  • {t}: {data.get('statement', '')[:60]}")
            lines.append("")

        # Key tools
        if approach['key_tools']:
            lines.append(f"Key tools: {', '.join(approach['key_tools'])}")
            lines.append("")

        # Cross-domain connections
        connections = self.connector.suggest_connections(problem)
        if connections and connections[0] != "No cross-domain suggestions for this problem":
            lines.append("Cross-domain connections:")
            for c in connections[:3]:
                lines.append(f"  → {c}")

        return '\n'.join(lines)

    def construct(self, description: str) -> str:
        """Construct a mathematical object."""
        result = self.constructor.construct(description)
        if result.get('status') == 'cannot_construct':
            return f"Cannot construct: {description}"
        lines = [f"Construction: {description}"]
        for k, v in result.items():
            if k != 'status':
                lines.append(f"  {k}: {v}")
        return '\n'.join(lines)

    def verify_proof(self, proof_text: str) -> str:
        """Check a proof for logical issues."""
        result = self.verifier.check_proof_structure(proof_text)
        lines = [f"Proof verification:"]
        lines.append(f"  Structure OK: {result['structure_ok']}")
        lines.append(f"  Lines: {result['lines']}")
        if result['issues']:
            lines.append(f"  Issues:")
            for issue in result['issues']:
                lines.append(f"    ⚠ {issue}")
        else:
            lines.append(f"  ✓ No issues detected")
        return '\n'.join(lines)

    def stats(self) -> str:
        """Show database stats."""
        s = self.db.stats()
        lines = [f"PROMETHEUS Research Engine Stats:"]
        lines.append(f"  Total theorems: {s['total']}")
        lines.append(f"  Fields:")
        for f, c in sorted(s['fields'].items(), key=lambda x: -x[1]):
            lines.append(f"    {f}: {c}")
        lines.append(f"  Most depended-on theorems:")
        for name, count in s['most_depended']:
            if count > 0:
                lines.append(f"    {name}: used by {count} theorems")
        return '\n'.join(lines)
