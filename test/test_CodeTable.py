import pytest
from src.CodeTable import CodeTable
from src.Transaction import Transaction
from src.Pattern import Pattern
import math

t1 = Transaction([1, 2, 3])
t2 = Transaction([5, 8, 9])
t3 = Transaction([2])
p1 = Pattern(t1)
p2 = Pattern(t2)
p3 = Pattern(t3)


@pytest.fixture
def ct():
    return CodeTable()


@pytest.fixture
def ct_full():
    ct = CodeTable()
    ct.set(p1)
    ct.set(p2)
    return ct


def test_set(ct):
    t = Transaction([1, 2, 3])
    p = Pattern(t)
    ct.set(p)
    # assert ct.patternMap[p] == 1
    # assert p.usage == 1
    # assert ct.contains(p)
    pass


def test_get(ct_full):
    assert ct_full.get(1) == p2


def test_remove(ct_full):
    ct_full.remove(p1)
    assert not ct_full.contains(p1)


def test_contains(ct_full):
    pass
    # assert p1 in ct_full.patternMap.items()
    # assert p3 not in ct_full.patternMap.items()


def test_size(ct_full, ct):
    assert ct_full.size() == 2
    assert ct.size() == 0
    ct_full.set(p2)
    # assert ct_full.size() == 2
    pass


def test_usage_sum(ct_full, ct):
    assert ct_full.usageSum() == 2
    assert ct.usageSum() == 0
    ct_full.set(p2)
    assert ct_full.usageSum() == 3


def test_calculate_code(ct_full):
    ct_full.calculateCode()
    assert ct_full.patternMap[p2] == bytes(-math.log2(p2.usage/ct_full.usageSum()))  # TO CHECK


def test_database_encoded_length(ct):
    pass


def test_code_table_length(ct):
    pass


def test_compare_gain(ct):
    pass


def test_post_prune(ct):
    pass


def test_order_by_usage(ct):
    pass
