import argparse
import csv
import os
import re

from openpyxl import load_workbook


def get_parser():
    parser = argparse.ArgumentParser(description='Compile BICC data or prepare Excel BICC return forms.')
    parser.add_argument('-c', '--clean-datamap', dest='datamap', nargs=1, help='clean datamap file'
                                                                                     'whose path is given as string')
    parser.add_argument('-v', '--version', help='displays the current version of bcompiler', action="store_true")
    parser.add_argument('-p', '--parse', dest='parse', nargs=1, help='parse master.csv and flip'
                                                                     ' to correct orientation')
    parser.add_argument('-b', '--populate-blanks', dest='populate', help='populate blank bicc forms from master')
    return parser

def _clean_datamap(source_file):

    CLEANED_DATAMAP_FILE = 'source_files/cleaned_datamap'
    try:
        os.remove(CLEANED_DATAMAP_FILE)
    except FileNotFoundError:
        pass
    cleaned_datamap = open(CLEANED_DATAMAP_FILE, 'a+')
    with open(source_file, 'r', encoding='UTF-8') as f:
        # make sure every line has a comma at the end
        for line in f.readlines():
            newline = line.rstrip()
            if ',' in newline[-1]:
                newline = newline + '\n'
                cleaned_datamap.write(newline)
            else:
                newline = newline + ',' + '\n'
                cleaned_datamap.write(newline)


def _parse_csv_to_file(source_file):
    """
    Transposes the master to a new master_transposed.csv file.
    :param source_file:
    :return:
    """
    output = open('source_files/master_transposed.csv', 'w+')
    with open(source_file, 'r') as source_f:
        lis = [x.split(',') for x in source_f]
        for i in lis:
            # we need to do this to remove trailing "\n" from the end of each original master.csv line
            i[-1] = i[-1].rstrip()

    for x in zip(*lis):
        for y in x:
            output.write(y + ',')
        output.write('\n')


def create_master_dict_transposed(source_master_csv):
    _parse_csv_to_file(source_master_csv)
    with open('source_files/master_transposed.csv', 'r') as f:
        r = csv.DictReader(f)
        l = [row for row in r]
    return l


def _get_list_projects(source_master_file):
    reader = create_master_dict_transposed(source_master_file)
    pl = [row['Project Name'] for row in reader]
    return pl

def get_datamap():
    cell_regex = re.compile('[A-Z]+[0-9]+')
    output_excel_map_list = []
    f = open('source_files/cleaned_datamap', 'r')
    data = f.readlines()
    for line in data:
        # split on , allowing us to access useful data from data map file
        data_map_line = line.split(',')
        if data_map_line[1] in ['Summary', 'Finance & Benefits', 'Resources', 'Approval and Project milestones',
                                'Assurance planning']:
            # the end item in the list is a newline - get rid of that
            del data_map_line[-1]
        if cell_regex.search(data_map_line[-1]):
            try:
                m_map = dict(cell_description=data_map_line[0],
                             sheet=data_map_line[1],
                             cell_coordinates=data_map_line[2])
            except IndexError:
                m_map = dict(cell_description=data_map_line[0],
                             sheet="CAN'T FIND SHEET")
            output_excel_map_list.append(m_map)
    return output_excel_map_list

def project_data_line():
    dict = {}
    with open('source_files/master_transposed.csv', 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            key = row.pop('Project Name')
            if key in dict:
                pass
            dict[key] = row
    return dict


def populate_blank_bicc_form(source_master_file):
    datamap = get_datamap()
    proj_data = project_data_line()
    ls = _get_list_projects(source_master_file)
    test_proj = ls[0]
    test_proj_data = proj_data[test_proj]
    blank = load_workbook('source_files/bicc_template.xlsx')
    ws_summary = blank.get_sheet_by_name('Summary')
    for item in datamap:
        if item['sheet'] == 'Summary':
            try:
                ws_summary[item['cell_coordinates']].value = test_proj_data[item['cell_description']]
            except KeyError:
                print("Cannot find {} in master.csv".format(item['cell_description']))
                pass
    blank.save('source_files/{}.xlsx'.format(test_proj))






def main():
    parser = get_parser()
    args = vars(parser.parse_args())
    if args['version']:
        print("1.0")
        return
    if args['datamap']:
        _clean_datamap(args['datamap'][0])
        print("{} cleaned".format(args['datamap'][0]))
        return
    if args['parse']:
        _parse_csv_to_file(args['parse'][0])
        return
    if args['populate']:
        populate_blank_bicc_form('source_files/master.csv')
        return

if __name__ == '__main__':
    main()