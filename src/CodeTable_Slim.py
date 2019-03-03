# -*- coding: utf-8 -*-

from src.database import *
from src.Codetable import *


class CodeTable_Slim(CodeTable):
    """
        A CodeTable_Slim is consisted of a Dictionnary Pattern_Slim -> Double
        The Double represents the size of the byte array that will
        be used to encode the database corresponding to this

        Its attribute is patternMap
    """

    def __init__(self):
        """
            Creates a CodeTable_Slim with an empty PatternMap
        """
        self.patternMap = {}

    def add(self, pattern, transaction):
        """
            Add a Pattern to the CodeTable_Slim, if it's already present it
            adds 1 to its usage else it's put in

            :param pattern: Pattern_Slim you want to add to CodeTable_Slim
            :param transaction: The Transaction your pattern appears in
            :type pattern: Pattern_Slim
            :type transaction: Transaction | List<Transaction>
            :return: The CodeTable_Slim with the pattern added
            :rtype: CodeTable_Slim
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

    def order_by_usage(self):
        """
            Order the Codetable by its pattern's usage

            :return: The Codetable ordered by pattern's usage
            :rtype: Codetable
        """
        return sorted(self.patternMap, key=lambda p: p.usage, reverse=True)
