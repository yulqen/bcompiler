import datetime

import pytest

from ..core import Quarter


def test_existence():
    q = Quarter(1, 2017)
    assert q.start_date == datetime.date(2017, 4, 1)
    assert q.end_date == datetime.date(2017, 6, 30)
    q = Quarter(2, 2017)
    assert q.start_date == datetime.date(2017, 7, 1)
    assert q.end_date == datetime.date(2017, 9, 30)


def test_errors():
    with pytest.raises(ValueError) as excinfo:
        Quarter(5, 2017)
    assert "A quarter must be either 1, 2, 3 or 4" in str(excinfo.value)

    with pytest.raises(ValueError) as excinfo:
        Quarter(3, 1921)
    assert "Year must be between 1950 and 2100 - surely that will do?" in str(excinfo.value)

    with pytest.raises(ValueError) as excinfo:
        Quarter("3", 2016)
    assert "A quarter must be either 1, 2, 3 or 4" in str(excinfo.value)

    with pytest.raises(ValueError) as excinfo:
        Quarter(3, "1921")
    assert "Year must be between 1950 and 2100 - surely that will do?" in str(excinfo.value)
