# -*- coding: utf-8 -*-
"""
Created on Tue Mar  5 17:25:04 2019

@author: Shito
"""

from src.SLIM import slimalgo
from src.SLIM.slimalgo import DatabaseSlim


def test_generate_candidate_default_sct():

    db = [[2, 1, 3, 4], [1, 2, 4], [1, 2, 4], [1, 2, 4],
          [2, 4], [2, 4], [1], [1], [3]]
    database = DatabaseSlim(db)
    standard_code_table = database.make_standard_code_table()
    print(standard_code_table)
    res = slimalgo.generate_candidat(standard_code_table)


test_generate_candidate_default_sct()