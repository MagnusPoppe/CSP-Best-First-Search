from CSP._old.datastructure import Constraint
from CSP._old.datastructure import Domain
from CSP._old.datastructure import Variable

ROW = 0
COL = 1


def revise(variable: Variable) -> bool:
    # Initial number of domains is saved for later comparison.
    initial_number_of_domains = len(variable.domain)

    # Looping through the entire domain of the variable
    # and running all constraints.
    for domain in variable.domain:  # type: Domain
        positive = 0
        for constraint in domain.constraints: # type: Constraint
            # This constraint is upheld.
            if constraint.run(): positive += 1

        # If no valid constrait, the domain value is trash
        if positive == 0:
            # No legal move found for this domain value:
            variable.delete(domain)

    return initial_number_of_domains > len(variable.domain)

def GAC_loop(queue):
    seen = {ROW:[], COL:[]}

    while queue:
        todo = queue.pop(0)
        seen[todo.type].append(todo)
        if revise(todo):
            if len(seen[todo.type]) > 0:
                queue += seen[todo.type]
                seen[todo.type] = []
            # Domain has changed, do something with children..
        elif len(todo.domain) > 0:
            seen[todo.type].append(todo)

        # NO ADDING IF THERE IS NO CHANGES.
        # else:
        #     queue.append(todo)
    return False
