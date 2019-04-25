import pytest

from src.Pattern import Pattern
from src.Transaction import Transaction
from src.SQS_v2.Window import Window
from src.SQS_v2.Sequence import Sequence
from src.SQS_v2.SQS import SQS, Database

import math


def test_find_window_simple():
    p = Pattern([1, 2])

    sqs = SQS(Database([[1, 2, 3, 1, 2, 3, 1, 2, 3]]))

    list_window = [Window(p, 0, 1, 0), Window(p, 3, 4, 0), Window(p, 6, 7, 0)]

    assert list_window == sqs.find_windows(p)


def test_find_window_repetition():
    p = Pattern([1, 1])

    sqs = SQS(Database([[1, 1, 1, 2, 1, 1, 1, 1]]))
    list_window = [Window(p, 0, 1, 0), Window(p, 4, 5, 0), Window(p, 6, 7, 0)]

    assert list_window == sqs.find_windows(p)


def test_find_window_long():
    p = Pattern([1, 2,3,4,3,2,1])

    sqs = SQS(Database([[1,2,3,1,2,3,1,2,3,4,3,2,1,2,3,4,3,2,1,1,2,3,4,5,3,2,1]]))
    list_window = []
    list_window.append(Window(p, 6, 12, 0))

    for w in sqs.find_windows(p):
        print(w.first)

    assert list_window == sqs.find_windows(p)

def test_find_window_4():
    p = Pattern([1, 1, 2])
    sqs = SQS(Database([[1, 1,1,2]]))
    for w in sqs.find_windows(p):
        print(w.first)