class Transaction:
    """docstring for Transaction"""
    items = []

    def __init__(self, elements):
        self.items = elements.copy()

    def append(self, item):
        self.items.append(item)

    def remove(self, item):
        self.items.remove(item)

    """def to_string(self):
        return ",".join(self.items)
    """
    def __str__(self):
        res = ""
        for element in self.items:
            res += str(element) + " "
        return res

    def __repr__(self):
        return repr(self.items)

    def __add__(self, transaction):
        return self.items + transaction.items

    def __len__(self):
        return len(self.items)

    def __iter__(self):
        return iter(self.items)

    def __hash__(self):
        return len(self.items)

    def otherequal(self, t):
        return self.items == t.items

    def copy(self):
        return Transaction(self.items)
