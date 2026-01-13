from typing import Any, Tuple, Dict, Optional
from pathlib import Path

from engine.evaluators import NashEvaluator, CSPEvaluator, MinMaxEvaluator, StrategyEvaluator
from core_logic.strategy_solver import StrategySolver
from engine.answer_generator import AnswerGenerator
from core_logic.nash_logic import find_pure_nash
from core_logic.csp_logic import backtrack, ac3
from core_logic.minmax_logic import dict_to_tree, minmax as minmax_compute


class EvaluationService:
    # Tag mappings for each question type
    TYPE_TAGS = {
        'nash': ['nash', 'game-theory'],
        'csp': ['csp', 'backtracking'],
        'minmax': ['minmax', 'alpha-beta'],
    }
    
    def __init__(self, knowledge_base_path: Optional[str] = None):
        """
        Initialize evaluation service with answer generator.
        
        Args:
            knowledge_base_path: Optional path to knowledge_base.json.
                                If None, uses default location.
        """
        if knowledge_base_path is None:
            # Default path relative to this file
            project_root = Path(__file__).resolve().parent.parent
            knowledge_base_path = str(project_root / "assets" / "json_output" / "knowledge_base.json")
        
        self.answer_generator = AnswerGenerator(knowledge_base_path)

    def evaluate(self, question_type: str, submission: Any):
        """
        Dispatch evaluation based on question_type.
        
        Args:
            question_type: Type of question ('nash', 'csp', 'minmax', 'strategy')
            submission: Submission object with user_answer and raw_data
            
        Returns:
            Tuple of (score, feedback_text) or (score, feedback_text, correct_answer) for strategy
        """
        if question_type == 'nash':
            return self._evaluate_nash(submission)
        
        if question_type == 'csp':
            return self._evaluate_csp(submission)
        
        if question_type == 'minmax':
            return self._evaluate_minmax(submission)
        
        if question_type == 'strategy':
            return self._evaluate_strategy(submission)
        
        raise ValueError(f"No evaluator for type '{question_type}'")
    
    def _evaluate_nash(self, submission: Any) -> Tuple[float, str]:
        """
        Evaluate Nash equilibrium submission.
        
        Returns:
            Tuple of (score, feedback_text)
        """
        # Calculate score
        evaluator = NashEvaluator()
        score = evaluator.evaluate(submission.user_answer, submission.raw_data)
        
        # Calculate ground truth for feedback
        correct_coords = find_pure_nash(submission.raw_data)
        
        # Generate feedback
        tags = self.TYPE_TAGS['nash']
        feedback = self.answer_generator.generate_full_answer('nash', correct_coords, tags)
        
        return score, feedback
    
    def _evaluate_csp(self, submission: Any) -> Tuple[float, str]:
        """
        Evaluate CSP submission.

        Returns:
            Tuple of (score, feedback_text)
        """
        # Calculate score
        evaluator = CSPEvaluator()
        score = evaluator.evaluate(submission.user_answer, submission.raw_data)

        # Calculate the correct solution (ground truth)
        try:
            variables = submission.raw_data['variables']
            domains = submission.raw_data['domains']
            constraints = submission.raw_data['constraints']
            partial_assignment = submission.raw_data.get('partial_assignment', {})
            tags = submission.raw_data.get('tags', [])

            if 'use_ac3' in tags:
                # Use AC-3 for arc consistency
                correct_solution = ac3(variables, domains, constraints)
            else:
                # Use Backtracking with optional MRV and Forward Checking
                use_mrv = 'use_mrv' in tags
                use_fc = 'use_forward_checking' in tags
                correct_solution = backtrack(variables, domains, constraints, partial_assignment, use_mrv, use_fc)
        except Exception:
            correct_solution = None

        # Generate feedback
        tags = self.TYPE_TAGS['csp'] + submission.raw_data.get('tags', [])

        # Add the template_id as a tag if it exists
        if hasattr(submission, 'template_id') and submission.template_id:
            tags.append(str(submission.template_id))

        feedback = self.answer_generator.generate_full_answer('csp', correct_solution, tags)

        return score, feedback
    
    def _evaluate_minmax(self, submission: Any) -> Tuple[float, str]:
        """
        Evaluate MinMax submission.
        
        Returns:
            Tuple of (score, feedback_text)
        """
        # Calculate score
        evaluator = MinMaxEvaluator()
        user_answer = {
            "root_value": submission.root_value,
            "visited_count": submission.visited_count,
        }
        score = evaluator.evaluate(user_answer, submission.raw_data)
        
        # Calculate ground truth for feedback
        try:
            tree = dict_to_tree(submission.raw_data)
            visited = []
            correct_root = minmax_compute(tree, 0, float('-inf'), float('inf'), True, visited)
            correct_result = {
                'root_value': correct_root,
                'visited_count': len(visited)
            }
        except Exception:
            correct_result = None
        
        # Generate feedback
        tags = self.TYPE_TAGS['minmax']
        feedback = self.answer_generator.generate_full_answer('minmax', correct_result, tags)
        
        return score, feedback
    
    def _evaluate_strategy(self, submission: Any) -> Tuple[float, str, str]:
        """
        Evaluate Strategy submission.

        Returns:
            Tuple of (score, feedback_text, correct_answer)
        """
        # Use StrategySolver to determine the correct solution
        from core_logic.strategy_solver import StrategySolver
        solver = StrategySolver()
        computed_solution, justification_key = solver.solve(submission.raw_data)

        # Calculate score
        evaluator = StrategyEvaluator()
        score = evaluator.evaluate(submission.user_answer, computed_solution)

        # Include template_id in tags
        tags = ['strategy'] + submission.raw_data.get('tags', [])
        if submission.template_id:
            tags.append(submission.template_id)

        # Generate feedback
        feedback = self.answer_generator.generate_full_answer('strategy', score, tags)

        return score, feedback, computed_solution

    def evaluate_submission(self, question_type: str, submission: Any) -> Tuple[float, str]:
        """
        Evaluate a submission based on its question type or template_id.

        Args:
            question_type: Type of question ('nash', 'csp', 'minmax', 'strategy')
            submission: Submission object with user_answer and raw_data

        Returns:
            Tuple of (score, feedback_text)
        """
        # Route based on template_id prefix
        if submission.template_id and submission.template_id.startswith('strat-'):
            return self._evaluate_strategy(submission)

        # Default routing based on question_type
        return self.evaluate(question_type, submission)
