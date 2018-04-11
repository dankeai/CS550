from csp_lib.backtrack_util import (first_unassigned_variable,
                                    unordered_domain_values,
                                    no_inference)
from csp_lib.csp import CSP


def backtracking_search(csp: CSP,
                        select_unassigned_variable=first_unassigned_variable,
                        order_domain_values=unordered_domain_values,
                        inference=no_inference):
    """backtracking_search
    Given a constraint satisfaction problem (CSP),
    a function handle for selecting variables, 
    a function handle for selecting elements of a domain,
    and a set of inferences, solve the CSP using backtrack search
    """

    # See Figure 6.5] of your book for details

    def backtrack(assignment: dict):
        """Attempt to backtrack search with current assignment
        Returns None if there is no solution.  Otherwise, the
        csp should be in a goal state.
        """
        try:
            var = select_unassigned_variable(assignment, csp)
        except ValueError:
            print("Caught")
            return assignment
        for value in order_domain_values(var, assignment, csp):
            # Is consistent
            if csp.nconflicts(var, value, assignment) is 0:
                csp.assign(var, value, assignment)
                # Propagate new constraints?
                inferences = inference(csp, var, value, assignment, None)
                if inferences is not None or inferences:
                    assignment[var] = value
                    removals = csp.suppose(var, value)

                    r = backtrack(assignment)
                    if r is not None or r:
                        return r
                    csp.unassign(var, assignment)
                    csp.restore(removals)

        return None

    # Call with empty assignments, variables acces sed
    # through dynamic scoping (variables in outer
    # scope can be accessed in Python)
    result = backtrack({})

    assert result is None or csp.goal_test(result)
    return result
