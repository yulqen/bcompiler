"""
Docstring here
"""
import csv
import logging
import os

from bcompiler.datamap import DatamapGMPP

from openpyxl import load_workbook

logger = logging.getLogger('bcompiler.utils')

rdel_cdel_merge = ''


def populate_blank_gmpp_form(openpyxl_template, project):
    blank = openpyxl_template
    dm = DatamapGMPP(
        '/home/lemon/Documents/bcompiler/source/datamap-master-to-gmpp')
    logger.info("Grabbing GMPP datamap {}".format(dm.source_file))
    target_ws = blank.get_sheet_by_name('GMPP Return')
    project_data = project_data_line()
    logger.info("Grabbing project_data from master")
    for line in dm.data:
        if 'Project/Programme Name' in line.cellname:
            d_to_migrate = project
            target_ws[line.cellref].value = d_to_migrate
        elif line.cellref is not None:
            d_to_migrate = project_data[project][line.cellname]
            target_ws[line.cellref].value = d_to_migrate
            logger.debug(
                "Migrating {} from {} to blank template".format(
                    d_to_migrate, line.cellref))
    # inject additonal data
    additional_data = dm.add_additional_data()
    for line in additional_data:
        target_ws[line.cellref].value = line.added_data_field
    fn = OUTPUT_DIR + project + ' Q2_GMPP.xlsx'
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
        if data[project]['GMPP'] == 'Yes':
            gmpp_project_data_list.append(data[project])
    return gmpp_project_data_list


def gmpp_project_names():
    data = project_data_line()
    return [project for project in data if data[project]['GMPP'] == 'Yes']


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


VALIDATION_REFERENCES = {
    'Quarter': "=\'Dropdown List\'!$A$2:$A$9",
    'Joining Qtr': "=\'Dropdown List\'!$B$2:$B$25",
    'Classification': "=\'Dropdown List\'!$C$2:$C$4",
    'Agencies': "=\'Dropdown List\'!$D$2:$D$7",
    'Group': "=\'Dropdown List\'!$E$2:$E$7",
    'DfT Division': "=\'Dropdown List\'!$F$2:$F$13",
    'Entity': "=\'Dropdown List\'!$G$2:$G$4",
    'Methodology': "=\'Dropdown List\'!$H$2:$H$10",
    'Category': "=\'Dropdown List\'!$I$2:$I$7",
    'Scope Changed': "=\'Dropdown List\'!$J$2:$J$4",
    'Monetised / Non Monetised Benefits': "=\'Dropdown List\'!$K$2:$K$4",
    'SDP': "=\'Dropdown List\'!$L$2:$L$5",
    'RAG': "=\'Dropdown List\'!$M$2:$M$7",
    'RAG_Short': "=\'Dropdown List\'!$N$2:$N$4",
    'RPA': "=\'Dropdown List\'!$O$2:$O$4",
    'MPLA / PLP': "=\'Dropdown List\'!$P$2:$P$29",
    'Yes/No': "=\'Dropdown List\'!$Q$2:$Q$3",
    'PL Changes': "=\'Dropdown List\'!$R$2:$R$31",
    'Capability RAG': "=\'Dropdown List\'!$S$2:$S$5",
    'Stage': "=\'Dropdown List\'!$T$2:$T$10",
    'Business Cases': "=\'Dropdown List\'!$U$2:$U$10",
    'Milestone Types': "=\'Dropdown List\'!$V$2:$V$4",
    'Finance figures format': "=\'Dropdown List\'!$W2:$W$3",
    'Index Years': "=\'Dropdown List\'!$X2:$X$27",
    'Discount Rate': "=\'Dropdown List\'!$Y2:$Y$32",
    'Finance type': "=\'Dropdown List\'!$Z2:$Z$6",
    'Years (Spend)': "=\'Dropdown List\'!$AC2:$AC$89",
    'Years (Benefits)': "=\'Dropdown List\'!$AD2:$AD$91",
    'Snapshot Dates': "=\'Dropdown List\'!$AE2:$AE$5",
    'Percentage of time spent on SRO role': "=\'Dropdown List\'!$AF2:$AF$21",
    'AR Category': "=\'Dropdown List\'!$AG2:$AG$5",
    'Project': "=\'Dropdown List\'!$AH2:$AH$10",
    'Programme': "=\'Dropdown List\'!$AI2:$AI$7",
    'Other': "=\'Dropdown List\'!$AJ2:$AJ$19"
}

SHEETS = ['Summary', 'Finance & Benefits', 'Resources',
          'Approval & Project milestones',
          'Assurance planning']
