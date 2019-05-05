# -*- coding: utf-8 -*-

import time
from src.SLIM.slimalgo import slim
from src.DiffNorm.DiffNorm1 import DiffNorm1
from src.Files import Files
from src.SQS_v2.Database import Database
from src.SQS_v2.SQS import SQS
import os


def slim_iris():
    x = time.time()
    code_table = slim("iris", 1000)
    print("Result found in "+str(time.time() - x)+" seconds : \n")
    print("open res file to check results")


def slim_ticket():
    x = time.time()
    code_table = slim("tickets", 1000)
    print("Result found in "+str(time.time() - x)+" seconds : \n")
    print("open res file to check results")


def diffnorm():
    if __name__ == '__main__':
        d = DiffNorm1("all_demo", "u_demo")
        d.run()


def sqs():
    if __name__ == "__main__":
        absolute_path = os.path.dirname(os.path.abspath(__file__))
        file_path = absolute_path + "\simpleS"
        my_file = Files(file_path)
        print(my_file.list_string)
        database = Database(my_file.list_int)
        s = SQS(database)
        s.search()


# slim_iris()
# slim_ticket()
diffnorm()
# sqs()

