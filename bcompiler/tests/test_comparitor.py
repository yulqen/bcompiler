import pytest
import os

from openpyxl import Workbook


key_col_data = [
    'Project/Programme Name',
    'SRO Sign-Off',
    'Reporting period (GMPP - Snapshot Date)',
    'Quarter Joined',
    'GMPP (GMPP – formally joined GMPP)',
    'IUK top 40',
    'Top 37',
    'DfT Business Plan',
    'GMPP - IPA ID Number',
    'DFT ID Number',
    'Working Contact Name',
    'Working Contact Telephone',
    'Working Contact Email',
    'DfT Group',
    'DfT Division',
    'Agency or delivery partner (GMPP - Delivery Organisation primary)',
    'Strategic Alignment/Government Policy (GMPP – Key drivers)',
    'Project Scope',
    'Brief project description (GMPP – brief descripton)',
    'Delivery Structure',
    'Description if \'Other',
    'Change Delivery Methodology'
]

project_b_data = [
    'Digital Signalling',
    '2016-10-12 0:00:00',
    'Q2 1617',
    None,
    None,
    None,
    None,
    None,
    None,
    8,
    'Niall Le Mage',
    '2079442043',
    'niall.lemage@dft.gsi.gov.uk',
    'Rail Group',
    'Network Services',
    'Network Rail',
    'In line with DfTs single Departmental Plan to roll out new technology',
    'Scope of the ETCS cab-fitment fund: | to facilitate the inclusion of',
    'The fitting of digital signalling technology to prototype passenger',
    'Project',
    None,
    'Waterfall',
]


class BCCell:

    def __init__(self, value, row_num=None, col_num=None, cellref=None):
        self.value = value
        self.row_num = row_num
        self.col_num = col_num
        self.cellref = cellref





def populate_col(worksheet, bc_cells=[]):
    """
    Populate a worksheet with bc_cell object data.
    """
    for item in bc_cells:
        if item.cellref:
            worksheet[item.cellref].value = item.value
        else:
            worksheet.cell(row=item.row_num, column=item.col_num, value=item.value)
    return worksheet



#@pytest.fixture
#def old_master():
#    wb = Workbook()
#    ws = wb.active
#    count = 0
#    # first column
#    for row in ws.iter_rows(min_row=1, max_col=1, max_row=len(key_col_data)):
#        for cell in row:
#            cell.value = key_col_data[count]
#            print(f"cell {cell}: {cell.value}")
#            count += 1
#
#    # project_b (as in b column)
#    for row in ws.iter_rows(min_row=1, max_col=1, max_row=len(key_col_data)):
#        for cell in row:
#            cell.value = key_col_data[count]
#            print(f"cell {cell}: {cell.value}")
#            count += 1
#
#    yield wb

@pytest.fixture
def populate_cols():
    wb = Workbook()
    ws = wb.active
    populate_col(ws, [BCCell("Fist", cellref="A1"), BCCell("Snker", cellref="B1")])
    populate_col(ws, [BCCell("Fist", 2, 3), BCCell("Snker", 3, 3)])
    yield ws

def test_wb_creation(populate_cols):
    assert populate_cols['A1'].value == 'Fist'
