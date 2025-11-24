from typing import Dict, List, Tuple, Optional

Variable = str
Domain = List[int]
Assignment = Dict[Variable, int]
Constraint = Tuple[Variable, Variable]


def is_consistent(var: Variable, value: int, assignment: Assignment, constraints: List[Constraint]) -> bool:
    for (v1, v2) in constraints:
        if var == v1 and v2 in assignment and assignment[v2] == value:
            return False
        if var == v2 and v1 in assignment and assignment[v1] == value:
            return False
    return True


def select_unassigned_variable(variables: List[Variable], assignment: Assignment, domains: Dict[Variable, Domain]) -> Variable:
    unassigned = [v for v in variables if v not in assignment]
    return min(unassigned, key=lambda v: len(domains[v]))


def forward_check(domains: Dict[Variable, Domain], var: Variable, value: int, constraints: List[Constraint]) -> Dict[Variable, Domain]:
    new_domains = {v: list(domains[v]) for v in domains}
    for (v1, v2) in constraints:
        if v1 == var and value in new_domains[v2]:
            new_domains[v2].remove(value)
        elif v2 == var and value in new_domains[v1]:
            new_domains[v1].remove(value)
    return new_domains


def backtrack(variables: List[Variable], domains: Dict[Variable, Domain], constraints: List[Constraint], assignment: Assignment) -> Optional[Assignment]:
    if len(assignment) == len(variables):
        return assignment

    var = select_unassigned_variable(variables, assignment, domains)
    for value in domains[var]:
        if is_consistent(var, value, assignment, constraints):
            new_assignment = assignment.copy()
            new_assignment[var] = value
            new_domains = forward_check(domains, var, value, constraints)
            result = backtrack(variables, new_domains, constraints, new_assignment)
            if result:
                return result
    return None
