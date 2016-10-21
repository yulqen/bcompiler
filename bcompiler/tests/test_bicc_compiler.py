import csv
import os
import unittest

import re
from bcompiler.bcompiler import create_master_dict_transposed, clean_datamap, create_datamap_n_tuples
from bcompiler.utils import VALIDATION_REFERENCES, SHEETS
from bcompiler.compile import parse_source_cells, get_current_quarter
from bcompiler.datamap import Datamap, DatamapLine, DatamapGMPP
from bcompiler.utils import DATAMAP_RETURN_TO_MASTER


@unittest.skip("only running GMPP tests for now")
class TestMasterFunctions(unittest.TestCase):
    def setUp(self):
        self.docs = os.path.join(os.path.expanduser('~'), 'Documents')
        bcomp_working_d = 'bcompiler'
        self.path = os.path.join(self.docs, bcomp_working_d)
        self.source_path = os.path.join(self.path, 'source')
        self.output_path = os.path.join(self.path, 'output')
        self.datamap_master_to_returns = os.path.join(self.source_path, 'datamap-master-to-returns')
        self.datamap_returns_to_master = os.path.join(self.source_path, 'datamap-returns-to-master')
        self.master = os.path.join(self.source_path, 'master.csv')
        self.transposed_master = os.path.join(self.source_path, 'master_transposed.csv')
        self.example_return = os.path.join(self.source_path, 'returns/Q2 16-17 BICC SAR H - Final.xlsx')

    def test_presence_base_master_csv(self):
        self.assertTrue(os.path.exists(self.master))

    def test_presence_transposed_csv(self):
        create_master_dict_transposed(self.master)
        self.assertTrue(os.path.exists(self.transposed_master))

    def test_for_individual_project_data_lines(self):
        test_st = "Project/Programme Name,Classification,SRO Sign-Off,FD Sign-Off,"
        len_test_st = len(test_st)
        with open(self.transposed_master, 'r') as f:
            f_line = f.readline(len_test_st)
            self.assertEqual(f_line, test_st)

    def test_for_data_migrated_to_blank_form(self):
        selected_data = {}
        with open(self.transposed_master, 'r') as f:
            projects = list([row for row in csv.DictReader(f)])
            project = projects[0]
            selected_data['Project/Programme Name'] = project['Project/Programme Name']
            selected_data['SRO Sign-Off'] = project['SRO Sign-Off']
            selected_data['Change Delivery Methodology'] = project['Change Delivery Methodology']
        # pass for now
        pass

    def test_parse_returned_form(self):
        return_f = self.example_return
        data = parse_source_cells(return_f, self.datamap_master_to_returns)
        self.assertEqual(data[0]['gmpp_key'], 'Project/Programme Name')

    def test_dropdown_not_passing_to_master_bug(self):
        return_f = self.example_return
        data = parse_source_cells(return_f, self.datamap_master_to_returns)
        example_validated_cell = "IO1 - Monetised?"
        matches = [x for x in data if x['gmpp_key'] == example_validated_cell]
        self.assertEqual(matches[0]['gmpp_key'], example_validated_cell)

    # trial of creating list of named tuples from the datamap - not sure why yet
    def test_list_of_named_tuples_from_datamap(self):
        clean_datamap(DATAMAP_RETURN_TO_MASTER)
        datamap_data = create_datamap_n_tuples()
        self.assertEqual(datamap_data[0][0], 'Project/Programme Name')


class TestCompilationFromReturns(unittest.TestCase):
    def setUp(self):
        self.cell_regex = re.compile('[A-Z]+[0-9]+')
        self.dropdown_regex = re.compile('^\D*$')
        self.docs = os.path.join(os.path.expanduser('~'), 'Documents')
        bcomp_working_d = 'bcompiler'
        self.path = os.path.join(self.docs, bcomp_working_d)
        self.source_path = os.path.join(self.path, 'source')
        self.output_path = os.path.join(self.path, 'output')
        self.returns_path = os.path.join(self.source_path, 'returns')
        self.source_file_name = 'DVSA IT Sourcing _Q2_Return v1.1.xlsx'
        self.source_excel = os.path.join(self.returns_path, self.source_file_name)
        self.datamap_returns_to_master = os.path.join(self.source_path, 'datamap-returns-to-master')
        self.dm = Datamap(type='returns-to-master', source_file=self.datamap_returns_to_master)

    def test_parse_source_excel_file(self):
        parsed_data = parse_source_cells(self.source_excel, self.datamap_returns_to_master)
        self.assertEqual('Project/Programme Name', parsed_data[0]['gmpp_key'])
        self.assertEqual('DVSA IT Sourcing', parsed_data[0]['gmpp_key_value'])

    def test_run_compilation_run(self):
        pass

    def test_get_quarter(self):
        self.assertEqual(get_current_quarter(self.source_file_name), 'Q1 Apr - Jun')


class TestDatamapFunctionality(unittest.TestCase):
    def setUp(self):
        self.cell_regex = re.compile('[A-Z]+[0-9]+')
        self.dropdown_regex = re.compile('^\D*$')
        self.docs = os.path.join(os.path.expanduser('~'), 'Documents')
        bcomp_working_d = 'bcompiler'
        self.path = os.path.join(self.docs, bcomp_working_d)
        self.source_path = os.path.join(self.path, 'source')
        self.output_path = os.path.join(self.path, 'output')
        self.datamap_master_to_returns = os.path.join(self.source_path, 'datamap-master-to-returns')
        self.datamap_returns_to_master = os.path.join(self.source_path, 'datamap-returns-to-master')
        self.master = os.path.join(self.source_path, 'master.csv')
        self.transposed_master = os.path.join(self.source_path, 'master_transposed.csv')
        self.dm = Datamap(type='returns-to-master', source_file=self.datamap_returns_to_master)

    def test_verified_lines(self):
        # these are DatamapLine objects that have 4 attributes, the last of which is verification
        # dropdown text
        # the last element in each should be a dropdown text string
        for item in self.dm._dml_cname_sheet_cref_ddown:
            self.assertTrue(self.dropdown_regex, item.dropdown_txt)

    def test_verified_lines_for_dropdown_text(self):
        # we're expecting the dropdown_txt attr in the DatamapLine object to be what we expect
        for item in self.dm._dml_cname_sheet_cref_ddown:
            self.assertTrue(item.dropdown_txt in VALIDATION_REFERENCES.keys())

    def test_non_verified_lines(self):
        # these are DatamapLine objects that have 3 attributes, the last of which is a regex
        for item in self.dm._dml_cname_sheet_cref:
            self.assertTrue(self.cell_regex, item.cellref)

    def test_cells_that_will_not_migrate(self):
        # these are DatamapLine objects that have 2 attributes, the last of which is a sheet ref
        for item in self.dm._dml_cname_sheet:
            self.assertTrue(item.sheet in SHEETS)

    def test_single_item_lines(self):
        # DatamapLines that have a single attribute
        for item in self.dm._dml_cname:
            # TODO this is fragile - shouldn't be counting lines in this test
            self.assertEqual(self.dm.count_dml_cellname_only, 20)

    def test_datamap_is_cleaned_attr(self):
        self.assertTrue(self.dm.is_cleaned)

    def test_pretty_dataline_print(self):
        dml = DatamapLine()
        dml.cellname = 'Test cellname'
        dml.sheet = 'Summary'
        dml.cellref = 'C12'
        dml.dropdown_txt = 'Finance Figures'
        self.assertEqual(dml.pretty_print(),
                         "Name: Test cellname | Sheet: Summary | Cellref: C12 | Dropdown: Finance Figures")

    def test_blocks_of_finance_blocks(self):
        """
        The datamap needs to contain blocks like this in this order:

        16-17 RDEL Baseline - One off new costs - investment in change
        16-17 RDEL Baseline - Recurring new costs - investment in change
        16-17 RDEL Baseline - Recurring old costs
        16-17 RDEL Baseline - Whole Life Cost breakdown

        16-17 RDEL Forecast - One off new costs - investment in change
        16-17 RDEL Forecast - Recurring new costs - investment in change
        16-17 RDEL Forecast - Recurring old costs
        16-17 RDEL Forecast - Whole Life Cost breakdown

        16-17 CDEL Baseline - One off new costs - investment in change
        16-17 CDEL Baseline - Recurring new costs - investment in change
        16-17 CDEL Baseline - Recurring old costs
        16-17 CDEL Baseline - Whole Life Cost breakdown

        16-17 CDEL Forecast - One off new costs - investment in change
        16-17 CDEL Forecast - Recurring new costs - investment in change
        16-17 CDEL Forecast - Recurring old costs
        16-17 CDEL Forecast - Whole Life Cost breakdown

        16-17 RDEL Baseline - Non-Gov both Revenue and Capital
        16-17 RDEL Forecast - Non-Gov both Revenue and Capital
        16-17 CDEL Baseline - Non-Gov both Revenue and Capital
        16-17 CDEL Forecast - Non-Gov both Revenue and Capital
        """
        quarter_regex = re.compile('(\d\d)-(\d\d)')
        rdel_str, cdel_str, baseline_str, forecast_str = 'RDEL,CDEL,Baseline,Forecast'.split(',')
        cellname1, cellname2, cellname3, cellname4 = 'One off new costs - investment in change,' \
                                                     'Recurring new costs - investment in change,' \
                                                     'Recurring old costs,' \
                                                     'Whole Life Cost breakdown'.split(',')
        cellname_non_gov = 'Non-Gov both Revenue and Capital'

        rdel_baseline_block = []

        l_cell_refs = []
        with open(DATAMAP_RETURN_TO_MASTER, 'r') as f:
            for line in f.readlines():
                line = line.split(',')
                l_cell_refs.append(line[0])




class TestGMPPExport(unittest.TestCase):
    def setUp(self):
        self.cell_regex = re.compile('[A-Z]+[0-9]+')
        self.dropdown_regex = re.compile('^\D*$')
        self.docs = os.path.join(os.path.expanduser('~'), 'Documents')
        bcomp_working_d = 'bcompiler'
        self.path = os.path.join(self.docs, bcomp_working_d)
        self.source_path = os.path.join(self.path, 'source')
        self.output_path = os.path.join(self.path, 'output')
        self.datamap_master_to_gmpp = os.path.join(self.source_path, 'datamap-master-to-gmpp')
        self.master = os.path.join(self.source_path, 'master.csv')
        self.transposed_master = os.path.join(self.source_path, 'master_transposed.csv')
        self.dm = DatamapGMPP(type='master-to-gmpp', source_file=self.datamap_master_to_gmpp)

    def test_there_is_the_correct_datamap_source_file(self):
        self.assertTrue(os.path.exists(self.datamap_master_to_gmpp))

    def test_create_gmpp_datamap_object(self):
        self.assertEqual(self.dm.data[0].cellname, 'Project/Programme Name')
        self.assertEqual(self.dm.data[0].sheet, 'GMPP Return')
        self.assertEqual(self.dm.data[0].cellref, 'C25')
        self.assertEqual(self.dm.data[0].dropdown_txt, None)
        self.assertEqual(self.dm.data[1].cellname, 'SRO Sign-Off')
        self.assertEqual(self.dm.data[1].sheet, 'GMPP Return')
        self.assertEqual(self.dm.data[1].cellref, 'C5')
        self.assertEqual(self.dm.data[1].dropdown_txt, None)

    def test_object_attrs(self):
        # there shouldn't be any single item lines in the DatamapGMPP
        self.assertEqual(self.dm._dml_cname, [])
        # there shouldn't be any 2 item lines either
        self.assertEqual(self.dm._dml_cname_sheet, [])
        # there should be lots of 3 item lines though!
        self.assertGreater(len(self.dm._dml_cname_sheet_cref), 0)


if __name__ == "__main__":
    unittest.main()
