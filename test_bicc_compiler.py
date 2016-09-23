import unittest
import pandas as pd

from bcmaster import BCMasterCSV

class TestMasterFunctions(unittest.TestCase):

    def setUp(self):
        self.master = BCMasterCSV('source_files/master.csv')

    def test_get_master(self):
        self.assertIsInstance(self.master, BCMasterCSV)

    def test_check_for_expected_strings(self):
        header = self.master.csv_header
        check_string = 'Project name'
        first_word_from_datafile = header.split(',')[0]
        self.assertEqual(check_string, first_word_from_datafile)

    def test_id_master_object(self):
        m = BCMasterCSV('source_files/master.csv')
        self.assertEqual('BCMasterCSV from source_files/master.csv', str(m))

    def test_get_pandas_dataframe_from_master(self):
        m_pand_true = pd.read_csv('source_files/master.csv')
        m_pand_true_type = type(m_pand_true)
        m_pand = BCMasterCSV('source_files/master.csv', dataframe=True)
        m_pand_data = m_pand.data
        self.assertTrue(type(m_pand_data) == m_pand_true_type)

    def test_flip_csv(self):
        frame = BCMasterCSV('source_files/master.csv', dataframe=True)
        flipped = frame.flip()
        # this test needs to change to something immutable
        self.assertIn('High Speed Rail Programme (HS2) v2', flipped.index)

    def test_get_project_list(self):
        frame = BCMasterCSV('source_files/master.csv', dataframe=True)
        projects = frame.projects()
        # this test needs to change to something immutable
        self.assertIn('High Speed Rail Programme (HS2) v2', projects)


if __name__ == "__main__":
    unittest.main()

