# rcf.py
"""
Analyser to do Reference Class Forecasting on master documents.
"""
import operator

from typing import List, Tuple, Dict

from pathlib import PurePath
from openpyxl import load_workbook, Workbook

from ..utils import project_data_from_master
from ..core import Quarter, Master, Row


cells_we_want_to_capture = ['Reporting period (GMPP - Snapshot Date)',
                            'Approval MM1',
                            'Approval MM1 Forecast / Actual',
                            'Approval MM3',
                            'Approval MM3 Forecast / Actual',
                            'Approval MM10'
                            'Approval MM10 Forecast / Actual',
                            'Project MM18',
                            'Project MM18 Forecast - Actual',
                            'Project MM19',
                            'Project MM19 Forecast - Actual',
                            'Project MM20',
                            'Project MM20 Forecast - Actual',
                            'Project MM21',
                            'Project MM21 Forecast - Actual']


def _process_masters(path: PurePath) -> Tuple[Quarter, Dict[str, Tuple]]:
    hold = {}
    year = path.strpath[-9:][:4]
    quarter = path.strpath[-11]
    q = Quarter(int(quarter), int(year))
    m = Master(q, path.strpath)
    for p in m.projects:
        pd = m[p]
        hold[p] = pd.pull_keys(cells_we_want_to_capture)
    return q, hold



def create_rcf_output(path: PurePath):
    return _process_masters(path)


def _main_keys(dictionary) -> list:
    return [k for k, _ in dictionary[1].items()]


def _headers(p_name: str, dictionary):
    return [x[0] for x in dictionary[1][p_name]]


def _vals(p_name: str, dictionary):
    return [x[1] for x in dictionary[1][p_name]]


def _inject(lst: list, op, place: int, idxa: int, idxb: int) -> list:
    lst[place] = op(lst[idxa], lst[idxb])
    return lst


def _insert_gaps(lst: list, indices: list) -> list:
    for x in indices:
        lst.insert(x, None)
    return lst


def run(master_repository):
    wb = Workbook()
    ws = wb.active
    for f in master_repository.listdir():
        d = create_rcf_output(f)

        # create a header row first off
        h_keys = _main_keys(d)

        # then take a project at a time
        import pdb; pdb.set_trace()  # XXX BREAKPOINT
        for proj in h_keys:
            h_row = _headers(proj, d)
            _insert_gaps(h_row, [3, 6, 9, 12, 15, 18, 21])
            Row(2, 2, h_row).bind(ws)

            d_row = []
            for x in _vals(proj, d):
                d_row.append(x)
            _insert_gaps(d_row, [3, 6, 9, 12, 15, 18, 21])
            _inject(d_row, operator.sub, 3, 2, 11)
            Row(2, 3, d_row).bind(ws)
            wb.save('/tmp/testes.xlsx')
