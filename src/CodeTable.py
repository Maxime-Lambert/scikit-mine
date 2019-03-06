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
        return self == ct

    def __repr__(self):
        """
            Gives a string representation of a Codetable

            :return: A String representing the Codetable
            :rtype: String
        """
        res = ""
        for pattern in self.patternMap.keys():
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
        return self.patternMap[item]

    def add(self, pattern_to_add):
        """
            Add a Pattern to the Codetable, if it's already present it adds
            1 to its usage else it's put in

            :param pattern_to_add: The pattern you want to add to the Codetable
            :type pattern_to_add: Pattern
        """
        pattern_found = False
        for pattern in self.patternMap.keys():
            if pattern == pattern_to_add:
                to_remove = pattern
                to_remove.add_usage()
                to_remove.add_support()
                pattern_found = True
        if not pattern_found:
            self.patternMap[pattern_to_add] = 0
        else:
            pattern_to_add.usage = to_remove.usage
            pattern_to_add.support = to_remove.support
            self.remove(to_remove)
            self.patternMap[pattern_to_add] = 0
        self.calculate_code_length()

    def remove(self, pattern_to_remove):
        """
            Remove a Pattern from the Codetable

            :param pattern: The pattern you want to remove from the Codetable
            :type pattern: Pattern
        """
        print(pattern_to_remove)
        change = {}
        found_one = False
        for pattern in self.patternMap.keys():
            if found_one:
                    change[pattern] = self.patternMap[pattern]
            else:
                if not pattern == pattern_to_remove:
                    change[pattern] = self.patternMap[pattern]
                else:
                    found_one = True
        self.patternMap.clear()
        for pattern in change.keys():
            self.patternMap[pattern] = change[pattern]

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
        change = {}
        for pattern in self.patternMap.keys():
            change[pattern] = (-math.log2(pattern.usage/us_sum))
        for pattern in change.keys():
            self.patternMap[pattern] = change[pattern]

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
            for singleton in pattern:
                i += sct.patternMap.getitem(singleton)
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
