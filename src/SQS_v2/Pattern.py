from src.Pattern import Pattern


class Pattern(Pattern):

    active = False
    index = 0
    usage = 0
    gain = 0.0
    elements = []

    def __init__(self, elements):
        self.elements = elements
        self.support = 1

    def __len__(self):
        return len(self.elements)

    def __repr__(self):
        return str(self.elements)

    def __str__(self):
        return str(self.elements)

    def __eq__(self, other):
        if not isinstance(other, Pattern):
            return False
        return self.elements == other.elements

    def __hash__(self):
        """
            Return the hash value of the usage
            :return: An hash value
            :rtype: Integer
        """
        return hash(self.usage)

    def is_active(self):
        return self.active

    def set_active(self):
        self.active = True

    def add(self, window):
        res = []
        for symbol in self.elements:
            res.append(symbol)
        res.append(window)
        self.elements = res

    def get_index(self):
        return self.index