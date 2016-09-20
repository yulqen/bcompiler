from openpyxl import load_workbook, Workbook
import re
from urllib.request import urlopen
from time import sleep

DATA_MAP_FILE = 'q2_source_files/datamap'
SOURCE_MASTER = 'q2_source_files/master_test.xlsx'
wb = load_workbook(SOURCE_MASTER, read_only=True)
ws = wb['GMPP Return - DfT']
with open(DATA_MAP_FILE, 'a') as f:
    for row in ws.rows:
        celldata = row[0].value
        if celldata != None:
            print("Writing {}".format(row[0].value))
            f.write(row[0].value + ':' + '\n')

