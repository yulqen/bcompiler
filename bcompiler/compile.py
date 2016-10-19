import fnmatch
import logging
import os
import re
from datetime import date

from bcompiler.utils import DATAMAP_RETURN_TO_MASTER, SHEETS
from bcompiler.datamap import Datamap
from openpyxl import load_workbook, Workbook

cell_regex = re.compile('[A-Z]+[0-9]+')
dropdown_regex = re.compile('^\D*$')
today = date.today().isoformat()

logger = logging.getLogger('bcompiler')

DATA_MAP_FILE = DATAMAP_RETURN_TO_MASTER


def get_current_quarter(source_file, path):
    wb = load_workbook(path + "/source/returns/" + source_file, read_only=True)
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

    docs = os.path.join(os.path.expanduser('~'), 'Documents')
    try:
        bcomp_working_d = 'bcompiler'
    except FileNotFoundError:
        print("You need to run with --create-wd to create the working directory")
    root_path = os.path.join(docs, bcomp_working_d)
    count = 1
    for file in os.listdir(os.path.join(root_path, 'source/returns')):
        if fnmatch.fnmatch(file, '*.xlsx'):
            print("Processing {}".format(file))
            write_excel((root_path + '/source/returns/' + file), count=count, workbook=workbook)
            count += 1
    for file in os.listdir(os.path.join(root_path, 'source/returns')):
        cq = get_current_quarter(file, root_path)
        if cq is not None:
            break
    OUTPUT_FILE = '{}/output/compiled_master_{}_{}.xlsx'.format(root_path, today, cq)
    workbook.save(OUTPUT_FILE)
