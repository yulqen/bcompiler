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
import re

from openpyxl import Workbook, load_workbook
from bcompiler.cleansers import clean_master


@pytest.fixture
def dirty_master():
    inc = 0
    wb = Workbook()
    ws = wb.active
    top_row = ws['A1':'E1']
    second_row = ws['A2':'E2']
    third_row = ws['A3':'E3']
    fourth_row = ws['A4':'E4']
    fifth_row = ws['A5':'E5']
    for cell in top_row[0]:
        cell.value = "Header {}".format(inc)
        inc += 1
    inc = 0
    for cell in second_row[0]:
        cell.value = "Data {}".format(inc)
        inc += 1
    # now we're going to put some horrible commas in these cells
    for cell in third_row[0]:
        cell.value = "Garbage data, with commas!"
    for cell in fourth_row[0]:
        cell.value = "Garbage data with\nnewlines!"
    for cell in fifth_row[0]:
        cell.value = "'Apostrophe! The pernicious apostrophe."
    ws['A6'].value = '20/1/75'
    ws['B6'].value = '21/10/16'
    ws['C6'].value = '2/1/2016'
    ws['D6'].value = '8/7/2220'
    ws['E6'].value = '18/7/20'
    return wb


def test_write_wb(dirty_master):
    dirty_master.save('/tmp/dirty_master.xlsx')


def test_phantom_wb(dirty_master):
    """
    Just test that we are creating an openpyxl object for testing. Thanks
    pytest!
    """
    ws = dirty_master.active
    assert ws['A1'].value == 'Header 0'
    assert ws['B1'].value == 'Header 1'
    assert ws['C1'].value == 'Header 2'


def test_presence_of_garbage(dirty_master):
    ws = dirty_master.active
    assert ',' in ws['C3'].value
    assert 'X' not in ws['C3'].value
    assert 'Garbage' in ws['C3'].value
    assert '\n' in ws['A4'].value
    assert 'with\n' in ws['A4'].value


def test_clean_master(dirty_master):
    # we get this from the fixture: the auto-gen workbook
    dirty_ws = dirty_master.active
    # we need to pass the path of the workbook to kill_commas()
    # this is simulated, because it doesn't have a path as it was
    # generated in the fixture
    path = '/tmp/dirty_master.xlsx'
    # when clean_master() runs, it outputs the workbook it is given
    # with '_cleaned' appended
    c_path = '/tmp/dirty_master_cleaned.xlsx'
    # give it the openpyxl wb object and give it the sheet and the path
    # of the openpyxl object
    clean_master(dirty_master, dirty_ws.title, path)
    # now clean_master() is done, we expect to find a cleaned xlsx file
    cleaned_wb = load_workbook(c_path)
    cleaned_ws = cleaned_wb.active
    assert ',' not in cleaned_ws['C3'].value
    assert cleaned_ws['C3'].value == 'Garbage data with commas!'
    assert '\n' not in cleaned_ws['A4'].value
    assert cleaned_ws['A4'].value == "Garbage data with | newlines!"
    assert cleaned_ws['A5'].value == "Apostrophe! The pernicious apostrophe."


def test_for_dates(dirty_master):
    date_regex = re.compile("^\d{1,2}(/|-)(\d{1,2})(/|-)\d{2,4}")
    dirty_ws = dirty_master.active
    path = '/tmp/dirty_master.xlsx'
    c_path = '/tmp/dirty_master_cleaned.xlsx'
    clean_master(dirty_master, dirty_ws.title, path)
    cleaned_wb = load_workbook(c_path)
    cleaned_ws = cleaned_wb.active
    assert re.match(date_regex, cleaned_ws['A6'].value)
