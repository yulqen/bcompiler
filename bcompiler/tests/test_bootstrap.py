from ..process.bootstrap import AuxReport


class TestAuxReportBase(object):

    def test_base_AuxReport(self):
        assert AuxReport.modified == []
        assert AuxReport.untracked == []
        assert AuxReport.master == []


    def test_add_attribute_value_Auxreport(self):
        AuxReport.modified.append('test')
        assert AuxReport.modified[0] == 'test'


    def test_add_AuxReport_instance(self):
        r = AuxReport()
        assert str(r) == "Report(['modified', 'untracked', 'master'])"


    def test_change_instance_expect_attribute_change(self):
        AuxReport.modified.append('test')
        assert AuxReport.modified[0] == 'test'
        r = AuxReport()
        assert hasattr(r, 'modified')
        assert r.modified[0] == 'test'


