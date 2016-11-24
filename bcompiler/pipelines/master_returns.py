import colorlog
import csv

from bcompiler.utils import SOURCE_DIR

logger = colorlog.getLogger('bcompiler.master_returns')


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
            logger.debug("Stripping \\n from {}".format(i))
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
