# -*- coding: utf-8 -*-
"""
Created on Sun Mar  3 19:14:36 2019

@author: Shito
"""

from slimalgo import slim

db = [[2, 1, 3, 4], [1, 2, 4], [1, 2, 4], [1, 2, 4],
      [2, 4], [2, 4], [1], [1], [3]]

res = slim(db, 0)

res.print_res()
