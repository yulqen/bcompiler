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
    ws = wb.active
    ws['B5'] == 'Cookfield Rebuild'
    wb.save('/tmp/test-bicc-return.xlsx')
    yield '/tmp/test-bicc-return.xlsx'
    os.unlink('/tmp/test-bicc-return.xlsx')


@pytest.fixture
def db():
    return Database('db.json').connect()


def test_digest_single_file(bicc_return, series):
    digest = Digest(bicc_return, series, 'Q2 April')
    assert digest.table == 'q2-april'
    assert digest.series == 'Financial Quarters'
    assert digest.data['Project/Programme Name'] == 'Cookfield Rebuild'


@pytest.mark.skip("Too resource intensive for now.")
def test_digest_source_files(db):
    base_dir = '/home/lemon/Documents/bcompiler/source/returns'
    digest_source_files(base_dir, db)
