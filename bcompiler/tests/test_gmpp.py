# we want to test the GMPP datamap functionality

import os

from bcompiler.datamap import DatamapGMPP
from bcompiler.utils import SOURCE_DIR, DATAMAP_MASTER_TO_GMPP, GMPP_TEMPLATE
from bcompiler.utils import OUTPUT_DIR
from bcompiler.utils import open_openpyxl_template
from bcompiler.utils import project_data_line
from bcompiler.utils import gmpp_project_data
from bcompiler.utils import gmpp_project_names
from bcompiler.utils import populate_blank_gmpp_form

dm = DatamapGMPP(
    '/home/lemon/Documents/bcompiler/source/datamap-master-to-gmpp')
dm_file = '/home/lemon/Documents/bcompiler/source/datamap-master-to-gmpp'

project_to_test = 'Rail Franchising Programme'
transposed_master = SOURCE_DIR + "master_transposed.csv"
dm_file = DATAMAP_MASTER_TO_GMPP
datamap = DatamapGMPP(DATAMAP_MASTER_TO_GMPP)


def test_there_is_the_correct_datamap_source_file():
    assert os.path.exists(dm_file)


def test_clean_creation_of_dm_object():
    assert dm.data[0].cellname == 'Project/Programme Name'
    assert dm.data[1].cellref == 'C5'


def test_that_empty_cell_ref_returns_none():
    assert dm.data[3].cellref is None


def test_report_lines_no_cellref():
    """
    Hard-coded test: FRAGILE!
    """
    assert dm.no_cellrefs == 188


#    def test_print_lines_no_cellref():
#        no_cellref_lines = dm.print_no_cellref_lines()
#        assert "FD Sign Off" in no_cellref_lines


def test_create_gmpp_datamap_object():
    """
    WEAK testing. Need to replace with proper fixtures.
    """
    assert dm.data[0].cellname, 'Project/Programme Name'
    assert dm.data[0].sheet, 'GMPP Return'
    assert dm.data[0].cellref, 'C25'
    assert dm.data[1].cellname, 'SRO Sign-Off'
    assert dm.data[1].sheet, 'GMPP Return'
    assert dm.data[1].cellref, 'C5'


def test_object_attrs():
    # there shouldn't be any single item lines in the DatamapGMPP
    assert dm._dml_cname == []
    # there shouldn't be any 2 item lines either
    assert dm._dml_cname_sheet == []
    # there should be lots of 3 item lines though!
    assert len(dm._dml_cname_sheet_cref) == 612


def test_transposed_master():
    """
    This is probably done already elsewhere...
    """
    with open(transposed_master, 'r') as f:
        first_line = f.readline()
        assert first_line[0:17] == 'Project/Programme'


def test_return_single_gmpp_form():
    template_opyxl = open_openpyxl_template(GMPP_TEMPLATE)
    ws = template_opyxl['GMPP Return']
    assert ws['B5'].value == 'SRO Sign-Off'
    assert ws['B13'].value == 'Snapshot Date'
    assert ws['B60'].value == 'Intended Outcome 9'
    assert ws['B296'].value == 'Benefits Narrative'


def test_get_project_data_line():
    data = project_data_line()
    assert data[project_to_test]['DfT Group'] == ('Rail Group')


def test_get_list_of_gmpp_project_data():
    gmpp_list = gmpp_project_data()
    assert len(gmpp_list) == 15


def test_get_list_of_gmpp_project_names():
    assert project_to_test in gmpp_project_names()


def test_populate_single_gmpp_form():
    template_opyxl = open_openpyxl_template(GMPP_TEMPLATE)
    populate_blank_gmpp_form(template_opyxl, project_to_test)
    assert os.path.exists(OUTPUT_DIR + project_to_test + 'Q2_GMPP.xlsx')
