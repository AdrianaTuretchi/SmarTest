from typing import Dict, Any, Tuple

class StrategySolver:
    """
    Determines the optimal algorithm/strategy based on the specific instance parameters.
    Returns a tuple: (Ideal Answer Text, Justification Key).
    """

    def solve(self, raw_data: Dict[str, Any]) -> Tuple[str, str]:
        problem_type = raw_data.get('problem_type')

        # --- 1. N-Queens Logic ---
        # Theory: Backtracking is complete but slow (good for N<=20). 
        # Min-Conflicts is local search, incomplete but fast (needed for N>20).
        if problem_type == 'n-queens':
            # Support both 'n_value' (from generator) and 'n' (from parser)
            n = int(raw_data.get('n_value') or raw_data.get('n', 8))
            if n <= 20:
                return "Backtracking (sau CSP standard)", "reason_nqueens_small"
            else:
                return "Min-Conflicts (Căutare Locală)", "reason_nqueens_large"

        # --- 2. Hanoi Logic ---
        # Theory: BFS is optimal for shortest path. DFS/Recursive is standard for 'any solution'.
        elif problem_type == 'hanoi':
            goal = raw_data.get('goal_type', 'any')
            if goal == 'optimal':
                return "BFS (Breadth First Search)", "reason_hanoi_bfs"
            else:
                return "DFS (sau Recursivitate / Divide et Impera)", "reason_hanoi_dfs"

        # --- 3. Graph Coloring Logic ---
        # Theory: Different strategies based on graph structure and size
        elif problem_type == 'graph-coloring':
            scenario_type = raw_data.get('scenario_type', 'standard')
            is_tree = raw_data.get('is_tree', False)
            num_nodes = raw_data.get('num_nodes', 20)
            
            # Tree structure -> Tree-CSP (linear time)
            if is_tree or scenario_type == 'tree':
                return "Tree-CSP (Arc Consistency + Sortare Topologică)", "reason_coloring_tree"
            
            # Giant graph -> Min-Conflicts (local search)
            elif scenario_type == 'giant' or num_nodes > 1000:
                return "Min-Conflicts (Căutare Locală)", "reason_coloring_giant"
            
            # Standard graph -> Backtracking + FC + MRV
            else:
                return "Backtracking (optimizat cu FC + MRV)", "reason_coloring_standard"

        # --- 4. Knight's Tour Logic ---
        # Theory: Warnsdorff's Rule (Heuristic) is for fast solutions. Backtracking is for completeness.
        elif problem_type in ['knights-tour', 'knight-tour']:
            goal = raw_data.get('goal_type', 'fast')
            if goal == 'fast':
                return "Regula lui Warnsdorff (Euristică Greedy)", "reason_knight_warnsdorff"
            else:
                return "Backtracking", "reason_knight_backtracking"

        return "Necunoscut", "default"