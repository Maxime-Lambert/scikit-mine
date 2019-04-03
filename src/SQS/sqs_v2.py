from src.SQS.Window import Window


from builtins import list

from reportlab.lib.validators import matchesPattern

from src.Pattern import *
from src.SQS.sqs import find_windows


class SQS:

    def __init__(self, data, list_pattern):
        self.data = data
        self.list_pattern = list_pattern

    def find_usage(self, sequence, data):
        res = 0
        for s in data:
            if s == sequence:
                res += 1
        return res

    def find_windows(self, pattern, data):
        res = []
        for sequence in data:
            if pattern == sequence:
                res += [Window(0, pattern)]
        return res

    def find_windows_in_sequence(self, pattern, sequence):
        list_window = []
        f = {}
        b = {}
        Q = []

        for v in pattern.elements:
            f[v] = sequence.getListItem().index(v)
            b[v] = float("-inf")
            Q.append(v)

        while True:
            while len(Q) > 0:
                v = Q[0]
                Q.remove(v)
                matches = (idx for idx, val in enumerate(sequence.getListItem) if val == v)
                f[v] = None
                for i in matches:
                    if i > b[v]:
                        f[v] = i
                        break
                if f[v] is None:
                    return list_window
                w = sequence.getListItem[sequence.getListItem().index(v) + 1]
                b[w] = max(b[w], f[v])
                if b[w] > f[w] and w not in Q:
                    Q.append(w)
            print(f.values())
            maximum = max(f, key=f.get)  # Just use 'min' instead of 'max' for minimum.
            minimum = min(f, key=f.get)  # Just use 'min' instead of 'max' for minimum.
            #if f[maximum] - f[minimum] > window_size:
            if f[maximum] == list_window[len(list_window)-1][1]:
                list_window.pop()
            list_window.append([f[minimum], f[maximum]])
            v = min(f, key=f.get())
            b[v] = f[v]
            Q.append(v)

    def find_windows2(self, pattern, data, window_size):
        list_window = []
        f = {}
        b = {}
        Q = []
        for sequence in data:
            list_window.append(self.find_windows_in_sequence(pattern, sequence, window_size))
        return list_window

    def align(self, window):
        pass

    def merge(self, list_window):
        res = []
        for window in list_window:
            res.append(window[0])
        return res

    def new_list(self, list_window):
        res = []
        for window in list_window:
            res.append(window[0])
        return res

    def run(self):
        changes = True
        list_window = []
        for sequence in self.data:
            sequence.set_usage(self.find_usage(sequence, self.data))
        for pattern in self.list_pattern:
            if len(pattern) > 0:
                list_window.append(self.find_windows(pattern, self.data))
                pattern.set_usage(len(list_window))
                pattern.set_gap(len(pattern) - 1)
        print("list_window : " + str(list_window))

        z = self.merge(list_window)
        print(z)
        for win in z:
            print(win)
            print("z : " + str(win) + " usage : " + str(win.get_cost()))
        #while changes:
            #a = self.align(w)

        return []