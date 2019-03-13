from src.SQS.sqs import find_windows


def sqs_search(data):
    p_array = []
    a = []
    changes = True
    gap_event = []

    for sequence in data:
        ct = build_window(sequence)

    while changes:
        f = []
        for pattern in ct:
            f.append(estimate(pattern, a, data))
        #f.sort()

        for pattern in f:
            if l(data, pattern + p_array + ct) < l(data, p_array + ct):
                p_array = prune(p_array + pattern , data, False)
                if(p_array.contains(pattern)):
                    scan_for_gaps(pattern + gap_event)
    p_array = prune(p_array,data,True)
    return p_array

def build_window(sequence):
    res = []
    for item in sequence:
        if item not in res:
            res.append(item)
    return res


def estimate(pattern, a, data):

    pass


def l(data, pattenr):
    pass


def prune(patterns, data, bool):
    ct = []
    ct_2 = []
    g = 0

    for pattern in patterns:
        ct = codetable(data, patterns)
        ct_2 = codetable(data, private(patterns,pattern))

        g += sum_gain(gain(find_windows(pattern))) #ici c'est la somme mais je vois pas comment la faire
        if bool or g < l(ct) - l(ct_2):
            if l(data,  private(patterns,pattern)) < l(data,patterns):
                patterns.remove(pattern)
    return patterns


def sum_gain(gain):
    pass


def gain(windows):
    pass


def scan_for_gaps(pattern):
    pass


def codetable(data, patterns):
    pass


def private(list_pattern, pattern):
    res = []
    for p in list_pattern:
        if not p == pattern:
            res += p
    return p
