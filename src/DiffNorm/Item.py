from src.DiffNorm.ItemSet import *


class Item:

    def __init__(self, integer):
        self.integer = integer

    def __repr__(self):
        return repr(self.integer)

    def __eq__(self, other):
        if isinstance(other, Item):
            return self.integer == other.integer
        else:
            return False

    def __hash__(self):
        return hash(self.integer)

    def __ge__(self, other):
        if isinstance(other, ItemSet):
            return other.contains(self)
        else:
            return False
