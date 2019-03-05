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
        for k in self.order_by_standard_cover_order():
            res += "pattern : " + str(k) + " | usage : " + str(k.usage)
            res += "codeLength : " + self.patternMap.getitem(k)
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

    def add(self, pattern):
        """
            Add a Pattern to the Codetable, if it's already present it adds
            1 to its usage else it's put in

            :param pattern: The pattern you want to add to the Codetable
            :type pattern: Pattern
            :return: The Codetable with the pattern added
            :rtype: Codetable
        """
        b = True
        for key in self.patternMap.keys():
            if key == pattern:
                key.add_usage()
                key.add_support()
                b = False
        if b:
            self.patternMap[pattern] = 0
            pattern.usage = 1
            pattern.support = 1
        self.calculate_code_length()
        pass

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
        pass

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
                      key=lambda p: (len(p.elements), p.support, str(p)),
                      reverse=True)

    def usage_sum(self):
        """
            Gives the sum of all the pattern's usage in the Codetable
            This function is used locally

            :return: The sum of all usages
            :rtype: double
        """
        i = 0
        for k in self.patternMap.keys():
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
        us_sum = self.usage_sum()
        for k, v in self.patternMap:
            # TODO : correct Error -> dictionary changed size during iteration
            self.patternMap[k] = (-math.log2(k.usage/us_sum))
        pass

    def database_encoded_length(self):
        """
            Gives the size of the database encoded with the Codetable
            This function is used locally

            :return: The size of the database encoded with the Codetable
            :rtype: double
        """
        i = 0
        for k, v in self.patternMap.items():
            i += (k.usage * v)
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
        for k, v in self.patternMap:
            ct = self.copy()  # peut-être une copie profonde à faire?
            ct.remove(k)
            if self.best_code_table(ct, data, sct) == ct:
                self.patternMap = ct.copy()
        return self

    def copy(self):
        ct = CodeTable()
        for k in self.patternMap.keys():
            ct.add(k)
        return ct
