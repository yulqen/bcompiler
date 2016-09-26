import pandas as pd
import io

class BCMasterCSV(object):

    def __init__(self, source_file, as_dataframe=False):

        self.source_file = source_file

        if as_dataframe:
            self.as_dataframe = self._create_dataframe()
        else:
            self.as_csv = self._open_datafile()

    @property
    def csv_header(self):
        try:
            d = io.StringIO(self.as_csv)
        except AttributeError:
            print("You can only call this when passing as_dataframe=True to constructor")
        else:
            header = d.readline()
            d.close()
            return header

    def transpose_csv(self, to_file=False):
        """
        Transposes the rows and columns of the BICC data file so it is in recognisable CSV format.
        :param to_file: True if you need to write the file to 'source_files/transposed.csv'; False to
        return a StringIO file object.
        :return: if to_file=False or omitted, returns a StringIO file object
        """
        with open(self.source_file, 'r') as source_f:
            lis = [x.split(',') for x in source_f]

        if to_file:
            out_f = open('source_files/transposed.csv', 'w')
        else:
            out_f = io.StringIO()

        for x in zip(*lis):
            for y in x:
                out_f.write(y + ',')
            out_f.write(',')
        if to_file:
            out_f.close()
        else:
            return out_f


    @property
    def projects(self):
        f = self.as_dataframe.T
        return f.index

    def flip(self):
        return self.as_dataframe.T

    def _open_datafile(self):
        d = open(self.source_file, 'r')
        data = d.read()
        d.close()
        return data

    def _create_dataframe(self):
        df = pd.read_csv(self.source_file, index_col=0)
        return df


    def __repr__(self):
        return "BCMasterCSV from {}".format(self.source_file)

