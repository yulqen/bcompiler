# rcf.py
"""
Analyser to do Reference Class Forecasting on master documents.
"""
import operator
import os
import logging
import re

from typing import List, Tuple, Dict

from pathlib import PurePath, Path
from openpyxl import load_workbook, Workbook

from ..utils import project_data_from_master
from ..core import Quarter, Master, Row

logger = logging.getLogger('bcompiler.compiler')

target_master_fn = re.compile(r'^.+_\d{4}.xlsx')

cells_we_want_to_capture = ['Reporting period (GMPP - Snapshot Date)',
                            'Approval MM1',
                            'Approval MM1 Forecast / Actual',
                            'Approval MM3',
                            'Approval MM3 Forecast / Actual',
                            'Approval MM10',
                            'Approval MM10 Forecast / Actual',
                            'Project MM18',
                            'Project MM18 Forecast - Actual',
                            'Project MM19',
                            'Project MM19 Forecast - Actual',
                            'Project MM20',
                            'Project MM20 Forecast - Actual',
                            'Project MM21',
                            'Project MM21 Forecast - Actual']


def _process_masters(path: str) -> Tuple[Quarter, Dict[str, Tuple]]:
    hold = {}
    year = path[-9:][:4]
    quarter = path[-11]
    q = Quarter(int(quarter), int(year))
    m = Master(q, path)
    for p in m.projects:
        pd = m[p]
        hold[p] = pd.pull_keys(cells_we_want_to_capture)
    return q, hold



def create_rcf_output(path: str):
    return _process_masters(path)


def _main_keys(dictionary) -> list:
    return [k for k, _ in dictionary[1].items()]


def _headers(p_name: str, dictionary):
    return [x[0] for x in dictionary[1][p_name]]


def _vals(p_name: str, dictionary):
    return [x[1] for x in dictionary[1][p_name]]


def _inject(lst: list, op, place: int, idxa: int, idxb: int) -> list:
    try:
        lst[place] = op(lst[idxa], lst[idxb])
    except TypeError:
        logger.warning(f'Can\'t calculate difference between {lst[idxa]} and {lst[idxb]}')
        return
    return lst


def _insert_gaps(lst: list, indices: list) -> list:
    for x in indices:
        lst.insert(x, None)
    return lst


def _replace_underscore(name: str):
    return name.replace('/', '_')


def _get_master_files_and_order_them(path: str):
    m = [f for f in os.listdir(path) if re.match(target_master_fn, f)]
    get_quarter = lambda x: x[-11]
    get_year = lambda x: x[-9::][:4]
    m = sorted(m, key=get_quarter)
    m = sorted(m, key=get_year)
    return m


def run(master_repository: str):
    wb = Workbook()
    ws = wb.active
    mxs = _get_master_files_and_order_them(master_repository)
    for start_row, f in list(enumerate(mxs, start=2)):
        d = create_rcf_output(os.path.join(master_repository, f))
        # create a header row first off
        project_titles = _main_keys(d)
        # then take a project at a time
        for proj in project_titles:
            h_row = _headers(proj, d)
            _insert_gaps(h_row, [3, 6, 9, 12, 15, 18, 21])
            Row(2, 2, h_row).bind(ws)

            d_row = []
            for x in _vals(proj, d):
                d_row.append(x)

            # make spaces in the row
            _insert_gaps(d_row, [3, 6, 9, 12, 15, 18, 21])

            # inject the calculations
            _inject(d_row, operator.sub, 3, 2, 11)
            _inject(d_row, operator.sub, 6, 5, 11)
            _inject(d_row, operator.sub, 9, 8, 5)
            _inject(d_row, operator.sub, 15, 14, 8)
            _inject(d_row, operator.sub, 18, 17, 15)
            _inject(d_row, operator.sub, 21, 20, 17)

            Row(2, start_row + 1, d_row).bind(ws)
            proj = ''.join([proj, ' ', str(d[0])])
            proj = _replace_underscore(proj)
            proj = proj.replace(' ', '_')
            logger.info(f"Saving {proj}_RCF.xlsx to {master_repository}")

        wb.save(os.path.join(master_repository, f'{proj}_RCF.xlsx'))

if __name__ == '__main__':
    run('/tmp/master_repo')
