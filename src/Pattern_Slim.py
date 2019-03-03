# -*- coding: utf-8 -*-

from src.Transaction import *
from src.Pattern import *


class Pattern_Slim(Pattern):

    """
        A Pattern_Slim is consisted of a Collection of Items.
        It has an usage (double) : the occurrence of that pattern in the
        cover of the Database
        It has a support (double) : the total occurrence of that pattern
        in the Database
        It has an usageList (set(Transaction)) : all the transactions
        containing the pattern
    """

    def __init__(self, item, transaction):
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
        self.elements = {item}
        self.usage_list = {transaction}
        return self

    def union(self, pattern):
        """
            Merged two patterns into one bigger
            :param pattern: the pattern you want to merge self with
            :type pattern: Pattern_Slim
            :return: The merged pattern
            :rtype: Pattern_Slim
        """
        p = Pattern_Slim(self.elements & pattern.elements,
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
        self.usage_list.add(transaction)
        return self
