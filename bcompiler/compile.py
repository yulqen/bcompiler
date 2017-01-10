"""
Initial Docstring.
"""
import fnmatch
import logging
import os
import re
from datetime import date

from bcompiler.datamap import Datamap
from bcompiler.process import Cleanser

from bcompiler.process.simple_comparitor import parse_master

from bcompiler.utils import DATAMAP_RETURN_TO_MASTER, OUTPUT_DIR, RETURNS_DIR
from openpyxl import load_workbook, Workbook

from openpyxl.styles import PatternFill, Color

CELL_REGEX = re.compile('[A-Z]+[0-9]+')
DROPDOWN_REGEX = re.compile('^\D*$')
TODAY = date.today().isoformat()

logger = logging.getLogger('bcompiler.compiler')

DATA_MAP_FILE = DATAMAP_RETURN_TO_MASTER


def get_current_quarter(source_file):
    """
    DOCSTRING HERE
    """
    wb = load_workbook(RETURNS_DIR + source_file, read_only=True)
    ws = wb['Summary']
    q = ws['G3'].value
    logger.info('Getting current Quarter as {}'.format(q))
    return q


def parse_source_cells(source_file, datamap_source_file):
    """
    Doc string in here.
    """
    ls_of_dataline_dicts = []
    wb = load_workbook(source_file, read_only=True, data_only=True)
    datamap_obj = Datamap(
        datamap_type='returns-to-master',
        source_file=datamap_source_file)
    for item in datamap_obj.data:
        # hack for importation (we have a new sheet!)
        if item.sheet is not None and item.cellref is not None:
            ws = wb[item.sheet.rstrip()]
            try:
                v = ws[item.cellref.rstrip()].value
            except IndexError:
                logger.error(
                    "Datamap wants sheet: {}; cellref: {} but this is out"
                    "of range.\n\tFile: {}".format(
                        item.sheet,
                        item.cellref,
                        source_file))
                v = ""
            else:
                if v is None:
                    logger.debug(
                        "{} in {} is empty.".format(
                            item.cellref,
                            item.sheet))
                elif type(v) == str:
                    v = v.rstrip()
                else:
                    logger.debug(
                        "{} in {} is {}".format(
                            item.cellref,
                            item.sheet,
                            v))
                try:
                    c = Cleanser(v)
                except IndexError:
                    logger.error(
                        ("Trying to clean an empty cell {} at sheet {} in {}. "
                         "Ignoring.").format(
                            item.cellref, item.sheet, source_file))
                except TypeError:
                    pass
                else:
                    v = c.clean()
            destination_kv = dict(gmpp_key=item.cellname, gmpp_key_value=v)
            ls_of_dataline_dicts.append(destination_kv)
    return ls_of_dataline_dicts


def write_excel(source_file, count, workbook, compare_workbook=None):
    """
    count is used to count number of times function is run so that multiple
    returns can be added
    and not overwrite the GMPP key column
    let's create an Excel file in memory
    it will have one worksheet - let's get it
    """
    ws = workbook.active
    # give it a title
    ws.title = "Constructed BICC Data Master"

#    if compare_workbook:
#        sc = parse_master(compare_workbook)

    out_map = parse_source_cells(source_file, DATAMAP_RETURN_TO_MASTER)
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
            rgb = [255, 0, 0]
            red = "{0:02X}{1:02X}{2:02X}".format(*rgb)
            redFill = PatternFill(
                patternType='solid',
                fgColor=red,
                bgColor=red
            )
            c.fill = redFill
            i += 1


def run():
    """
    Doc string here.
    """
    workbook = Workbook()
    count = 1
    for file in os.listdir(RETURNS_DIR):
        if fnmatch.fnmatch(file, '*.xlsx'):
            logger.info("Processing {}".format(file))
            write_excel((RETURNS_DIR + file), count=count, workbook=workbook)
            count += 1
    for file in os.listdir(RETURNS_DIR):
        cq = get_current_quarter(file)
        if cq is not None:
            break
    OUTPUT_FILE = '{}compiled_master_{}_{}.xlsx'.format(OUTPUT_DIR, TODAY, cq)
    workbook.save(OUTPUT_FILE)
