class Sequence:
    list_item = []
    usage = 0
    gap = 0

    def __init__(self, element):
        self.index = 0
        self.list_item = set(element)

    def __str__(self):
        res = ""
        for item in self.list_item:
            res += str(item) + " "
        return res

    def __len__(self):
        return len(self.list_item)

    def __iter__(self):
        return iter(self.list_item)

    def __next__(self):
        self.index += 1
        try:
            return self.list_item[self.index - 1]
        except IndexError:
            self.index = 0
            raise StopIteration

    def __eq__(self, other):
        if not isinstance(other, Sequence):
            return False
        return self.list_item == other.list_item

    def __str__(self):
        return str(self.list_item)

    def append(self, item):
        self.list_item += [item]

    def remove(self, item):
        res = []
        for it in self.list_item:
            if it != item:
                res += [it]
        self.list_item = res

    def set_usage(self, usage):
        self.usage = usage

    def set_gap(self, gap):
        self.gap = gap

    def get_usage(self):
        return self.usage
