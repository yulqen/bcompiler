import pandas as pd

class BCMasterCSV(object):

    def __init__(self, source_file, dataframe=None):
        
        self.data = None
        self.source_file = source_file
        
        if dataframe:
            self.data = self._create_dataframe()
        else:
            self.data = self.open_datafile()

    @property
    def header(self):
        d = open(self.source_file, 'r')
        header = d.readline()
        d.close()
        return header
        
    def open_datafile(self):
        d = open(self.source_file, 'r')
        data = d.read()
        d.close()
        return data


    def _create_dataframe(self):
        df = pd.read_csv(self.source_file)
        return df


    def __repr__(self):
        return "BCMasterCSV from {}".format(self.source_file)


def get_master(source_file):
    master = BCMasterCSV('source_files/master.csv')
    return master
