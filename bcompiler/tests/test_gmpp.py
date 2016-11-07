# we want to test the GMPP datamap functionality

import os

from unittest import TestCase

from bcompiler.datamap import DatamapGMPP
from bcompiler.utils import SOURCE_DIR, DATAMAP_MASTER_TO_GMPP, GMPP_TEMPLATE
from bcompiler.utils import OUTPUT_DIR
from bcompiler.utils import open_openpyxl_template
from bcompiler.utils import project_data_line
from bcompiler.utils import gmpp_project_data
from bcompiler.utils import gmpp_project_names
from bcompiler.utils import populate_blank_gmpp_form


class TestGMPPDatamap(TestCase):
    def setUp(self):
        self.dm = DatamapGMPP(
            '/home/lemon/Documents/bcompiler/source/datamap-master-to-gmpp')
        self.dm_file = ('/home/lemon/Documents/bcompiler/source/'
                        'datamap-master-to-gmpp')
        self.project_to_test = 'Rail Franchising Programme'
        self.transposed_master = SOURCE_DIR + "master_transposed.csv"
        self.dm_file = DATAMAP_MASTER_TO_GMPP
        self.datamap = DatamapGMPP(DATAMAP_MASTER_TO_GMPP)

    def test_there_is_the_correct_datamap_source_file(self):
        self.assertTrue(os.path.exists(self.dm_file))

    def test_clean_creation_of_dm_object(self):
        self.assertEqual(self.dm.data[0].cellname, 'Project/Programme Name')
        self.assertEqual(self.dm.data[0].cellref, 'C23')

    def test_that_empty_cell_ref_returns_none(self):
        self.assertIsNone(self.dm.data[3].cellref)

    def test_report_lines_no_cellref(self):
        """
        Hard-coded test: FRAGILE!
        """
        self.assertEqual(self.dm.no_cellrefs, 188)

    def test_create_gmpp_datamap_object(self):
        """
        WEAK testing. Need to replace with proper fixtures.
        """
        self.assertEqual(self.dm.data[0].cellname, 'Project/Programme Name')
        self.assertEqual(self.dm.data[0].sheet, 'GMPP Return')
        self.assertEqual(self.dm.data[0].cellref, 'C23')
        self.assertEqual(self.dm.data[1].cellname, 'SRO Sign-Off')
        self.assertEqual(self.dm.data[1].sheet, 'GMPP Return')
        self.assertEqual(self.dm.data[1].cellref, 'C5')

    def test_object_attrs(self):
        # there shouldn't be any single item lines in the DatamapGMPP
        self.assertEqual(self.dm._dml_cname, [])
        # there shouldn't be any 2 item lines either
        self.assertEqual(self.dm._dml_cname_sheet, [])
        # there should be lots of 3 item lines though!
        self.assertEqual(len(self.dm._dml_cname_sheet_cref), 612)

    def test_transposed_master(self):
        """
        This is probably done already elsewhere...
        """
        with open(self.transposed_master, 'r') as f:
            first_line = f.readline()
            self.assertEqual(first_line[0:17], 'Project/Programme')

    def test_return_single_gmpp_form(self):
        template_opyxl = open_openpyxl_template(GMPP_TEMPLATE)
        ws = template_opyxl['GMPP Return']
        self.assertEqual(ws['B5'].value, 'SRO Sign-Off')
        self.assertEqual(ws['B13'].value, 'Snapshot Date')
        self.assertEqual(ws['B60'].value, 'Intended Outcome 9')
        self.assertEqual(ws['B296'].value, 'Benefits Narrative')

    def test_get_project_data_line(self):
        data = project_data_line()
        self.assertEqual(data[self.project_to_test]['DfT Group'], 'Rail Group')

    def test_get_list_of_gmpp_project_data(self):
        gmpp_list = gmpp_project_data()
        self.assertEqual(len(gmpp_list), 15)

    def test_get_list_of_gmpp_project_names(self):
        self.assertIn(self.project_to_test, gmpp_project_names())

    def test_populate_single_gmpp_form(self):
        template_opyxl = open_openpyxl_template(GMPP_TEMPLATE)
        populate_blank_gmpp_form(template_opyxl, self.project_to_test)
        self.assertTrue(os.path.exists(
            OUTPUT_DIR + self.project_to_test + ' Q2_GMPP.xlsx'))

    def test_additional_datalines(self):
        """We need to include some data in the outputted template
        that are not included in the datamap because we don't collect them
        in the BICC return."""
        dm_a = self.dm.add_additional_data()
        self.assertEqual(
            "OFFICIAL SENSITIVE", dm_a[0].added_data_field)
        self.assertEqual(
            "Michelle Jennings", dm_a[1].added_data_field)
        self.assertEqual(
            "michelle.jennings@dft.gsi.gov.uk", dm_a[2].added_data_field)
        self.assertEqual(
            "Michelle Jennings", dm_a[3].added_data_field)
        self.assertEqual(
            "michelle.jennings@dft.gsi.gov.uk", dm_a[4].added_data_field)
