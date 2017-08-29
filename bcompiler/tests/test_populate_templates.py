import bcompiler.main as main_module
import os

from openpyxl import load_workbook

from ..main import populate_blank_bicc_form as populate
from ..main import get_list_projects
from ..utils import project_data_from_master


def test_get_list_projects_main_xlsx(master):
    l = get_list_projects(master)
    assert l[0] == 'PROJECT/PROGRAMME NAME 1'


def test_pull_data_from_xlsx_master(master):
    data = project_data_from_master(master)
    assert data['PROJECT/PROGRAMME NAME 1']['SRO Sign-Off'] == 'SRO SIGN-OFF 1'
    assert data['PROJECT/PROGRAMME NAME 1'][
        'Reporting period (GMPP - Snapshot Date)'] == 'REPORTING PERIOD (GMPP - SNAPSHOT DATE) 1'


def test_populate_single_template(master, blank_template):
    SOURCE_DIR = '/tmp/bcompiler-test'
    OUTPUT_DIR = '/tmp/bcompiler-test-output/'
    setattr(main_module, 'OUTPUT_DIR', OUTPUT_DIR)
    setattr(main_module, 'SOURCE_DIR', SOURCE_DIR)
    setattr(main_module, 'BLANK_TEMPLATE_FN', blank_template)
    populate(master, 1)
    wb = load_workbook(os.path.join(OUTPUT_DIR, 'A303_Q1_2013_Return.xlsm'))
    ws = wb['Summary']
    assert ws['A5'] == 'Chumpers'


