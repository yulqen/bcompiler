import os
import re


class DataMap(object):


    def __init__(self, file):
        self.source_file = file
        self.output_excel_map_list = []

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

    # we're going to output data from this function as a list of dict items

    def parse(self):

        cell_regex = re.compile('[A-Z]+[0-9]+')
        f = open('source_files/cleaned_datamap', 'r')
        data = f.readlines()
        for line in data:
            # split on , allowing us to access useful data from data map file
            data_map_line = line.split(',')
            if data_map_line[1] in ['Summary', 'Finance & Benefits', 'Resources', 'Approval and Project milestones',
                                    'Assurance planning']:
                # the end item in the list is a newline - get rid of that
                del data_map_line[-1]
            if cell_regex.search(data_map_line[-1]):
                try:
                    m_map = dict(cell_description=data_map_line[0],
                                 sheet=data_map_line[1],
                                 cell_coordinates=data_map_line[2])
                except IndexError:
                    m_map = dict(cell_description=data_map_line[0],
                                 sheet="CAN'T FIND SHEET")
                self.output_excel_map_list.append(m_map)
