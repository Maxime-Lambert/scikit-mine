import unittest

from .fichier import *
from .database import *
from sqs_search import *

class MyTest(unittest.TestCase):
    
    def test_sequence_windows(self):
        test = [1]
        self.assertEquals(test, build_window(test))
        self.assertEquals([1], build_window(test))
        
    def test_sequence_search(self):
        test = [[1]]
        self.assertEquals(test, sqs_search(test))
        self.assertEquals([1], sqs_search())
        
        
if __name__ == '__main__':
    unittest.main()