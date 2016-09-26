import os

class DataMap(object):

    def __init__(self, file):
        self.source_file = file

        #clean it first
        self._clean()


    def _clean(self):
        """
        Clean the datamap and create a cleaned_datamap file.
        :return:
        """
        DIRTY_DATAMAP_FILE = 'source_files/datamap'
        CLEANED_DATAMAP_FILE = 'source_files/cleaned_datamap'
        try:
            os.remove(CLEANED_DATAMAP_FILE)
        except FileNotFoundError:
            print('There is no existing cleaned_datamap file found, so continuing. Will create one.')
            pass

        cleaned_datamap = open(CLEANED_DATAMAP_FILE, 'a')

        with open(DIRTY_DATAMAP_FILE, 'r', encoding='UTF-8') as f:

            # make sure every line has a comma at the end
            for line in f.readlines():
                newline = line.rstrip()
                if ',' in newline[-1]:
                    newline = newline + '\n'
                    cleaned_datamap.write(newline)
                else:
                    newline = newline + ',' + '\n'
                    cleaned_datamap.write(newline)
        print("New cleaned_datamap file created from datamap.")
