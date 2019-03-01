# -*- coding: utf-8 -*-

import math
from src.database import *


class CodeTable:
    """
        A Codetable is consisted of a Dictionnary Pattern -> Double
        The Double represents the size of the byte array that will
        be used to encode the database corresponding to this

        Its attribute is patternMap
    """

    def __init__(self):
        """
            Creates a Codetable with an empty PatternMap
        """
        self.patternMap = {}

    def __eq__(self, ct):
        return self == ct

    def __repr__(self):
        """
            Gives a string representation of a Codetable

            :return: A String representing the Codetable
            :rtype: String
        """
        self.order_by_standard_cover_order()
        res = ""
        for k, v in self.patternMap.items():
            res += "pattern : " + str(k) + " | usage : " + str(k.usage) + "\n"
        return res

    def __len__(self):
        """
            Says the number of patterns contained in the Codetable

            :return: the number of patterns contained in the Codetable
            :rtype: int
        """
        return len(self.patternMap)

    def __getitem__(self, item):
        """
            Gets the corresponding code length to a pattern

            :return: the number of patterns contained in the Codetable
            :rtype: double
        """
        self.calculate_code_length()
        return self.patternMap[item]

    def __contains__(self, pattern):
        """
            Says if a pattern is contained in the Codetable or not

            :param pattern: The pattern concerned
            :type pattern: Pattern
            :return: True if the Codetable contains pattern, else False
            :rtype: boolean
        """
        return pattern in self.patternMap.items()

    def add(self, pattern, transaction):
        """
            Add a Pattern to the Codetable, if it's already present it adds
            1 to its usage else it's put in

            :param pattern: The pattern you want to add to the Codetable
            :param transaction: The Transaction your pattern appears in
            :type pattern: Pattern
            :type transaction: Transaction | List<Transaction>
            :return: The Codetable with the pattern added
            :rtype: Codetable
        """
        b = False
        for key, value in self.patternMap.items():
            if key == pattern:
                key.add_usage()
                key.add_support()
                key.add_usageList(transaction)
                b = True
        if b:
            self.patternMap[pattern] = 0
            pattern.usage = 1
            pattern.support = 1
            pattern.usageList = transaction
        self.calculate_code_length()
        return self.order_by_standard_cover_order()

    def remove(self, pattern):
        """
            Remove a Pattern from the Codetable

            :param pattern: The pattern you want to remove from the Codetable
            :type pattern: Pattern
            :return: The Codetable with pattern removed
            :rtype: Codetable
        """
        if pattern in self.patternMap:
            del self.patternMap[pattern]
        self.calculate_code_length()
        return self.order_by_standard_cover_order()

    def get(self, number):
        """
            Gives the pattern at a certain index in the Codetable

            :param number: The index you want access to
            :type number: int
            :return: The pattern at the index if it exists, else -1
            :rtype: Pattern | int
        """
        i = 0
        for k, v in self.patternMap.items():
            if i == number:
                return k
            else:
                i += 1
        return -1

    def order_by_usage(self):
        """
            Order the Codetable by its pattern's usage

            :return: The Codetable ordered by pattern's usage
            :rtype: Codetable
        """
        return sorted(self.patternMap, key=self.patternMap.get, reverse=True)

    def order_by_standard_cover_order(self):
        """
            Order the Codetable by following Standard Cover Order
            Standard Cover Order is :
                1 - Pattern's elements length
                2 - Pattern's support
                3 - Pattern's name lexicographilly
            This function is used locally

            :return: The Codetable ordered by Standard Cover Order
            :rtype: Codetable
        """
        return sorted(self.patternMap, key=lambda p: (p.elements.__len__,
                                                      p.support,
                                                      repr(p)),
                      reverse=True)

    def usage_sum(self):
        """
            Gives the sum of all the pattern's usage in the Codetable
            This function is used locally

            :return: The sum of all usages
            :rtype: double
        """
        i = 0
        for k, v in self.patternMap.items():
            i += k.usage
        return i

    def calculate_code_length(self):
        """
            Gives each pattern in the Codetable a corresponding code length to
            encode the database
            This function is used locally

            :return: The Codetable with its values updated
            :rtype: Codetable
        """
        sum = self.usage_sum()
        for k, v in self.patternMap.items():
            self.patternMap[k] = (-math.log2(k.usage/sum))
        return self

    def database_encoded_length(self):
        """
            Gives the size of the database encoded with the Codetable
            This function is used locally

            :return: The size of the database encoded with the Codetable
            :rtype: double
        """
        self.calculate_code_length()
        i = 0
        for k, v in self.patternMap.items():
            i += (k.usage * v)
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
        for k, v in self.patternMap.items():
            for p in k.elements:
                for x, y in sct.patternMap.items():
                    if p == x:
                        i += y
        return i

    def best_code_table(self, ct, data, sct):
        """
            Compare the size of the database encoded with two different
            Codetables

            :param ct: The other Codetable you want to compare to
            :param data: The database concerned
            :param sct: The standard code table of the database
            :type ct: Codetable
            :type data: Database
            :type sct: Codetable
            :return: The Codetable which encodes best the database
            :rtype: boolean

        """
        compct = ct.codetable_length(sct)+ct.database_encoded_length()
        compself = self.codetable_length(sct)+self.database_encoded_length()
        if compct > compself:
            return ct
        return self

    def post_prune(self, data, sct):
        """
            Checks whether the Codetable is better with some of its elements
            deleted

            :param data: The database concerned
            :param sct: The standard code table of the database
            :type data: Database
            :type sct: Codetable
            :return: The Codetable without useless elements
            :rtype: Codetable
        """
        for k, v in self.patternMap:
            ct = self
            ct.remove(k)
            if self.best_code_table(ct, data, sct) == ct:
                self.patternMap = ct
        return self

    def copy(self):
        ct = CodeTable()
        for k, v in self.patternMap.items():
            ct.add(k, k.usagelist)
        return ct
