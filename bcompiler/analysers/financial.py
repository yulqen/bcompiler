import os

from bcompiler.core import Quarter, Master, Row
from ..utils import logger, ROOT_PATH, CONFIG_FILE, runtime_config
from itertools import zip_longest

from openpyxl.chart import ScatterChart, Reference, Series
from openpyxl import Workbook
from openpyxl.drawing.line import LineProperties

runtime_config.read(CONFIG_FILE)


def _replace_underscore(name: str):
    return name.replace('/', '_')


def _color_gen():
    for c in [
        'ce5089',
        'ce5650',
        'ce50c8',
        '5050ce',
        '8f50ce',
        '508fce',
        '50ceac',
        '50b1ce',
        '50ce6d'
    ]:
        yield c


def _create_chart(worksheet):
    """Create the fucking chart"""
    chart = ScatterChart()
    chart.varyColors = True
    chart.title = "Financial Analysis"
    chart.style = 1
    chart.height = 10
    chart.width = 20
    chart.x_axis.title = "Financial Quarter"
    chart.y_axis.title = "Cost"
    chart.legend = None
    chart.x_axis.majorUnit = 0.5
    chart.x_axis.minorGridlines = None
#   chart.y_axis.majorUnit = 200

    xvalues = Reference(worksheet, min_col=1, min_row=3, max_row=6)
    picker = _color_gen()
    for i in range(2, 6):
        values = Reference(worksheet, min_col=i, min_row=2, max_row=6)
        series = Series(values, xvalues, title_from_data=True)
        series.smooth = True
        series.marker.symbol = "circle"
        lineProp = LineProperties(solidFill=next(picker))
        series.graphicalProperties.line = lineProp
        chart.series.append(series)
    worksheet.add_chart(chart, "G1")
    return worksheet


def run(masters_repository_dir, output_path=None):
    wb = Workbook()

    q1 = Quarter(1, 2017)
    q2 = Quarter(2, 2017)
    q3 = Quarter(3, 2016)
    q4 = Quarter(4, 2016)

    # TODO - we need a function in here that gleans quarter from the filename
    # of the master

    master_q1 = Master(q1, os.path.join(masters_repository_dir, 'compiled_master_2017-07-18_Q1 Apr - Jun 2017 FOR Q2 COMMISSION DO NOT CHANGE.xlsx'))
    master_q2 = Master(q2, os.path.join(masters_repository_dir, '1718_Q2_master.xlsx'))
    master_q3 = Master(q3, os.path.join(masters_repository_dir, 'compiled_master_2017-01-25_Q3 Oct  Dec 2016_FINAL.xlsx'))
    master_q4 = Master(q4, os.path.join(masters_repository_dir, 'compiled master 2017-04-20 Q4 Jan – Mar 2017_FINAL_VERSION_DO_NOT_CHANGE.xlsx'))
    target_keys = [
        'RDEL Total Forecast',
        'CDEL Total Forecast',
        'Non-Gov Total Forecast',
        'Total Forecast',
        'Total Forecast SR (20/21)'
    ]

    q3_keys = [
        'Total forecast Whole Life Cost (RDEL) (GMPP - Total)',
        'Total Forecast Whole Life Cost (CDEL) (GMPP - Total)',
        'Total Forecast Whole Life Cost (Non-Gov) (GMPP - Total)',
        'Total Forecast Whole Life Cost (GMPP - Total)',
        'Total Cost up to 2020/21- Forecast'
    ]

    q4_keys = [
        'Total Forecast Whole Life Cost (RDEL) (GMPP - Total)',
        'Total Forecast Whole Life Cost (CDEL) (GMPP - Total)',
        'Total Forecast Whole Life Cost (Non-Gov) (GMPP - Total)',
        'Total Forecast Whole Life Cost (GMPP - Total)',
        'Total Cost up to 2020/21- Forecast'
    ]

    # projects from latest master
    projects = master_q2.projects

    project_totals = {key: t for key in target_keys for t in [0]}
    project_totals = {str(q): pt for q in range(1, 5) for pt in [project_totals]}
    global_totals = {}


    std = wb.get_sheet_by_name('Sheet')
    wb.remove_sheet(std)

    def _update_total(keys: list, target_keys: list, data: list, quarter=None):
        keys, target_keys = target_keys, keys
        z = list(zip_longest(project_totals['1'].keys(), data)) # don't like the hardcode here in the key
        for t in z:
            try:
                project_totals[str(quarter)][t[0]] += t[1]
            except TypeError:
                pass



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

        for m in [master_q3, master_q4, master_q1, master_q2]:
            try:
                p_data = m[p]
            except KeyError:
                logger.warning(f"Cannot find {p}")
                continue
            if m.quarter.quarter == 1:
                d = p_data.pull_keys(target_keys, flat=True)
                _update_total(target_keys, target_keys, d, m.quarter.quarter)
            if m.quarter.quarter == 2:
                d = p_data.pull_keys(target_keys, flat=True)
                _update_total(target_keys, target_keys, d, m.quarter.quarter)
            if m.quarter.quarter == 3:
                d = p_data.pull_keys(q3_keys, flat=True)
                _update_total(q3_keys, target_keys, d, m.quarter.quarter)
            elif m.quarter.quarter == 4:
                d = p_data.pull_keys(q4_keys, flat=True)
                _update_total(q4_keys, target_keys, d, m.quarter.quarter)
            ws.cell(row=start_row + 2, column=1, value=str(m.quarter))
            r = Row(2, start_row + 2, d)
            r.bind(ws)

            start_row += 1

        global_totals[p] = project_totals
        project_totals = {key: t for key in target_keys for t in [0]}
        project_totals = {q: pt for q in range(1, 5) for pt in [project_totals]}

        _create_chart(ws)

    # create total sheet

    def _total_calc_for_all_projects(data: dict):
        pass

    total_ws = wb.create_sheet('Totals')
    start_row = 1
    ws.cell(row=start_row, column=1, value="Totals")
    header = Row(2, start_row + 1, target_keys)
    header.bind(total_ws)
    for m in [master_q3, master_q4, master_q1, master_q2]:
        total_ws.cell(row=start_row + 2, column=1, value=str(m.quarter))
        d = _total_calc_for_all_projects(global_totals)
        r = Row(2, start_row + 2, d)
        r.bind(total_ws)




    if output_path:
        wb.save(os.path.join(output_path[0], 'financial_analysis.xlsx'))
        logger.info(f"Saved financial_analysis.xlsx to {output_path}")
    else:
        output_path = os.path.join(ROOT_PATH, 'output')
        wb.save(os.path.join(output_path, 'financial_analysis.xlsx'))
        logger.info(f"Saved financial_analysis.xlsx to {output_path}")


if __name__ == '__main__':
    run('/tmp/master_repo')
