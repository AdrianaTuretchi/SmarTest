from typing import List

class StrategyEvaluator:
    """
    Evaluates user answers by checking for the presence of required keywords
    associated with the correct strategy.
    """

    def evaluate(self, user_answer: str, computed_solution: str) -> float:
        """
        Args:
            user_answer: The string provided by the user.
            computed_solution: The ideal solution string from StrategySolver.
            
        Returns:
            1.0 if keywords match, 0.0 otherwise.
        """
        if not user_answer:
            return 0.0
            
        user_text = user_answer.lower()
        
        # Ensure computed_solution is a string
        if isinstance(computed_solution, dict):
            computed_solution = computed_solution.get('problem_type', '')

        solution_key = computed_solution.lower()
        
        keywords: List[str] = []
        
        # Define synonym mapping based on the output of StrategySolver
        if "bfs" in solution_key:
            keywords = ["bfs", "breadth", "latime", "lățime"]
        elif "dfs" in solution_key or "recursivitate" in solution_key:
            keywords = ["dfs", "depth", "adancime", "adâncime", "recursiv", "divide"]
        elif "min-conflicts" in solution_key:
            keywords = ["min-conflicts", "min conflicts", "local search", "locala", "locală", "conflicte minime"]
        elif "backtracking" in solution_key:
            keywords = ["backtracking", "bkt"]
        elif "mrv" in solution_key:
            keywords = ["mrv", "fc", "forward checking", "forward-checking", "csp"]
        elif "warnsdorff" in solution_key:
            keywords = ["warnsdorff", "euristica", "greedy"]
            
        # Check if any keyword exists in the user's answer
        for kw in keywords:
            if kw in user_text:
                return 1.0
                
        return 0.0