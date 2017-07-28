"""
This module tests external dependencies in the bcompiler system,
including the datamap and the bicc_template.xlsx.

If the template changes, the cell references in test_generated_template()
function below MUST be amended accordingly.
"""
import csv

from openpyxl import load_workbook


def test_existence(datamap):
    with open(datamap, 'r', newline='') as f:
        assert next(f).startswith('Project/Programme Name')
        reader = csv.reader(f)
        assert next(reader)[2] == 'B49'


def test_generated_template(blank_template):
    wb = load_workbook(blank_template)
    sheet_s = wb['Summary']
    sheet_fb = wb['Finance & Benefits']
    sheet_r = wb['Resource']
    sheet_apm = wb['Approval & Project milestones']
    sheet_ap = wb['Assurance Planning']
    assert sheet_s['A8'].value == 'DfT Group'
    assert sheet_s['A46'].value == 'SRO Overall Delivery Confidence'
    assert sheet_fb['A121'].value == '2027/2028'
    assert sheet_fb['F26'].value == 'All RDEL (WLC) Total'
    assert sheet_r['A36'].value == 'Other (please specify)'
    assert sheet_r['A12'].value == 'SEO (PB5)'
    assert sheet_apm['E7'].value == 'Type of milestone'
    assert sheet_ap['B32'].value == 'External'
    assert sheet_ap['C31'].value == None

def test_incorrect_template_cells(blank_template):
    wb = load_workbook(blank_template)
    sheet_apm = wb['Approval & Project milestones']
    assert sheet_apm['A43'].value == None
    assert sheet_apm['A430'].value == None



