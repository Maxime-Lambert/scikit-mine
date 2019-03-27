from src.Sequence import Sequence


class Database:

    list_sequence = []

    def __init__(self, list_sequence_int):
        self.index = 0
        for sequence_int in list_sequence_int:
            self.list_sequence.append(Sequence(sequence_int))

    def __iter__(self):
        return iter(self.list_sequence)

    def __next__(self):
        self.index += 1
        try:
            return self.list_sequence[self.index - 1]
        except IndexError:
            self.index = 0
            raise StopIteration