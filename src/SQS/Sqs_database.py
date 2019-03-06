from src.database import *
from src.SQS.Sequence import *


class SqsDatabase(Database):

    data_collection = []

    def __init__(self, data_list):
        for data in data_list:
            sequence = Sequence(data)
            self.data_collection.append(sequence)

