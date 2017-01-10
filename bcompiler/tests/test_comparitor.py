import pytest

from bcompiler.process.simple_comparitor import BCCell
from bcompiler.process.simple_comparitor import populate_cells

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


@pytest.fixture
def populate_cells_fixture():
    wb = Workbook()
    ws = wb.active
    populate_cells(
        ws, [BCCell("Fist", cellref="A1"), BCCell("Snker", cellref="B1")])
    populate_cells(
        ws, [BCCell("Fist", 2, 3), BCCell("Snker", 3, 3)])
    yield ws


def test_wb_creation(populate_cells_fixture):
    assert populate_cells_fixture['A1'].value == 'Fist'
