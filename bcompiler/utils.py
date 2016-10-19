import os


def working_directory(dir_type=None):
    """
    Returns the working direct for source files
    :return: path to the working directory intended for the source files
    """
    docs = os.path.join(os.path.expanduser('~'), 'Documents')
    try:
        bcomp_working_d = 'bcompiler'
    except FileNotFoundError:
        print("You need to run with --create-wd to create the working directory")
    root_path = os.path.join(docs, bcomp_working_d)
    if dir_type == 'source':
        return root_path + "/source/"
    elif dir_type == 'output':
        return root_path + "/output/"
    else:
        return


SOURCE_DIR = working_directory('source')
OUTPUT_DIR = working_directory('output')
DATAMAP_RETURN_TO_MASTER = SOURCE_DIR + 'datamap-returns-to-master'
DATAMAP_MASTER_TO_RETURN = SOURCE_DIR + 'datamap-master-to-returns'
CLEANED_DATAMAP = SOURCE_DIR + 'cleaned_datamap'
MASTER = SOURCE_DIR + 'master.csv'
TEMPLATE = SOURCE_DIR + 'bicc_template.csv'


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
SHEETS = ['Summary', 'Finance & Benefits', 'Resources', 'Approval & Project milestones',
          'Assurance planning']
