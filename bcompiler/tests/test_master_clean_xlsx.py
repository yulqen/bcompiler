import pytest

from openpyxl import Workbook


@pytest.fixture
def dirty_master():
    inc = 0
    wb = Workbook()
    ws = wb.active
    top_row = ws['A1':'A5']
    second_row = ws['B1':'B5']
    for cell in top_row:
        cell[0].value = "Header {}".format(inc)
        inc += 1
    inc = 0
    for cell in second_row:
        cell[0].value = "Data {}".format(inc)
        inc += 1
    return wb


def test_phantom_wb(dirty_master):
    """
    Just test that we are creating an openpyxl object for testing. Thanks
    pytest!
    """
    ws = dirty_master.active
    assert ws['A1'].value == 'Header 0'
    assert ws['A2'].value == 'Header 1'
    assert ws['B1'].value == 'Data 0'
