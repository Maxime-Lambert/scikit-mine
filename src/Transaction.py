class Transaction:
    """docstring for Transaction"""
    items = []

    def __init__(self, elements):
        self.items = elements

    def append(self, item):
        self.items.append(item)

    def remove(self, item):
        self.items.remove(item)

    """def to_string(self):
        return ",".join(self.items)
    """
    def __str__(self):
        return ",".join(self.items)

    def __add__(self, transaction):
        return self.items + transaction.items

    def __eq__(self, transaction):
        for item in items:
            if item not in transaction.items:
                return False
        return True
