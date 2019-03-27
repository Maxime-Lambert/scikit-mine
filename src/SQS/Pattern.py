

class Pattern:

    active = False
    index = 0
    usage = 0
    gain = 0
    list_symbol = []

    def __init__(self, list_symbol):
        self.list_symbol = list_symbol

    def __len__(self):
        return len(self.list_symbol)

    def __repr__(self):
        return str(self.list_symbol)

    def __str__(self):
        return str(self.list_symbol)

    def add(self, window):
        res = []
        for symbol in self.list_symbol:
            res.append(symbol)
        res.append(window)
        self.list_symbol = res
