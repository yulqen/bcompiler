import datetime
import logging
import os
import sys

from openpyxl import load_workbook

from bcompiler.utils import ROOT_PATH, runtime_config

MASTER_XLSX = os.path.join(ROOT_PATH, runtime_config['MasterForAnalysis']['name'])
logger = logging.getLogger('bcompiler.compiler')


def diff_date_list(start_date: datetime.date, end_date: datetime.date) -> list:
    """
    Return a list of date objects given start and end date objects.
    """
    return [end_date - datetime.timedelta(days=x) for x in range(0, (end_date - start_date).days)]


def get_number_of_projects(source_wb) -> int:
    """
    Simple helper function to get an accurate number of projects in a master.
    Also strips out any additional columns that openpyxl thinks exist actively
    in the spreadsheet.

    Returns an integer.
    """
    ws = source_wb.active
    top_row = next(ws.rows)  # ws.rows produces a "generator"; use next() to get next value
    top_row = list(top_row)[1:]  # we don't want the first column value
    top_row = [i.value for i in top_row if i.value is not None]  # list comprehension to remove None values
    return len(top_row)


def projects_in_master(master: str):
    """
    Return list of project titles in master.
    :type str: master
    :return:
    """
    try:
        wb = load_workbook(master)
    except FileNotFoundError:
        logger.critical("Please ensure you specify a master file in the command or use the correctly named"
                        " master file in your auxiliary directory.")
        sys.exit(1)
    ws = wb.active
    top_row = next(ws.rows)
    top_row = list(top_row)[1:]
    top_row = [i.value for i in top_row if i.value is not None]
    return len(top_row)
