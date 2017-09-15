from CSP._old.CSP import CSP


class Entry():

    def __init__(self, specs: list, rowlen):
        self.variables = [int(element) for element in specs]
        self.length = rowlen

        # Creating CSP variables.
        self.domains = self.generate_domains(rowlen)
        self.possibles = self.get_all_possibilities(self.domains)

    def __getitem__(self, item) :
        return CSP(self.variables[item], self.domains[item], None)

    def __str__(self):
        return " ".join([str(entry) for entry in self.variables])

    def __len__(self):
        return len(self.variables)

    def get_all_possibilities(self, domain):
        def permutations_by_row(grid, i, values, results):
            if i == len(grid):
                # output = [0] * self.length
                # for val in values:
                #     output[val] = 1
                # results.append(output)
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

    def total_length(self):
        """ Sum of all rules + the required spaces """
        return sum(self.variables) + len(self) - 1


class SuperEntry():

    def __init__(self):
        pass