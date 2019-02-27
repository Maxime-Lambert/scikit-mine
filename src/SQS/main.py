from src.Files import *
from src.database import *
from src.SQS.sqs_v2 import *

if __name__ == '__main__':
    print(len([[1, 2, 3], [4, 6]]))
    monfichier = Files("monfichier")
    print(len(monfichier.list_int))
    database = Database(monfichier.list_int)
    sqs = SQS(database, [1, 2, 3])
    sqs.run()
