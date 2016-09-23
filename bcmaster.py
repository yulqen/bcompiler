import pandas as pd
import io

class BCMasterCSV(object):

    def __init__(self, source_file, dataframe=False):
        
        self.data = None
        self.source_file = source_file
        
        if dataframe:
            self.data = self._create_dataframe()
            self.this_is_dataframe = True
        else:
            self.data = self._open_datafile()

    @property
    def csv_header(self):
        d = open(self.source_file, 'r')
        header = d.readline()
        d.close()
        return header

    def flip(self):
        return self.data.T
        
        
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

