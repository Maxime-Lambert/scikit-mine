# -*- coding: utf-8 -*-

import math
from src.database import Database
from src.CodeTable import CodeTable
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
            self.calcul_usage()
        self.calculate_code_length()

    def order_by_usage(self):
        """
            Order the Codetable by its pattern's usage

            :return: The Patterns from patternmap ordered
            :rtype: List<Pattern_Slim>
        """
        return sorted(self.patternMap.keys(),
                      key=lambda p: (p.usage, len(p.elements), int),
                      reverse=True)

    def copy(self):
        """
            Makes a copy of any CodeTableSlim

            :return: The copy of self
            :rtype: CodeTableSlim
        """
        ct = CodeTableSlim(None, self.data)
        for pattern in self.patternMap.keys():
            copy = PatternSlim(0)
            copy.usage = pattern.usage
            copy.support = pattern.support
            copy.usage_list = pattern.usage_list.copy()
            copy.elements = pattern.elements
            ct.patternMap[copy] = self.patternMap[pattern]
        return ct

    # Cover # ajouter un index à partir duquel on recalcul?
    def calcul_usage(self):
        """
            Update usage and usage_list of pattern in the code table.
        """
        keys = self.order_by_standard_cover_order()
        # reset usage and usage_list
        for pattern in keys:
            pattern.usage = 0
            pattern.usage_list.clear()
        curitemcovered = set()
        for trans in self.data:
            it = 0
            # if trans is not completely covered
            while len(trans) != len(curitemcovered) and it < len(self):
                pattern = keys[it]
                # if pattern's item have not been seen yet and
                # they are all in trans
                if not len(pattern.elements & curitemcovered) == len(pattern):
                    if len(pattern.elements & set(trans)) == len(pattern):
                        # increase usage du pattern and add covered items in
                        # the covered items list
                        pattern.usage += 1
                        pattern.usage_list.add(trans)
                        for item in pattern:
                            curitemcovered.add(item)
                it += 1
            curitemcovered.clear()


class DatabaseSlim(Database):
    """
        A CodeTable_Slim is consisted of a Dictionnary Pattern_Slim -> Double
        The Double represents the size of the byte array that will
        be used to encode the database corresponding to this

        Its attribute is patternMap
    """

    def make_standard_code_table(self):
        """Make and return the standard code table of the database."""
        sct = CodeTableSlim(None, self.data_collection)  # map pattern code
        # On ajoute les singletons de la base à la SCT
        for trans in self.data_collection:
            for item in trans:
                pattern = PatternSlim(item)
                sct.add(pattern, trans)
        return sct

    def get_support(self, pattern):
        support = 0
        for trans in self.data_collection:
            inter = set(trans.items).intersection(pattern.elements)
            if inter == pattern.elements:
                support += 1
        return support


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
        self.gain = 0

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

    def union(self, pattern, data):
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
        p.support = data.get_support(p)
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


def generate_candidat(code_table, sct, memory, data):
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
    candidates_list = memory.copy()
    best_usage = 1
    indice_pattern_x = 0
    indice_pattern_y = 0
    x_current = ct[indice_pattern_x]  # attention si viiiiiide
    # ------------- Mine candidates -------------#
    """
    while indice_pattern_x < len(ct)-1 and ct[indice_pattern_x].usage >= best_usage:
        x_current = ct[indice_pattern_x]
        indice_pattern_y = indice_pattern_x + 1
        while indice_pattern_y < len(ct) and ct[indice_pattern_y].usage >= best_usage:
            y_current = ct[indice_pattern_y]
            x_y_current = x_current.union(y_current)
            if best_usage <= x_y_current.usage:
                x_y_current.gain = estimateGain(code_table,x_current,y_current, sct)
                candidates_list.append(x_y_current)
                best_usage = x_y_current.usage
            indice_pattern_y += 1
        indice_pattern_x += 1
    """
    while indice_pattern_x < len(ct)-1:
        x_current = ct[indice_pattern_x]
        indice_pattern_y = indice_pattern_x + 1
        while indice_pattern_y < len(ct):
            y_current = ct[indice_pattern_y]
            x_y_current = x_current.union(y_current, data)
            if x_y_current not in candidates_list:
                if x_y_current.usage > 0:
                    x_y_current.gain = estimateGain(code_table, x_current,
                                                    y_current, sct, data)
                    candidates_list.append(x_y_current)
            indice_pattern_y += 1
        indice_pattern_x += 1
    return candidates_list


def estimateGain(code_table, pattern1, pattern2, standardct, data):
    # copy of parameters
    p1 = pattern1.copy()
    p2 = pattern2.copy()
    ct = code_table.copy()
    sct = standardct.copy()

    # init of usefull variables
    xy_prim = p1.union(p2, data)
    ct_temp = ct.copy()
    ct_temp.add(xy_prim, None)
    s = ct.usage_sum()
    s_prim = s - xy_prim.usage

    diff_usg = ct.different_usages(ct_temp)
    diff_usg2 = ct_temp.different_usages(ct)
    diff_usg_c_0 = []
    diff_usg_cprim_0 = []
    diff_usg_c_cprim_not0 = []
    diff_usg2_c_0 = []
    diff_usg2_cprim_0 = []
    diff_usg2_c_cprim_not0 = []

    for x in diff_usg:
        if x.usage == 0:
            diff_usg_c_0.append(x)
            for y in diff_usg2:
                if y == x:
                    diff_usg2_c_0.append(y)

    for x in diff_usg2:
        if x.usage == 0:
            diff_usg2_cprim_0.append(x)
            for y in diff_usg:
                if y == x:
                    diff_usg_cprim_0.append(y)

    for x in diff_usg:
        if not x.usage == 0:
            for y in diff_usg2:
                if y == x:
                    if not y.usage == 0:
                        diff_usg_c_cprim_not0.append(x)
                        diff_usg2_c_cprim_not0.append(y)
    encoded_union = 0
    for x in xy_prim.elements:
        for pattern, codelength in sct.patternMap.items():
            if list(pattern.elements)[0] == x:
                encoded_union += codelength

    cote1 = (s*math.log(s) - s_prim*math.log(s_prim))
    cote1 += (xy_prim.usage*math.log(xy_prim.usage))

    for x in diff_usg:
        if not x.usage == 0:
            cote1 -= x.usage*math.log(x.usage)
    for y in diff_usg2:
        if not y.usage == 0:
            cote1 -= y.usage*math.log(y.usage)

    cote2 = 0
    cote2 += math.log(xy_prim.usage)
    cote2 -= encoded_union
    cote2 += len(ct)*math.log(s)
    cote2 -= len(ct_temp)*math.log(s_prim)

    for y in diff_usg2_c_cprim_not0:
        cote2 += math.log(y.usage)

    for x in diff_usg_c_cprim_not0:
        cote2 -= math.log(x.usage)

    for y in diff_usg2_c_0:
        cote2 += math.log(y.usage)

    for x in diff_usg_c_0:
        encoded_pattern = 0
        for s in x.elements:
            for pattern, codelength in sct.patternMap.items():
                if list(pattern.elements)[0] == s:
                    encoded_pattern += codelength
        cote2 -= encoded_pattern

    for x in diff_usg_cprim_0:
        encoded_pattern = 0
        for s in x.elements:
            for pattern, codelength in sct.patternMap.items():
                if list(pattern.elements)[0] == s:
                    encoded_pattern += codelength
        cote2 += (encoded_pattern - math.log(x.usage))
    return cote1 + cote2


def removeList(l1, l2):
    res = []
    for x in l1:
        r = True
        for y in l2:
            if y in x.elements:
                r = False
        if r:
            res.append(x)
    return res


def slim(filename, max_iter):
    """
        Get a model of the data. The model is construct from
        frequent itemset following MDL principle.

        :param filename: name of data file to treat
        :param max_iter: number of iteration maximum
        :return: The CodeTableSlim as a model of data
        :rtype: CodeTableSlim
    """
    file = Files(filename)
    database = DatabaseSlim(file.list_int)
    standard_code_table = database.make_standard_code_table()
    code_table = standard_code_table.copy()
    candidate_list = []
    ct_has_improved = True
    iter = 0
    nb_candidat = 0
    while (ct_has_improved) and (iter < max_iter):
        ct_has_improved = False
        candidate_list = generate_candidat(code_table, standard_code_table,
                                           candidate_list, database)
        candidate_list = sorted(candidate_list, key=lambda p: (p.usage),
                                reverse=True)
    # ------------- Improve CT -------------#
        indice_candidat = 0
        while (indice_candidat < len(candidate_list)) and not(ct_has_improved):
            nb_candidat += 1
            candidate = candidate_list[indice_candidat]
            code_table_temp = code_table.copy()
            code_table_temp.add(candidate, None)
            is_ct_best = code_table.best_code_table(code_table_temp,
                                                    standard_code_table)

            indice_candidat += 1
            ct_has_improved = not is_ct_best
            comp = code_table.codetable_length(standard_code_table)
            comp += code_table.database_encoded_length()
            if ct_has_improved:
                test = code_table.different_usages(code_table_temp)
                to_prune = []
                for pat in test:
                    if len(pat) > 1:
                        to_prune.append(pat)
                code_table = code_table_temp
                code_table = code_table.post_prune(standard_code_table,
                                                   to_prune)
                comp2 = code_table.codetable_length(standard_code_table)
                comp2 += code_table.database_encoded_length()
                candidate_list = removeList(candidate_list, candidate.elements)
                if candidate.elements == {3, 7}:
                    for x in code_table.patternMap.keys():
                        print(repr(x))
                print("Accepted : "+repr(candidate)+" ["+str(comp2)+", "+str(comp)+", "+str(candidate.gain)+", "+str(nb_candidat)+"]")
            else:
                comp2 = code_table_temp.codetable_length(standard_code_table)
                comp2 += code_table_temp.database_encoded_length()
                print("Rejected : "+repr(candidate)+" ["+str(comp2)+", "+str(comp)+", "+str(candidate.gain)+", "+str(nb_candidat)+"]")
        iter += 1
    Files.to_file(code_table, "res_"+filename)
    Convert.to_code_table_slim("res_"+filename, standard_code_table)
    return code_table
