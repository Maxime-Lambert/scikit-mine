class ItemSet:
    """Itemset.

    General structure which represents database transactions,
    patterns and single items of the alphabet I.

    todo:
        Make this class inherit from list and get rid of useless
        built-in functions.

    Parameters
    ----------
    items : list of int
        List of items of this pattern/transaction.

    Attributes
    ----------
    index : int
        Iterator over the contents of this itemset.
    items : set of int
        List of items of this pattern/transaction.
    """

    usage = 0
    old_usage = 0

    def __init__(self, items):
        self.index = 0
        self.items = set(items)

    def __repr__(self):
        return repr(self.items)

    def __iter__(self):
        return iter(self.items)

    def __next__(self):
        self.index += 1
        try:
            return self.items[self.index - 1]
        except IndexError:
            self.index = 0
            raise StopIteration

    def __and__(self, other):
        return ItemSet(self.items & other.items)

    def __or__(self, other):
        return self.items | other.items

    def __sub__(self, other):
        return ItemSet(self.items - other.items)

    def __len__(self):
        return len(self.items)

    def __eq__(self, other):
        if isinstance(other, ItemSet):
            return self.items == other.items
        else:
            return False

    def __ge__(self, other):
        if isinstance(other, ItemSet):
            for item in other.items:
                if not self.contains(item):
                    return False
            return True
        elif isinstance(other, int):
            return self.contains(other)
        else:
            return False

    def fuse(self, other):
        """Returns union/or/| of an ItemSet object and another one
        in a list ([ItemSet]), used in a recursive function.

        Parameters
        ----------
        other : ItemSet object
              ItemSet with which we want to fuse self.
        """
        res = [self]
        for element in other:
            res.append(element)
        return res

    # These 3 functions are useless if class inherits from list.
    def copy(self):
        """Returns a clone of self
        """
        copy = ItemSet(self.items)
        return copy

    def contains(self, item):
        """Returns the result of verification of presense of this item in self.

        Parameters
        ----------
        item : int
            Item, presense of which we want to verify.
        """
        return item in self.items

    def add(self, item):
        """Adds item to self.

        Parameters
        ----------
        item : int
            Item to add to self.
        """
        self.items.add(item)
