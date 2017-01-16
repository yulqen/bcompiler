# digest.py

#
# Pull data from an Excel form, based on a datamap.
import os
import fnmatch

from datetime import datetime
from typing import List, Dict

from tinydb import TinyDB, Query
from tinydb_serialization import SerializationMiddleware
from tinydb_serialization import Serializer

from concurrent import futures

from bcompiler.compile import parse_source_cells
from bcompiler.utils import DATAMAP_MASTER_TO_RETURN


class Schema:
    """
    What was once a Datamap...
    """
    pass


class Series:
    """
    A collective for SeriesItem objects.
    """
    pass


class SeriesItem:
    """
    A SeriesItem is collective term for Digest objects. An example of a
    SeriesItem is a Financial Quarter. They are supposed to represent temporal
    change.
    """
    pass


class Digest:
    """
    A Digest object is a compilation of key/value pairs from a specific Excel
    file. By default, the Digest is serialized and written to a database.

    The result of a Digest is a SeriesItem, which is the name of the table in
    the database
    """
    pass


class DateTimeSerializer(Serializer):
    """
    If are going to get datetime objects in and our of TinyDB, they have to
    be encoded correctly. This makes use of of the tinydb_serialization lib.
    """
    OBJ_CLASS = datetime

    def encode(self, obj):
        return obj.strftime('%Y-%m-%d')

    def decode(self, s):
        return datetime.strptime(s, '%Y-%m-%d')


serialization = SerializationMiddleware()
serialization.register_serializer(DateTimeSerializer(), 'TinyDate')


db = TinyDB('db.json', storage=serialization)


def flatten_project(future) -> Dict[str, str]:
    """
    Get rid of the gmpp_key gmpp_key_value stuff pulled from a single
    spreadsheet. Must be given a future.
    """
    p_data = future.result()
    p_data = {item['gmpp_key']: item['gmpp_key_value'] for item in p_data}
    return p_data


def digest_source_files() -> None:
    source_files = []
    future_data = []
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
            f = flatten_project(future)
            db.insert(f)


def main():
    digest_source_files()


if __name__ == "__main__":
    main()

# print("{0:<67}{1:>20}{2:>40}".format(
#     'Imported Project',
#     'Data Length',
#     'DfT Group'))
# print("{:*<127}".format(""))
# for proj in d:
#     print("{0:<67}{1:>20}{2:>40}".format(
#         proj['Project/Programme Name'],
#         len(proj),
#         proj['DfT Group']))
