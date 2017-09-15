from CSP.datastructure import Variable, Domain

class Puzzle():

    def __init__(self, spec):
        lines = spec.split("\n")

        self.spec = spec
        first_line = lines[0].split(" ")
        self.w = w = int(first_line[0])
        self.h = h = int(first_line[1])
        self.grid = [[0] * h for i in range(w)]
        self.rows = [Entry(lines[i].split(), w) for i in range(h, 0, -1)]
        self.columns = [Entry(lines[i].split(), h) for i in range(h + 1, h + w + 1)]

        for i in range(len(self.rows)):
            self.rows[i] = self.rows[i].datastructure
        for i in range(len(self.columns)):
            self.columns[i] = self.columns[i].datastructure



class Entry():

    def __init__(self, specs: list, rowlen):
        self.variables = [int(element) for element in specs]
        self.length = rowlen

        # Creating CSP variables.
        self.domains = self.generate_domains(rowlen)

        self.datastructure = []

        for i, var in enumerate(self.variables):
            variable = self.generate_variable(var, self.domains[i])
            self.datastructure.append(variable)
        self.possibles = self.get_all_possibilities(self.domains, aggregate=True)

    def generate_variable(self, var, domain_values):
        v = Variable(var)
        for d in domain_values:
            _d = Domain(v, d, [], None)
            v.map_domain[d] = _d
            v.domain.append(_d)
        return v


    def __getitem__(self, item) -> tuple:
        return self.variables[item], self.domains[item]

    def get_all_possibilities(self, domain, aggregate = True):

        def permutations_by_row(grid, i, values, results):
            if i == len(grid):
                if aggregate:
                    output = [0] * self.length
                    append = True
                    for j, val in enumerate(values):
                        for k in range(val, val + self.variables[j]):
                            # Skipping illegal values.
                            if append and k == val and val > 0 and output[val-1] == 1:
                                append = False
                            output[k] = 1
                    if append:
                        results.append(output)
                        for j, val in enumerate(values):
                            self.datastructure[j].map_domain[val].possibles.append(output)
                else:
                    results.append(values) # If only positions of values.
                return
            for val in grid[i]:
                permutations_by_row(grid, i + 1, values + [val], results)
            return results

        return permutations_by_row(domain, 0, [], [])

    def generate_domains(self, rowlen):
        domains = []
        for i, variable in enumerate(self.variables):
            max_behind = 0 if i == 0 else sum(self.variables[:i-1]) +i +1
            max_infront = rowlen - sum(self.variables[i+1:]) -1 if len(self.variables)-1 > i else rowlen
            domain = []
            unexplored = max_behind
            while (unexplored + variable <= max_infront):
                domain.append(unexplored)
                unexplored += 1

            domains.append(domain)
        return domains
