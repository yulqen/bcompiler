import csv

from openpyxl import load_workbook


def test_existence(datamap):
    with open(datamap, 'r', newline='') as f:
        assert next(f).startswith('Project/Programme Name')
        reader = csv.reader(f)
        assert next(reader)[2] == 'B49'


def test_existence_generated_template(blank_template):
    wb = load_workbook(blank_template)
    sheet = wb['Summary']
    assert sheet['A8'].value == 'DfT Group'


