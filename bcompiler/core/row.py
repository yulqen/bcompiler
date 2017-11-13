class Row:
    def __init__(self, anchor_column, anchor_row, seq):
        self._anchor_column = anchor_column
        self._anchor_row = anchor_row
        self._seq = seq

    def bind(self, worksheet):
        self._ws = worksheet

        for x in list(enumerate(self._seq, start=self._anchor_column)):
            self._ws.cell(row=self._anchor_row, column=x[0], value=x[1])


