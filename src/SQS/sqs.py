def sqs(data, patterns):
    changes = True
    for sequence in data:
        sequence.set_usage(find_usage(sequence, data))
    for pattern in patterns:
        if(pattern.length > 0):
            list_window = find_windows(pattern, data)
            pattern.set_usage(list_window.length)
            pattern.set_gap(pattern.length - 1)
    w = merge(list_window)

    while changes:
        a = align(w)


    return a


def find_usage(sequence, data):
    res = 0
    for s in data:
        if s == sequence:
            res += 1
    return res


def find_windows(pattern, data):


def align(window):
    pass


def merge(window):
    res = []
    for item in window:
        res += [item]
    return res
