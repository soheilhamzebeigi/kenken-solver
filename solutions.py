from utils import first
from csp import *
import sys

# Variable ordering

def first_unassigned_variable(assignment, csp):
    """The default variable order."""
    return first([var for var in csp.variables if var not in assignment])


def mrv(assignment, csp):
    """
    Q5-1
    Minimum-remaining-values heuristic.
	returns minimun remaining value for variables
    """
    # pass
    return argmin_random_tie(
        [i for i in csp.variables if i not in assignment],
        key=lambda variable: number_Of_Remain_values(csp, variable, assignment))


def number_Of_Remain_values(csp, var, assignment):
        return count(csp.nconflicts(var, val, assignment) == 0
                     for val in csp.domains[var])


def unordered_domain_values(var, assignment, csp):
    """The default value order."""
    return csp.choices(var)


def lcv(var, assignment, csp):
    """
    Q5-2
    Least-constraining-values heuristic.
	returns list of variables
    """
    # pass

    return sorted(csp.choices(var),
                  key=lambda value: csp.nconflicts(var, value, assignment))
# Filtering

def no_inference(csp, var, value, assignment, removals):
    return True


def forward_checking(csp, var, value, assignment, removals):
    """
    Q5-3
    Prune neighbor values inconsistent with var=value.
    """
    # pass
    for i in csp.neighbors[var]:
        if i not in assignment:
            for j in csp.curr_domains[i][:]:
                if not csp.constraints(var, value, i, j):
                    csp.prune(i, j, removals)
            if not csp.curr_domains[i]:
                return False
    return True


def arc_cons(csp, var, value, assignment, removals):
    """
    Q5-4
    Maintain arc consistency.
    """
    # pass
    return ARC(csp, [(i, var) for i in csp.neighbors[var]], removals)

def ARC(csp, queue=None, removals=None):
    if queue is None:
        queue = [(Xi, Xk) for Xi in csp.variables for Xk in csp.neighbors[Xi]]
    csp.support_pruning()
    while queue:
        (xi, xj) = queue.pop()
        if revise(csp, xi, xj, removals):
            if not csp.curr_domains[xi]:
                return False
            for xk in csp.neighbors[xi]:
                if xk != xi:
                    queue.append((xk, xi))
    return True

def revise(csp, xi, xj, removals):
    revised = False
    for x in csp.curr_domains[xi][:]:
        if all(not csp.constraints(xi, x, xj, y) for y in csp.curr_domains[xj]):
            csp.prune(xi, x, removals)
            revised = True
    return reversed


def backtracking_search(csp,
                        select_unassigned_variable=first_unassigned_variable,
                        order_domain_values=unordered_domain_values,
                        inference=forward_checking):

    def backtrack(assignment):
        if len(assignment) == len(csp.variables):
            return assignment
        var = select_unassigned_variable(assignment, csp)
        for value in order_domain_values(var, assignment, csp):
            if 0 == csp.nconflicts(var, value, assignment):
                csp.assign(var, value, assignment)
                removals = csp.suppose(var, value)
                if inference(csp, var, value, assignment, removals):
                    result = backtrack(assignment)
                    if result is not None:
                        return result
                csp.restore(removals)
        csp.unassign(var, assignment)

        return None

    result = backtrack({})

    print(f"Total size of the program is {sys.getsizeof(result)}")

    assert result is None or csp.goal_test(result)
    return result
