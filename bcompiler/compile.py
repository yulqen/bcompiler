import fnmatch
import logging
import os
import re
from datetime import date

from bcompiler.utils import DATAMAP_RETURN_TO_MASTER, SHEETS, OUTPUT_DIR
from bcompiler.datamap import Datamap
from bcompiler.utils import RETURNS_DIR
from openpyxl import load_workbook, Workbook

cell_regex = re.compile('[A-Z]+[0-9]+')
dropdown_regex = re.compile('^\D*$')
today = date.today().isoformat()

logger = logging.getLogger('bcompiler')

DATA_MAP_FILE = DATAMAP_RETURN_TO_MASTER


def get_current_quarter(source_file):
    wb = load_workbook(RETURNS_DIR + source_file, read_only=True)
    ws = wb['Summary']
    q = ws['G3'].value
    return q


def parse_source_cells(source_file, datamap_source_file):
    ls_of_dataline_dicts = []
    wb = load_workbook(source_file, read_only=True, data_only=True)
    datamap_obj = Datamap(type='returns-to-master', source_file=datamap_source_file)
    for item in datamap_obj.data:
        if item.sheet is not None:
            ws = wb[item.sheet]
            if item.cellref is not None:
                destination_kv = dict(gmpp_key=item.cellname, gmpp_key_value=str(ws[item.cellref].value).rstrip())
                ls_of_dataline_dicts.append(destination_kv)
    return ls_of_dataline_dicts


# noinspection PyTypeChecker,PyTypeChecker,PyTypeChecker
def write_excel(source_file, count, workbook):
    # count is used to count number of times function is run so that multiple returns can be added
    # and not overwrite the GMPP key column
    # let's create an Excel file in memory
    # it will have one worksheet - let's get it
    ws = workbook.active
    # give it a title
    ws.title = "Constructed BICC Data Master"

    out_map = parse_source_cells(source_file)
    if count == 1:
        i = 1
        for d in out_map:
            c = ws.cell(row=i, column=1)
            c.value = d['gmpp_key']
            i += 1
        i = 1
        for d in out_map:
            c = ws.cell(row=i, column=2)
            c.value = d['gmpp_key_value']
            i += 1
    else:
        i = 1
        for d in out_map:
            c = ws.cell(row=i, column=count + 1)
            c.value = d['gmpp_key_value']
            i += 1


def run():
    workbook = Workbook()
    count = 1
    for file in os.listdir(RETURNS_DIR):
        if fnmatch.fnmatch(file, '*.xlsx'):
            print("Processing {}".format(file))
            write_excel((RETURNS_DIR + file), count=count, workbook=workbook)
            count += 1
    for file in os.listdir(RETURNS_DIR):
        cq = get_current_quarter(file)
        if cq is not None:
            break
    OUTPUT_FILE = '{}/output/compiled_master_{}_{}.xlsx'.format(OUTPUT_DIR, today, cq)
    workbook.save(OUTPUT_FILE)
