from src.SQS_v2.CodeTable import CodeTable
from src.SQS_v2.Alignement import Alignement
from src.SQS_v2.Database import Database
from src.SQS_v2.Pattern import Pattern
from src.SQS_v2.Window import Window
from src.SQS_v2.Utils import merge, private, sum_gain, calculate_length, calculate_length_codetable, find_usage, \
    end_index_next_window, arg_min
import math


class SQS:
    changes = True

    def __init__(self, database):
        self.database = database
        self.codetable = self.database.make_standard_code_table()
        self.list_pattern_from_estimate = []
        self.alignement = Alignement(0, 0, Pattern([]))

    def search(self):
        list_patern = []
        self.alignement = self.run([])
        # while self.changes:
        list_patern_old = list_patern.copy()
        self.list_pattern_from_estimate = []
        for pattern in self.codetable.patternMap.keys():
            print("search1")
            print(pattern)
            self.list_pattern_from_estimate.append(self.estimate(pattern, self.alignement))
        for pattern_from_estimate in self.list_pattern_from_estimate:
            print("search")
            list_patern_union_x = list_patern.append(pattern_from_estimate)
            if calculate_length(self.database, list_patern_union_x) < calculate_length(self.database, list_patern):
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
            sequence.set_usage(find_usage(self.database, sequence))
        for pattern in set_pattern:
            print("run")
            if len(pattern) > 0:
                list_window.append(self.find_windows(pattern))
                pattern.set_usage(len(list_window))
        list_window_merged = merge(self.database, list_window)
        # while changes:
        old_alignement = alignement
        alignement = self.align(list_window_merged)
        if alignement == old_alignement:
            changes = False
        return alignement

    def estimate(self, pattern, alignement):
        pass
        """ vx = {}
        wx = {}
        ux = {}
        dx = {}
        T = []
        for x in self.codetable:
            print("estimate 1")
            vx[x] = None
            wx[x] = None
            ux[x] = None
            dx[x] = None
        for item in pattern:
            print("estimate")
            new_align = Alignement(0, len(pattern), pattern)
            d = end_index_next_window(new_align, pattern)
            t = (new_align, d, 0)
            t.length = d - new_align.index_of_beginning_pattern
            T.append(t)
        #while T != []:
           # t_min = arg_min(T)"""

    def prune(self, list_pattern, full):
        for pattern in list_pattern:
            print("prune")
            codetable = self.codetable.codetable_from_sqs(self.list_pattern_from_estimate)
            codetable_except_x = codetable.private(pattern)
            g = sum_gain(self.alignement)
            if full or g < calculate_length_codetable(codetable) - calculate_length_codetable(codetable_except_x):
                list_pattern_private_x = private(list_pattern, pattern)
                if calculate_length(self.database, list_pattern_private_x) < calculate_length(self.database,
                                                                                              list_pattern):
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
            if self.gain(n) + c > window.optimalgain | window.pat.active is False:
                n.optimalgain = self.gain(n) + c
                n.optimalwindow = n
            else:
                n.optimalgain = self.gain(window)
                n.optimalwindow = window
            taboptimal.append(n)
            n = window
        return taboptimal

    def find_windows_in_sequence(self, pattern, sequence, index):
        list_window = []
        li = sequence.list_item
        i = 0

        while i < len(li) - len(pattern.elements) + 1:
            window = True
            if li[i] == pattern.elements[0]:
                for j in range(1, len(pattern.elements)):
                    if li[i + j] != pattern.elements[j]:
                        window = False
                        break

                if window:
                    list_window.append(Window(pattern, i, i + len(pattern.elements) - 1, index))
                    i = i + len(pattern.elements) - 1  # On saute tout le pattern si il est ajoute
            i += 1
        return list_window

        '''while len(li) :

            for v in pattern.elements:
                if not v in li:
                    return list_window
                f[v] = li.index(v)


            while True:
                while len(Q) > 0:
                    v = Q[0]
                    Q.remove(v)
                    matches = (idx for idx, val in enumerate(li) if val == v)
                    f[v] = None
                    for i in matches:
                        if i > b[v]:
                            f[v] = i
                            break

                    if f[v] is None:
                        return list_window
                    w = li[li.index(v) +1]
                    for i in matches:
                        if i < len(li)-1:
                            w=li[i+1]
                            b[w] = (max(int(b[w]), int(f[v])))
                            if b[w] >= f[w] and w not in Q:
                                Q.append(w)
                maximum = max(f, key=f.get)  # Just use 'min' instead of 'max' for minimum.
                minimum = min(f, key=f.get)  # Just use 'min' instead of 'max' for minimum.
                # if f[maximum] - f[minimum] > window_size:
                if len(list_window)>0:
                    if f[maximum] == list_window[len(list_window) - 1].last:
                        list_window.pop()
                w = Window(pattern, f[minimum], f[maximum], index)
                list_window.append(w)
                v = min(f, key=f.get)
                b[v] = f[v]
                Q.append(v)'''

    def find_windows(self, pattern):
        list_window = []
        f = {}
        b = {}
        Q = []
        i = 0;

        for sequence in self.database.list_sequence:
            list_window.extend(self.find_windows_in_sequence(pattern, sequence, i))
            i += 1;
        return list_window
