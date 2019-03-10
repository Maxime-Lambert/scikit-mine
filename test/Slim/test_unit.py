# -*- coding: utf-8 -*-
"""
Created on Tue Mar  5 17:25:04 2019

@author: Shito
"""

from src.SLIM import slimalgo
from src.SLIM.slimalgo import DatabaseSlim
from src.SLIM.slimalgo import PatternSlim


def test_generate_candidate_default_sct():

    db = [[2, 1, 3, 4], [1, 2, 4], [1, 2, 4], [1, 2, 4],
          [2, 4], [2, 4], [1], [1], [3]]
    database = DatabaseSlim(db)
    standard_code_table = database.make_standard_code_table()
    # code_table = standard_code_table.copy()
    res = slimalgo.generate_candidat(standard_code_table)
    p = PatternSlim([1,2])
    p2  = PatternSlim([2,4])
    expected = []
    expected.append(p)
    expected.append(p2)
    print(res == expected)
    for p in expected:
        print(p)

test_generate_candidate_default_sct()
