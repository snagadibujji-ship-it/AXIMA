"""
ACES v2 — Phase 2: Input Shield
Normalizes messy input into clean, structured form.
Handles: typos, missing spaces, mixed symbols, noisy punctuation, formulas.
"""

import re
from typing import List, Tuple
from .models import NormalizedInput


class InputShield:
    """Normalize and clean user input before processing."""

    # Common typo patterns (structure-based, not word-list)
    TYPO_PATTERNS = [
        # Double letters that should be single
        (r'([a-z])\1{2,}', r'\1\1'),  # "helllo" → "hello"
        # Missing space after punctuation
        (r'([.!?])([A-Z])', r'\1 \2'),
        # Multiple spaces
        (r'\s{2,}', ' '),
        # Multiple punctuation
        (r'([!?.]){2,}', r'\1'),
    ]

    # Domain detection patterns (grammar-based, not topic-word-based)
    DOMAIN_PATTERNS = {
        'math': [
            r'\b(?:solve|calculate|compute|evaluate|simplify|integrate|differentiate|factor)\b',
            r'[=+\-*/^√∫∑∏]',
            r'\b(?:equation|formula|theorem|proof|derivative|integral)\b',
            r'\d+\s*[+\-*/^]\s*\d+',
        ],
        'physics': [
            r'\b(?:force|energy|velocity|acceleration|momentum|gravity|quantum|wave)\b',
            r'\b(?:Newton|Einstein|Planck|Bohr|Heisenberg)\b',
            r'\b(?:m/s|kg|joule|watt|volt|amp|Hz|N)\b',
        ],
        'biology': [
            r'\b(?:cell|DNA|gene|protein|organism|evolution|species|enzyme)\b',
            r'\b(?:mitochondria|chloroplast|nucleus|membrane|photosynthesis)\b',
        ],
        'chemistry': [
            r'\b(?:atom|molecule|reaction|bond|element|compound|acid|base)\b',
            r'\b(?:oxidation|reduction|electron|proton|neutron|ion)\b',
        ],
        'cs': [
            r'\b(?:algorithm|function|variable|loop|array|class|object|recursion)\b',
            r'\b(?:complexity|O\(n\)|stack|queue|tree|graph|sort|search)\b',
        ],
    }

    def process(self, raw: str) -> NormalizedInput:
        """Full input normalization pipeline."""
        # Step 1: Basic cleanup
        clean = self._basic_clean(raw)

        # Step 2: Fix common typo patterns
        clean = self._fix_typos(clean)

        # Step 3: Normalize symbols
        clean = self._normalize_symbols(clean)

        # Step 4: Detect domain
        domain = self._detect_domain(clean)

        # Step 5: Check for formulas/code
        has_formula = self._has_formula(clean)
        has_code = self._has_code(clean)

        # Step 6: Tokenize
        tokens = self._tokenize(clean)

        return NormalizedInput(
            raw=raw,
            clean=clean,
            tokens=tokens,
            domain_hint=domain,
            language="en",  # TODO: language detection in future
            has_formula=has_formula,
            has_code=has_code,
            confidence=1.0
        )

    def _basic_clean(self, text: str) -> str:
        """Remove noise, normalize whitespace."""
        # Strip leading/trailing whitespace
        text = text.strip()
        # Normalize unicode quotes
        text = text.replace('\u201c', '"').replace('\u201d', '"')
        text = text.replace('\u2018', "'").replace('\u2019', "'")
        # Normalize dashes
        text = text.replace('\u2014', '—').replace('\u2013', '-')
        # Remove zero-width characters
        text = re.sub(r'[\u200b\u200c\u200d\ufeff]', '', text)
        # Collapse whitespace
        text = re.sub(r'\s+', ' ', text)
        return text

    def _fix_typos(self, text: str) -> str:
        """Fix structural typo patterns (not word-level spell check)."""
        for pattern, replacement in self.TYPO_PATTERNS:
            text = re.sub(pattern, replacement, text)
        return text

    def _normalize_symbols(self, text: str) -> str:
        """Normalize math/physics symbols to standard forms."""
        # Common symbol alternatives → standard
        replacements = {
            '×': '*', '÷': '/', '≠': '!=', '≤': '<=', '≥': '>=',
            '→': '->', '←': '<-', '↔': '<->',
            '²': '^2', '³': '^3', '½': '1/2', '¼': '1/4',
            'π': 'pi', 'θ': 'theta', 'λ': 'lambda',
            '∞': 'infinity', '√': 'sqrt',
        }
        for old, new in replacements.items():
            text = text.replace(old, new)
        return text

    def _detect_domain(self, text: str) -> str:
        """Detect knowledge domain from sentence structure and keywords."""
        scores = {}
        text_lower = text.lower()
        for domain, patterns in self.DOMAIN_PATTERNS.items():
            score = 0
            for pattern in patterns:
                matches = re.findall(pattern, text_lower, re.IGNORECASE)
                score += len(matches)
            if score > 0:
                scores[domain] = score

        if scores:
            return max(scores, key=scores.get)
        return "general"

    def _has_formula(self, text: str) -> bool:
        """Check if input contains mathematical expressions."""
        # Look for equation-like patterns
        if re.search(r'[a-zA-Z]\s*=\s*[a-zA-Z0-9+\-*/^(]', text):
            return True
        if re.search(r'\b(?:sin|cos|tan|log|ln|sqrt|integral|sum)\s*\(', text):
            return True
        if re.search(r'\d+\s*[+\-*/^]\s*\d+', text):
            return True
        return False

    def _has_code(self, text: str) -> bool:
        """Check if input contains code."""
        if re.search(r'(?:def |class |import |for .+ in |if .+:|print\()', text):
            return True
        if re.search(r'[{}\[\];].*[{}\[\];]', text):
            return True
        return False

    def _tokenize(self, text: str) -> List[str]:
        """Split into meaningful tokens."""
        # Split on whitespace but keep punctuation attached to words
        tokens = re.findall(r"[\w']+|[^\w\s]", text)
        return tokens
