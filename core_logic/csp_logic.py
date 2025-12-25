from typing import Dict, List, Tuple, Optional, Set
from collections import deque

Variable = str
Domain = List[int]
Assignment = Dict[Variable, int]
Constraint = Tuple[Variable, Variable]


def is_consistent(var: Variable, value: int, assignment: Assignment, constraints: List[Constraint]) -> bool:
    """
    Consistency Check
    
    Verifies whether assigning a specific value to a variable is consistent with
    the current partial assignment and the CSP constraints.
    
    Args:
        var: The variable to check
        value: The value to potentially assign to var
        assignment: Current partial assignment of variables to values
        constraints: List of binary constraints (v1, v2) representing v1 != v2
    
    Returns:
        True if the assignment is consistent with all constraints, False otherwise
    """
    for (v1, v2) in constraints:
        if var == v1 and v2 in assignment and assignment[v2] == value:
            return False
        if var == v2 and v1 in assignment and assignment[v1] == value:
            return False
    return True


def select_unassigned_variable(variables: List[Variable], assignment: Assignment, domains: Dict[Variable, Domain], use_mrv: bool = True) -> Variable:
    """
    Variable Selection for CSP
    
    Selects the next unassigned variable using either:
    - MRV (Minimum Remaining Values) heuristic: Chooses the variable with the smallest
      domain (most constrained variable, fail-first strategy)
    - Static Ordering: Returns the first unassigned variable from the list
    
    The MRV heuristic (also known as "most constrained variable" or "fail-first")
    reduces the branching factor and leads to earlier detection of failures.
    Static ordering is simpler but less efficient.
    
    Args:
        variables: List of all variables in the CSP
        assignment: Current partial assignment
        domains: Current domains for all variables
        use_mrv: If True, use MRV heuristic; if False, use static ordering
    
    Returns:
        The selected unassigned variable
    """
    unassigned = [v for v in variables if v not in assignment]
    
    if use_mrv:
        # MRV Heuristic: Select variable with minimum remaining values
        return min(unassigned, key=lambda v: len(domains[v]))
    else:
        # Static Ordering: Return first unassigned variable
        return unassigned[0]


def forward_check(domains: Dict[Variable, Domain], var: Variable, value: int, constraints: List[Constraint]) -> Dict[Variable, Domain]:
    """
    Forward Checking
    
    Propagates the effect of a variable assignment by removing the assigned value
    from the domains of all neighboring (constrained) variables. This is a form of
    constraint propagation that detects some inconsistencies early.
    
    Forward checking is less powerful than arc consistency (AC-3) but faster to compute.
    
    Args:
        domains: Current domains for all variables
        var: The variable that was just assigned
        value: The value assigned to var
        constraints: List of binary constraints (v1, v2) representing v1 != v2
    
    Returns:
        New domains dictionary with updated domains for neighbors of var
    """
    new_domains = {v: list(domains[v]) for v in domains}
    for (v1, v2) in constraints:
        if v1 == var and value in new_domains[v2]:
            new_domains[v2].remove(value)
        elif v2 == var and value in new_domains[v1]:
            new_domains[v1].remove(value)
    return new_domains


def backtrack(variables: List[Variable], domains: Dict[Variable, Domain], constraints: List[Constraint], assignment: Assignment, use_mrv: bool = True, use_fc: bool = True) -> Optional[Assignment]:
    """
    Backtracking Search for CSP (Configurable)
    
    Core CSP solving algorithm that recursively assigns values to variables while
    maintaining consistency. Supports multiple configurations:
    
    - Standard Backtracking (use_mrv=False, use_fc=False):
      Basic depth-first search with static variable ordering and no constraint propagation.
    
    - Backtracking + MRV (use_mrv=True, use_fc=False):
      Uses Minimum Remaining Values heuristic for smarter variable selection.
    
    - Backtracking + Forward Checking (use_mrv=False, use_fc=True):
      Propagates constraints after each assignment to prune domains early.
    
    - Backtracking + MRV + Forward Checking (use_mrv=True, use_fc=True) [DEFAULT]:
      Combines both optimizations for maximum efficiency.
    
    Algorithm steps:
    1. If all variables are assigned, return the complete assignment (solution found)
    2. Select the next unassigned variable (using MRV or static ordering)
    3. Try each value in the variable's domain
    4. If the value is consistent with current assignment:
       a. Create new assignment with this value
       b. Optionally apply forward checking to propagate constraints
       c. Recursively solve the reduced problem
    5. If no solution found with any value, backtrack (return None)
    
    Args:
        variables: List of all variables in the CSP
        domains: Current domains for all variables
        constraints: List of binary constraints (v1, v2) representing v1 != v2
        assignment: Current partial assignment
        use_mrv: If True, use MRV heuristic for variable selection; if False, use static ordering
        use_fc: If True, apply forward checking; if False, use standard backtracking
    
    Returns:
        Complete assignment if solution exists, None if no solution found
    """
    # Base case: All variables assigned
    if len(assignment) == len(variables):
        return assignment

    # Select next variable to assign
    var = select_unassigned_variable(variables, assignment, domains, use_mrv)
    
    # Try each value in the variable's domain
    for value in domains[var]:
        if is_consistent(var, value, assignment, constraints):
            # Create new assignment
            new_assignment = assignment.copy()
            new_assignment[var] = value
            
            # Apply constraint propagation if forward checking is enabled
            if use_fc:
                new_domains = forward_check(domains, var, value, constraints)
            else:
                # Standard backtracking: use current domains without propagation
                new_domains = domains
            
            # Recursive call
            result = backtrack(variables, new_domains, constraints, new_assignment, use_mrv, use_fc)
            if result:
                return result
    
    # No solution found with this partial assignment
    return None


def ac3(variables: List[Variable], domains: Dict[Variable, Domain], constraints: List[Constraint]) -> Optional[Dict[Variable, Domain]]:
    """
    AC-3 (Arc Consistency Algorithm #3)
    
    Enforces arc consistency on the CSP by iteratively removing values from domains
    that cannot satisfy the constraints with any value in connected variable domains.
    
    Args:
        variables: List of variable names
        domains: Dictionary mapping variables to their domains (list of possible values)
        constraints: List of binary constraints as tuples (v1, v2) representing v1 != v2
    
    Returns:
        Updated domains dictionary with reduced domains, or None if inconsistency detected
    """
    # Create a working copy of domains
    reduced_domains = {v: list(domains[v]) for v in domains}
    
    # Initialize queue with all arcs (bidirectional)
    queue: deque[Tuple[Variable, Variable]] = deque()
    for (v1, v2) in constraints:
        queue.append((v1, v2))
        queue.append((v2, v1))
    
    def revise(xi: Variable, xj: Variable) -> bool:
        """
        Remove values from domains[xi] that don't satisfy the constraint xi != xj
        with any value in domains[xj].
        
        Returns True if the domain of xi was modified.
        """
        revised = False
        values_to_remove = []
        
        for value_xi in reduced_domains[xi]:
            # Check if there exists any value in xj's domain that satisfies the constraint
            satisfies_constraint = False
            for value_xj in reduced_domains[xj]:
                if value_xi != value_xj:  # Constraint: xi != xj
                    satisfies_constraint = True
                    break
            
            # If no value in xj's domain satisfies the constraint, mark for removal
            if not satisfies_constraint:
                values_to_remove.append(value_xi)
                revised = True
        
        # Remove the values that don't satisfy the constraint
        for value in values_to_remove:
            reduced_domains[xi].remove(value)
        
        return revised
    
    # Build neighbor map for efficient lookup
    neighbors: Dict[Variable, Set[Variable]] = {v: set() for v in variables}
    for (v1, v2) in constraints:
        neighbors[v1].add(v2)
        neighbors[v2].add(v1)
    
    # Process arcs
    while queue:
        xi, xj = queue.popleft()
        
        if revise(xi, xj):
            # Check for inconsistency
            if len(reduced_domains[xi]) == 0:
                return None  # Domain wipeout - no solution possible
            
            # Add all incoming neighbors of xi (except xj) back to the queue
            for xk in neighbors[xi]:
                if xk != xj:
                    queue.append((xk, xi))
    
    return reduced_domains
