# -*- coding: utf-8 -*-

import math


class CodeTable:
    """
        A Codetable is consisted of a Dictionnary Pattern -> Code
        Its attribute is patternMap
    """

    def __init__(self):
        self.patternMap = {}

    def __repr__(self):
        """
            Gives a string representation of a Codetable

            :return: A String representing the Codetable
            :rtype: String
        """
        res = ""
        for k, v in self.patternMap.items():
            res += "pattern : " + str(k) + " | usage : " + str(k.usage) + "\n"
        return res

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
        self.patternMap[pattern] = 1
        pattern.usage = 1
        return self

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
        return self

    def contains(self, pattern):
        """
            Says if a pattern is contained in the Codetable or not

            :param pattern: The pattern concerned
            :type pattern: Pattern
            :return: True if the Codetable contains pattern, else False
            :rtype: boolean
        """
        return pattern in self.patternMap.items()

    def size(self):
        """
            Says the number of patterns contained in the Codetable

            :return: the number of patterns contained in the Codetable
            :rtype: int
        """
        return len(self.patternMap)

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

    def usageSum(self):
        """
            Gives the sum of all the pattern's usage in the Codetable

            :return: The sum of all usages
            :rtype: int
        """
        i = 0
        for k, v in self.patternMap.items():
            i += k.usage
        return i

    def calculateCode(self):
        """
            Gives each pattern in the Codetable a corresponding code to encode
            the database

            :return: The Codetable with its value updated
            :rtype: Codetable
        """
        for k, v in self.patternMap.items():
            self.patternMap[k] = bytes(-math.log2(k.usage/self.usageSum()))
        return self

    def databaseEncodedLength(self):
        """
            Gives the size of the database encoded with the Codetable

            :return: The size of the database encoded with the Codetable
            :rtype: int
        """
        self.calculateCodeLength()
        i = 0
        for k, v in self.patternMap.items():
            i += (k.usage * len(v))
        return i

    def codeTableLength(self, sct):
        """
            Gives the size of the current Codetable encoded

            :param sct: The standard code table of the database
            :type sct: Codetable
            :return: the size of the current Codetable encoded
            :rtype: int
        """
        self.calculateCodeLength()
        sct.calculateCodeLength()
        i = 0
        for k, v in self.patternMap.items():
            for p in k.elements:
                for x, y in sct.patternMap.items():
                    if(p == x):
                        i += y
        return i

    def compareGain(self, CT, data):
        """
            Compare the size of the database encoded with two different
            Codetables

            :param CT: The other Codetable you want to compare to
            :param data: The database concerned
            :type CT: Codetable
            :type data: Database
            :return: True if the Codetable has a better encoding, False if
                     CT has a better encoding
            :rtype: boolean
        """
        compression1 = 0
        compression2 = 0
        if compression1 > compression2:
            return True
        return False

    def postPrune(self, data):
        """
            Checks whether the Codetable is better with some of its elements
            deleted

            :param data: The database concerned
            :type data: Database
            :return: The Codetable optimized
            :rtype: Codetable
        """
        for k, v in self.patternMap:
            ct = self
            del ct.patternMap[k]
            if self.compareGain(ct, data):
                self.patternMap = ct
        return self

    def orderByUsage(self):
        """
            Order the Codetable by its pattern's usage

            :return: The Codetable ordered
            :rtype: Codetable
        """
        return sorted(self.patternMap, key=self.patternMap.usage)
