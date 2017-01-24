import os
import pytest

from bcompiler.process.database import Database
from bcompiler.process.digest import Series

from openpyxl import Workbook


@pytest.fixture
def bicc_return():
    wb = Workbook()
    wb.create_sheet('Summary')
    wb.create_sheet('Finance & Benefits')
    wb.create_sheet('Approval & Project milestones')
    wb.create_sheet('Resources')
    wb.create_sheet('Assurance planning')
    wb.create_sheet('GMPP info')
    ws_summary = wb['Summary']
    # enter some values in the right slots
    ws_summary['A5'].value = 'Project/Programme Name'
    ws_summary['B5'].value = 'Cookfield Rebuild'
    ws_summary['A8'].value = 'DfT Group'
    ws_summary['B8'].value = 'Roads, Monitoring and Horse'

    ws_finance = wb['Finance & Benefits']
    ws_finance['A6'].value = 'SRO Finance Confidence'
    ws_finance['C6'].value = 'Red'
    ws_finance['B11'].value = 'Date of Business Case'
    ws_finance['A19'].value = 'Index Year'
    ws_finance['B19'].value = '2012'
    ws_finance['A18'].value = 'Real or Nominal'
    ws_finance['C18'].value = 'Nominal'
    ws_finance['A36'].value = '2019/2020'
    ws_finance['C36'].value = 2.00
    ws_finance['A44'].value = 'Total'
    ws_finance['C44'].value = 23.30033
    ws_finance['A77'].value = 'Total WLC (RDEL)'
    ws_finance['C77'].value = 232.32


    wb.save('/tmp/test-bicc-return.xlsx')
    yield '/tmp/test-bicc-return.xlsx'
    os.unlink('/tmp/test-bicc-return.xlsx')


@pytest.fixture
def series():
    series = Series('Financial Quarters')
    return series


@pytest.fixture
def db():
    yield Database('/tmp/db.json').connect()
    os.unlink('/tmp/db.json')
