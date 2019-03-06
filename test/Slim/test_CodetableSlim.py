import pytest
from src.Transaction import Transaction
from src.SLIM.slimalgo import PatternSlim
from src.SLIM.slimalgo import CodeTableSlim

t1 = Transaction([1, 2, 3])
t2 = Transaction([5, 8, 9])
t3 = Transaction([2])
p1 = PatternSlim(1)
p2 = PatternSlim(2)
p3 = PatternSlim(3)
p5 = PatternSlim(5)
p8 = PatternSlim(8)
p9 = PatternSlim(9)


@pytest.fixture
def ct():
    return CodeTableSlim()


@pytest.fixture
def ctadd():
    ct = CodeTableSlim()
    ct.add(p1, t1)
    ct.add(p2, t1)
    ct.add(p3, t1)
    ct.add(p5, t2)
    ct.add(p8, t2)
    ct.add(p9, t2)
    ct.add(p2, t3)
    print(ct)


ctadd()
