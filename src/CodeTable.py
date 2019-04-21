# -*- coding: utf-8 -*-

import math
from src import Pattern


class CodeTable:
    """
        A Codetable is consisted of a Dictionnary Pattern -> Double
        The Double represents the size of the byte array that will
        be used to encode the database corresponding to this

        Its attribute's name is patternMap
    """

    def __init__(self, patternMap, database):
        """
            Creates a Codetable with an empty PatternMap if the given
            patternMap is None, else with the given patternMap

            :param patternMap: the patternMap you want to initiate with
            :param database: the database corresponding to this codetable
            :ptype database: Database
            :ptype patternMap: Dictionnary <Pattern,Double>
        """
        if patternMap is None:
            self.patternMap = {}
        else:
            self.patternMap = patternMap.copy()
        self.data = database

    def __eq__(self, ct):
        """
            Gives the equality between two codetables which means if their
            respective patternMap are equal

            :param ct: The Codetable you want to compare self to
            :ptype ct: Codetable
            :return: True if both codetables are equal else False
            :rtype: Boolean
        """
        return self.patternMap == ct.patternMap

    def __repr__(self):
        """
            Gives a string representation of a Codetable

            :return: A String representing the Codetable
            :rtype: String
        """
        res = "nbPattern : "+str(len(self))
        x = self.database_encoded_length()
        res += " L(D | CT) : " + str(x) + "\n"
        for pattern in self.order_by_standard_cover_order():
            res += "pattern : " + str(pattern.elements) + " #USG : "
            res += str(pattern.usage) + " "
            res += "#CODELEN : " + str(self.patternMap[pattern]) + "\n"
        return res

    def __len__(self):
        """
            Gives the number of patterns contained in the Codetable

            :return: the number of patterns contained in the Codetable
            :rtype: int
        """
        return len(self.patternMap)

    def __getitem__(self, pattern_to_find):
        """
            Gives the corresponding code length to a pattern

            If the pattern isn't in the patternMap returns None

            :return: the code length corresponding to the pattern_to_find
            :rtype: double | None
        """
        for pattern, codelength in self.patternMap.items():
            if pattern == pattern_to_find:
                return codelength
        return None

    def add(self, pattern_to_add):
        """
            Adds a Pattern to the Codetable.

            :param pattern_to_add: The pattern you want to add to the Codetable
            :type pattern_to_add: Pattern
        """
        if pattern_to_add in self.patternMap:
            for k in self.patternMap.keys():
                if k == pattern_to_add:
                    k.usage += 1
                    k.support += 1
        else:
            self.patternMap[pattern_to_add] = 0
        if len(pattern_to_add.elements) > 1:
            self.calcul_usage()

    def remove(self, pattern_to_remove):
        """
            Removes a Pattern from the Codetable

            :param pattern: The pattern you want to remove from the Codetable
            :type pattern: Pattern
        """
        if pattern_to_remove in self.patternMap:
            del self.patternMap[pattern_to_remove]
            self.calcul_usage()

    def different_usages(self, ct):
        """
            Gives a list of all patterns with different usage present in self
            and in ct

            :param ct: The codetable you want to compare patterns to
            :type ct: Codetable
            :return: The list of patterns from self with different usages in ct
            :rtype: List<Pattern>
        """
        res = []
        for pattern in self.patternMap.keys():
            if pattern in ct.patternMap.keys():
                for pattern2 in ct.patternMap.keys():
                    if pattern == pattern2:
                        if not pattern.usage == pattern2.usage:
                            res.append(pattern)
        return res

    def order_by_standard_cover_order(self):
        """
            Order the Codetable by following Standard Cover Order
            Standard Cover Order is :
                1 - Pattern's elements length
                2 - Pattern's support
                3 - Pattern's name lexicographilly

            To iterate on the sorted map, simply write :
                for pattern in codetable.order_by_standard_cover_order()

            :return: The Patterns from patternmap ordered
            :rtype: List<Pattern>
        """
        return sorted(self.patternMap.keys(),
                      key=lambda p: (-len(p.elements), -p.support, int))

    def usage_sum(self):
        """
            Gives the sum of all the pattern's usage in the Codetable

            This function is used locally

            :return: The sum of all usages
            :rtype: double
        """
        us_sum = 0
        for pattern in self.patternMap.keys():
            us_sum += pattern.usage
        return us_sum

    def calculate_code_length(self):
        """
            Gives each pattern in the Codetable a corresponding code length to
            encode the database

            This function is used locally
        """
        us_sum = self.usage_sum()
        for pattern in self.patternMap.keys():
            if pattern.usage == 0:
                self.patternMap[pattern] = 0
            else:
                self.patternMap[pattern] = (-math.log2(pattern.usage/us_sum))

    def database_encoded_length(self):
        """
            Gives the size of the database encoded with the Codetable

            This function is used locally

            :return: The size of the database encoded with the Codetable
            :rtype: double
        """
        i = 0
        for pattern, codelength in self.patternMap.items():
            i += (pattern.usage * codelength)
        return i

    def codetable_length(self, sct):
        """
            Gives the size of the current Codetable encoded

            This function is used locally

            :param sct: The standard code table of the database
            :type sct: Codetable
            :return: the size of the current Codetable encoded
            :rtype: double
        """
        i = 0
        for pattern, codelength in self.patternMap.items():
            if not pattern.usage == 0:
                for singleton in pattern.elements:
                    for patterns, codelengths in sct.patternMap.items():
                        if list(patterns.elements)[0] == singleton:
                            i += codelengths
                i += codelength
        return i

    def calcul_usage(self):
        """
            Update usage and usage_list of patterns for database db
            in the code table.
        """
        keys = self.order_by_standard_cover_order()
        # reset usage
        for p in keys:
            p.usage = 0
        curitemcovered = set()
        for trans in self.data:
            it = 0
            # if trans is not completely covered
            while len(trans) != len(curitemcovered) and it < len(self):
                pattern = keys[it]
                # if pattern's item have not been seen yet and
                # they are all in trans
                if not len(pattern.elements & curitemcovered) == len(pattern):
                    if len(pattern.elements & trans) == len(pattern):
                        # increase usage du pattern and add covered items in
                        # the covered items list
                        pattern.usage += 1
                        for item in pattern:
                            curitemcovered.add(item)
                it += 1
            curitemcovered.clear()

    def best_code_table(self, ct, sct):
        """
            Compare the size of the database encoded with two different
            Codetables

            :param ct: The other Codetable you want to compare to
            :param sct: The standard code table of the database
            :type ct: Codetable
            :type sct: Codetable
            :return: True if self encodes best the data, else False
            :rtype: boolean

        """
        compct = ct.codetable_length(sct)+ct.database_encoded_length()
        compself = self.codetable_length(sct)+self.database_encoded_length()
        if compself < compct:
            return True
        return False

    def post_prune(self, sct, pattern_list):
        """
            Checks whether the Codetable is better with some of its elements
            deleted

            Right now, post_prune isn't implemented yet. The only thing it does
            is delete pattern with usages = 0

            :param data: The database concerned
            :param sct: The standard code table of the database
            :type data: Database
            :type sct: Codetable
            :return: The Codetable without useless elements
            :rtype: Codetable
        """
        for pattern in pattern_list:
            copy = self.copy()
            copy.remove(pattern)
            copy.calculate_code_length()
            if not self.best_code_table(copy, sct):
                self = copy.copy()
        return self

    def copy(self):
        """
            Makes a copy of any CodeTable

            :return: The copy of self
            :rtype: CodeTable
        """
        ct = CodeTable(None, self.data)
        for k in self.patternMap.keys():
            copy = Pattern(0)
            copy.usage = k.usage
            copy.support = k.support
            copy.elements = k.elements
            ct.patternMap[copy] = self.patternMap[k]
        return ct
