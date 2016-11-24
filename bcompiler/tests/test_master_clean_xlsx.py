"""
After data from the BICC forms is migrated into a compiled_master.xlsx file,
we need to avoid having to re-save this file as csv and then manually removing
all in-cell commas, so that we can create a transposed_master elsewhere in the
application, because that's a major pain in the backside. So what we're going
here is performing clean-up functions on the resulting compiled_master.xlsx
file that is created straight after the BICC forms compilation. That will then
absolve us from all hassle.
"""
import pytest

from openpyxl import Workbook


@pytest.fixture
def dirty_master():
    inc = 0
    wb = Workbook()
    ws = wb.active
    top_row = ws['A1':'A5']
    second_row = ws['B1':'B5']
    third_row = ws['C1':'C5']
    for cell in top_row:
        cell[0].value = "Header {}".format(inc)
        inc += 1
    inc = 0
    for cell in second_row:
        cell[0].value = "Data {}".format(inc)
        inc += 1
    # now we're going to put some horrible commas in these cells
    for cell in third_row:
        cell[0].value = "Garbage data, with commas!"
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
    assert ',' in ws['C1'].value
    assert 'X' not in ws['C1'].value
    assert 'Garbage' in ws['C1'].value
