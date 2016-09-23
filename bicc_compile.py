class BCMasterCSV(object):
    def __init__(self, source_file):
       self.source_file = source_file
       self.data = self.open_datafile()

    def open_datafile(self):
        d = open(self.source_file, 'r')
        data = d.read()
        d.close()
        return data

    def header(self):
        d = open(self.source_file, 'r')
        header = d.readline()
        d.close()
        return header

    def __repr__():
        return self.source_file


def get_master(source_file):
    master = BCMasterCSV('source_files/master.csv')
    return master
