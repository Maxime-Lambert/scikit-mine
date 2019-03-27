from src.SQS_v2.Pattern import Pattern


class Window(Pattern):

    cost = 0
    optcost = 0

    def __init__(self, pattern):
        self.pattern = pattern
        self.first = pattern.list_symbol[0]
        self.last = pattern.list_symbol[-1]
        self.tail = pattern.list_symbol[1:-1]
