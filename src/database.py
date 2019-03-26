# -*- coding: utf-8 -*-
"""
Database class

Created on Mon Feb 11 14:45:31 2019

@author: Josie Signe
"""
from src.CodeTable import CodeTable
from src.Pattern import Pattern
# from src.item_collection import ItemCollection
from src.Transaction import Transaction


class Database:
    """
        Get a model of the data. The model is construct from
        frequent itemset following MDL principle.

        :param filename: name of data file to treat
        :param max_iter: number of iteration maximum
        :return: The CodeTableSlim as a model of data
        :rtype: CodeTableSlim
    """

    def __init__(self, data_list):
        self.data_collection = []
        for item_list in data_list:
            transaction = Transaction(item_list)
            self.data_collection.append(transaction)
        self.index = 0
        self.db_card = len(data_list)

    def make_standard_code_table(self):
        """
            Make the standard code table of the database, i.e. Code table
            composed of singleton item of database

            :return: The Standard code table
            :rtype: CodeTableSlim
        """
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
