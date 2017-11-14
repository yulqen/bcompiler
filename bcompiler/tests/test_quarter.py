import datetime

from ..core import Quarter


def test_existence():
    q = Quarter(1, 2017)
    assert q.start_date == datetime.date(2017, 4, 1)
    assert q.end_date == datetime.date(2017, 6, 30)
    q = Quarter(2, 2017)
    assert q.start_date == datetime.date(2017, 7, 1)
    assert q.end_date == datetime.date(2017, 9, 30)
