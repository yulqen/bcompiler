from ..core import Row
from openpyxl import Workbook, load_workbook


def test_for_basic_row_object_given_list(tmpdir):
    values_l = ['Test Value A1', 'Test Value B1', 'Test Value C1']
    wb = Workbook()
    ws = wb.active
    r = Row(1, 1, values_l)
    r.bind(ws)
    wb.save(tmpdir.join('test_row_object.xlsx'))
    loaded_wb = load_workbook(tmpdir.join('test_row_object.xlsx'))
    ws = loaded_wb.active
    assert ws['A1'].value == 'Test Value A1'
