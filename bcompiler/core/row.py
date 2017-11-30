import string

from ..process.cell import Cell

from itertools import chain


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
                self._cell_map = []
            elif len(anchor_column) == 2:
                enumerated_alphabet = list(enumerate(list(chain(
                    string.ascii_uppercase, ["{}{}".format(x[0], x[1]) for x in list(zip(['A'] * 26, string.ascii_uppercase))])), start=1))
                col_letter = [x for x in enumerated_alphabet if x[1] == anchor_column][0]
                self._anchor_column = col_letter[0]
                self._anchor_row = anchor_row
                self._cell_map = []
            else:
                raise ValueError("You can only have a column up to AZ")
        else:
            self._anchor_column = anchor_column
            self._anchor_row = anchor_row
            self._cell_map = []
        self._seq = seq


    def _basic_bind(self, ws):
        for x in list(enumerate(self._seq, start=self._anchor_column)):
            self._ws.cell(row=self._anchor_row, column=x[0], value=x[1])


    def _cell_bind(self, ws):
        self._cell_map = []
        for x in list(enumerate(self._seq, start=self._anchor_column)):
            self._cell_map.append(
                Cell(
                    cell_key="",
                    cell_value=x[1],
                    cell_reference=f"{self._anchor_column}{self._anchor_row}",
                    template_sheet=ws,
                    bg_colour=None,
                    fg_colour=None,
                    number_format=None,
                    verification_list=None,
                    r_idx=self._anchor_row,
                    c_idx=x[0]
                )
            )
        for c in self._cell_map:
            self._ws.cell(row=c.r_idx, column=c.c_idx, value=c.cell_value)


    def bind(self, worksheet):
        self._ws = worksheet
#       self._basic_bind(self._ws)
        self._cell_bind(self._ws)
