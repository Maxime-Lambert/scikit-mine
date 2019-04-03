from src.SQS_v2.CodeTable import CodeTable
from src.SQS_v2.Alignement import Alignement
from src.SQS_v2.Pattern import Pattern
from src.SQS_v2.Utils import merge, private, sum_gain, calculate_length, calculate_length_codetable, find_usage


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
            sequence.set_usage(find_usage(sequence))
        for pattern in set_pattern:
            if len(pattern) > 0:
                list_window.append(self.find_windows(pattern))
                pattern.set_usage(len(list_window))
        list_window_merged = merge(list_window)
        while changes:
            old_alignement = alignement
            alignement = self.align(list_window_merged)
            if alignement == old_alignement:
                changes = False
        return alignement

    def estimate(self, pattern, alignement):
        pass

    def prune(self, list_pattern, full):
        for pattern in list_pattern:
            codetable = self.codetable.codetable_from_sqs(self.list_pattern_from_estimate)
            codetable_except_x = codetable.private(pattern)
            g = sum_gain(self.alignement)
            if full or g < calculate_length_codetable(codetable) - calculate_length_codetable(codetable_except_x):
                list_pattern_private_x = private(list_pattern, pattern)
                if calculate_length(list_pattern_private_x) < calculate_length(list_pattern):
                    list_pattern = list_pattern_private_x
        return list_pattern

    def align(self, tabwindow):
        if tabwindow[0] is None:
            return
        taboptimal = []
        if (tabwindow[0].cost > 0) & tabwindow[0].pat.active:
            tabwindow[0].optcost = tabwindow[0].cost
        else:
            tabwindow[0].optcost = 0
        n = tabwindow[0]
        for window in tabwindow[1:]:
            c = 0
            if next(n):
                c = next(n).optimalgain
            if self.gain(n)+c > window.optimalgain | window.pat.active is False:
                n.optimalgain=self.gain(n)+c
                n.optimalwindow=n
            else:
                n.optimalgain = self.gain(window)
                n.optimalwindow = window
            taboptimal.append(n)
            n = window
        return taboptimal

    def find_windows(self, pattern):
        pass
