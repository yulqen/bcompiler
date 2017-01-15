# digest.py
#
# Pull data from an Excel form, based on a datamap.
import os
import fnmatch
import shelve

from concurrent import futures

from bcompiler.compile import parse_source_cells
from bcompiler.utils import DATAMAP_MASTER_TO_RETURN


def flatten_project(future) -> dict:
    """
    Get rid of the gmpp_key gmpp_key_value stuff pulled from a single
    spreadsheet. Must be given a future.
    """
    p_data = future.result()
    p_data = {item['gmpp_key']: item['gmpp_key_value'] for item in p_data}
    return p_data


def digest_source_files() -> list:
    source_files = []
    future_data = []
    flattened_data = []
    for f in os.listdir('/home/lemon/Documents/bcompiler/source/returns'):
        if fnmatch.fnmatch(f, '*.xlsx'):
            source_files.append(
                os.path.join(
                    '/home/lemon/Documents/bcompiler/source/returns', f))
    with futures.ThreadPoolExecutor(max_workers=4) as executor:
        for f in source_files:
            future_data.append(executor.submit(
                parse_source_cells, f, DATAMAP_MASTER_TO_RETURN))
            print("Processing {}".format(f))
        for future in futures.as_completed(future_data):
            flattened_data.append(flatten_project(future))
    return flattened_data


d = digest_source_files()
print("{0:<60}{1:>20}{2:>30}".format('Imported Project', 'Data Length', 'DfT Group'))
print("{:*<110}".format(""))
for proj in d:
    print("{0:<60}{1:>20}{2:>30}".format(
        proj['Project/Programme Name'],
        len(proj),
        proj['DfT Group']))
