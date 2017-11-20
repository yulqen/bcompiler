import os

import sys

from bcompiler.core import Quarter, Master, Row
from ..utils import logger, ROOT_PATH

from openpyxl import load_workbook, Workbook


def _replace_underscore(name: str):
    return name.replace('/', '_')


def run(masters_list, output_path=None):
    wb = Workbook()
    q1 = Quarter(1, 2017)
    q2 = Quarter(2, 2017)
    start_row = 1
    target_keys = ['RDEL Total Forecast', 'CDEL Total Forecast']
    for m in masters_list:
        master = Master(q1, m)
        projects = master.projects
        for p in projects:
            try:
                ws = wb.create_sheet(_replace_underscore(p))
            except AttributeError:
                continue
            p_data = master[p]
            d = p_data.pull_keys(target_keys, flat=True)
            header = Row(2, start_row + 1, target_keys)
            r = Row(2, start_row + 2, d)
            ws.cell(row=start_row + 2, column=1, value=str(master.quarter))
            header.bind(ws)
            r.bind(ws)
            ws.cell(row=start_row, column=1, value=p)
    if output_path:
        wb.save(os.path.join(output_path[0], 'financial_analysis.xlsx'))
        logger.info(f"Saved swimlane_milestones.xlsx to {output_path}")
    else:
        output_path = os.path.join(ROOT_PATH, 'output')
        wb.save(os.path.join(output_path, 'financial_analysis.xlsx'))
        logger.info(f"Saved financial_analysis.xlsx to {output_path}")


if __name__ == '__main__':
    run([
        '/home/lemon/Documents/bcompiler/compiled_master_2017-07-18_Q1 Apr - Jun 2017 FOR Q2 COMMISSION DO NOT CHANGE.xlsx']
        )
#   run([
#       '/home/lemon/Documents/bcompiler/compiled_master_2017-07-18_Q1 Apr - Jun 2017 FOR Q2 COMMISSION DO NOT CHANGE.xlsx',
#       '/home/lemon/Documents/bcompiler/1718_Q2_master.xlsx']
#       )
