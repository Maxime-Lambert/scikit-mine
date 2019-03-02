from src.DiffNorm.ItemSet import *
from src.DiffNorm.DiffNormUtils import *


class CodeTable:

    patterns = []

    def __init__(self, database):
        self.index = 0
        self.usage = 0
        self.size = 0
        self.patterns = []
        self.database = database
        self.i = self.database.id
        self.t_data = {}
        self.mb_rollback = []
        self.initial_encoded_size = 0.0
        self.final_encoded_size = 0.0
        self.encoded_db_size = 0.0
        self.old_db_size = 0.0

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

    def copy(self):
        copy = CodeTable(self.database)
        for pattern in self.patterns:
            copy.add(pattern.copy())
        copy.usage = self.usage
        copy.size = self.size
        copy.update_t_data()
        return copy

    def update_t_data(self):
        tid = 0
        for transaction in self.database:
            self.t_data[int(str(self.database.id) + str(tid))] = self.calculate_cover(transaction)
            tid += 1

    def set_encoded_db_size(self, size):
        self.encoded_db_size = size

    def update_usage(self):
        self.usage = self.calculate_usage()

    def calculate_usage(self):
        usage = 0
        for pattern in self.patterns:
            usage += len(self.gather_usages(pattern))
        return usage

    def update_usages(self):
        for pattern in self.patterns:
            pattern.old_usage = pattern.usage
            pattern.usage = len(self.gather_usages(pattern))

    def rollback_usages(self):
        for pattern in self.patterns:
            pattern.usage = pattern.old_usage

    def calculate_db_encoded_size(self):
        constant = 0.5
        x = log_gamma(self.usage + constant * self.size)
        y = log_gamma(constant * self.size)
        t = 0.0
        # print("CALCULATION")
        for pattern in self.patterns:
            usage = pattern.usage
            t += calc_log_double_factorial(2 * usage - 1) - usage
            """print(repr(pattern) + " " + repr(usage))
        print(self.usage)
        print(x)
        print(y)
        print(t)"""
        return x - y - t

    def gather_usages(self, pattern):
        usages = set()
        for tid in self.t_data:
            if pattern in self.get_cover(tid):
                usages.add(tid)
        return usages

    def get_support(self, pattern):
        return self.database.get_support(pattern)

    def get_cover(self, tid):
        return self.t_data[tid]

    def calculate_cover(self, transaction):
        for pattern in self.patterns:
            if transaction >= pattern:
                return pattern.fuse(self.calculate_cover(ItemSet(transaction) - ItemSet(pattern)))
        return ItemSet([])

    def try_add(self, candidate):
        self.old_db_size = self.encoded_db_size
        self.add(candidate.copy())
        self.sort_in_sco()
        self.update_t_data()
        self.update_usage()
        self.update_usages()

    def try_del(self, candidate):
        self.old_db_size = self.encoded_db_size
        self.delete_pattern(candidate)
        self.sort_in_sco()
        self.update_t_data()
        self.update_usage()
        self.update_usages()

    def delete_pattern(self, pattern):
        """print(self.i)
        self.pp()
        print(pattern)"""
        self.patterns.remove(pattern)
        self.size -= 1

    def rollback(self):
        self.encoded_db_size = self.old_db_size
        self.sort_in_sco()
        self.update_t_data()
        self.update_usage()
        self.rollback_usages()

    def sort_in_sco(self):
        self.patterns.sort(key=lambda x: (len(x), self.get_support(x), str(x)), reverse=True)

    def add(self, pattern):
        if pattern not in self.patterns:
            self.patterns.append(pattern)
            self.size += 1

    def pp(self):
        print("NИNИNИNИNИNИN ct de " + self.database.name + " NИNИNИNИNИNИNИ")
        print()
        print("Initial encoded size")
        print(self.initial_encoded_size)
        print("Final encoded size")
        print(self.final_encoded_size)
        print()
        for x in self.patterns:
            print(repr(x) + " " + repr(len(self.gather_usages(x))))
        print()
