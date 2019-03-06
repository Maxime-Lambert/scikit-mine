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


test_iter0_default()
