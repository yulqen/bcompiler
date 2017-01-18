"""
Docstring here
"""
import csv
import fnmatch
import logging
import os

from datetime import date, datetime
from math import isclose

from bcompiler.datamap import DatamapGMPP

from openpyxl import load_workbook
from openpyxl.styles import PatternFill

logger = logging.getLogger('bcompiler.utils')

rdel_cdel_merge = ''



def quick_typechecker(*args):
    """
    Very simple function to filter allowed types (int, float). Any other type
    returns False. All arguments must be of same type.
    """
    for arg in args:
        if isinstance(arg, (int, float, date)):
            pass
        else:
            return False
    return True


def simple_round(fl, prec):
    """Rounds a fl to prec precision."""
    return round(fl, prec)


def bc_is_close(x, y):
    """Returns true if acceptably close."""
    if isinstance(x, (date, datetime)) or isinstance(y, (date, datetime)):
        return False
    else:
        return isclose(x, y, rel_tol=0.001)


def cell_bg_colour(rgb=[]):
    """
    Give it a list of integers between 0 and 255 - three of them.
    """
    c_value = "{0:02X}{1:02X}{2:02X}".format(*rgb)
    return PatternFill(
        patternType='solid',
        fgColor=c_value,
        bgColor=c_value
    )


def populate_blank_gmpp_form(openpyxl_template, project):
    blank = openpyxl_template
    dm = DatamapGMPP(
        '/home/lemon/Documents/bcompiler/source/datamap-master-to-gmpp')
    logger.info("Grabbing GMPP datamap {}".format(dm.source_file))
    target_ws = blank['GMPP Return']
    project_data = project_data_line()
    logger.info("Grabbing project_data from master")
    for line in dm.data:
        if 'Project/Programme Name' in line.cellname:
            d_to_migrate = project
            target_ws[line.cellref].value = d_to_migrate
        elif line.cellref is not None:
            try:
                d_to_migrate = project_data[project][line.cellname]
            except KeyError:
                logger.warning("Unable to find {} in master.csv".format(
                    line.cellref))
                target_ws[line.cellref].value = "UNDEFINED IN DATAMAP"
            else:
                target_ws[line.cellref].value = d_to_migrate
                logger.debug(
                    "Migrating {} from {} to blank template".format(
                        d_to_migrate, line.cellref))
    # inject additonal data
    additional_data = dm.add_additional_data()
    for line in additional_data:
        target_ws[line.cellref].value = line.added_data_field
    fn = OUTPUT_DIR + project + ' Q3_GMPP.xlsx'
    logger.info("Writing {}".format(fn))
    blank.save(fn)


def project_data_line():
    p_dict = {}
    with open(SOURCE_DIR + 'master_transposed.csv', 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            key = row.pop('Project/Programme Name')
            if key in p_dict:
                pass
            p_dict[key] = row
            logger.debug(
                "Adding {} to project_data_line dictionary".format(key))
    return p_dict


def gmpp_project_data():
    data = project_data_line()
    gmpp_project_data_list = []
    for project in data:
        if data[project]['GMPP (GMPP – formally joined GMPP)']:
            gmpp_project_data_list.append(data[project])
    return gmpp_project_data_list


def gmpp_project_names():
    data = project_data_line()
    return [project for project in data if data[project][
        'GMPP (GMPP – formally joined GMPP)']]


def open_openpyxl_template(template_file):
    """
    Opens an xlsx file (the template) and returns the openpyxl object.
    """
    wb = load_workbook(template_file, keep_vba=True)
    logger.info("Opening {} as an openpyxl object".format(template_file))
    return wb


def working_directory(dir_type=None):
    """
    Returns the working direct for source files
    :return: path to the working directory intended for the source files
    """
    docs = os.path.join(os.path.expanduser('~'), 'Documents')
    try:
        bcomp_working_d = 'bcompiler'
    except FileNotFoundError:
        print("You need to run with --create-wd to",
              "create the working directory")
    root_path = os.path.join(docs, bcomp_working_d)
    if dir_type == 'source':
        return root_path + "/source/"
    elif dir_type == 'output':
        return root_path + "/output/"
    elif dir_type == 'returns':
        return root_path + "/source/returns/"
    else:
        return


SOURCE_DIR = working_directory('source')
OUTPUT_DIR = working_directory('output')
RETURNS_DIR = working_directory('returns')
DATAMAP_RETURN_TO_MASTER = SOURCE_DIR + 'datamap-returns-to-master'
DATAMAP_MASTER_TO_RETURN = SOURCE_DIR + 'datamap-master-to-returns'
DATAMAP_MASTER_TO_GMPP = SOURCE_DIR + 'datamap-master-to-gmpp'
CLEANED_DATAMAP = SOURCE_DIR + 'cleaned_datamap'
MASTER = SOURCE_DIR + 'master.csv'
TEMPLATE = SOURCE_DIR + 'bicc_template.xlsx'
GMPP_TEMPLATE = SOURCE_DIR + 'gmpp_template.xlsx'


def index_returns_directory():
    """
    Prior to compiling a master, it is useful to get the order of projects
    by their file name, as the compile.run() function traverses the directory
    top to bottom to build the master. We can then use this to compare with the
    order or projects (columns) in the old master document we are comparing
    the current compile. This is pretty hackish but needs must...
    """
    target_files = []
    for f in os.listdir(RETURNS_DIR):
        target_files.append(f)

    pnames_in_returns_dir = []
    for f in target_files:
        if fnmatch.fnmatch(f, '*.xlsx'):
            wb = load_workbook(os.path.join(RETURNS_DIR, f))
            ws = wb['Summary']
            pnames_in_returns_dir.append(ws['B5'].value)
    return pnames_in_returns_dir

def parse_csv_to_file(source_file):
    """
    Transposes the master to a new master_transposed.csv file.
    :param source_file:
    :return:
    """
    output = open(SOURCE_DIR + 'master_transposed.csv', 'w+')
    with open(source_file, 'r') as source_f:
        lis = [x.split(',') for x in source_f]
        for i in lis:
            # we need to do this to remove trailing "\n" from the end of
            # each original master.csv line
            i[-1] = i[-1].rstrip()

    for x in zip(*lis):
        for y in x:
            output.write(y + ',')
        output.write('\n')
    output.close()


def create_master_dict_transposed(source_master_csv):
    """
    The side-effect of the following function is to ensure there is a
    'master_transposed.csv' file present in SOURCE_DIR
    returns a list of dicts, which makes up all the data from the master
    """
    parse_csv_to_file(source_master_csv)
    with open(SOURCE_DIR + 'master_transposed.csv', 'r') as f:
        r = csv.DictReader(f)
        ls = [row for row in r]
    return ls


VALIDATION_REFERENCES = {
    'Quarter': "=\'Dropdown List\'!$A$2:$A$9",
    'Joining Qtr': "=\'Dropdown List\'!$B$2:$B$25",
    'Classification': "=\'Dropdown List\'!$C$2:$C$4",
    'Agency': "=\'Dropdown List\'!$D$2:$D$7",
    'DfT Group': "=\'Dropdown List\'!$E$2:$E$7",
    'Delivery Structure': "=\'Dropdown List\'!$F$2:$F$7",
    'Methodology': "=\'Dropdown List\'!$G$2:$G$10",
    'Category': "=\'Dropdown List\'!$H$2:$H$7",
    'Scope Changed': "=\'Dropdown List\'!$I$2:$I$4",
    'Monetised / Non Monetised Benefits': "=\'Dropdown List\'!$J$2:$J$4",
    'SDP': "=\'Dropdown List\'!$K$2:$K$5",
    'RAG': "=\'Dropdown List\'!$L$2:$L$7",
    'RAG_Short': "=\'Dropdown List\'!$M$2:$M$4",
    'RPA level': "=\'Dropdown List\'!$N$2:$N$4",
    'MPLA / PLP': "=\'Dropdown List\'!$O$2:$O$29",
    'Yes/No': "=\'Dropdown List\'!$P$2:$P$3",
    'PD Changes': "=\'Dropdown List\'!$Q$2:$Q$31",
    'Capability RAG': "=\'Dropdown List\'!$R$2:$R$5",
    'Business Cases': "=\'Dropdown List\'!$S$2:$S$11",
    'Milestone Types': "=\'Dropdown List\'!$T$2:$T$4",
    'Finance figures format': "=\'Dropdown List\'!$U2:$U$3",
    'Index Years': "=\'Dropdown List\'!$V2:$V$27",
    'Discount Rate': "=\'Dropdown List\'!$W2:$W$32",
    'Finance type': "=\'Dropdown List\'!$X2:$X$6",
    'Years (Spend)': "=\'Dropdown List\'!$Y2:$Y$89",
    'Years (Benefits)': "=\'Dropdown List\'!$Z2:$Z$91",
    'Snapshot Dates': "=\'Dropdown List\'!$AA2:$AA$5",
    'Percentage of time spent on SRO role': "=\'Dropdown List\'!$AB2:$AB$21",
    'Project Classification': "=\'Dropdown List\'!$AC2:$AC$5",
    'Project': "=\'Dropdown List\'!$AD2:$AD$10",
    'Programme': "=\'Dropdown List\'!$AE2:$AE$7",
    'Other': "=\'Dropdown List\'!$AF2:$AF$19",
    'VFM': "=\'Dropdown List\'!$AG2:$AG$11",
    'Count': "=\'Dropdown List\'!$AH2:$AH$22",
    'DfT Division': "=\'Dropdown List\'!$AI2:$AI$15",
    'High Speed Rail': "=\'Dropdown List\'!$AJ2:$AJ$4",
    'Rail Group': "=\'Dropdown List\'!$AK2:$AK$4",
    'Roads, Devolution & Motoring': "=\'Dropdown List\'!$AL2:$AL$5",
    'International, Security and Environment': "=\'Dropdown List\'!$AM2:$AM$4",
    'Resource and Strategy': "=\'Dropdown List\'!$AN2:$AN$2",
    'Non-Group': "=\'Dropdown List\'!$AO2:$AO$2",
    'GMPP Annual Report Category': "=\'Dropdown List\'!$AP2:$AP$2",
}

SHEETS = ['Summary', 'Finance & Benefits', 'Resources',
          'Approval & Project milestones',
          'Assurance planning']
