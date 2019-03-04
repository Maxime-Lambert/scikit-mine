import pytest
from src.DiffNorm.DiffNorm import DiffNorm


def test_iteration0_empty():
    b = True
    try:
        d = DiffNorm("empty_all", "empty_u")
        d.init_alphabet()
        d.init_all_ct_i()
        d.generate_candidates()
    except Exception as e:  # to cover the max number of errors we can, other option : list of errors
        b = False
    assert b is True  # to check if DiffNorm hasn't failed


def test_iteration0_simple():
    b = True
    try:
        d = DiffNorm("all", "u")  # TEMPORARY
        d.init_alphabet()
        d.init_all_ct_i()
        d.generate_candidates()
    except Exception:
        b = False
    assert b is True


def test_iteration0_normal():
    b = True
    try:
        d = DiffNorm("normal_all", "normal_u")
        d.init_alphabet()
        d.init_all_ct_i()
        d.generate_candidates()
    except Exception:
        b = False
    assert b is True

