# -*- coding: utf-8 -*-

import math


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
        return self.patternMap == ct.patternMap

    def __repr__(self):
        """
            Gives a string representation of a Codetable

            :return: A String representing the Codetable
            :rtype: String
        """
        res = ""
        for pattern in self.order_by_standard_cover_order():
            res += "pattern : " + str(pattern) + " #USG : "
            res += str(pattern.usage) + " "
            res += "#CODELEN : " + str(self.patternMap[pattern]) + "\n"
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
        for pattern, codelength in self.patternMap:
            if pattern == item:
                return codelength
        return None

    def add(self, pattern_to_add):
        """
            Add a Pattern to the Codetable, if it's already present it adds
            1 to its usage else it's put in

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
            for pattern in self.patternMap.keys():
                if pattern is not pattern_to_add:
                    if pattern.elements.issubset(pattern_to_add.elements):
                        pattern.usage_list -= pattern_to_add.usage_list
                        pattern.usage -= pattern_to_add.usage
        self.calculate_code_length()

    def remove(self, pattern_to_remove):
        """
            Remove a Pattern from the Codetable

            :param pattern: The pattern you want to remove from the Codetable
            :type pattern: Pattern
        """
        if pattern in self.patternMap:
            del self.patternMap[pattern]
        self.calculate_code_length()

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
                      key=lambda p: (-len(p.elements), -p.support, str(p)))

    def usage_sum(self):
        """
            Gives the sum of all the pattern's usage in the Codetable
            This function is used locally

            :return: The sum of all usages
            :rtype: double
        """
        sum = 0
        for pattern in self.patternMap.keys():
            sum += pattern.usage
        return sum

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
        # Je pense qu'il faut prendre en compte d'autres choses en plus
        # pour la taille :
        # typiquement le nombre de patterns et pas uniquement leur longueur
        # ex: tu as 2 patterns de longueur 5 (10 +2), c'est plus intéressant
        # que 5 patterns de longueur 2 (10 + 5) je pense
        # c'est le principe de MDL un peu (miser sur un nb réduit de patterns),
        # mais cela se discute certainement
        # notamment en fonction de l'influence que ça
        # a sur la database_encoded_length
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
            for singleton in pattern.elements:
                for patterns, codelengths in sct.patternMap.items():
                    if patterns.elements == singleton:
                        i += codelengths
            i += codelength
        return i

    def best_code_table(self, ct, data, sct):  # data to be removed?
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
            return True
        return False

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
        for pattern in self.patternMap.keys():
            ct = self.copy()
            ct.remove(pattern)
            if self.best_code_table(ct, data, sct) == ct:
                self.patternMap = ct.copy()
        return self

    def copy(self):
        ct = CodeTable()
        for k in self.patternMap.keys():
            ct.add(k)
        return ct
