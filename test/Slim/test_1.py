# -*- coding: utf-8 -*-
"""
Created on Sun Mar  3 19:14:36 2019

@author: Shito
"""

from src.SLIM.slimalgo import slim
from src.Files import Files
from src.SLIM.slimalgo import DatabaseSlim


def test_iter0_file():

    file = Files("iris")
    database = DatabaseSlim(file.list_int)
    expected = database.make_standard_code_table()
    res = slim("iris", 0)
    print(res)
    assert res == expected


def test_iter1_file():
    file = Files("iris")
    database = DatabaseSlim(file.list_int)
    sct = database.make_standard_code_table()
    Files.to_file(sct, "expected_iris_sct")
    res = slim("iris", 1)
    Files.to_file(res, "res_test_iter1_iris")
    print(res)


def test_iter1_file_correct():
    file = Files("iris")
    database = DatabaseSlim(file.list_int)
    sct = database.make_standard_code_table()
    res = slim("iris", 1)
    print(res)


def test_itern_file_correct():
    res = slim("iris", 10000)
    print(res)


def test_itern_file():
    res = slim("iris", 100)
    Files.to_file(res, "res_test_itern_iris")
    codetableslim.to_code_table_slim("res_test_itern_iris",)


def test_iter0_empty():
    db = []
    res = slim(db, 0)
    print(res)


def test_iter0_default():
    db = [[2, 1, 3, 4], [1, 2, 4], [1, 2, 4], [1, 2, 4],
          [2, 4], [2, 4], [1], [1], [3]]
    res = slim(db, 0)
    print(res)


def test_iter1_empty():
    db = []
    res = slim(db, 1)
    print(res)


def test_iter1_default():

    db = [[2, 1, 3, 4], [1, 2, 4], [1, 2, 4], [1, 2, 4],
          [2, 4], [2, 4], [1], [1], [3]]
    res = slim(db, 1)
    print(res)


def test_itern_nofail():
    db = []
    res = slim(db, 100)
    assert True is True


def test_itern_easy():
    db = [[1, 2, 3, 4], [1, 2, 3], [1, 2, 3], [1, 2, 3], [1, 2, 3],
          [1, 2, 3], [1, 2, 3], [2, 3], [4, 1], [4, 1], [4, 1], [4, 1], [4]]
    res = slim(db, 10000)
    print(res)


def test_itern_hard():
    # cette base de donnée doit être une base de donnée officielle
    # il faut ensuite comparer les résultats avec le SLIM officiel
    db = []
    res = slim(db, 10000)
    print(res)


test_itern_file_correct()
