import pytest
from src.Transaction import Transaction
from SLIM.PatternSlim import PatternSlim
from SLIM.CodeTableSlim import CodeTableSlim

t1 = Transaction([1, 2, 3])
t2 = Transaction([5, 8, 9])
t3 = Transaction([2])
p1 = PatternSlim(1)
p2 = PatternSlim(2)
p5 = PatternSlim(5)


@pytest.fixture
def ct():
    return CodeTableSlim()


@pytest.fixture
def ctadd():
    ct = CodeTableSlim()
    ct.add(p1, t1)
    ct.add(p2, t1)
    ct.add(p5, t2)
    ct.add(p2, t3)
    print(ct)
