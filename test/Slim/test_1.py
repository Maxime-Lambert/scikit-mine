# -*- coding: utf-8 -*-
"""
Created on Sun Mar  3 19:14:36 2019

@author: Shito
"""

from src.SLIM.slimalgo import slim


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
    res = slim(db, 10000)
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


test_itern_easy()
