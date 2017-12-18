import datetime
from ..process.cleansers import Cleanser


def test_cleaning_dot_date():
    ds = "25.1.72"
    ds_double = "25.01.72"
    four_year = "25.01.1972"
    c = Cleanser(ds)
    c_double = Cleanser(ds_double)
    c_four = Cleanser(four_year)
    assert c.clean() == datetime.date(1972, 1, 25)
    assert c_double.clean() == datetime.date(1972, 1, 25)
    assert c_four.clean() == datetime.date(1972, 1, 25)


def test_cleaning_slash_date():
    ds = "25/1/72"
    ds_double = "25/01/72"
    four_year = "25/01/1972"
    c = Cleanser(ds)
    c_double = Cleanser(ds_double)
    c_four = Cleanser(four_year)
    assert c.clean() == datetime.date(1972, 1, 25)
    assert c_double.clean() == datetime.date(1972, 1, 25)
    assert c_four.clean() == datetime.date(1972, 1, 25)
