import os
from datetime import datetime
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

    # Summary fixture
    ws_summary = wb['Summary']
    ws_summary['A5'].value = 'Project/Programme Name'
    ws_summary['B5'].value = 'Cookfield Rebuild'
    ws_summary['A8'].value = 'DfT Group'
    ws_summary['B8'].value = 'Roads, Monitoring and Horse'

    # Finance & Benefits fixture
    ws_finance = wb['Finance & Benefits']
    ws_finance['A6'].value = 'SRO Finance Confidence'
    ws_finance['C6'].value = 'Red'
    ws_finance['B11'].value = 'Date of Business Case'
    ws_finance['C11'].value = datetime(2000, 10, 23)
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

    # Resources fixture
    ws_resources = wb['Resources']
    ws_resources['A7'].value = 'SCS(PB2)'
    ws_resources['C7'].value = 1.00
    ws_resources['A17'].value = 'Total'
    ws_resources['G17'].value = 0.0
    ws_resources['A30'].value = 'Change Implementation'
    ws_resources['I30'].value = 'Green'
    ws_resources['J30'].value = 'Amber'
    ws_resources['G38'].value = 'Overall Assessment'
    ws_resources['J38'].value = 'Red'

    # Approval and Project Milestones fixture
    ws_approvals = wb['Approval & Project milestones']
    ws_approvals['A10'].value = 'SOBC - HMT Approval'
    ws_approvals['C10'].value = datetime(2009, 2, 20)
    ws_approvals['A19'].value = 'FBC - HMT Approval'
    ws_approvals['F19'].value = 'A lot of very uninteresting test text here.'
    ws_approvals['A39'].value = 'Completion of Construction'
    ws_approvals['B39'].value = datetime(2018, 9, 1)

    # Assurance fixture
    ws_assurance = wb['Assurance planning']
    ws_assurance['B4'].value = 'Date Created'
    ws_assurance['C4'].value = datetime(2017, 1, 12)
    ws_assurance['A10'].value = 'Gate 0 (Programme)'
    ws_assurance['D10'].value = datetime(2013, 5, 21)
    ws_assurance['A17'].value = 'Review Point 4 MPRG'
    ws_assurance['E17'].value = 'Amber/Green'

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
