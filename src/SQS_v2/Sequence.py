class Sequence:

    list_item = []
    usage = 0

    def __init__(self, sequence_int):
        self.index = 0
        self.list_item = sequence_int

    def __repr__(self):
        return str(self.list_item)

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

    def set_usage(self, usage):
        self.usage = usage
