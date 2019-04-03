from src.SQS.Pattern import Pattern


class Window(Pattern):

    cost = 0

    def __init__(self, cost, pattern):
        self.cost = cost
        self.pattern = pattern

    def __repr__(self):
        return str(self.pattern)

    def __eq__(self, other):
        if not isinstance(other, Window):
            return False
        return self.pattern == other.pattern

    def __hash__(self):
        return hash(self.pattern)

    def get_cost(self):
        return self.cost

    def get_pattern(self):
        return self.pattern
