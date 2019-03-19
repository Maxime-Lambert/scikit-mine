# -*- coding: utf-8 -*-
"""
Created on Tue Mar  5 17:25:04 2019

@author: Shito
"""

from src.SLIM import slimalgo
from src.SLIM.slimalgo import DatabaseSlim
from src.SLIM.slimalgo import PatternSlim
from src.SLIM.slimalgo import CodeTableSlim


def test_generate_candidate_sct():

    db = [[2, 1, 3, 4], [1, 2, 4], [1, 2, 4], [1, 2, 4],
          [2, 4], [2, 4], [1], [1], [3]]
    database = DatabaseSlim(db)
    print(database)
    standard_code_table = database.make_standard_code_table()
    # code_table = standard_code_table.copy()
    res = slimalgo.generate_candidat(standard_code_table,standard_code_table)
    print(res)
    
def test_cover_default_sct():
    
    db = [[2, 1, 3, 4], [1, 2, 4], [1, 2, 4], [1, 2, 4],
          [2, 4], [2, 4], [1], [1], [3]]
    database = DatabaseSlim(db)
    print(database)
    standard_code_table = database.make_standard_code_table()
    standard_code_table.calcul_usage(database)
    print(standard_code_table)
    for e in standard_code_table.patternMap.keys():
        print(e.usagelist)

test_cover_default_sct()
