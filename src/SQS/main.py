from src.Files import Files
from src.SQS.Sqs_database import SqsDatabase
from src.SQS.Sequence import Sequence
from src.SQS.sqs_v2 import SQS
import os

if __name__ == '__main__':
    absolute_path = os.path.dirname(os.path.abspath(__file__))
    file_path = absolute_path + "/../../test/data/SQS/monfichier"
    test = [[1, 2, 3, 4, 5, 6, 7], [8, 2, 4, 6]]
    list_seq = []
    for it in test:
        list_seq.append(Sequence(it))
    monfichier = Files(file_path)
    database = SqsDatabase(monfichier.list_int)
    sqs = SQS(database, list_seq)
    sqs.run()
