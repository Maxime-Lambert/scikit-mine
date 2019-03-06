

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
        res = 0
        for item in self.list_item:
            res += 1
        return res

    def __iter__(self):
        return iter(self.list_item)

    def __next__(self):
        self.index += 1
        try:
            return self.list_item[self.index - 1]
        except IndexError:
            self.index = 0
            raise StopIteration

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