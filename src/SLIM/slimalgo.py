# -*- coding: utf-8 -*-

import math
from src.database import Database
from src.CodeTable import CodeTable
from src.Transaction import Transaction
from src.Pattern import Pattern
from src.Files import Files
from src.SLIM.codetableslim import Convert


class CodeTableSlim(CodeTable):
    """
        A CodeTable_Slim is consisted of a Dictionnary Pattern_Slim -> Double
        The Double represents the size of the byte array that will
        be used to encode the database corresponding to this

        Its attribute is patternMap
    """

    def add(self, pattern_to_add, transaction):
        """
            Add a Pattern to the CodeTable_Slim, if it's already present it
            adds 1 to its usage else it's put in

            :param pattern_to_add
                Pattern_Slim you want to add to CodeTable_Slim
            :param transaction: The Transaction your pattern appears in
            :type pattern_to_add: Pattern_Slim
            :type transaction: Transaction | List<Transaction>
            :return: The CodeTable_Slim with the pattern added
            :rtype: CodeTable_Slim
        """
        if pattern_to_add in self.patternMap:
            for k in self.patternMap.keys():
                if k == pattern_to_add:
                    k.usage += 1
                    k.support += 1
                    if transaction is not None:
                        k.usage_list.add(transaction)
        else:
            if transaction is not None:
                pattern_to_add.usage_list.add(transaction)
            self.patternMap[pattern_to_add] = 0
        if len(pattern_to_add.elements) > 1:
            for pattern in self.patternMap.keys():
                if pattern is not pattern_to_add:
                    if pattern.elements.issubset(pattern_to_add.elements):
                        pattern.usage_list -= pattern_to_add.usage_list
                        pattern.usage = len(pattern.usage_list)
        self.calculate_code_length()

    def order_by_usage(self):
        """
            Order the Codetable by its pattern's usage

            :return: The Patterns from patternmap ordered
            :rtype: List<Pattern_Slim>
        """
        return sorted(self.patternMap.keys(), key=lambda p: p.usage,
                      reverse=True)

    def copy(self):
        """
            Makes a copy of any CodeTableSlim

            :return: The copy of self
            :rtype: CodeTableSlim
        """
        ct = CodeTableSlim(None)
        for k in self.patternMap.keys():
            copy = PatternSlim(0)
            copy.usage = k.usage
            copy.support = k.support
            copy.usage_list = k.usage_list.copy()
            copy.elements = k.elements
            ct.patternMap[copy] = self.patternMap[k]
        return ct


class DatabaseSlim(Database):
    """Database class

    Parameters
    ----------
    int_data_collection : list of integer list
    elements to put in the database

    Attributes
    ----------
    data_list: ItemCollection list
    """

    def __init__(self, transaction_set):
        self.transactions = []
        for itemset in transaction_set:
            trans = Transaction(itemset.copy())
            self.transactions.append(trans)
        self.index = 0
        self.db_card = len(transaction_set)

    def make_standard_code_table(self):
        """Make and return the standard code table of the database."""
        sct = CodeTableSlim(None)  # map pattern code
        # On ajoute les singletons de la base à la SCT
        for trans in self.transactions:
            for item in trans:
                pattern = PatternSlim(item)
                sct.add(pattern, trans)
        return sct


class PatternSlim(Pattern):

    """
        A Pattern_Slim is consisted of a Collection of Items.
        It has an usage (double) : the occurrence of that pattern in the
        cover of the Database
        It has a support (double) : the total occurrence of that pattern
        in the Database
        It has an usageList (set(Transaction)) : all the transactions
        containing the pattern
    """
    def __init__(self, item):
        """
            Create a Pattern with a given transaction and an usage/support of 0
            Has an index 0 for easier time with iterators

            :param item: The item corresponding to the Pattern
            :param transaction: The transaction where the Pattern appears
            :type item: int
            :type transaction: Transaction
            :return: A new Pattern_Slim
            :rtype: Pattern_Slim
        """
        self.usage = 1
        self.support = 1
        self.elements = set()
        self.elements.add(item)
        self.usage_list = set()

    def copy(self):
        """
            Makes a copy of any PatternSlim

            :return: The copy of self
            :rtype: PatternSlim
        """
        copy = PatternSlim(0)
        copy.usage = self.usage
        copy.support = self.support
        copy.elements = self.elements.copy()
        copy.usage_list = self.usage_list.copy()
        return copy

    def __repr__(self):
        """
            Gives a string representation of a PatternSlim

            :return: A String representing the PatternSlim
            :rtype: String
        """
        res = ""
        for k in self.elements:
            res += repr(k) + " "
        res += "("+str(self.usage)+","+str(self.support)+")"
        return res

    def toString(self):
        """
            Gives a string representation of a PatternSlim

            :return: A String representing the PatternSlim
            :rtype: String
        """
        res = repr(self.elements) + " #USG : " + str(self.usage)
        res += " #USGLIST : " + repr(self.usage_list)
        return res

    def union(self, pattern):
        """
            Merged two patterns into one bigger
            :param pattern: the pattern you want to merge self with
            :type pattern: Pattern_Slim
            :return: The merged pattern
            :rtype: Pattern_Slim
        """
        p = PatternSlim(0)
        p.elements = self.elements | pattern.elements
        p.usage_list = self.usage_list & pattern.usage_list
        p.usage = len(p.usage_list)
        p.support = p.usage
        return p

    def getusage(self):
        return self.usage

    def add_usagelist(self, transaction):
        """
            Add a transaction to the current usage_list
            :param transaction: the transaction you want to add
            :type transaction: Transaction
            :return: The merged pattern
            :rtype: Pattern_Slim
        """
        self.usage_list.add(transaction.copy())

    def __eq__(self, pattern):
        return self.elements == pattern.elements

    def __hash__(self):
        """
            Return the hash value of the usage
            :return: An hash value
            :rtype: Integer
        """
        return len(self.elements)


def generate_candidat(code_table,sct):
    """Generate a list of candidates from a code table.

    Parameters
    ----------
    code_table : CodeTable
        Code table where we want to mine candidate

    Returns
    ----------
    list of candidates
    """
    # must work on the list code_table.order_by_usage()
    ct = code_table.order_by_usage()
    candidates_list = []
    best_usage = 1
    indice_pattern_x = 0
    indice_pattern_y = 0
    x_current = ct[indice_pattern_x]  # attention si viiiiiide
    # ------------- Mine candidates -------------#
    while indice_pattern_x < len(ct)-1 and ct[indice_pattern_x].usage >= best_usage:
        x_current = ct[indice_pattern_x]
        indice_pattern_y = indice_pattern_x + 1
        while indice_pattern_y < len(ct) and ct[indice_pattern_y].usage >= best_usage:
            y_current = ct[indice_pattern_y]
            x_y_current = x_current.union(y_current)
            if best_usage <= x_y_current.usage:
                if estimateGain(code_table, x_current, y_current, sct) > 0:
                    candidates_list.append(x_y_current)
                    best_usage = x_y_current.usage
            indice_pattern_y += 1
        indice_pattern_x += 1
    return candidates_list


def estimateGain(code_table, pattern1, pattern2, standardct):
    p1 = pattern1.copy()
    p2 = pattern2.copy()
    ct = code_table.copy()
    sct = standardct.copy()
    xy_prim = p1.union(p2)
    code_table_temp = ct.copy()
    code_table_temp.add(xy_prim, None)
    s = ct.usage_sum()
    s_prim = s - xy_prim.usage
    code1 = ct[p1]
    code2 = ct[p2]
    code1_prim = code_table_temp[p1]
    code2_prim = code_table_temp[p2]
    log_1_prim = 0
    if not code1_prim == 0:
        log_1_prim = math.log(code1_prim)
    log_2_prim = 0
    if not code2_prim == 0:
        log_2_prim = math.log(code2_prim)
    cote1 = s*math.log(s) - s_prim*math.log(s_prim)
    cote1 += xy_prim.usage*math.log(xy_prim.usage)
    cote1 -= (code1*math.log(code1) - code1_prim*log_1_prim)
    cote1 -= (code2*math.log(code2) - code2_prim*log_2_prim)
    encoded_union = 0
    for x in xy_prim.elements:
        for pattern, codelength in sct.patternMap.items():
            if pattern.elements == x:
                encoded_union += codelength
    cote2 = math.log(xy_prim.usage)
    cote2 -= encoded_union
    cote2 += len(ct)*math.log(s)
    cote2 -= len(code_table_temp)*math.log(s_prim)
    cote2 += math.log(code1) - log_1_prim
    cote2 += math.log(code2) - log_2_prim
    encoded_pattern1 = 0
    for x in p1.elements:
        for pattern, codelength in sct.patternMap.items():
            if pattern.elements == x:
                encoded_pattern1 += codelength
    encoded_pattern2 = 0
    for x in p2.elements:
        for pattern, codelength in sct.patternMap.items():
            if pattern.elements == x:
                encoded_pattern2 += codelength
    cote2 += log_1_prim - encoded_pattern1
    cote2 += log_2_prim - encoded_pattern2
    cote2 += encoded_pattern1 - math.log(code1)
    cote2 += encoded_pattern2 - math.log(code2)
    return cote1 + cote2


def slim(filename, max_iter):
    """
    Parameters
    ----------

    """
    file = Files(filename)
    database = DatabaseSlim(file.list_int)
    standard_code_table = database.make_standard_code_table()
    code_table = standard_code_table.copy()
    ct_has_improved = True
    iter = 0
    while (ct_has_improved) and (iter < max_iter):
        ct_has_improved = False
        candidate_list = generate_candidat(code_table, standard_code_table)
        candidate_list = sorted(candidate_list, key=lambda p: (p.usage),
                                reverse=True)
    # ------------- Improve CT -------------#
        indice_candidat = 0
        while (indice_candidat < len(candidate_list)) and not(ct_has_improved):
            candidate = candidate_list[indice_candidat]
            code_table_temp = code_table.copy()
            code_table_temp.add(candidate, None)
            is_ct_best = code_table.best_code_table(code_table_temp, database,
                                                    standard_code_table)

            indice_candidat += 1
            ct_has_improved = not is_ct_best
            if ct_has_improved:
                code_table = code_table_temp
        iter += 1
    Files.to_file(code_table, "res_"+filename)
    Convert.to_code_table_slim("res_"+filename, standard_code_table)
    return code_table
