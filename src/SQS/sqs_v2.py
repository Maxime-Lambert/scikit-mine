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
        pass

    def align(self, window):
        pass

    def merge(self, window):
        res = []
        for item in window:
            res += [item]
        return res

    def run(self):
        changes = True
        print(self.data)
        for sequence in self.data:
            print(sequence)
            sequence.set_usage(self.find_usage(sequence, self.data))
        for pattern in self.list_pattern:
            if pattern.length > 0:
                list_window = self.find_windows(pattern, self.data)
                pattern.set_usage(list_window.length)
                pattern.set_gap(pattern.length - 1)
        w = self.merge(list_window)

        while changes:
            a = self.align(w)

        return a