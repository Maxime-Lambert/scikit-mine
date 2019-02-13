import unittest

from sqs_search import *

class MyTest(unittest.TestCase):
    
    def test_sequence_windows(self):
        test = [1]
        mongo = "mongo"
        self.assertEquals(test, build_window(test))
        self.assertEquals([1], build_window(test))
        with self.assertRaises(TypeError):
            result = build_window(mongo)

        
    def test_sequence_search(self):
        test = [[1]]
        bongo = "bongo"
        self.assertEquals(test, sqs_search(test))
        self.assertEquals([1], sqs_search())
        with self.assertRaises(TypeError):
            result = sqs_search(bongo)

        
if __name__ == '__main__':
    unittest.main()