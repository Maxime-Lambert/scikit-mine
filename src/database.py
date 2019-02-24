# -*- coding: utf-8 -*-
"""
Database class

Created on Mon Feb 11 14:45:31 2019

@author: Josie Signe
"""
from CodeTable import CodeTable
from Pattern import Pattern


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

    def __init__(self, int_trans_list):
        self.data_collection_ = int_trans_list.copy
        self.index = 0
        self.db_card = len(self.data_collection)

    def make_standard_code_table(self):
        """Make and return the standard code table of the database."""
        sct = CodeTable()  # map pattern code
        # On ajoute les singletons de la base à la SCT
        for trans in self.trans_collection_:
            for item in trans:
                pattern = Pattern([item])
                sct.set(pattern)
            # puis calcul des codes de la sct
        return sct

    def __repr__(self):
        return repr(self.trans_collection_)

    def __len__(self):
        """Returns the number of transaction of the database."""
        return len(self.trans_collection)

    def __getitem__(self, index_trans):
        """Returns the transaction at index_trans"""
        return self.trans_collection[index_trans]

    def __iter__(self):
        """Returns iterator over estimators in the ensemble."""
        return iter(self.trans_collection)

    def __next__(self):
        self.index += 1
        try:
            return self.transactions[self.index - 1]
        except IndexError:
            self.index = 0
            raise StopIteration

    def get_support(self, pattern):
        support = 0
        for transaction in self.transactions:
            if transaction >= pattern:
                support += 1
        return support
