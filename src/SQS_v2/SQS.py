from src.SQS_v2.CodeTable import CodeTable
from src.SQS_v2.Alignement import Alignement
from src.SQS_v2.Window import Window
from src.SQS_v2.Database import Database
from src.SQS_v2.Pattern import Pattern
from src.SQS_v2.Utils import merge, copy, private, sum_gain, calculate_length, calculate_length_codetable, find_usage, end_index_next_window, arg_min, gain_window


class SQS:
    changes = True

    def __init__(self, database):
        """
            Initialize the algorithm with its database,
            and set all its internal parameters to their initial states

            :param database: name of the database used
        """
        self.database = database
        self.codetable = self.database.make_standard_code_table()
        self.list_pattern_from_estimate = []

    def search(self):
        """
            Main function of the algorithm SQS_SEARCH
            Use the internal database that was initialized
            to return a set of interesting patterns for data mining

            :return: The set of relevant patterns
            :rtype: set_pattern
        """
        list_patern = []
        list_patern_union_x = []
        standart_ct = self.codetable
        alignment = self.run(self.list_pattern_from_estimate)
        while self.changes:
            if isinstance(list_patern,list):
                list_patern_old = list_patern.copy()
            else:
                list_patern = [list_patern]
                list_patern_old = list_patern.copy()
            self.list_pattern_from_estimate = []
            for pattern in self.codetable.patternMap.keys():
                tmp = self.estimate(pattern)
                if tmp != Pattern([]):
                    self.list_pattern_from_estimate.append(tmp)
            for pattern_from_estimate in self.list_pattern_from_estimate:
                if list_patern == []:
                    list_patern = [pattern_from_estimate]
                else:
                    list_patern_union_x = list_patern + [pattern_from_estimate]
                if calculate_length(self.database, list_patern_union_x) < calculate_length(self.database, copy(self.codetable.patternMap.keys())):
                    list_patern = self.prune(list_patern_union_x, False)
            if list_patern == list_patern_old:
                self.changes = False
            list_patern = self.prune(list_patern, True)
        #self.codetable.reduce()
        return list_patern

    def run(self, set_pattern):
        """
            Function ???

            :param set_pattern: set of pattern used
            :return: The Alignement of the sequence
            :rtype: Alignement
        """
        changes = True
        list_window = []
        a = []
        for sequence in self.database:
            sequence.set_usage(find_usage(self.database, sequence))
        for pattern in set_pattern:
            if len(pattern) > 0:
                list_window.extend(self.find_windows(pattern))
                pattern.set_usage(len(list_window))
        list_window_merged = merge(list_window)
        while changes:
            old_a = a
            a = self.align(list_window_merged)
            if a == old_a:
                break
        return a

    def estimate(self, pattern):
        """
            Estimate take a pattern, its internal database and an alignement
            to find a pattern with a better length than the one
            provided in the parameter

            :param pattern: pattern looked upon
            :param alignement: Alignement considered
            :return: The pattern with the minimum length
            :rtype: pattern
        """
        mini = 8000
        p_res = Pattern([])
        dx = {}
        t = []
        for x in self.codetable.patternMap.keys():
            dx[x] = 0

        for x in dx.keys():
            t.extend(self.find_windows(pattern.union(x)))
            t_merged = merge(t)
        tmp = {}
        for pat in t_merged:
            if pat.pattern not in tmp.keys():
                tmp[pat.pattern] = 1
            else:
                tmp[pat.pattern] += 1
        for p, usage in tmp.items():
            if usage < mini:
                mini = usage
                p_res = p
        p_res.set_usage(mini)
        return p_res

    def prune(self, list_pattern, full):
        """
            Prune sort the list of patterns and at the same time,
            search in an iterative way if the list is the most optimal

            :param list_pattern: list of patterns looked upon
            :param full: Execute a total search instead of an heuristic one
            :return: The optimal list of patterns
            :rtype: list_pattern
        """
        self.codetable.codetable_from_sqs(self.list_pattern_from_estimate)
        for pattern in list_pattern:
            codetable_except_x = self.codetable.private(pattern)
            g = sum_gain(self.codetable.get_list_pattern())
            if full or g < calculate_length_codetable(self.codetable) - calculate_length_codetable(codetable_except_x):
                list_pattern_private_x = private(list_pattern, pattern)
                if calculate_length(self.database, list_pattern_private_x) < calculate_length(self.database,
                                                                                              list_pattern):
                    list_pattern = list_pattern_private_x
        return list_pattern

    def align(self, tabwindow):
        """
            From a list of windows provided, create the most optimal list of window
            disjoint between each other included in the original list.

            :param tabwindow: List of windows for the search
            :return: The list of mutually dijoint windows with an optimal gain
            :rtype: list_window
        """
        if tabwindow == []:
            return
        taboptimal = []
        if (tabwindow[0].cost > 0) & tabwindow[0].pattern.active:
            tabwindow[0].optcost = tabwindow[0].cost
        else:
            tabwindow[0].optcost = 0
        n = 0
        for window in tabwindow[1:]:
                c = 0
                if n < len(tabwindow) - 1:
                    c = gain_window(self.codetable, tabwindow[n+1])
                if gain_window(self.codetable, tabwindow[n])+c > window.optcost or window.pattern.active is False:
                    tabwindow[n].optcost=gain_window(self.codetable, tabwindow[n])+c
                    tabwindow[n].optimalwindow=n
                else:
                    tabwindow[n].optcost = gain_window(self.codetable, window)
                    tabwindow[n].optimalwindow = window
                taboptimal.append(n)
                n+=1
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
        i = 0

        for sequence in self.database.list_sequence:
            list_window.extend(self.find_windows_in_sequence(pattern, sequence, i))
            i += 1
        return list_window
