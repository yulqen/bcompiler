import pytest
import os
import shelve

from openpyxl import Workbook

from bcompiler.process import BCShelve
from bcompiler.utils import SOURCE_DIR


@pytest.fixture
def empty_shelve():
    sh_f = SOURCE_DIR + 'test_quarters'
    shel = shelve.open(sh_f)
    shel['name'] = 'Quarters'
    yield shel
    shel.close()
    os.unlink(sh_f + '.db')


@pytest.fixture
def parsed_kvs():
    return {
        'Programme/Project Name': 'South East Rail',
        'SRO Sign-Off': '2016-09-29 00:00:00',
        'Reporting period (GMPP - Snapshot Date)': 'Q2 1617',
    }


def test_create_bcshelve(parsed_kvs):
    s = BCShelve()
    pass


def test_shelve_exists(empty_shelve):
    f = empty_shelve
    assert f['name'] == 'Quarters'
