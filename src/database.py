# -*- coding: utf-8 -*-
"""
Database class

Created on Mon Feb 11 14:45:31 2019

@author: Josie Signe
"""
from src.CodeTable import CodeTable
from src.Pattern import *


class Database:
    """Database class

    Use derived classes?

    Parameters
    ----------
    trans_collection : object, optional (default=None)
        The base estimator from which the ensemble is built.

    Attributes
    ----------
    trans_collection_ : estimator
        The base estimator from which the ensemble is grown.
    """

    def __init__(self, int_data_list):
        self.data_collection = self.copy(int_data_list)
        self.index = 0
        self.db_card = len(self.data_collection)

    def make_standard_code_table(self):
        """Make and return the standard code table of the database."""
        sct = CodeTable()  # map pattern code
        # On ajoute les singletons de la base à la SCT
        for trans in self.data_collection:
            for item in trans:
                pattern = Pattern([item])
                sct.set(pattern)
            # puis calcul des codes de la sct
        return sct

    def __repr__(self):
        return repr(self.data_collection)

    def __len__(self):
        """Returns the number of transaction of the database."""
        return len(self.data_collection)

    def __getitem__(self, index_trans):
        """Returns the transaction at index_trans"""
        return self.data_collection[index_trans]

    def __iter__(self):
        """Returns iterator over estimators in the ensemble."""
        return iter(self.data_collection)

    def __next__(self):
        self.index += 1
        try:
            return self.data_collection[self.index - 1]
        except IndexError:
            self.index = 0
            raise StopIteration

    def get_support(self, pattern):
        support = 0
        for transaction in self.data_collection:
            if transaction >= pattern:
                support += 1
        return support

    def copy(self,list_int):
        res = []
        for element in list_int:
            tmp = []
            for sous_element in element:
                tmp += [sous_element]
            res += tmp
        return res
