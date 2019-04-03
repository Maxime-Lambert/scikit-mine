from typing import re

from src.Transaction import *


class Pattern:
    """
        A pattern is consisted of a Collection of Transactions.
        It also has an usage, a double, the occurrence of that pattern in the Database;
        a support, a double, being the total occurrence of that pattern,
         even if it is part of a bigger pattern.
         
    """

    def __init__(self, transaction):
        """
            Create a Pattern with a given transaction and an usage/support of 0
            Has an index 0 for easier time with iterators
        """
        self.usage = 1
        self.support = 1
        self.elements = transaction
        self.index = 0

    def __iter__(self):
        """Returns iterator over the transactions in the pattern."""
        return self.elements

    def __next__(self):
        """
            Return the next element of the collection
            :return: A transaction at index-position
            :rtype: Transaction
        """
        try:
            result = self.elements[self.index].upper()
        except IndexError:
            raise StopIteration
        self.index += 1
        return result

    def __repr__(self):
        """
            Return a String representation of the pattern
            :return: A String representing the Pattern
            :rtype: String
        """
        res = "["
        res += self.elements.toString()
        res += "]"
        return res

    def __eq__(self, pattern):
        """
            Return a boolean to compare an equality between two patterns
            :return: The result of the comparison
            :rtype: Boolean
        """
        return self.elements.__eq__(pattern.elements)

    def __str__(self):
        """
            Return a String representation of the transactions inside the pattern
            :return: A String representing the transactions
            :rtype: String
        """
        res = ""
        for transaction in self.elements:
            res += str(transaction)
        return res

    def __hash__(self):
        """
            Return the hash value of the usage
            :return: An hash value
            :rtype: Integer
        """
        return hash(self.usage)

    def union(self, pattern):
        """
            Merged two patterns into one bigger
            :return: The merged pattern
            :rtype: Pattern
        """
        res = self.elements + pattern.elements
        transaction = Transaction(sorted(list(set(res))))
        return Pattern(transaction)

    def add_usage(self):
        """
            Add an usage of that pattern
            :return: void
        """
        self.usage += 1

    def add_support(self):
        """
            Add a support of that pattern
            :return: void
        """
        self.support += 1

    def get_elements(self):
        return self.elements
