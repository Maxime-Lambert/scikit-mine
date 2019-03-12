from src.DiffNorm.Item import Item


class ItemSet:

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
        elif isinstance(other, Item):
            return self.contains(other)
        else:
            return False

    def copy(self):
        copy = ItemSet(self.items)
        return copy

    def fuse(self, other):
        res = [self]
        for element in other:
            res.append(element)
        return res

    def contains(self, item):
        return item in self.items

    def add(self, item):
        self.items.add(item)
