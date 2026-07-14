"""
AXIMA Multilingual — Response Shaper
Mirrors the user's language style in the output.
If they type casual Romanized Telugu → respond the same way.
"""

import re
from typing import Dict


class ResponseShaper:
    """Shape English responses back into user's language style."""

    # Response templates per language (Romanized)
    TEMPLATES = {
        'te': {
            'answer_prefix': {
                'casual': "{topic} ante: ",
                'formal': "{topic} antey: ",
                'neutral': "{topic}: ",
            },
            'because': {
                'casual': "enduku ante, ",
                'formal': "kaaranam emitante, ",
                'neutral': "endukante, ",
            },
            'steps_intro': {
                'casual': "ila cheyyi: ",
                'formal': "ee vidhamga cheyyandi: ",
                'neutral': "steps: ",
            },
            'step_prefix': "Step {n}: ",
            'formula_intro': "Formula: ",
            'result': {
                'casual': "answer: {answer}",
                'formal': "samadhaanam: {answer}",
                'neutral': "result: {answer}",
            },
            'connectors': {
                'and': 'mariyu',
                'so': 'kabatti',
                'but': 'kani',
                'then': 'tarvata',
                'first': 'modatiga',
                'means': 'ante',
            },
        },
        'hi': {
            'answer_prefix': {
                'casual': "{topic} matlab: ",
                'formal': "{topic} ka matlab hai: ",
                'neutral': "{topic}: ",
            },
            'because': {
                'casual': "kyunki, ",
                'formal': "iska kaaran yeh hai ki, ",
                'neutral': "kyunki, ",
            },
            'steps_intro': {
                'casual': "aise karo: ",
                'formal': "is tarah karein: ",
                'neutral': "steps: ",
            },
            'step_prefix': "Step {n}: ",
            'formula_intro': "Formula: ",
            'result': {
                'casual': "answer: {answer}",
                'formal': "uttar: {answer}",
                'neutral': "result: {answer}",
            },
            'connectors': {
                'and': 'aur',
                'so': 'isliye',
                'but': 'lekin',
                'then': 'phir',
                'first': 'pehle',
                'means': 'matlab',
            },
        },
        'ta': {
            'answer_prefix': {
                'casual': "{topic} na: ",
                'formal': "{topic} endral: ",
                'neutral': "{topic}: ",
            },
            'because': {
                'casual': "en na, ",
                'formal': "karanam ennvendral, ",
                'neutral': "endraal, ",
            },
            'steps_intro': {
                'casual': "ipdi pannu: ",
                'formal': "ivvaru seyyungal: ",
                'neutral': "steps: ",
            },
            'step_prefix': "Step {n}: ",
            'formula_intro': "Formula: ",
            'result': {
                'casual': "answer: {answer}",
                'formal': "vidai: {answer}",
                'neutral': "result: {answer}",
            },
            'connectors': {
                'and': 'matrum',
                'so': 'athanaal',
                'but': 'aanaal',
                'then': 'piragu',
                'first': 'mudhalil',
                'means': 'enbathu',
            },
        },
    }

    def shape(self, english_answer: str, language: str, style: str,
              intent: str, topic: str) -> str:
        """Shape English answer into user's language style.
        
        KEY RULE: Keep technical/English content words as-is.
        Only add native language GRAMMAR GLUE around them.
        """
        if language == "en" or language not in self.TEMPLATES:
            return english_answer

        templates = self.TEMPLATES[language]
        style = style if style in ('casual', 'formal') else 'neutral'

        # For simple answers (numbers, formulas)
        if re.match(r'^[\d\.\+\-\*/=\s]+$', english_answer.strip()):
            return templates['result'][style].format(answer=english_answer.strip())

        # For formula answers
        if '=' in english_answer and any(c.isalpha() for c in english_answer):
            return templates['formula_intro'] + english_answer

        # For step-by-step answers
        if '\n' in english_answer and re.search(r'^\d+\.', english_answer):
            intro = templates['steps_intro'][style]
            return intro + "\n" + english_answer

        # For explanation answers — add prefix in native style
        prefix = templates['answer_prefix'][style].format(topic=topic)

        # Inject native connectors into the English answer
        shaped = self._inject_connectors(english_answer, templates['connectors'])

        return prefix + shaped

    def _inject_connectors(self, text: str, connectors: Dict) -> str:
        """Replace English connectors with native ones (light touch)."""
        # Only replace at sentence boundaries, not inside technical terms
        result = text
        # Replace leading connectors only
        result = re.sub(r'^So,?\s+', connectors.get('so', 'So') + ', ', result)
        result = re.sub(r'^But\s+', connectors.get('but', 'But') + ' ', result)
        result = re.sub(r'^First,?\s+', connectors.get('first', 'First') + ', ', result)
        result = re.sub(r'^Then,?\s+', connectors.get('then', 'Then') + ', ', result)
        return result
