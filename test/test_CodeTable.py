import pytest
from src.CodeTable import CodeTable
from src.Transaction import Transaction
from src.Pattern import Pattern

import math

t1 = Transaction([1, 2, 3])  # Change the transactions creation process using item_collection
t2 = Transaction([5, 8, 9])
t3 = Transaction([2])
t4 = Transaction([1, 2, 3, 4])
p1 = Pattern(t1)
p2 = Pattern(t2)
p3 = Pattern(t3)


@pytest.fixture
def ct():
    return CodeTable()


@pytest.fixture
def ct_full():
    ct = CodeTable()
    ct.add(p1)
    ct.add(p2)
    return ct


def test_contains(ct_full):
    assert p2 in ct_full.patternMap.keys()
    assert p3 not in ct_full.patternMap.keys()


def test_add_1(ct):
    t = Transaction([5, 2, 3])
    p = Pattern(t)
    ct.add(p)
    assert p in ct.patternMap.keys()
    assert ct.patternMap[p] == 0
    assert p.usage == 1
    assert p.support == 1  # maybe useless


def test_add_2(ct_full):
    ct_full.add(p1)  # add a pattern for the second time [1, 2, 3]
    assert p1 in ct_full.patternMap.keys()
    assert ct_full.patternMap[p1] == 1
    assert p1.usage == 2
    assert p1.support == 2  # maybe useless


def test_remove(ct_full):
    ct_full.remove(p1)
    assert p1 not in ct_full.patternMap.keys()


""""
def test_get(ct_full):
    assert ct_full.get(0) == p1  # first element
    assert ct_full.get(ct_full.__len__()) == p2  # TOCHECK : returns last element
    assert ct_full.get(5) == -1  # returns -1 if can't find any pattern for this index


def test_order_by_usage(ct_full):
    ct_full.add(p3)
    ct_full.add(p3)
    ct_full.add(p3)
    ct_full.order_by_usage()
    assert ct_full.get(0) == p3
"""


def test_order_by_standard_cover_order(ct_full):
    pass


def test_usage_sum(ct, ct_full):
    assert ct.usage_sum() == 0
    assert ct_full.usage_sum() == 2
    ct_full.add(p1)  # adding 1 usage for pattern p1
    assert ct_full.usage_sum() == 3
    ct_full.remove(p2)
    ct_full.remove(p1)
    assert ct_full.usage_sum() == 0


def test_calculate_code_length(ct_full):
    ct_full.calculate_code_length()
    assert ct_full.patternMap[p2] == (-math.log2(p2.usage/ct_full.usage_sum()))  # pattern in 1 transaction
    assert ct_full.patternMap[p1] == (-math.log2(p1.usage / ct_full.usage_sum()))  # pattern in 2 transactions
    assert ct_full.patternMap[p2] >= ct_full.patternMap[p1]  # logically p1's code is smaller than p2's code


def test_database_encoded_length(ct, ct_full):
    assert ct.database_encoded_length() == 0
    ct_full.add(p1)
    assert ct_full.database_encoded_length() == ((ct_full.patternMap[p1]*2) + (ct_full.patternMap[p2]*1))


def test_codetable_length(ct_full, ct, sct):  # TODO: Create Standard Code Table sct, wrong length numbers
    assert ct.codetable_length(sct) == 0  # empty CodeTable
    assert ct_full.codetable_length(sct) == 2
    ct_full.add(p1)
    assert ct_full.codetable_length(sct) == 2  # adding the same pattern is not changing the CodeTable length
    ct_full.add(p3)
    assert ct_full.codetable_length(sct) == 3  # adding a new pattern
    ct_full.remove(p1)
    assert ct_full.codetable_length(sct) == 2  # removing one pattern


def test_best_code_table(ct, ct_full, sct):  # TODO : to be completed with sct and with a second better example
    # data = Database()
    # assert ct_full.best_code_table(ct, data, sct) == ct_full  # simple example
    pass


def test_post_prune(ct):  # TODO
    pass


def test_copy(ct_full):  # TODO : to be completed
    ct_bis = ct_full.copy()
    assert type(ct_bis) == CodeTable
    assert p1 in ct_bis.patternMap.keys()
