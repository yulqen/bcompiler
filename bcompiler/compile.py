import fnmatch
import logging
import os
import re
from datetime import date

from bcompiler.workingdir import DATAMAP
from openpyxl import load_workbook, Workbook

cell_regex = re.compile('[A-Z]+[0-9]+')
dropdown_regex = re.compile('^\D*$')
today = date.today().isoformat()

logger = logging.getLogger('bcompiler')

DATA_MAP_FILE = DATAMAP


def get_sheet_names(source_file):
    wb = load_workbook(source_file, read_only=True)
    return wb.get_sheet_names()


def get_sheet_data(source_file):
    wb = load_workbook(source_file, read_only=True)
    ws = wb['Finance & Benefits']

    for row in ws.rows:
        for cell in row:
            if cell.value is not None:
                print(cell.value)


def get_current_quarter(source_file, path):
    wb = load_workbook(path + "/source/returns/" + source_file, read_only=True)
    ws = wb['Summary']
    q = ws['G3'].value
    return q


def get_project_name(source_file):
    wb = load_workbook(source_file, read_only=True)
    ws = wb['Summary']
    cn = ws['C10'].value
    print(cn)


def parse_data_file():
    with open(DATA_MAP_FILE, 'r') as f:
        data = f.readlines()

        for line in data:
            words = line.split(',')
            print(words)


def parse_source_cells(source_file):
    """
    :param source_file: an Excel file containing project return data
    :return: a list of dict items mapping each key:value pair for the output column in GMPP's template
    """

    # first, we load the source file
    global ws
    wb = load_workbook(source_file, read_only=True, data_only=True)

    # we're going to output data from this function as a list of dict items
    output_excel_map_list = []

    # load the DATA_MAP_FILE, containing mappings to cells in the form based on key values
    # from GMPP's master template
    with open(DATA_MAP_FILE, 'r', encoding='UTF-8') as f:
        data = f.readlines()

        for line in data:
            # split on , allowing us to access useful data from data map file
            data_map_line = line.split(',')
            # if the second word in each MAP line is a named sheet from the template file, we're interested
            if data_map_line[1] in ['Summary', 'Finance & Benefits', 'Resources', 'Approval & Project milestones',
                                    'Assurance planning']:
                # the end item in the list is a newline - get rid of that
                logger.info('newline at the end of {}'.format(line.rstrip()))
                del data_map_line[-1]
                # the worksheet in the source Excel file needs to be accessible
                try:
                    ws = wb[data_map_line[1]]
                except KeyError as e:
                    print("{} has no {} sheet! - {}".format(source_file, data_map_line[1], e))
                # we only want to act query the source Excel file if there is a valid cell reference there
                # so we use a regex to do that

                # if the last entry is a cell reference
                if cell_regex.search(data_map_line[-1]):
                    try:
                        destination_kv = dict(gmpp_key=data_map_line[0], gmpp_key_value=ws[data_map_line[-1]].value)
                    except IndexError:
                        destination_kv = dict(gmpp_key=data_map_line[0], gmpp_key_value="OUT OF BOUNDS!")
                    output_excel_map_list.append(destination_kv)

                # or if the last entry is likely dropdown text and the preceeding text is a cell reference...
                elif cell_regex.search(data_map_line[-2]) and dropdown_regex.search(data_map_line[-1]):
                    try:
                        destination_kv = dict(gmpp_key=data_map_line[0], gmpp_key_value=ws[data_map_line[-2]].value)
                    except IndexError:
                        destination_kv = dict(gmpp_key=data_map_line[0], gmpp_key_value="OUT OF BOUNDS!")
                    output_excel_map_list.append(destination_kv)

            # if the DATA_MAP doesn't suggest the data is sourced in the template Excel, we just want to
            # take the default data we have entered there (e.g. 'michelle dawson' as default)
            # OR we return an empty string if there is no data
            else:
                # the end item in the list is a newline - get rid of that
                del data_map_line[-1]
                if len(data_map_line) > 1:
                    destination_kv = dict(gmpp_key=data_map_line[0], gmpp_key_value=data_map_line[-1])
                # if the list has only one item, that means there is no data entered, so we want the value to
                # be an empty string for now
                else:
                    destination_kv = dict(gmpp_key=data_map_line[0], gmpp_key_value="")
                output_excel_map_list.append(destination_kv)

    return output_excel_map_list


# noinspection PyTypeChecker,PyTypeChecker,PyTypeChecker
def write_excel(source_file, count, workbook):
    # count is used to count number of times function is run so that multiple returns can be added
    # and not overwrite the GMPP key column
    # let's create an Excel file in memory
    # it will have one worksheet - let's get it
    ws = workbook.active
    # give it a title
    ws.title = "Constructed BICC Data Master"

    out_map = parse_source_cells(source_file)
    if count == 1:
        i = 1
        for d in out_map:
            c = ws.cell(row=i, column=1)
            c.value = d['gmpp_key']
            i += 1
        i = 1
        for d in out_map:
            c = ws.cell(row=i, column=2)
            c.value = d['gmpp_key_value']
            i += 1
    else:
        i = 1
        for d in out_map:
            c = ws.cell(row=i, column=count + 1)
            c.value = d['gmpp_key_value']
            i += 1


def run():
    workbook = Workbook()

    docs = os.path.join(os.path.expanduser('~'), 'Documents')
    try:
        bcomp_working_d = 'bcompiler'
    except FileNotFoundError:
        print("You need to run with --create-wd to create the working directory")
    root_path = os.path.join(docs, bcomp_working_d)
    count = 1
    for file in os.listdir(os.path.join(root_path, 'source/returns')):
        if fnmatch.fnmatch(file, '*.xlsx'):
            print("Processing {}".format(file))
            write_excel((root_path + '/source/returns/' + file), count=count, workbook=workbook)
            count += 1
    for file in os.listdir(os.path.join(root_path, 'source/returns')):
        cq = get_current_quarter(file, root_path)
        if cq is not None:
            break
    OUTPUT_FILE = '{}/output/compiled_master_{}_{}.xlsx'.format(root_path, today, cq)
    workbook.save(OUTPUT_FILE)
