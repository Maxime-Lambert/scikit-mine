# -*- coding: utf-8 -*-
"""
Database class

Created on Mon Feb 11 14:45:31 2019

@author: Josie Signe
"""
from codetable import CodeTable
from patern import Pattern


class Database:

    def __init__(self, int_trans_list):
        self.trans_collection = int_trans_list

    def standard_code_table(self):
        sct = CodeTable()  # map pattern code
        # On ajoute les singletons de la base à la SCT
        for trans in self.trans_collection:
            # les trans sont des ensemble d'int
            for item in trans:
                pattern = Pattern([item])
                if not sct.contains(pattern):
                    sct.add(pattern)
                pattern.usage = pattern.usage + 1  # ne fonctionne pas
                print(pattern.usage)
            # puis calcul des codes de la sct
        return sct

    def __repr__(self):
        return repr(self.trans_collection)

    def __len__(self):
        return len(self.trans_collection)

    def __getitem__(self, transaction):
        return self.trans_collection[transaction]
