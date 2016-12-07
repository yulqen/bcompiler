"""
Copyright (c) 2016 Matthew Lemon

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy,  modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the  Software is
furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
IN THE SOFTWARE. """

import argparse
import colorlog
import logging
import os
import re
import shutil
import sys

import bcompiler.compile as compile_returns

from bcompiler import __version__
from bcompiler.utils import VALIDATION_REFERENCES
from bcompiler.utils import SOURCE_DIR, OUTPUT_DIR, DATAMAP_MASTER_TO_RETURN
from bcompiler.utils import CLEANED_DATAMAP, GMPP_TEMPLATE
from bcompiler.utils import working_directory, DATAMAP_RETURN_TO_MASTER
from bcompiler.utils import project_data_line, populate_blank_gmpp_form
from bcompiler.utils import open_openpyxl_template
from bcompiler.utils import gmpp_project_names
from bcompiler.pipelines.master_returns import parse_csv_to_file
from bcompiler.pipelines.master_returns import create_master_dict_transposed
from bcompiler.process import Cleanser
from openpyxl import load_workbook
from openpyxl.worksheet.datavalidation import DataValidation


logger = colorlog.getLogger('bcompiler')
logger.setLevel(logging.DEBUG)


def get_parser():
    parser = argparse.ArgumentParser(
        description='Compile BICC data or prepare Excel BICC return forms.')
    parser.add_argument(
        '-c', '--clean-datamap',
        action="store_true",
        dest="clean-datamap",
        help='clean datamap file whose path is given as string')
    parser.add_argument(
        '-v', '--version',
        action="store_true",
        help='displays the current version of bcompiler')
    parser.add_argument(
        '-p', '--parse',
        dest='parse',
        metavar='source file',
        nargs=1,
        help='parse master.csv and flip to correct orientation')
    parser.add_argument(
        '-b', '--populate-bicc-form',
        dest='populate',
        metavar='project integer',
        help='populate blank bicc forms from master for project N')
    parser.add_argument(
        '-g', '--populate-gmpp-form',
        dest='populate-gmpp',
        metavar='project title',
        help='populate blank gmpp forms from master for project N')
    parser.add_argument(
        '-j', '--populate-all-gmpp',
        action="store_true",
        dest='populate-all-gmpp',
        help='populate blank gmpp forms from master for all projects')
    parser.add_argument(
        '-a', '--all',
        action="store_true")
    parser.add_argument(
        '-d', '--create-wd',
        action="store_true",
        dest='create-wd',
        help='create working directory at $HOME/Documents/bcompiler')
    parser.add_argument(
        '-f', '--force-create-wd',
        action="store_true",
        dest='f-create-wd',
        help='remove existing working directory and create a new one')
    parser.add_argument(
        '--compile',
        action="store_true",
        dest='compile',
        help='compile returns to master')
    parser.add_argument(
        '-ll', '--loglevel',
        type=str,
        choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'],
        help=(
            'Set the logging level for the console.'
            'The log file is set to DEBUG.'))
    return parser


def clean_datamap(dm_file):
    """
    Used for its side-effects only which isn't ideal, but this isn't
    Haskell, so why not?
    """
    logger.info("Cleaning {}.".format(dm_file))
    cleaned_datamap_file = CLEANED_DATAMAP
    try:
        os.remove(cleaned_datamap_file)
    except FileNotFoundError:
        pass
    cleaned_datamap = open(cleaned_datamap_file, 'a+')
    with open(dm_file, 'r', encoding='UTF-8') as f:
        # make sure every line has a comma at the end
        for line in f.readlines():
            newline = line.rstrip()
            if ',' in newline[-1]:
                newline += '\n'
                cleaned_datamap.write(newline)
            else:
                newline = newline + ',' + '\n'
                cleaned_datamap.write(newline)
    cleaned_datamap.close()


def get_list_projects(source_master_file):
    """
    Returns a list of Project/Programme Names.
    """
    reader = create_master_dict_transposed(source_master_file)
    pl = [row['Project/Programme Name'] for row in reader]
    return pl


def get_datamap():
    """
    The old-style datamap design, using parsing rather than creating a Datamap
    class.
    """
    cell_regex = re.compile('[A-Z]+[0-9]+')
    dropdown_headers = get_dropdown_headers()
    output_excel_map_list = []
    f = open(SOURCE_DIR + 'cleaned_datamap', 'r')
    data = f.readlines()
    for line in data:
        # split on , allowing us to access useful data from data map file
        data_map_line = line.split(',')
        if data_map_line[1] in ['Summary', 'Finance & Benefits',
                                'Resources', 'Approval & Project milestones',
                                'Assurance planning']:
            # the end item in the list is a newline - get rid of that
            del data_map_line[-1]
        if cell_regex.search(data_map_line[-1]):
            try:
                m_map = dict(
                    cell_description=data_map_line[0],
                    sheet=data_map_line[1],
                    cell_coordinates=data_map_line[2],
                    validation_header='')
            except IndexError:
                m_map = dict(
                    cell_description=data_map_line[0],
                    sheet="CAN'T FIND SHEET")
            output_excel_map_list.append(m_map)
        elif data_map_line[-1] in dropdown_headers:
            try:
                m_map = dict(
                    cell_description=data_map_line[0],
                    sheet=data_map_line[1],
                    cell_coordinates=data_map_line[2],
                    validation_header=data_map_line[3])
            except IndexError:
                logger.error(
                    "Something wrong with the datamap indexing", m_map.items())
            output_excel_map_list.append(m_map)
    return output_excel_map_list


def populate_blank_bicc_form(source_master_file, proj_num):
    logger.info("Reading datamap...")
    datamap = get_datamap()
    proj_data = project_data_line()
    logger.info("Getting list of projects...")
    ls = get_list_projects(source_master_file)
    test_proj = ls[int(proj_num)]
    logger.info("Processing project {}.".format(test_proj))
    test_proj_data = proj_data[test_proj]
    logger.info("Getting template...")
    blank = load_workbook(SOURCE_DIR + 'bicc_template.xlsx')
    ws_summary = blank['Summary']
    ws_fb = blank['Finance & Benefits']
    ws_res = blank['Resources']
    ws_apm = blank['Approval & Project milestones']
    ws_ap = blank['Assurance planning']
    logger.info("Getting data from master.csv...")
    for item in datamap:
        if item['sheet'] == 'Summary':
            if 'Project/Programme Name' in item['cell_description']:
                ws_summary[
                    item['cell_coordinates']].value = test_proj
            try:
                c = Cleanser(test_proj_data[item['cell_description']])
                cleaned = c.clean()
                logger.debug(
                    "Changed {} to {} for cell_description: {}".format(
                        test_proj_data[item['cell_description']],
                        cleaned,
                        item['cell_description'],
                        ))
                ws_summary[
                    item['cell_coordinates']].value = cleaned
            except KeyError:
                logger.error("Cannot find {} in master.csv".format(
                    item['cell_description']))
                pass
            if item['validation_header']:
                dv = create_validation(item['validation_header'])
                ws_summary.add_data_validation(dv)
                dv.add(ws_summary[item['cell_coordinates']])
        elif item['sheet'] == 'Finance & Benefits':
            try:
                c = Cleanser(test_proj_data[item['cell_description']])
                cleaned = c.clean()
                logger.debug(
                    "Changed {} to {} for cell_description: {}".format(
                        test_proj_data[item['cell_description']],
                        cleaned,
                        item['cell_description'],
                        ))
                ws_fb[
                    item['cell_coordinates']].value = cleaned
            except KeyError:
                logger.error("Cannot find {} in master.csv".format(
                    item['cell_description']))
                pass
            if item['validation_header']:
                dv = create_validation(item['validation_header'])
                ws_fb.add_data_validation(dv)
                dv.add(ws_apm[item['cell_coordinates']])
        elif item['sheet'] == 'Resources':
            try:
                c = Cleanser(test_proj_data[item['cell_description']])
                cleaned = c.clean()
                logger.debug(
                    "Changed {} to {} for cell_description: {}".format(
                        test_proj_data[item['cell_description']],
                        cleaned,
                        item['cell_description'],
                        ))
                ws_res[
                    item['cell_coordinates']].value = cleaned
            except KeyError:
                logger.error("Cannot find {} in master.csv".format(
                    item['cell_description']))
                pass
            if item['validation_header']:
                dv = create_validation(item['validation_header'])
                ws_res.add_data_validation(dv)
                dv.add(ws_apm[item['cell_coordinates']])
        elif item['sheet'] == 'Approval & Project milestones':
            try:
                c = Cleanser(test_proj_data[item['cell_description']])
                cleaned = c.clean()
                logger.debug(
                    "Changed {} to {} for cell_description: {}".format(
                        test_proj_data[item['cell_description']],
                        cleaned,
                        item['cell_description'],
                        ))
                ws_apm[
                    item['cell_coordinates']].value = cleaned
            except KeyError:
                logger.error("Cannot find {} in master.csv".format(
                    item['cell_description']))
                pass
            if item['validation_header']:
                dv = create_validation(item['validation_header'])
                ws_apm.add_data_validation(dv)
                dv.add(ws_apm[item['cell_coordinates']])
        elif item['sheet'] == 'Assurance planning':
            try:
                c = Cleanser(test_proj_data[item['cell_description']])
                cleaned = c.clean()
                logger.debug(
                    "Changed {} to {} for cell_description: {}".format(
                        test_proj_data[item['cell_description']],
                        cleaned,
                        item['cell_description'],
                        ))
                ws_ap[
                    item['cell_coordinates']].value = cleaned
            except KeyError:
                logger.error("Cannot find {} in master.csv".format(
                    item['cell_description']))
                pass
            if item['validation_header']:
                dv = create_validation(item['validation_header'])
                ws_ap.add_data_validation(dv)
                dv.add(ws_ap[item['cell_coordinates']])

    logger.info("Writing {}".format(test_proj))
    blank.save(OUTPUT_DIR + '{}_Q3_Return.xlsx'.format(test_proj))


def pop_all():
    """
    Populates the blank bicc_template file with data from the master, one
    form for each project dataset.
    """
    number_of_projects = len(get_list_projects(SOURCE_DIR + 'master.csv'))
    # we need to iterate through the master based on indexes so we use a range
    # based on the number of projects
    for p in range(number_of_projects):
        populate_blank_bicc_form(SOURCE_DIR + 'master.csv', p)


def check_for_correct_source_files():
    docs = os.path.join(os.path.expanduser('~'), 'Documents')
    bcomp_working_d = 'bcompiler'
    if not os.path.exists(os.path.join(docs, bcomp_working_d)):
        print("No working directory set up. Creating working directory.")
        create_working_directory()
        print("Please ensure the correct source files are installed:\n"
              "\t\tsource/bicc_template.xlsx\n"
              "\t\tsource/master.csv\n"
              "\t\tsource/datamap-master-to-returns\n")
        sys.exit()
    else:
        return


def create_working_directory():
    """
    We need a proper directory to work in.
    :return:
    """
    docs = os.path.join(os.path.expanduser('~'), 'Documents')
    bcomp_working_d = 'bcompiler'
    root_path = os.path.join(docs, bcomp_working_d)
    folders = ['source', 'output']
    if not os.path.exists(root_path):
        os.mkdir(root_path)
        for folder in folders:
            os.mkdir(os.path.join(root_path, folder))
        print("Clean working directory created at {}".format(root_path))
    else:
        print("Working directory exists. You can either run the program"
              "like this and files will be overwritten, or you should do"
              "--force-create-wd to remove the working directory and create "
              "a new one.\n\nWARNING: this will remove any datamap and "
              "master.csv files persent.")


def delete_working_directory():
    docs = os.path.join(os.path.expanduser('~'), 'Documents')
    bcomp_working_d = 'bcompiler'
    root_path = os.path.join(docs, bcomp_working_d)
    try:
        shutil.rmtree(root_path)
        return "{} deleted".format(root_path)
    except FileNotFoundError:
        return


def get_dropdown_data(header=None):
    """
    Pull the dropdown data from the Dropdown List sheet in
    bicc_template.xlsx. Location of this template file might need
    to be dynamic.
    :return tuple of column values from sheet, with header value at list[0]:
    """
    wb = load_workbook(SOURCE_DIR + 'bicc_template.xlsx', data_only=True)
    ws = wb['Dropdown List']
    columns = ws.columns
    col_lis = [col for col in columns]
    dropdown_data = [[c.value for c in t if c.value] for t in col_lis]
    if header:
        h = [h for h in dropdown_data if header in h[0]]
        h = tuple(h[0])
        # print("Getting {}".format(h))
        return h
    else:
        return dropdown_data


def get_dropdown_headers():
    wb = load_workbook(SOURCE_DIR + 'bicc_template.xlsx', data_only=True)
    ws = wb['Dropdown List']
    rows = ws.rows
    a_row = next(rows)
    return [h.value for h in a_row]


def create_validation(header):
    # if we need the regex to match the dropdown string - from pythex.org
    # dropdown_regex =
    # re.compile('"=\\'Dropdown List\\'!\$([A-Z]+)\$(\d+):\$([A-Z]+)\$(\d+)"')
    #

    try:
        f_str = VALIDATION_REFERENCES[header]
        dv = DataValidation(type='list', formula1=f_str, allow_blank=True)
        dv.prompt = "Please select from the list"
        dv.promptTitle = 'List Selection'
        return dv
    except KeyError:
        print("No validation")
        return


def main():
    parser = get_parser()
    args = vars(parser.parse_args())
    check_for_correct_source_files()
    if args['loglevel']:
        log_lev = args['loglevel']
        logger.setLevel(logging.DEBUG)
        fh = logging.FileHandler(OUTPUT_DIR + 'bcompiler.log', mode='w')
        fh.setLevel(logging.DEBUG)
        console = logging.StreamHandler()
        console.setLevel(log_lev)
        formatter = logging.Formatter('%(levelname)s - %(name)s - %(message)s')
        fh.setFormatter(formatter)
        console.setFormatter(colorlog.colorlog.ColoredFormatter())
        logger.addHandler(fh)
        logger.addHandler(console)
    else:
        logger.setLevel(logging.DEBUG)
        fh = logging.FileHandler(OUTPUT_DIR + 'bcompiler.log', mode='w')
        fh.setLevel(logging.DEBUG)
        console = logging.StreamHandler()
        console.setLevel(logging.INFO)
        formatter = logging.Formatter('%(levelname)s - %(name)s - %(message)s')
        fh.setFormatter(formatter)
        console.setFormatter(colorlog.colorlog.ColoredFormatter())
        logger.addHandler(fh)
        logger.addHandler(console)

    if args['version']:
        print("{}".format(__version__))
        return
    if args['clean-datamap']:
        # THIS NEEDS TO BE SORTED OUT. We need to be able to clean based
        # on the task (RETURN -> MASTER; MASTER -> RETURN)
        # DO WE NEED THIS FUNCTION AT ALL?
        clean_datamap(DATAMAP_RETURN_TO_MASTER)
        # clean_datamap(DATAMAP_MASTER_TO_RETURN)
        print("datamap cleaned")
        return
    if args['parse']:
        parse_csv_to_file(args['parse'][0])
        return
    if args['populate']:
        master = '{}master.csv'.format(working_directory('source'))
        clean_datamap(DATAMAP_MASTER_TO_RETURN)
        parse_csv_to_file(master)
        populate_blank_bicc_form(master, args['populate'])
        return
    if args['populate-gmpp']:
        master = '{}master.csv'.format(working_directory('source'))
        parse_csv_to_file(master)
        template_opyxl = open_openpyxl_template(GMPP_TEMPLATE)
        populate_blank_gmpp_form(template_opyxl, args['populate-gmpp'])
        return
    if args['populate-all-gmpp']:
        master = '{}master.csv'.format(working_directory('source'))
        parse_csv_to_file(master)
        template_opyxl = open_openpyxl_template(GMPP_TEMPLATE)
        gmpp_projects = gmpp_project_names()
        for project in gmpp_projects:
            populate_blank_gmpp_form(template_opyxl, project)
        return
    if args['all']:
        pop_all()
        return
    if args['create-wd']:
        create_working_directory()
        return
    if args['f-create-wd']:
        print("This will destroy your existing working directory prior to"
              "creating a new one.\n\nAre you sure?")
        response = input('(y/n) --> ')
        if response in ('y', 'ye', 'yes', 'Y', 'YES'):
            delete_working_directory()
            create_working_directory()
            return
        else:
            return
    if args['compile']:
        clean_datamap(DATAMAP_RETURN_TO_MASTER)
        compile_returns.run()


if __name__ == '__main__':
    main()
