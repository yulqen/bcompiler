"""
Docstring here
"""
import csv
import logging
import os

from bcompiler.datamap import DatamapGMPP

from openpyxl import load_workbook

logger = logging.getLogger('bcompiler.utils')


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
            pass
        elif line.cellref is not None:
            d_to_migrate = project_data[project][line.cellname]
            target_ws[line.cellref].value = d_to_migrate
            logger.debug(
                "Migrating {} from {} to blank template".format(
                    d_to_migrate, line.cellref))
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
    wb = load_workbook(template_file)
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
    'Quarter': '"=\'Dropdown List\'!$A$9:$A$2"',
    'Joining Qtr': "=\'Dropdown List\'!$B$25:$B$2",
    'Classification': '"=\'Dropdown List\'!$C$4:$C$2"',
    'Agencies': '"=\'Dropdown List\'!$D$7:$D$2"',
    'Group': '"=\'Dropdown List\'!$E$7:$E$2"',
    'DfT Division': '"=\'Dropdown List\'!$F$13:$F$2"',
    'Entity': '"=\'Dropdown List\'!$G$4:$G$2"',
    'Methodology': '"=\'Dropdown List\'!$H$10:$H$2"',
    'Category': '"=\'Dropdown List\'!$I$7:$I$2"',
    'Scope Changed': '"=\'Dropdown List\'!$J$4:$J$2"',
    'Monetised / Non Monetised Benefits': '"=\'Dropdown List\'!$K$4:$K$2"',
    'SDP': '"=\'Dropdown List\'!$L$5:$L$2"',
    'RAG': '"=\'Dropdown List\'!$M$7:$M$2"',
    'RAG_Short': '"=\'Dropdown List\'!$N$4:$N$2"',
    'RPA': '"=\'Dropdown List\'!$O$4:$O$2"',
    'MPLA / PLP': '"=\'Dropdown List\'!$P$29:$P$2"',
    'Yes/No': '"=\'Dropdown List\'!$Q$3:$Q$2"',
    'PL Changes': '"=\'Dropdown List\'!$R$31:$R$2"',
    'Capability RAG': '"=\'Dropdown List\'!$S$5:$S$2"',
    'Stage': '"=\'Dropdown List\'!$T$10:$T$2"',
    'Business Cases': '"=\'Dropdown List\'!$U$10:$U$2"',
    'Milestone Types': '"=\'Dropdown List\'!$V$4:$V$2"',
    'Finance figures format': '"=\'Dropdown List\'!$W3:$W$2"',
    'Index Years': '"=\'Dropdown List\'!$X27:$X$2"',
    'Discount Rate': '"=\'Dropdown List\'!$Y32:$Y$2"',
    'Finance type': '"=\'Dropdown List\'!$Z6:$Z$2"',
    'Years (Spend)': '"=\'Dropdown List\'!$AC89:$AC$2"',
    'Years (Benefits)': '"=\'Dropdown List\'!$AD91:$AD$2"',
    'Snapshot Dates': '"=\'Dropdown List\'!$AE5:$AE$2"',
    'Percentage of time spent on SRO role': '"=\'Dropdown List\'!$AF21:$AF$2"',
    'AR Category': '"=\'Dropdown List\'!$AG5:$AG$2"',
    'Project': '"=\'Dropdown List\'!$AH10:$AH$2"',
    'Programme': '"=\'Dropdown List\'!$AI7:$AI$2"',
    'Other': '"=\'Dropdown List\'!$AJ19:$AJ$2"'
}
SHEETS = ['Summary', 'Finance & Benefits', 'Resources',
          'Approval & Project milestones',
          'Assurance planning']
