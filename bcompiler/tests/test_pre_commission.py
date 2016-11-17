import os
import unittest

from bcompiler.templates import CommissioningTemplate


class TestCommissioningTemplate(unittest.TestCase):
    def setUp(self):
        self.docs = os.path.join(
            os.path.expanduser('~'), 'Documents')
        bcomp_working_d = 'bcompiler'
        self.path = os.path.join(
            self.docs, bcomp_working_d)
        self.source_path = os.path.join(
            self.path, 'source')
        self.output_path = os.path.join(
            self.path, 'output')
        self.datamap_master_to_returns = os.path.join(
            self.source_path, 'datamap-master-to-returns')
        self.datamap_returns_to_master = os.path.join(
            self.source_path, 'datamap-returns-to-master')
        self.master = os.path.join(
            self.source_path, 'master.csv')
        self.transposed_master = os.path.join(
            self.source_path, 'master_transposed.csv')
        self.example_return = os.path.join(
            self.source_path, 'returns/SARH_Q2_Return_Final.xlsx')
        self.bicc_template = os.path.join(
            self.source_path, 'bicc_template.xlsx')

    def test_presence_of_blank_bicc_template_file(self):
        self.assertTrue(os.path.exists(self.bicc_template))

    def test_for_commissioning_template_object(self):
        commissioning_template_blank = CommissioningTemplate()
        self.assertIsInstance(
            commissioning_template_blank,
            CommissioningTemplate)

    def test_for_commissioning_template_basic_data(self):
        ct = CommissioningTemplate()
        sheets = ct.sheets
        self.assertIn('Summary', sheets)
        self.assertIn('Resources', sheets)
        self.assertNotIn('Non Sheet', sheets)
        self.assertIn('Approval & Project milestones', sheets)
        self.assertIn('Assurance planning', sheets)
        self.assertIn('Dropdown List', sheets)

    def test_for_blank_template(self):
        """
        The template itself, prior to commissioning should have no data
        in it, so this test picks a load of random cells and checks that their
        contents is empty.
        """
        pass

if __name__ == "__main__":
    unittest.main()
