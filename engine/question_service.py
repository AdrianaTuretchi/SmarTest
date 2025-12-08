import json
from pathlib import Path
from typing import Dict, Any

from engine.generators.nash_generator import NashGenerator
from engine.generators.csp_generator import CSPGenerator
from engine.generators.minmax_generator import MinMaxGenerator


class QuestionService:
    def __init__(self, templates_path: str):
        self.templates_path = templates_path
        self.templates = {}
        tp = Path(templates_path)
        try:
            with open(tp, 'r', encoding='utf-8') as f:
                all_templates = json.load(f)
            # map id -> template dict (kept for NashGenerator compatibility)
            self.templates = {t['id']: t for t in all_templates if t.get('tags')}
        except Exception:
            # keep templates empty; generators will handle missing templates
            self.templates = {}

    def generate_question_by_type(self, q_type: str = 'nash') -> Dict[str, Any]:
        if q_type == 'nash':
            gen = NashGenerator(self.templates)
            return gen.generate()

        if q_type == 'csp':
            gen = CSPGenerator(self.templates_path)
            return gen.generate()

        if q_type == 'minmax':
            gen = MinMaxGenerator(self.templates_path)
            return gen.generate()

        return {"error": f"Generator for type '{q_type}' not implemented."}
