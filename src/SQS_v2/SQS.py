from src.CodeTable import CodeTable
from src.Alignement import Alignement
from src.Pattern import Pattern


class SQS:

    changes = True

    def __init__(self, database):
        self.database = database
        self.codetable = CodeTable()
        self.list_pattern_from_estimate = []
        self.alignement = Alignement(0, 0, Pattern([]))

    def search(self):
        list_patern = []
        self.alignement = self.run([])
        while self.changes:
            list_patern_old = list_patern.copy()
            self.list_pattern_from_estimate = []
            for pattern in self.codetable:
                self.list_pattern_from_estimate.append(self.estimate(pattern, self.alignement))
            for pattern_from_estimate in self.list_pattern_from_estimate:
                list_patern_union_x = list_patern.append(pattern_from_estimate)
                if self.l(list_patern_union_x) < self.l(list_patern):
                    list_patern = self.prune(list_patern_union_x, False)
            if list_patern == list_patern_old:
                self.changes = False
        list_patern = self.prune(list_patern, True)
        return list_patern

    def run(self, set_pattern):
        changes = True
        list_window = []
        alignement = Alignement(0, 0, Pattern([]))
        for sequence in self.database:
            sequence.set_usage(self.find_usage(sequence))
        for pattern in set_pattern:
            if len(pattern) > 0:
                list_window.append(self.find_windows(pattern))
                pattern.set_usage(len(list_window))
        list_window_merged = self.merge(list_window)
        while changes:
            old_alignement = alignement
            alignement = self.align(list_window_merged)
            if alignement == old_alignement:
                changes = False
        return alignement

    def estimate(self, pattern, alignement):
        pass

    def l(self, list_pattern):
        pass

    def l_codetable(self, codetable):
        pass

    def prune(self, list_pattern, full):
        for pattern in list_pattern:
            codetable = self.codetable.codetable_from_sqs(self.list_pattern_from_estimate)
            codetable_except_x = codetable.private(pattern)
            g = self.sum_gain(self.alignement)
            if full or g < self.l_codetable(codetable) - self.l_codetable(codetable_except_x):
                list_pattern_private_x = self.private(list_pattern, pattern)
                if self.l(list_pattern_private_x) < self.l(list_pattern):
                    list_pattern = list_pattern_private_x
        return list_pattern

    def align(self, list_window):
        pass

    def private(self, list_pattern, pattern):
        res = []
        if pattern not in list_pattern:
            return list_pattern
        for pat in list_pattern:
            if pat != pattern :
                res.append(pat)
        return pat

    def find_usage(self, sequence):
        res = 0
        for seq in self.database:
            if seq == sequence:
                res += 1
        return res

    def find_windows(self, pattern):
        pass

    def sum_gain(self, alignement):
        res = 0
        for align in alignement:
            res += self.gain(align)
        return res

    def merge(self, list_window):
        pass

    def gain(self, align):
        pass