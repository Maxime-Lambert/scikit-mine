# -*- coding: utf-8 -*-

from src.database import Database
from src.CodeTable import CodeTable
from src.Transaction import Transaction
from src.Pattern import Pattern
from src.Files import Files
class CodeTableSlim(CodeTable):
    """
        A CodeTable_Slim is consisted of a Dictionnary Pattern_Slim -> Double
        The Double represents the size of the byte array that will
        be used to encode the database corresponding to this

        Its attribute is patternMap
    """
    patternMap = {}

    def __init__(self):
        """
            Creates a CodeTable_Slim with an empty PatternMap
        """
        self.patternMap = {}

    def add(self, pattern_to_add, transaction):
        """
            Add a Pattern to the CodeTable_Slim, if it's already present it
            adds 1 to its usage else it's put in

            :param pattern_to_add: Pattern_Slim you want to add to CodeTable_Slim
            :param transaction: The Transaction your pattern appears in
            :type pattern_to_add: Pattern_Slim
            :type transaction: Transaction | List<Transaction>
            :return: The CodeTable_Slim with the pattern added
            :rtype: CodeTable_Slim
        """
        pattern_found = False
        for pattern in self.patternMap.keys():
            if pattern == pattern_to_add:
                to_remove = pattern
                to_remove.add_usage()
                to_remove.add_support()
                if transaction is not None:
                    to_remove.add_usagelist(transaction.copy())
                pattern_found = True
        if not pattern_found:
            self.patternMap[pattern_to_add] = 0
            if transaction is not None:
                pattern_to_add.add_usagelist(transaction)
        else:
            pattern_to_add.usage = to_remove.usage
            pattern_to_add.support = to_remove.support
            pattern_to_add.usage_list = to_remove.usage_list
            self.remove(to_remove)
            self.patternMap[pattern_to_add] = 0
        if len(pattern_to_add.elements) > 1:
            for pattern in self.patternMap.items():
                if pattern.elements.issubset(pattern_to_add.elements):
                    pattern.usage_list -= pattern_to_add.usage_list
                    pattern.usage -= pattern_to_add.usage
        self.calculate_code_length()

    def order_by_usage(self):
        """
            Order the Codetable by its pattern's usage

            :return: The Patterns from patternmap ordered
            :rtype: List<Pattern_Slim>
        """
        return sorted(self.patternMap.keys(), key=lambda p: p.usage, reverse=True)

    def copy(self):
        ct = CodeTableSlim()
        for k in self.patternMap.keys():
            ct.add(k, None)
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
        sct = CodeTableSlim()  # map pattern code
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
        copy = PatternSlim(0)
        copy.usage = self.usage
        copy.support = self.support
        copy.elements = self.elements.copy()
        copy.usage_list = self.usage_list.copy()
        return copy

    def __repr__(self):
        repr(self.elements)

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
        return hash(self.usage)

def generate_candidat(code_table):
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
    candidates_list = [] #pattern list
    best_usage = 0
    indice_pattern_x = 0
    x_current = ct[indice_pattern_x] #attention si viiiiiide
	# ------------- Mine candidates -------------#
    while indice_pattern_x < len(ct) and x_current.usage >= best_usage:
        indice_pattern_y = indice_pattern_x + 1 #on ne prend que les patterns juste après x
        y_current = ct[indice_pattern_y]
        while indice_pattern_y < len(ct) and y_current.usage >= best_usage:
            x_y_current = x_current.union(y_current)
            if best_usage <= x_y_current.usage: #si bon usage on le garde et maj best_usage
                candidates_list.append(x_y_current)
                best_usage = x_y_current.usage
            indice_pattern_y = indice_pattern_y + 1
            y_current = ct[indice_pattern_y]
        indice_pattern_x = indice_pattern_x + 1
        x_current = ct[indice_pattern_x]
    return candidates_list

def slim(db,max_iter):
    """
    Parameters
    ----------

    """
    database = DatabaseSlim(db)
    standard_code_table = database.make_standard_code_table()
    code_table = standard_code_table.copy()
    ct_has_improved = True
    #ct_pattern_set = code_table.get_pattern_list
    iter = 0
    while ct_has_improved != False & iter < max_iter:
        ct_has_improved = False
	# ------------- Mine candidates -------------#
        candidate_list=[]
        candidate_list = generate_candidat(code_table)
	# ------------- Improve CT -------------#
        indice_candidat = 0
            # on parcours la liste de candidats tant que l'on a pas améliorer CT ou qu'il reste des candidats non testés
        while (indice_candidat < len(candidate_list)) and ct_has_improved==False:
            print(indice_candidat < len(candidate_list))
            print((indice_candidat < len(candidate_list)) and (not ct_has_improved))
            candidate = candidate_list[indice_candidat]
            code_table_temp = code_table.copy()
            print("boucle")
            print(code_table_temp)
            code_table_temp.add(candidate, None)
            code_table = code_table_temp.best_code_table(code_table, db, standard_code_table)
            if code_table == code_table_temp:
                ct_has_improved = True
            else:
                ct_has_improved = False
            indice_candidat = indice_candidat+1 #remove plutot que compteur
        iter+=1
    return code_table
