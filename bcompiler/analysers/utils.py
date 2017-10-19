import logging
import os

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
   wb = load_workbook(master)
   ws = wb.active
   top_row = ws.iter_cols(min_row=1, max_col=ws.max_column, max_row=1)
   return len(list(top_row)), list(top_row)
