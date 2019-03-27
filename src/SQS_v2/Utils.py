def private(list_pattern, pattern):
    res = []
    if pattern not in list_pattern:
        return list_pattern
    for pat in list_pattern:
        if pat != pattern :
            res.append(pat)
    return pat


def sum_gain(self, alignement):
    res = 0
    for align in alignement:
        res += self.gain(align)
    return res


def merge(self, list_window):
    pass


def gain(self, align):
    pass


def calculate_length(database, list_pattern):
    pass


def calculate_length_codetable(codetable):
    pass


def find_usage(self, sequence):
    res = 0
    for seq in self.database:
        if seq == sequence:
            res += 1
    return res