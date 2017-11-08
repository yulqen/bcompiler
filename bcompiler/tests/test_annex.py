from openpyxl import load_workbook

from ..analysers.annex import run as annex_run


def test_annex_title(tmpdir, master):
    annex_run([str(tmpdir)], master)
    wb = load_workbook(tmpdir.join('PROJECT_PROGRAMME NAME 1_ANNEX.xlsx'))
    ws = wb.active
    assert ws['A1'].value == 'PROJECT/PROGRAMME NAME 1'


def test_pound_sign(tmpdir, master):
    annex_run([str(tmpdir)], master)
    wb = load_workbook(tmpdir.join('PROJECT_PROGRAMME NAME 1_ANNEX.xlsx'))
    ws = wb.active
    assert ws['A5'].value == 'WLC(£m):'


def test_b5_one_decimal(tmpdir, master):
    annex_run([str(tmpdir)], master)
    wb = load_workbook(tmpdir.join('PROJECT_PROGRAMME NAME 1_ANNEX.xlsx'))
    ws = wb.active
    assert ws['B5'].value == '32.3'

