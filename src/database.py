# -*- coding: utf-8 -*-
"""
Database class

Created on Mon Feb 11 14:45:31 2019

@author: Josie Signe
"""
from src.CodeTable import *
from src.Pattern import Pattern
# from src.item_collection import ItemCollection
from src.Transaction import Transaction


class Database:
    """Database class

    Parameters
    ----------
    int_data_collection : list of integer list
    elements to put in the database

    Attributes
    ----------
    data_list: ItemCollection list
    """
    data_collection = []

    def __init__(self, data_list):
        for item_list in data_list:
            transaction = Transaction(item_list)
            self.data_collection.append(transaction)
        self.index = 0
        self.db_card = len(data_list)

    def make_standard_code_table(self):
        """Make and return the standard code table of the database."""
        sct = CodeTable()  # map pattern code
        # On ajoute les singletons de la base à la SCT
        for trans in self.data_collection:
            for item in trans:
                pattern = Pattern([item])
                sct.add(pattern, trans)
        return sct

    def __repr__(self):
        return repr(self.data_collection)

    def __len__(self):
        """Returns the number of database's elements."""
        return len(self.data_collection)

    def __getitem__(self, index_elem):
        """Returns the element at index_elem"""
        return self.data_collection[index_elem]

    def __iter__(self):
        """Returns iterator over data_list."""
        return iter(self.data_collection)
