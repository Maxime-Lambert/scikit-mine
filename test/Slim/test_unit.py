# -*- coding: utf-8 -*-
"""
Created on Tue Mar  5 17:25:04 2019

@author: Shito
"""

from src.SLIM import slimalgo
from src.SLIM.slimalgo import DatabaseSlim
from src.SLIM.slimalgo import PatternSlim
from src.SLIM.slimalgo import CodeTableSlim


def test_get_support():
    db = [[2, 1, 3, 4], [1, 2, 4], [1, 2, 4], [1, 2, 4],
          [2, 4], [2, 4], [1], [1], [3]]
    database = DatabaseSlim(db)
    a = database.get_support(PatternSlim(1))
    b = database.get_support(PatternSlim(2))
    c = database.get_support(PatternSlim(3))
    d = database.get_support(PatternSlim(4))
    assert a == 6
    assert b == 6
    assert c == 2
    assert d == 6
    
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


def test_cover2_default_sct():

    db = [[2, 1, 3, 4], [1, 2, 4], [1, 2, 4], [1, 2, 4],
          [2, 4], [2, 4], [1], [1], [3]]
    database = DatabaseSlim(db)
    print(database)
    standard_code_table = database.make_standard_code_table()
    standard_code_table.calcul_usage()
    code_table = standard_code_table.copy()
    candidate_list = slimalgo.generate_candidat(code_table, standard_code_table)
    candidate_list = sorted(candidate_list, key=lambda p: (p.usage),
                            reverse=True)
    code_table.add(candidate_list[0], None)
    print("CT")
    print(code_table)
    print(">>>>>>>>>>>>>>>>>>>>>>>>")
    code_table.calcul_usage()
    print(code_table)
    print("STANDARD")
    print(standard_code_table)
    for e in standard_code_table.patternMap.keys():
        print(e.usage_list)


test_get_support()
