import bcompiler.main as main_module
import glob
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
    setattr(main_module, 'BLANK_TEMPLATE_FN', ''.join(['/', blank_template.split('/')[-1]]))
    populate(master, 0)
    wb = load_workbook(os.path.join(OUTPUT_DIR, 'PROJECT_PROGRAMME NAME 1_Q2 Jul - Oct 2017_Return.xlsm'))
    ws = wb['Summary']
    assert ws['B5'].value == 'PROJECT/PROGRAMME NAME 1'
    for f in glob.glob('/'.join([OUTPUT_DIR, '*_Return.xlsm'])):
        os.remove(f)
