# -*- coding: utf-8 -*-

from Pattern import *
from Database import *


class CodeTable:

    def __init__(self):
        self.patternMap = {}

    def __repr__(self):
        res = ""
        for k, v in self.patternMap.items():
            res = res + k.repr + " " + v.toString() + " "
        return res

    def contains(self, pattern):
        return pattern in self.patternMap

    def size(self):
        return len(self.patternMap)

    def add(self, pattern):
        if(pattern in self.patternMap):
            self.patternMap[pattern].usage += 1
        else:
            self.patternMap[pattern] = 0
        return self

    def remove(self, pattern):
        if(pattern in self.patternMap):
            del self.patternMap[pattern]
        return self

    def get(self, number):
        i = 0
        for k, v in self.patternMap.items():
            if(i == number):
                return k
            else:
                i += 1
        return -1

    def calculateCodeLength(self):
        return self

    def codeTableLength(self, codeTable):
        return self

    def compareGain(self, codeTable, data, compression1, compression2):
        compression1
        compression2
        if(compression1 > compression2):
            return True
        return False

    def postPrune(self, data):
        for k, v in self.patternMap:
            ct = self
            del ct.patternMap[k]
            if(self.compareGain(ct, data)):
                self.patternMap = ct
                return self

    def orderByUsage(self):
        return sorted(self.patternMap, key=self.patternMap.usage)
