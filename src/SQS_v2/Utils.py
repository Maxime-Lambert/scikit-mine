import math

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


def merge(database, list_window):
    pass


def gain(database, align):
    pass


def gain_window(codetable, window):
    """
    gain(w) = − L(codep(X)) − (j − i − |X|)L(codeg(X))
    − (|X| − 1)L(coden(X)) + SOMME(∈X)  L(codep(x))
    """
    res = 0.0
    res -= codep(codetable, window.pattern)
    # res -= codeg(window.pattern) * (window.indexstart - window.indexend - len(window.pattern))
    # res -= coden(window.pattern) * (len(window.pattern) - 1)
    for patterns in window.pattern:
        res += codep(codetable, patterns)
    return res

def codep(codetable, pattern):
    res = 0.0
    res = - math.log(pattern.usage/codetable.usage)
    return res

def calculate_length(database, list_pattern):
    return 0


def calculate_length_codetable(codetable):
    pass


def find_usage(database, sequence):
    res = 0
    for seq in database:
        if seq == sequence:
            res += 1
    return res


def end_index_next_window(alignement, pattern):
    pass


def arg_min(T):
    res = T[0]
    for t in T:
        if t < res:
            res = t
    return res