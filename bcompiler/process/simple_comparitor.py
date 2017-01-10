from openpyxl import load_workbook


class BCCell:

    def __init__(self, value, row_num=None, col_num=None, cellref=None):
        self.value = value
        self.row_num = row_num
        self.col_num = col_num
        self.cellref = cellref


def parse_master(master_file):
    wb = load_workbook(master_file)
    ws = wb.active
    projects = [cell.value for cell in ws[1][1:]].sort()
    project_count = len(projects)
    key_col = [cell.value for cell in ws['A']]




def populate_cells(worksheet, bc_cells=[]):
    """
    Populate a worksheet with bc_cell object data.
    """
    for item in bc_cells:
        if item.cellref:
            worksheet[item.cellref].value = item.value
        else:
            worksheet.cell(
                row=item.row_num, column=item.col_num, value=item.value)
    return worksheet


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

