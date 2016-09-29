import os
import unittest
from bcompiler import _create_working_directory

class TestMasterFunctions(unittest.TestCase):

    def test_check_for_working_directory_location(self):
        # let's say we'll create a new bcomipler directory in the user space
        # inside this directory will be a source and an output directory
        # which is where our key files will go
        # source/master.csv
        # source/bicc_template.xlsx
        # source/datamap
        # output/West Midlands Franchise Competition.xlsx
        _create_working_directory()
        docs = os.path.join(os.path.expanduser('~'), 'Documents')
        bcomp_working_d = 'bcompiler'
        path = os.path.join(docs, bcomp_working_d)
        source_path = os.path.join(path, 'source')
        output_path = os.path.join(path, 'output')
        self.assertTrue(os.path.exists(path))
        self.assertTrue(os.path.exists(source_path))
        self.assertTrue(os.path.exists(output_path))

    def test_for_base_master_csv(self):
        pass

    def test_for_processed_csv(self):
        pass

    def test_for_individual_project_data_lines(self):
        pass

    def test_for_data_migrated_to_blank_form(self):
        pass


if __name__ == "__main__":
    unittest.main()

