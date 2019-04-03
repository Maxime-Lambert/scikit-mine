from src.Files import Files
from src.SQS_v2.Database import Database
from src.SQS_v2.CodeTable import CodeTable
from src.SQS_v2.SQS import SQS
import os

if __name__ == "__main__":
    absolute_path = os.path.dirname(os.path.abspath(__file__))
    file_path = absolute_path + "/../../test/data/SQS/monfichier"
    my_file = Files(file_path)
    database = Database(my_file.list_int)
    print(database.list_sequence)
    ct = database.make_standard_code_table()
    """ print(ct.patternMap)
    print(ct)
    sqs = SQS(database)
    sqs.search()
    print(sqs.alignement)"""
