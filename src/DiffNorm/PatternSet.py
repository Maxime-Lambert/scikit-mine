from src.DiffNorm.CodeTable import *


class PatternSet:

    patterns = []

    def __init__(self, coding_sets, j):
        self.index = 0
        self.j = j
        self.usage = 0
        self.size = 0
        self.patterns = []
        self.coding_sets = coding_sets
        self.databases = []
        for cs in coding_sets:
            self.databases.append(cs.database)

    def __repr__(self):
        return repr(self.patterns)

    def __iter__(self):
        return iter(self.patterns)

    def __next__(self):
        self.index += 1
        try:
            return self.patterns[self.index - 1]
        except IndexError:
            self.index = 0
            raise StopIteration

    def __contains__(self, element):
        return element in self.patterns

    def __len__(self):
        return len(self.patterns)

    def __getitem__(self, item):
        return self.patterns[item]

    def get_support(self, pattern):
        support = 0
        for database in self.databases:
            support += database.get_support(pattern)
        return support

    def calculate_cover(self, transaction):
        for pattern in self.patterns:
            if transaction >= pattern:
                return pattern.fuse(self.calculate_cover(ItemSet(transaction) - ItemSet(pattern)))
        return ItemSet([])

    def try_add(self, candidate):
        self.add(candidate.copy())
        self.sort_in_sco()

    def try_del(self, candidate):
        self.delete_pattern(candidate)
        self.sort_in_sco()

    def delete_pattern(self, pattern):
        self.patterns.remove(pattern)
        self.size -= 1

    def sort_in_sco(self):
        self.patterns.sort(key=lambda x: (len(x), self.get_support(x), str(x)), reverse=True)

    def add(self, pattern):
        if pattern not in self.patterns:
            self.patterns.append(pattern)
            self.size += 1

    def pp(self):
        print()
        print("NИNИNИNИNИNИN S" + repr(self.j) + " NИNИNИNИNИNИNИ")
        for x in self.patterns:
            print(x)
