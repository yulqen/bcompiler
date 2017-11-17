from ..core import Master, Quarter, ProjectData


def test_master(master):
    q1_2017 = Quarter(1, 2017)
    m = Master(q1_2017, master)
    assert m.path.name == 'master.xlsx'
    assert m.filename == 'master.xlsx'
    assert m.quarter == 1
    assert m.year == 2017
    assert len(m.projects) == 3

    assert m.projects[0] == 'PROJECT/PROGRAMME NAME 1'
    assert m.projects[1] == 'PROJECT/PROGRAMME NAME 2'
    assert m.projects[2] == 'PROJECT/PROGRAMME NAME 3'

    assert len(m['PROJECT/PROGRAMME NAME 1']) == 1276
    assert m['PROJECT/PROGRAMME NAME 1']['SRO Full Name'] == 'SRO FULL NAME 1'

    p1 = m['PROJECT/PROGRAMME NAME 1']
    assert p1['SRO Full Name'] == 'SRO FULL NAME 1'


def test_project_data_object(master):
    q2_2018 = Quarter(2, 2018)
    m = Master(q2_2018, master)
    assert m.path.name == 'master.xlsx'
    assert m.filename == 'master.xlsx'
    assert m.quarter == 2
    assert m.year == 2018
    assert len(m.projects) == 3
    assert isinstance(m['PROJECT/PROGRAMME NAME 1'], ProjectData)
