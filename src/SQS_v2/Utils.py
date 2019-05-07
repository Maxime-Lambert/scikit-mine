import math
from src.SQS_v2.CodeTable import CodeTable
from operator import itemgetter


def private(list_pattern, pattern):
    res = []
    if pattern not in list_pattern:
        return list_pattern
    for pat in list_pattern:
        if pat != pattern :
            res.append(pat)
    return pat


def sum_gain(alignement):
    res = 0
    for align in alignement:
        res += gain(align)
    return res


def merge(list_window):
    res = sorted(list_window, key=itemgetter('sequence', 'first'))
    return res


def gain(align):
    return align.usage


"""def codetable_from_sqs(database, list_window):
    tmp = {}
    for window in list_window:
        if window in tmp:
            tmp[window] += 1
        else:
            tmp[window] = 1
    return CodeTable(tmp, database)"""


def gain_window(codetable, window):
    """
    gain(w) = − L(codep(X)) − (j − i − |X|)L(codeg(X))
    − (|X| − 1)L(coden(X)) + SOMME(∈X)  L(codep(x))
    """
    # res -= codep(codetable, window.pattern)
    # res -= codeg(window.pattern) * (window.indexstart - window.indexend - len(window.pattern))
    # res -= coden(window.pattern) * (len(window.pattern) - 1)
    return - math.log(window.pattern.usage / usage_sum(codetable))


def usage_sum(codetable):
    res = 0
    if isinstance(codetable, dict):
        for pattern in codetable.keys():
            res += pattern.usage
    else:
        for pattern in codetable.patternMap.keys():
            res += pattern.usage
    return res


def calculate_length(database, list_pattern):
    if list_pattern == []:
        return 0
    elif isinstance(list_pattern, list):
        res = 0
        for p in list_pattern:
            if p.usage == 0:
                return 0
            res += - math.log(p.usage / usage_sum_database(database))
        return res
    else:
        if list_pattern == 0:
            return 0
        return - math.log(list_pattern.usage / usage_sum_database(database))


def usage_sum_database(database):
    res = 0
    for s in database:
        res += len(s.list_item)
    return res


def calculate_length_codetable(codetable):
    res = 0
    if isinstance(codetable, dict):
        for x in codetable.keys():
            res += - math.log(x.usage / usage_sum(codetable))
    else:
        for x in codetable.patternMap.keys():
            res += - math.log(x.usage / usage_sum(codetable))
    return res


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


def copy(d_keys):
    res = []
    for pattern in d_keys:
        res.append(pattern)
    return res