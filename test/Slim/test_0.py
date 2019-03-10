from src.Files import Files
from src.database import Database
from src.SLIM import slimalgo

file_reader = Files("example_slim")
database = Database(file_reader.list_int)


def t1():
    expect = "sct"
    res_df = slimalgo.slim(database, 0)
    assert res_df.equals(expect)


def t2():
    slimalgo.slim(database, 1)


def t3():
    expect = "expected_example_slim"
    res_df = slimalgo.slim(database, 1)
    assert res_df.equals(expect)
