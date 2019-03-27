class CodeTable:

    index = 0

    def __init__(self):
        self.list_pattern = []

    def private(self, pattern):
        if self.list_pattern == []:
            return self.list_pattern
        elif pattern not in self.list_pattern:
            return self.list_pattern
        res = []
        for pat in self.list_pattern:
            if pat != pattern:
                res.append(pat)
        return res

    def codetable_from_sqs(self, alignement):
        pass

    def __iter__(self):
        return iter(self.list_pattern)

    def __next__(self):
        self.index += 1
        try:
            return self.list_pattern[self.index - 1]
        except IndexError:
            self.index = 0
            raise StopIteration