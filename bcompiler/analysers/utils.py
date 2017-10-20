import logging
import os
import sys

from openpyxl import load_workbook

from bcompiler.utils import ROOT_PATH, runtime_config

MASTER_XLSX = os.path.join(ROOT_PATH, runtime_config['MasterForAnalysis']['name'])
logger = logging.getLogger('bcompiler.compiler')


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
