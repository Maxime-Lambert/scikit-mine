class Window:

    cost = 0

    def __init__(self, cost, pattern):
        self.cost = cost
        self.pattern = pattern

    def get_cost(self):
        return self.cost

    def get_pattern(self):
        return self.pattern