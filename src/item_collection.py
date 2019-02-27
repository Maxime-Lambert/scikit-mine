class ItemCollection:
    """docstring for Itemset
    Parameters
    ----------
    elements : integer list
    elements to put in the item collection

    Attributes
    ----------
    items: integer list
    list of items the item collection contains
    """

    def __init__(self, elements):
        self.items = elements.copy

    def __repr__(self):
        return repr(self.items)

    def __str__(self):
        return ",".join(self.items)

    def __len__(self):
        return len(self.items)

    def equals(self, other):
        """True if both itemsets contains same items"""
        if isinstance(other, ItemCollection):
            return self.items == other.items
        else:
            return False

    def copy(self):
        """Retrun a copy of the object"""
        copy = ItemCollection(self.items)
        return copy

    def contains(self, item):
        """True if contains item"""
        return item in self.items
