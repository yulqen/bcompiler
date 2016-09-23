import unittest

from bicc_compile import BCMasterCSV

class TestImportFunctions(unittest.TestCase):

    def setUp(self):
        self.master = BCMasterCSV('source_files/master.csv')
    
    def test_get_master(self):
        self.assertIsInstance(self.master, BCMasterCSV)

    def test_check_for_expected_strings(self):
        header = self.master.header()
        check_string = 'Project name'
        first_word_from_datafile = header.split(',')[0]
        self.assertEqual(check_string, first_word_from_datafile)

    def test_id_master_object(self):
        m = BCMasterCSV('source_files/master.csv')
        self.assertEqual('BCMasterCSV from source_files/master.csv', str(m))
        

if __name__ == "__main__":
    unittest.main()

