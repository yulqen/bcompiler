from pymongo import MongoClient
import pytest

from datetime import date


@pytest.fixture(scope="module")
def mock_datamap_object():
    """Mock a Datamap object to use for data retrieval, in MongoDB"""
    client = MongoClient()
    db = client.test_database
    collection = db.test_collection
    test_data = {'Map Type': 'BICC',
                 'First Name': 'B1',
                 'Last Name': 'B2',
                 'Age': 'B3',
                 'Birthday': 'B4',
                 }
    collection.insert_one(test_data)
    yield collection
    print("Teardown MongoDB")
    client.drop_database(db)


@pytest.fixture
def mock_bicc_form():
    """Set up a basic form for testing."""
    from openpyxl import Workbook
    wb = Workbook()
    ws = wb.active
    ws['A1'] = "First Name"
    ws['B1'] = "Matthew"
    ws['A2'] = "Last Name"
    ws['B2'] = "Lemon"
    ws['A3'] = "Age"
    ws['B3'] = 41
    ws['A4'] = "Birthday"
    ws['B4'] = date(1975, 1, 24)


def test_db_id(mock_datamap_object):
    doc = list(mock_datamap_object.find({"Map Type": {"$eq": "BICC"}}))
    assert doc[0]['Map Type'] == 'BICC'
