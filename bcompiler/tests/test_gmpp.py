# we want to test the GMPP datamap functionality

from bcompiler.datamap import DatamapGMPP


def test_clean_creation_of_dm_object():
    dm = DatamapGMPP(
        '/home/lemon/Documents/bcompiler/source/datamap-master-to-gmpp')
    assert dm.data[0].cellname == 'Project/Programme Name'
    assert dm.data[1].cellref == 'C5'


def test_no_single_item_datamap_lines_thanks():
    dm = DatamapGMPP(
        '/home/lemon/Documents/bcompiler/source/datamap-master-to-gmpp')
    assert dm.data[2].cellname != 'JUNK'
