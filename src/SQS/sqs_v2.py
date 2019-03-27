from src.SQS.Window import Window


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