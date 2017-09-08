
class NanoEntry():

    def __init__(self, specs: list):
        self.rules = [int(element) for element in specs]

    def __str__(self):
        return "Nano entry: " + " ".join(str(entry) for entry in self.rules)