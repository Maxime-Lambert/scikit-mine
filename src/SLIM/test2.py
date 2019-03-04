# -*- coding: utf-8 -*-
"""
Created on Sun Mar  3 19:14:36 2019

@author: Shito
"""


from slimalgo import slim
db = [[1, 2, 3, 4], [1, 2, 3], [1, 2, 3], [1, 2, 3],
      [2, 3], [2, 3], [1], [1], [4]]
res = slim(db, 0)

for k, v in res.patternMap.items():
    print(k)
