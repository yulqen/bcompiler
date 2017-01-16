import os
import pytest
from openpyxl import Workbook

from bcompiler.process.database import Database
from bcompiler.process.digest import digest_source_files, Digest, Series


@pytest.fixture
def series():
    series = Series('Financial Quarters')
    return series


@pytest.fixture
def bicc_return():
    wb = Workbook()
    wb.create_sheet('Summary')
    wb.create_sheet('Approval & Project milestones')
    wb.create_sheet('Finance & Benefits')
    wb.create_sheet('Resources')
    wb.create_sheet('Assurance planning')
    wb.create_sheet('GMPP info')
    ws = wb['Summary']
    # enter some values in the right slots
    ws['B5'].value = 'Cookfield Rebuild'
    ws['B8'].value = 'Roads, Monitoring and Horse'

    wb.save('/tmp/test-bicc-return.xlsx')
    yield '/tmp/test-bicc-return.xlsx'
    os.unlink('/tmp/test-bicc-return.xlsx')


@pytest.fixture
def db():
    yield Database('/tmp/db.json').connect()
    os.unlink('/tmp/db.json')


def test_digest_single_file(bicc_return, series):
    digest = Digest(bicc_return, series, 'Q2 April')
    assert digest.table == 'q2-april'
    assert digest.series == 'Financial Quarters'
    assert digest.data['Project/Programme Name'] == 'Cookfield Rebuild'
    # this works because the comma is getting cleansed
    assert digest.data['DfT Group'] == 'Roads Monitoring and Horse'


@pytest.mark.skip("Too resource intensive for now.")
def test_digest_source_files(db):
    base_dir = '/home/lemon/Documents/bcompiler/source/returns'
    digest_source_files(base_dir, db)
