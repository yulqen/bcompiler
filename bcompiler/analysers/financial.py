from bcompiler.core import Quarter, Master, Row

from openpyxl import load_workbook, Workbook


def run(masters_list):
    wb = Workbook()
    ws = wb.active
    q1 = Quarter(1, 2017)
    q2 = Quarter(2, 2017)
    start_row = 1
    target_keys = ['RDEL Total Forecast', 'CDEL Total Forecast']
    for m in masters_list:
        mo = Master(q1, m)
        projects = mo.projects
        for p in projects:
            p_data = mo[p]
            d = p_data.pull_keys(target_keys, flat=True)
            header = Row(2, start_row + 1, target_keys)
            r = Row(2, start_row + 2, d)
            ws.cell(row=start_row + 2, column=1, value=str(mo.quarter))
            header.bind(ws)
            r.bind(ws)
            ws.cell(row=start_row, column=1, value=p)
            start_row += 3
    wb.save('/tmp/baws.xlsx')



if __name__ == '__main__':
    run([
        '/home/lemon/Documents/bcompiler/compiled_master_2017-07-18_Q1 Apr - Jun 2017 FOR Q2 COMMISSION DO NOT CHANGE.xlsx']
        )
#   run([
#       '/home/lemon/Documents/bcompiler/compiled_master_2017-07-18_Q1 Apr - Jun 2017 FOR Q2 COMMISSION DO NOT CHANGE.xlsx',
#       '/home/lemon/Documents/bcompiler/1718_Q2_master.xlsx']
#       )
