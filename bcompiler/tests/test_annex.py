from openpyxl import load_workbook

from ..analysers.annex import run as annex_run


def test_annex(tmpdir, master):
    annex_run([str(tmpdir)], master)
    wb = load_workbook(tmpdir.join('PROJECT_PROGRAMME NAME 1_ANNEX.xlsx'))
    ws = wb.active
    assert ws['A1'].value == 'PROJECT/PROGRAMME NAME 1'
