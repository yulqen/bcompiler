from datetime import datetime
from bcompiler.process.database import BCQuery, Database

from tinydb import TinyDB


def test_db_connection():
    db = Database('db.json')
    assert isinstance(db.connect(), TinyDB)


def test_query_for_project():
    """
    We want to be able to return the data for a single project from the
    database, when we pass it the exact string. Also if we query for strings
    that are close, starting with, etc.

    # TODO refactor all this to use fixtures. Not worried about it for now.
    """
    db = Database('db.json').connect()
    q = BCQuery(db, 'Digital Signalling')
    assert q.get_item('Project/Programme Name') == 'Digital Signalling'
    assert q.get_item('SRO Sign-Off') is None
    assert q.get_item('SRO Tenure Start Date') == datetime(2016, 1, 1)
    assert q.get_item('SRO Tenure End Date') == datetime(2018, 1, 1)
    assert q.get_item('Fudgecake') == ("No item 'Fudgecake' in Digital "
                                       "Signalling")

    q = BCQuery(db, 'Search and Rescue Helicopters')
    assert q.get_item('DFT ID Number') == 30
    assert q.get_item('Project cost to closure') == 318.4

    q = BCQuery(db, 'North of England Programme')
    assert isinstance(q.data, dict)
    assert q.data['Quarter Joined'] == '1516 - Q4'
