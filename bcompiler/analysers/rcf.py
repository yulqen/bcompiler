# rcf.py
"""
Analyser to do Reference Class Forecasting on master documents.
"""

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


def run(master_repository):
    import pdb; pdb.set_trace()  # XXX BREAKPOINT
    wb = Workbook()
    ws = wb.active
    for f in master_repository.listdir():
        d = create_rcf_output(f)

        # create a header row first off
        h_keys = _main_keys(d)

        # then take a project at a time
        for proj in h_keys:
            d_row = []
            Row(2, 2, _headers(proj, d)).bind(ws)
            d_row.append(str(d[0]))
            for x in _vals(proj, d):
                d_row.append(x)
            Row(1, 3, d_row).bind(ws)
            wb.save('/tmp/testes.xlsx')
