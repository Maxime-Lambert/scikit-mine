import pytest
from src.DiffNorm.DiffNorm import *


def test_iteration0():
    b = True
    try:
        d = DiffNorm("all_dbs_names", "empty_dbs_subsets")
    except Exception as ex:
        b = False
    assert b is True

