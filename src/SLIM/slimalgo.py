#import numpy as np
#import scipy.sparse as sp
#from .Transaction import Transaction 
#from .codeTable import CodeTable
#from .database import Database

#v0 : helloworld?
#v1 : Pour une premiere version on peut zapper la comparaison des usages
#et tester toutes les combinaisons de candidats
# -*- coding: utf-8 -*-

from src.database import Database
from src.CodeTable import CodeTable
from src.Transaction import Transaction
from src.Pattern import Pattern
from src.Files import Files

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
    transactions = []

    def __init__(self, transaction_set):
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
                pattern = PatternSlim([item])
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
    elements = set()
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
        self.usage = 0
        self.support = 0
        self.elements = item.copy()
        self.usage_list = []

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
        p = PatternSlim(self.elements & pattern.elements,
                         self.usage_list | pattern.usage_list)
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
        self.usage_list.append(transaction)
        return self

    def __eq__(self, pattern):
         return self.elements==pattern.elements

    def __hash__(self):
        """
            Return the hash value of the usage
            :return: An hash value
            :rtype: Integer
        """
        return hash(self.usage)

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

    def patternset(self):
        return self.patternMap.keys()
        
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
                key.add_usagelist(transaction)
                b = True
        if not b:
            self.patternMap[pattern] = 0
            pattern.usage = 1
            pattern.support = 1
            pattern.usageList = transaction
       # return self.order_by_standard_cover_order()

    def order_by_usage(self):
        """
            Order the Codetable by its pattern's usage

            :return: The Codetable ordered by pattern's usage
            :rtype: Codetable
        """
        return sorted(self.patternMap, key=lambda p: p.usage, reverse=True)

def slim(db,max_iter):
    """
    Parameters
    ----------
    
    """
    database = DatabaseSlim(db)    
    standard_code_table = database.make_standard_code_table()
    code_table = standard_code_table
    ct_has_improved = True
    #ct_pattern_set = code_table.get_pattern_list
    iter = 0
    while ct_has_improved != False & iter < max_iter:
        #tri par usage de CT + liste de candidat
        candidates_list = [] #pattern list
        best_usage = 0
        ct_has_improved = False
        indice_pattern_x = 0
        x_current = code_table.get_pattern(indice_pattern_x) #attention si viiiiiide
	# ------------- Mine candidates -------------#
        while indice_pattern_x < code_table.size-1 & code_table.get(indice_pattern_x).usage>= best_usage:
            indice_pattern_y = indice_pattern_x + 1 #on ne prend que les patterns juste après x
            y_current = code_table.get_pattern(indice_pattern_y)
            while indice_pattern_y < code_table.size & y_current.usage <= best_usage: # ??
                y_current = code_table.get(indice_pattern_y) #indice dans un set?
                while best_usage < y_current.usage :
                    x_y_current = x_current.union(y_current)
                    if best_usage < x_y_current.usage: #si bon usage on le garde et maj best_usage
                        candidates_list.append(x_y_current)
                        best_usage = x_y_current.usage
                y_current = code_table.get_pattern(++indice_pattern_y)
            x_current = code_table.get_pattern(++indice_pattern_x) #on prend le premier pattern
	# ------------- Improve CT -------------#
        indice_candidat = 0
            # on parcours la liste de candidats tant que l'on a pas améliorer CT ou qu'il reste des candidats non testés
        while indice_candidat <= len(candidates_list) & ct_has_improved==False:
            candidate = candidates_list[indice_candidat] 
            code_table_temp = code_table.add_pattern(candidate)
            if code_table_temp.taille <= code_table.taille:
                code_table = code_table_temp.post_prune
                ct_has_improved = True
            else:
                indice_candidat = indice_candidat+1 #remove plutot que compteur
        iter+=1
    return code_table