import unittest

from bicc_compile import get_master, BCMasterCSV

class TestImportFunctions(unittest.TestCase):

    def setUp(self):
        self.master = get_master('source_files/master.csv')
    
    def test_get_master(self):
        self.assertIsInstance(self.master, BCMasterCSV)

    def test_check_for_expected_strings(self):
        header = self.master.header()
        check_string = 'Project name'
        first_word_from_datafile = header.split(',')[0]
        self.assertEqual(check_string, first_word_from_datafile)

if __name__ == "__main__":
    unittest.main()

