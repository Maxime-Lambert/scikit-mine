import unittest

from src.SQS.sqs_search import *
from src.Files import *
from src.database import *


class MyTest(unittest.TestCase):

    def test_sequence_windows(self):
        test = [1]
        bingo = "bingo"
        self.assertEquals(test, build_window(test))
        self.assertEquals([1], build_window(test))
        self.assertEquals([1], build_window([1, 1, 1]))
        with self.assertRaises(TypeError):
            result = build_window(bingo)

    def test_sequence_search(self):
        test = [[1]]
        bango = "bango"
        self.assertEquals([1], sqs_search(test))
        self.assertEquals([1], sqs_search([[1]]))
        with self.assertRaises(TypeError):
            result = sqs_search(bango)

    def test_sequence_estimae(self):
        test = [1]
        bongo = "bongo"

    def test_sequence_prune(self):
        test = [1]
        congo = "congo"

    def test_yvanresults(self):
        enter = Files("testenter")
        database1 = Database(enter.list_int)
        result = sqs_search(database1)
        exits = Files("testexit")
        database2 = Database(exits.list_int)
        self.assertEquals(result, database2)


if __name__ == '__main__':
    unittest.main()
