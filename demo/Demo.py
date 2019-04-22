# -*- coding: utf-8 -*-

import time
from src.SLIM.slimalgo import slim


def slim_iris():
    x = time.time()
    code_table = slim("iris", 1000)
    print("Result found in "+str(time.time() - x)+" seconds : \n")
    print(code_table)


def slim_ticket():
    x = time.time()
    code_table = slim("tickets", 1000)
    print("Result found in "+str(time.time() - x)+" seconds : \n")
    print(code_table)


# slim_iris()
# slim_ticket()
