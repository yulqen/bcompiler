from datetime import datetime

from tinydb import TinyDB
from tinydb.queries import where

from tinydb_serialization import SerializationMiddleware
from tinydb_serialization import Serializer


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


class Database:
    def __init__(self, db_file):
        self.serialization = SerializationMiddleware()
        self.serialization.register_serializer(
            DateTimeSerializer(), 'TinyDate')
        self.db = TinyDB(db_file, storage=self.serialization)

    def connect(self):
        return self.db


class BCQuery:

    def __init__(self, db, search_string, exact=True):
        """
        db should be a TinyDB instance.
        """
        self.db = db
        self.search_string = search_string
        self._query_result = self.db.search(
            where('Project/Programme Name') == self.search_string)

    def get_item(self, item_name):
        try:
            return self._query_result[0][item_name]
        except KeyError:
            return "No item '{}' in {}".format(
                item_name, self._query_result[0]['Project/Programme Name'])

    def _get_data(self):
        """
        Private method to expose data member.
        """
        return self._query_result[0]

    @property
    def data(self):
        return self._get_data()
