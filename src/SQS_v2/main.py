from src.Files import Files
from src.SQS_v2.Database import Database
from src.SQS_v2.SQS import SQS
import time
import os

if __name__ == "__main__":
    x = time.time()
    sqs = SQS("fichier2")
    sqs.run()
    print(sqs.codetable)
    print("result at " + str(time.time() - x))

