# -*- coding: utf-8 -*-

import time
from src.SLIM.slimalgo import slim
from src.DiffNorm.DiffNorm1 import DiffNorm1


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


def diffnorm():
    if __name__ == '__main__':
        d = DiffNorm1("chess_demo_all", "chess_demo_u")
        #  d = DiffNorm1("gen_all", "gen_u")
        d.run()


# slim_iris()
# slim_ticket()
diffnorm()
