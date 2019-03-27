from src.Files import Files
from src.Database import Database
from src.SQS import SQS

if __name__ == "__main__":
    my_file = Files("monfichier")
    database = Database(my_file.list_int)
    sqs = SQS(database)
    sqs.search()
    print(sqs.alignement)