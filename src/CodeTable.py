# -*- coding: utf-8 -*-

import math
from src import database
from src import Pattern


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

    def __repr__(self):
        """
            Gives a string representation of a Codetable

            :return: A String representing the Codetable
            :rtype: String
        """
        self.OrderByStandardCoverOrder()
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
            :rtype
        """
        self.calculateCode()
        return self.patterns[item]

    def __contains__(self, pattern):
        """
            Says if a pattern is contained in the Codetable or not

            :param pattern: The pattern concerned
            :type pattern: Pattern
            :return: True if the Codetable contains pattern, else False
            :rtype: boolean
        """
        return pattern in self.patternMap.items()

    def set(self, pattern):
        """
            Add a Pattern to the Codetable, if it's already present it adds
            1 to its usage else it's put in

            :param pattern: The pattern you want to add to the Codetable
            :type pattern: Pattern
            :return: The Codetable with the pattern added
            :rtype: Codetable
        """
        for key, value in self.patternMap.items():
            if key == pattern:
                key.add_usage()
        self.patternMap[pattern] = 0
        pattern.usage = 1
        return self.OrderByStandardCoverOrder()

    def Remove(self, pattern):
        """
            Remove a Pattern from the Codetable

            :param pattern: The pattern you want to remove from the Codetable
            :type pattern: Pattern
            :return: The Codetable with pattern removed
            :rtype: Codetable
        """
        if pattern in self.patternMap:
            del self.patternMap[pattern]
        return self.OrderByStandardCoverOrder()

    def Get(self, number):
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

    def OrderByUsage(self):
        """
            Order the Codetable by its pattern's usage

            :return: The Codetable ordered by pattern's usage
            :rtype: Codetable
        """
        return sorted(self.patternMap, key=self.patternMap.usage, reverse=True)

    def OrderByStandardCoverOrder(self):
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
                                                      p.__repr__),
                      reverse=True)

    def UsageSum(self):
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

    def CalculateCodeLength(self):
        """
            Gives each pattern in the Codetable a corresponding code length to
            encode the database
            This function is used locally

            :return: The Codetable with its values updated
            :rtype: Codetable
        """
        sum = self.UsageSum()
        for k, v in self.patternMap.items():
            self.patternMap[k] = (-math.log2(k.usage/sum))
        return self

    def DatabaseEncodedLength(self):
        """
            Gives the size of the database encoded with the Codetable
            This function is used locally

            :return: The size of the database encoded with the Codetable
            :rtype: double
        """
        self.CalculateCodeLength()
        i = 0
        for k, v in self.patternMap.items():
            i += (k.usage * v)
        return i

    def CodeTableLength(self, SCT):
        """
            Gives the size of the current Codetable encoded
            This function is used locally

            :param sct: The standard code table of the database
            :type sct: Codetable
            :return: the size of the current Codetable encoded
            :rtype: double
        """
        self.CalculateCodeLength()
        SCT.CalculateCodeLength()
        i = 0
        for k, v in self.patternMap.items():
            for p in k.elements:
                for x, y in SCT.patternMap.items():
                    if(p == x):
                        i += y
        return i

    def CompareGain(self, CT, data, SCT):
        """
            Compare the size of the database encoded with two different
            Codetables

            :param CT: The other Codetable you want to compare to
            :param data: The database concerned
            :param SCT: The standard code table of the database
            :type CT: Codetable
            :type data: Database
            :type SCT: Codetable
            :return: The Codetable which encodes best the database
            :rtype: boolean

        """
        compCT = CT.CodeTableLength(SCT)+CT.DatabaseEncodedLength()
        compSelf = self.CodeTableLength(SCT)+self.DatabaseEncodedLength()
        if(compCT > compSelf):
            return CT
        return self

    def PostPrune(self, data):
        """
            Checks whether the Codetable is better with some of its elements
            deleted

            :param data: The database concerned
            :type data: Database
            :return: The Codetable without useless elements
            :rtype: Codetable
        """
        self.OrderByStandardCoverOrder()
        for k, v in self.patternMap:
            CT = self
            CT.Remove(k)
            if (self.CompareGain(CT, data).__eq__(CT)):
                self.patternMap = CT
        return self
