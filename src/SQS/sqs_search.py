
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
        f.sort()

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


def prune(pattern, data, bool):
    pass


def scan_for_gaps(pattern):
    pass
