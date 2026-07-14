"""
ACES v2 — Phase 3: Intent & Mode Router
Detects question type, requested format, depth level, and domain.
Returns a structured routing decision.
"""

import re
from .models import NormalizedInput, RouterDecision


class Router:
    """Route questions to the correct explanation strategy."""

    def route(self, inp: NormalizedInput, requested_mode: str = "deep") -> RouterDecision:
        """Analyze input and decide explanation strategy."""
        text = inp.clean.lower()

        question_type = self._detect_question_type(text)
        format_mode = self._detect_format(text, requested_mode)
        depth = self._detect_depth(text)
        domain = inp.domain_hint or self._infer_domain(text)
        needs_solver = self._needs_solver(text, domain)
        needs_search = self._needs_search(text, question_type)

        confidence = 0.9 if question_type != "fact" else 0.7

        return RouterDecision(
            question_type=question_type,
            format_mode=format_mode,
            depth=depth,
            domain=domain,
            confidence=confidence,
            needs_solver=needs_solver,
            needs_search=needs_search,
        )

    def _detect_question_type(self, text: str) -> str:
        """Detect the TYPE of question being asked."""
        # Why questions → causal explanation
        if re.search(r'\bwhy\b', text):
            return "why"

        # How questions → process/mechanism
        if re.search(r'\bhow\b(?!\s+(?:many|much))', text):
            return "how"

        # Compare/contrast
        if re.search(r'\b(?:compare|difference|vs|versus|between|better)\b', text):
            return "compare"

        # Calculation request
        if re.search(r'\b(?:calculate|compute|solve|evaluate|find the value)\b', text):
            return "calculation"

        # Derivation request
        if re.search(r'\b(?:derive|derivation|prove|proof|show that)\b', text):
            return "derivation"

        # Process/procedure
        if re.search(r'\b(?:steps|procedure|process|method|how to)\b', text):
            return "process"

        # Teaching request
        if re.search(r'\b(?:teach|explain from|start from basics|help me understand)\b', text):
            return "teach"

        # Default: factual
        return "fact"

    def _detect_format(self, text: str, requested: str) -> str:
        """Detect or use the requested explanation format."""
        # Explicit format requests override
        if requested != "deep":
            return requested

        # Detect from text
        if re.search(r'\b(?:brief|short|quick|one line|tldr|summary)\b', text):
            return "one-line"
        if re.search(r'\b(?:list|bullet|points|enumerate)\b', text):
            return "bullets"
        if re.search(r'\b(?:step by step|steps|procedure|how to)\b', text):
            return "steps"
        if re.search(r'\b(?:detailed|in depth|thorough|comprehensive|full)\b', text):
            return "deep"
        if re.search(r'\b(?:expert|advanced|technical|formal)\b', text):
            return "expert"
        if re.search(r'\b(?:simple|easy|basic|eli5|for a child|beginner)\b', text):
            return "simple"
        if re.search(r'\b(?:teach|tutorial|lesson|from scratch)\b', text):
            return "teach"
        if re.search(r'\b(?:exam|test|quiz|prepare)\b', text):
            return "exam"

        return "deep"  # Default

    def _detect_depth(self, text: str) -> int:
        """Detect how deep the explanation should go. 1-4."""
        if re.search(r'\b(?:brief|quick|short|just tell me)\b', text):
            return 1
        if re.search(r'\b(?:detailed|thorough|comprehensive|everything)\b', text):
            return 4
        if re.search(r'\b(?:explain|understand|why|how)\b', text):
            return 3
        return 2  # Standard

    def _infer_domain(self, text: str) -> str:
        """Infer domain if not already detected by shield."""
        # Already done by shield in most cases
        return "general"

    def _needs_solver(self, text: str, domain: str) -> bool:
        """Does this need the math/physics solver?"""
        if domain in ('math', 'physics'):
            if re.search(r'\b(?:calculate|solve|compute|find|evaluate|derive)\b', text):
                return True
            if re.search(r'[=+\-*/^]', text) and any(c.isdigit() for c in text):
                return True
        return False

    def _needs_search(self, text: str, q_type: str) -> bool:
        """Does this need external knowledge search?"""
        # "Why" and "how" about general topics may need deeper context
        if q_type in ("why", "how", "teach") and not re.search(r'\b(?:math|physics|formula)\b', text):
            return True
        return False
