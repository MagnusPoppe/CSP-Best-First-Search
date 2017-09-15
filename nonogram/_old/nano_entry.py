
class NanoEntry():

    def __init__(self, specs: list):
        self.rules = [int(element) for element in specs]

    def total_length(self):
        """ Sum of all rules + the required spaces """
        return sum(self.rules) + len(self)-1

    def __str__(self):
        return "Nano entry: " + " ".join(str(entry) for entry in self.rules)

    def __len__(self):
        return len(self.rules)

    def __getitem__(self, item):
        return self.rules[item]