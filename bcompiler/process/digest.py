# digest.py

#
# Pull data from an Excel form, based on a datamap.
import os
import fnmatch
import re

from datetime import datetime
from typing import Dict

from tinydb import TinyDB
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
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name


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
    def __init__(self, file_name, series, series_item):
        self.file_name = file_name
        self.series = series.__str__()
        self.table = self.tableize(series_item)
        self._data = self._digest_source_file(file_name)

    def tableize(self, item):
        return re.sub('\s', '-', item).lower()

    def flatten_project(self, project_data):
        """
        Get rid of the gmpp_key gmpp_key_value stuff pulled from a single
        spreadsheet. Must be given a future.
        """
        return {
            item['gmpp_key']: item['gmpp_key_value'] for item in project_data}

    def _digest_source_file(self, file_name):
        flat = self.flatten_project(
            parse_source_cells(file_name, DATAMAP_MASTER_TO_RETURN))
        return flat

    @property
    def data(self):
        return self._data


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


def digest_source_files(base_dir, db_connection) -> None:
    source_files = []
    future_data = []
    for f in os.listdir(base_dir):
        if fnmatch.fnmatch(f, '*.xlsx'):
            source_files.append(os.path.join(base_dir, f))
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
