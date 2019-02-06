class Transaction:
    """docstring for Transaction"""
    elements = []

    def __init__(self, elements):
        self.elements = elements

    def append(self, item):
        self.elements.append(item)

    def remove(self, item):
        self.elements.remove(item)

    def toString(self):
        return ",".join(self.elements)

    def __add__(self, transaction):
        return self.elements + transaction.elements



