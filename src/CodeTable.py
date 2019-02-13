# -*- coding: utf-8 -*-

from Pattern import *
from Database import *

import math


class CodeTable:

    def __init__(self):
        self.patternMap = {}

    def __repr__(self):
        res = ""
        for k, v in self.patternMap.items():
            res = res + k.repr + " " + v.toString() + " "
        return res

    def add(self, pattern):
        for k, v in self.patternMap:
            if pattern.__eq__(k):
                k.usage += 1
            return 0
        self.patternMap[pattern] = 0
        return 1

    def remove(self, pattern):
        if pattern in self.patternMap:
            del self.patternMap[pattern]
        return self

    def contains(self, pattern):
        return pattern in self.patternMap

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
    """
    def repeats(string):
    # Lower the case in the string
    string = string.lower()
 
    # Get a set of the unique letters
    uniques = set(string)
 
    # Count the max occurrences of each unique letter
    counts = [string.count(letter) for letter in uniques]
 
    return max(counts)"""
