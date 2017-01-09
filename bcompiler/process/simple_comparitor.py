from openpyxl import load_workbook


class SimpleComparitor:
    """
    Simple method of comparing data in two master spreadsheets.
    """

    def __init__(self, masters=[]):
        """
        We want to get a list of master spreadsheets. These are simple
        file-references. The latest master should be master[-1].
        """
        if len(masters) > 2:
            raise ValueError("You can only analyse two spreadsheets.")

        self.masters = masters

    def get_data(self, spreadsheet_file, col):
        wb = load_workbook(spreadsheet_file)
        ws = wb['Constructed BICC Data Master']
        col_a = ws['A']
        col_b = ws[col]
        z = list(zip(col_a, col_b))
        return [((item[0].value), (item[1].value)) for item in z]

    def data(self, index, col):
        return self.get_data(self.masters[index], col)
