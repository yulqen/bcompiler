import pytest

import bcompiler.tests.fixtures

from bcompiler.process.digest import digest_source_files, Digest

BICC_RETURN_FIXTURE = bcompiler.tests.fixtures.bicc_return
DB_FIXTURE = bcompiler.tests.fixtures.db
SERIES_FIXTURE = bcompiler.tests.fixtures.series


def test_digest_single_file(BICC_RETURN_FIXTURE, SERIES_FIXTURE):
    digest = Digest(BICC_RETURN_FIXTURE, SERIES_FIXTURE, 'Q2 April')
    assert digest.table == 'q2-april'
    assert digest.series == 'Financial Quarters'
    assert digest.data['Project/Programme Name'] == 'Cookfield Rebuild'
    # this works because the comma is getting cleansed
    assert digest.data['DfT Group'] == 'Roads Monitoring and Horse'


@pytest.mark.skip("Too resource intensive for now.")
def test_digest_source_files(DB_FIXTURE):
    base_dir = '/home/lemon/Documents/bcompiler/source/returns'
    digest_source_files(base_dir, DB_FIXTURE)
