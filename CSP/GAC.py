import os


from CSP.state import State, Variable
from file_tostring import read_file_to_string


def GAC( state : State ) -> State :


    def initialize(state: State) -> list:
        queue = []

        for x, row in enumerate(state.rows):
            for constraint in state.constraints:
                if x == constraint.x:
                    queue += [(row, constraint, state.cols[constraint.y])]

        for y, col in enumerate(state.cols):
            for constraint in state.constraints:
                if y == constraint.y:
                    queue += [(col, constraint, state.rows[constraint.x])]

        return queue

    def satisfy_constraint(var:str, type:int, constraint:callable, other:Variable) -> bool:
        # Searching through all other variables:
        for other_var in other.domain:
            # If a single constraint is true, return True. No delete.
            if constraint.func(type, var, other_var):
                return True

        return False

    def revise(focal: Variable, constraint, other) -> bool:

        revised = False
        for var in focal.domain:
            if not satisfy_constraint(var, focal.type, constraint, other):
                focal.domain.remove(var)
                revised=True
                # break # Kanskje denne ikke trengs?

        return revised

    def domain_filter(queue: list):
        def create_neighbours(focal):
            neightbours = []
            # if focal.type == state.TYPE_ROW:
            #     for y, col in enumerate(state.cols):
            #         for constraint in state.constraints:
            #             if y == constraint.y and focal.index == constraint.x:
            #                 neightbours += [(col, constraint, focal)]
            # if focal.type == state.TYPE_COL:
            #     for x, row in enumerate(state.rows):
            #         for constraint in state.constraints:
            #             if focal.index == constraint.y and x == constraint.x:
            #                 neightbours += [(row, constraint, focal)]
                # return neightbours

            if focal.type == state.TYPE_COL:
                for x, row in enumerate(state.rows):
                    for constraint in state.constraints:
                        if x == constraint.x:
                            neightbours += [(row, constraint, state.cols[constraint.y])]

            if focal.type == state.TYPE_ROW:
                for y, col in enumerate(state.cols):
                    for constraint in state.constraints:
                        if y == constraint.y:
                            neightbours += [(col, constraint, state.rows[constraint.x])]
            return  neightbours


        while queue:
            focal, constraint, other = queue.pop(0)
            if revise(focal, constraint, other):
                if not focal.domain: return False
                queue += create_neighbours(focal)


    queue = initialize(state)

    domain_filter(queue)
    # if sum( [len(v.domain)-1 for v in state.rows + state.cols] ) != 0:
    #     domain_filter(queue)

    return state


if __name__ == '__main__':
    _initial_state = State(read_file_to_string(os.path.join("/Users/MagnusPoppe/Google Drive/Utvikling/appsPython/AI_project_1/nonogram/boards",
                                                            "nono-reindeer.txt")))

    result = GAC(_initial_state)
    if sum( [len(v.domain)-1 for v in result.rows + result.cols] ) == 0:
        print("SOLVED!")