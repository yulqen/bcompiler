from bcmaster import BCMasterCSV
from datamap import DataMap
from openpyxl import load_workbook, Workbook
import csv
import re

cell_regex = re.compile('[A-Z]+[0-9]+')

m = BCMasterCSV('source_files/master.csv', as_dataframe=True)
m.flip()

dm = DataMap('source_files/datamap')

