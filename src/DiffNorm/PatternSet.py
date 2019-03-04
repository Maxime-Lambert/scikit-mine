from src.DiffNorm.CodeTable import *


class PatternSet:

    patterns = []

    def __init__(self, coding_sets, all_databases, j):
        self.index = 0
        self.j = j
        self.usage = 0
        self.size = 0
        self.patterns = []
        self.coding_sets = coding_sets
        self.all_databases = all_databases
        self.all_db_card = 0
        for database in self.all_databases:
            self.all_db_card += database.db_card
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

    def get_cs_ids(self):
        ids = []
        for cs in self.coding_sets:
            ids.append(cs.i)
        return ids

    def get_support(self, pattern):
        support = 0
        for database in self.databases:
            support += database.get_support(pattern)
        return support

        #  Calculate sum(log(freq_in_D_cursive(x)))
    def get_freq_in_all(self, pattern):
        freq = 0.0
        for item in pattern:
            support = 0
            for database in self.all_databases:
                support += database.get_support(item)
            freq += log2(support / self.all_db_card)
        return freq

    def calculate_cover(self, transaction):
        for pattern in self.patterns:
            if transaction >= pattern:
                return pattern.fuse(self.calculate_cover(ItemSet(transaction) - ItemSet(pattern)))
        return ItemSet([])

    def calculate_patternset_diff_encoded_size(self, pattern):
        old_sj_card_size = universal_code_len(self.size)
        new_sj_card_size = universal_code_len(self.size + 1)
        pattern_size = universal_code_len(len(pattern))
        freq = self.get_freq_in_all(pattern)
        cs_sum_of_diff = 0.0
        for cs in self.coding_sets:
            cs_sum_of_diff += cs.old_db_size - cs.encoded_db_size
        return old_sj_card_size - new_sj_card_size - pattern_size + freq + cs_sum_of_diff

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
