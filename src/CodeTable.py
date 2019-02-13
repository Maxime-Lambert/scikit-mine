# -*- coding: utf-8 -*-

"""
    how to sort how you want
    def repeats(string):
    # Lower the case in the string
    string = string.lower()
    # Get a set of the unique letters
    uniques = set(string)
    # Count the max occurrences of each unique letter
    counts = [string.count(letter) for letter in uniques]
    return max(counts)
"""


import math
from src.Pattern import *

"""
import Database & Pattern
"""


class CodeTable:

    def __init__(self):
        self.patternMap = {}

    def __repr__(self):
        res = ""
        for k, v in self.patternMap.items():
            res += "pattern : " + str(k) + " | usage : " + str(k.usage) + "\n"
        return res

    def add(self, pattern):
        self.patternMap[pattern] = 0
        """if self.patternMap.has_key(pattern):
            #if pattern in self.patternMap:
            self.patternMap[pattern] += 1
        else:
            self.patternMap[pattern] = 0
        return self"""

    def set(self, pattern):
        for key, value in self.patternMap.items():
            if key == pattern:
                key.add_usage()
        self.patternMap[pattern] = 0
        pattern.usage = 1


    def get_pattern(self, pattern):
        for key in self.patternMap.keys():
            if key == pattern:
                return pattern
        return None

    def remove(self, pattern):
        if pattern in self.patternMap:
            del self.patternMap[pattern]
        return self

    def contains(self, pattern):
        return pattern in self.patternMap.items()

    def size(self):
        return len(self.patternMap)

    def get(self, number):
        i = 0
        for k, v in self.patternMap.items():
            if i == number:
                return k
            else:
                i += 1
        return -1

    def usageSum(self):
        i = 0
        for k, v in self.patternMap.items():
            i += k.usage
        return i

    def calculateCodeLength(self):
        for k, v in self.patternMap.items():
            self.patternMap[k] = bytes(-math.log2(k.usage/self.usageSum()))
        return self

    def databaseEncodedLength(self):
        self.calculateCodeLength()
        i = 0
        for k, v in self.patternMap.items():
            i += (k.usage * v)
        return i

    def codeTableLength(self, sct):
        self.calculateCodeLength()
        sct.calculateCodeLength()
        i = 0
        for k, v in self.patternMap.items():
            for p in k.elements:
                for x, y in sct.patternMap.items():
                    if(p == x):
                        i += y
        return i

    def compareGain(self, codeTable, data):
        compression1 = 0
        compression2 = 0
        if compression1 > compression2:
            return True
        return False

    def postPrune(self, data):
        for k, v in self.patternMap:
            ct = self
            del ct.patternMap[k]
            if self.compareGain(ct, data):
                self.patternMap = ct
        return self

    def orderByUsage(self):
        return sorted(self.patternMap, key=self.patternMap.usage)
