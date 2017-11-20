import os

import sys

from bcompiler.core import Quarter, Master, Row
from ..utils import logger, ROOT_PATH

from openpyxl import load_workbook, Workbook


def _replace_underscore(name: str):
    return name.replace('/', '_')


def run(masters_repository_dir, output_path=None):
    wb = Workbook()

    q1 = Quarter(1, 2017)
    q2 = Quarter(2, 2017)


    master_q1 = Master(q1, os.path.join(masters_repository_dir, 'compiled_master_2017-07-18_Q1 Apr - Jun 2017 FOR Q2 COMMISSION DO NOT CHANGE.xlsx'))
    master_q2 = Master(q2, os.path.join(masters_repository_dir, '1718_Q2_master.xlsx'))
    target_keys = ['RDEL Total Forecast', 'CDEL Total Forecast']

    # projects from latest master
    projects = master_q2.projects


    # set up sheets
    for p in projects:
        try:
            ws = wb.create_sheet(_replace_underscore(p))
            start_row = 1
        except AttributeError:
            continue
        else:
            ws.cell(row=start_row, column=1, value=p)
            header = Row(2, start_row + 1, target_keys)
            header.bind(ws)

        for m in [master_q1, master_q2]:
            try:
                p_data = m[p]
            except KeyError:
                logger.warning(f"Cannot find {p}")
                continue
            d = p_data.pull_keys(target_keys, flat=True)
            ws.cell(row=start_row + 2, column=1, value=str(m.quarter))
            r = Row(2, start_row + 2, d)
            r.bind(ws)

            start_row += 1

    if output_path:
        wb.save(os.path.join(output_path[0], 'financial_analysis.xlsx'))
        logger.info(f"Saved financial_analysis.xlsx to {output_path}")
    else:
        output_path = os.path.join(ROOT_PATH, 'output')
        wb.save(os.path.join(output_path, 'financial_analysis.xlsx'))
        logger.info(f"Saved financial_analysis.xlsx to {output_path}")


if __name__ == '__main__':
    run('/tmp/master_repo')
