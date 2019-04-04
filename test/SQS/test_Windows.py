import pytest

from src.Pattern import Pattern
from src.Transaction import Transaction
from src.SQS_v2.Window import Window
from src.SQS_v2.Sequence import Sequence
from src.SQS_v2.SQS import SQS, Database


import math


def test_findWindow():
    p = Pattern([3,2])

    sqs = SQS(Database([[5, 2, 3, 5, 2, 3, 5, 2, 3, 5, 3, 2]]))

    w = sqs.find_windows(p)
    print(w)


    assert p.support == 1  # maybe useless


