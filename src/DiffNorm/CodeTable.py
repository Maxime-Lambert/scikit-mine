from ItemSet import *


class CodeTable:

    patterns = []
    databases = []

    def __init__(self, database, ct_type):
        self.index = 0
        self.usage = 0
        self.size = 0
        self.patterns = []
        self.database = database
        self.ct_type = ct_type
        self.t_data = {}
        self.mb_rollback = []
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
        copy = CodeTable(self.database, self.ct_type)
        for pattern in self.patterns:
            copy.add(pattern)
        copy.usage = self.usage
        copy.size = self.size
        copy.update_t_data()
        return copy

    def update_t_data(self):
        tid = 0
        for transaction in self.database:
            self.t_data[tid] = self.calculate_cover(transaction)
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

    def gather_usages(self, pattern):
        usages = []
        tid = 0
        for transaction in self.database:
            if pattern in self.get_cover(tid):
                usages.append(transaction)
            tid += 1
        return usages

    def get_support(self, pattern):
        return self.database.get_support(pattern)

    def estimate_usage(self, candidate):
        usage = 0
        usages_left = self.gather_usages(candidate.left_is)
        usages_right = self.gather_usages(candidate.right_is)
        for transaction in usages_left:
            if transaction in usages_right:
                usage += 1
        return usage

    def get_cover(self, tid):
        return self.t_data[tid]

    def calculate_cover(self, transaction):
        for pattern in self.patterns:
            if transaction >= pattern:
                return pattern.fuse(self.calculate_cover(ItemSet(transaction) - ItemSet(pattern)))
        return ItemSet([])

    def try_add(self, candidate):
        self.old_db_size = self.encoded_db_size
        self.add(candidate)
        self.sort_in_sco()
        self.update_t_data()
        self.update_usage()
        self.mb_rollback.append(candidate)

    def delete_pattern(self, pattern):
        self.patterns.remove(pattern)

    def rollback(self):
        self.sort_in_sco()
        self.update_t_data()
        self.update_usage()

    def sort_in_sco(self):
        self.patterns.sort(key=lambda x: (len(x), self.get_support(x), str(x)), reverse=True)

    def add(self, element):
        self.patterns.append(element)
        self.size += 1

    def pp(self):
        if self.ct_type == 1:
            print("NИNИNИNИNИNИN ct de " + self.database.name + " NИNИNИNИNИNИNИ")
        elif self.ct_type == 0:
            print("NИNИNИNИNИNИNИ alphabet NИNИNИNИNИNИNИ")
        else:
            print("NИNИNИNИNИNИNИNИN Sj ИNИNИNИNИNИNИNИNИ")
        for x in self.patterns:
            print(repr(x))
        print()
