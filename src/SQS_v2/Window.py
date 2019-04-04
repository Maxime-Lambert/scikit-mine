from src.SQS_v2.Pattern import Pattern


class Window(Pattern):

    cost = 0
    optcost = 0
    optimalwindow = None

    def __init__(self, pattern, first = 0, last = 0, sequence = 0):
        self.pattern = pattern
        self.first = first
        self.last = last
        self.tail = pattern.elements[1:-1]
        self.sequence = sequence

