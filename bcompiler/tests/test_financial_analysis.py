import pytest

from openpyxl import load_workbook

from ..analysers.financial import run as financial_run
from ..analysers.utils import project_titles_in_master


@pytest.mark.skip("Not yet implemented")
def test_a1_cell(tmpdir, master):
    financial_run(master)
    wb = load_workbook(tmpdir.join('financial_analysis.xlsx'))
    ws = wb.active
    assert ws['A1'].value == 'PROJECT/PROGRAMME NAME 1'
