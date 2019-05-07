from src.Files import Files
from src.SQS_v2.Database import Database
from src.SQS_v2.SQS import SQS
import os

if __name__ == "__main__":
    absolute_path = os.path.dirname(os.path.abspath(__file__))
    file_path = absolute_path + "/../../test/data/SQS/fichier2"
    my_file = Files(file_path)
    # print(my_file.list_string)
    database = Database(my_file.list_int)
    ct = database.make_standard_code_table()
    print(ct)
    sqs = SQS(database)
    sqs.search()
    print(sqs.codetable)
