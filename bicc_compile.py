class BCMasterCSV(object):
    def __init__(self, source_file):
       self.source_file = source_file

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

    def __repr__(self):
        return "BCMasterCSV from {}".format(self.source_file)


def get_master(source_file):
    master = BCMasterCSV('source_files/master.csv')
    return master
