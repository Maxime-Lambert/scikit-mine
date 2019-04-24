import pytest

from src.Pattern import Pattern
from src.Transaction import Transaction
from src.SQS_v2.Window import Window
from src.SQS_v2.Sequence import Sequence
from src.SQS_v2.SQS import SQS, Database


import math


def test_findWindow():
    p = Pattern([1,2])

    sqs = SQS(Database([[1,2,3,1,2,3,1,2,3]]))

    for w in sqs.find_windows(p):

        print(w.first)



    assert p.support == 1  # maybe useless


