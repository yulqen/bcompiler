import csv

CSV_FILE = '/home/lemon/Documents/bcompiler/source/master_transposed.csv'


def get_approval_dates_for_project(project: str, csv_file: str) -> tuple:
    reader = csv.DictReader(csv_file)
    with open(csv_file, 'r') as f:
        reader = csv.DictReader(f)
        d = {}
        for line in reader:
            if line['Project/Programme Name'] == project:
                d['mm1'] = dict(
                    type=line['Approval MM1'],
                    date=line['Approval MM1 Forecast / Actual'],
                    position=1)
                d['mm2'] = dict(
                    type=line['Approval MM2'],
                    date=line['Approval MM2 Forecast / Actual'],
                    position=1)
                d['mm3'] = dict(
                    type=line['Approval MM3'],
                    date=line['Approval MM3 Forecast / Actual'],
                    position=1)
                d['mm4'] = dict(
                    type=line['Approval MM4'],
                    date=line['Approval MM4 Forecast / Actual'],
                    position=1)
                d['mm5'] = dict(
                    type=line['Approval MM5'],
                    date=line['Approval MM5 Forecast / Actual'],
                    position=1)
                d['mm6'] = dict(
                    type=line['Approval MM6'],
                    date=line['Approval MM6 Forecast / Actual'],
                    position=1)
                d['mm7'] = dict(
                    type=line['Approval MM7'],
                    date=line['Approval MM7 Forecast / Actual'],
                    position=1)
                d['mm8'] = dict(
                    type=line['Approval MM8'],
                    date=line['Approval MM8 Forecast / Actual'],
                    position=1)
                d['mm9'] = dict(
                    type=line['Approval MM9'],
                    date=line['Approval MM9 Forecast / Actual'],
                    position=1)
                d['mm10'] = dict(
                    type=line['Approval MM10'],
                    date=line['Approval MM10 Forecast / Actual'],
                    position=1)
                d['mm11'] = dict(
                    type=line['Approval MM11'],
                    date=line['Approval MM11 Forecast / Actual'],
                    position=1)
        return project, d


def get_project_names(csv_file: str) -> list:
    with open(csv_file, 'r') as f:
        reader = csv.DictReader(f)
        p_names = [item['Project/Programme Name'] for item in reader]
        return p_names


def write_to_csv(project_data: tuple) -> None:
    pd = project_data[0]
    with open('/home/lemon/Desktop/{}.csv'.format(pd), 'w') as csv_file:
        fieldnames = ['Project Milestone', 'Date', 'Position']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        for item in project_data[1].items():
            writer.writerow({
                'Project Milestone': item[1]['type'],
                'Date': item[1]['date'],
                'Position': 1
            })


for p in get_project_names(CSV_FILE):
    data = get_approval_dates_for_project(p, CSV_FILE)
    write_to_csv(data)
