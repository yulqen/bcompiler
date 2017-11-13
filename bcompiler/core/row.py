import string


class Row:
    """
    A Row object is populated with an iterable, bound to an openpyxl
    worksheet. It is used to populate a row of cells in an output
    Excel file with the values from the iterable.
    """
    def __init__(self, anchor_column, anchor_row, seq):

        if isinstance(anchor_column, str):
            if len(anchor_column) == 1:
                enumerated_alphabet = list(enumerate(string.ascii_uppercase, start=1))
                col_letter = [x for x in enumerated_alphabet if x[1] == anchor_column][0]
                self._anchor_column = col_letter[0]
                self._anchor_row = anchor_row
        else:
            self._anchor_column = anchor_column
            self._anchor_row = anchor_row
        self._seq = seq

    def bind(self, worksheet):
        self._ws = worksheet

        for x in list(enumerate(self._seq, start=self._anchor_column)):
            self._ws.cell(row=self._anchor_row, column=x[0], value=x[1])


