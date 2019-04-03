from src.SQS_v2.CodeTable import CodeTable
from src.SQS_v2.Alignement import Alignement
from src.SQS_v2.Database import Database
from src.SQS_v2.Pattern import Pattern
from src.SQS_v2.Utils import merge, private, sum_gain, calculate_length, calculate_length_codetable, find_usage, end_index_next_window, arg_min, gain_window


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
        print("#######CodeTable######")
        print(self.codetable)
        self.list_pattern_from_estimate = []
        self.alignement = Alignement(0, 0, Pattern([]))

    def search(self):
        """
            Main function of the algorithm SQS_SEARCH
            Use the internal database that was initialized
            to return a set of interesting patterns for data mining

            :return: The set of relevant patterns
            :rtype: set_pattern
        """
        list_patern = []
        self.alignement = self.run([])
        #while self.changes:
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
        """
            Function ???

            :param set_pattern: set of pattern used
            :return: The Alignement of the sequence
            :rtype: Alignement
        """
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
        print("list_window_merged")
        print(list_window_merged)
        #while changes:
        old_alignement = alignement
        alignement = self.align(list_window_merged)
        if alignement == old_alignement:
            changes = False
        return alignement

    def estimate(self, pattern, alignement):
        """
            Estimate take a pattern, its internal database and an alignement
            to find a pattern with a better length than the one
            provided in the parameter

            :param pattern: pattern looked upon
            :param alignement: Alignement considered
            :return: The pattern with the minimum length
            :rtype: pattern
        """
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
        """
            Prune sort the list of patterns and at the same time,
            search in an iterative way if the list is the most optimal

            :param list_pattern: list of patterns looked upon
            :param full: Execute a total search instead of an heuristic one
            :return: The optimal list of patterns
            :rtype: list_pattern
        """
        for pattern in list_pattern:
            print("prune")
            codetable = self.codetable.codetable_from_sqs(self.list_pattern_from_estimate)
            print(codetable.patternMap)
            codetable_except_x = self.codetable.private(pattern)
            g = sum_gain(self.alignement)
            if full or g < calculate_length_codetable(self.codetable) - calculate_length_codetable(codetable_except_x):
                list_pattern_private_x = private(list_pattern, pattern)
                if calculate_length(self.database, list_pattern_private_x) < calculate_length(self.database, list_pattern):
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
        print(tabwindow)
        if tabwindow is None:
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
            if gain_window(self.codetable, n)+c > window.optcost | window.pat.active is False:
                n.optcost=gain_window(self.codetable, n)+c
                n.optimalwindow=n
            else:
                n.optcost = gain_window(self.codetable, window)
                n.optimalwindow = window
            taboptimal.append(n)
            n = window
        return taboptimal

    def find_windows(self, pattern):
        pass
