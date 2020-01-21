import pytest

from pi88reader.tdm_importer import TDMData, TDMChannelGroup


@pytest.fixture(scope='class')
def tdm_data():
    filename = '../resources/quasi_static_12000uN.tdm'
    yield TDMData(filename)


class TestTdmData:
    def test__init__(self):
        filename = '../resources/quasi_static_12000uN.tdm'
        tdm_data = TDMData(filename)
        assert len(tdm_data.channel_groups) == 2
        assert hasattr(tdm_data, "root")

    def test_read_channel_groups(self, tdm_data):
        tdm_data.channel_groups = []
        tdm_data.read_channel_groups()
        assert len(tdm_data.channel_groups) == 2

    def test_get_channel_group_names(self, tdm_data):
        channel_group_0 = "Indentation All Data Points"
        channel_group_1 = "Segments"
        assert tdm_data.get_channel_group_names()[0] == channel_group_0
        assert tdm_data.get_channel_group_names()[1] == channel_group_1
        assert len(tdm_data.get_channel_group_names()) == 2

    def test_get_channel_names(self, tdm_data):
        assert len(tdm_data.get_channel_names(tdm_data.get_channel_group_names()[0])) == 6
        assert len(tdm_data.get_channel_names(tdm_data.get_channel_group_names()[1])) == 8

    def test_get_channel_dict(self, tdm_data):
        channel_group_0 = "Indentation All Data Points"
        assert len(tdm_data.get_channel_dict(channel_group_0)['Test Time']) == 1152
        assert len(tdm_data.get_channel_dict(channel_group_0)['Indent Disp.']) == 1152
        assert len(tdm_data.get_channel_dict(channel_group_0)['Indent Load']) == 1152
        assert len(tdm_data.get_channel_dict(channel_group_0)['Indent Disp. Volt.']) == 1152
        assert len(tdm_data.get_channel_dict(channel_group_0)['Indent Act. Load Volt.']) == 1152
        assert len(tdm_data.get_channel_dict(channel_group_0)['Indent Act. Output Volt.']) == 1152
        assert len(tdm_data.get_channel_dict(channel_group_0)) == 6
        channel_group_1 = "Segments"
        assert len(tdm_data.get_channel_dict(channel_group_1)) == 8

    def test_get_channel_group(self, tdm_data):
        assert tdm_data.get_channel_group("non existing group name") is None
        assert type(tdm_data.get_channel_group("Segments")) is TDMChannelGroup
        assert len(tdm_data.get_channel_group("Segments").channels) == 8

    def test_get_channel(self, tdm_data):
        assert False

    def test_get_endian_format(self, tdm_data):
        assert False

    def test__get_dtype_from_tdm_type(self, tdm_data):
        assert False

    def test__get_data(self, tdm_data):
        assert False

    def test__read_data(self, tdm_data):
        assert False

    def test__read_from_channel_group(self, tdm_data):
        assert False

    def test_get_instance_attributes_dict(self, tdm_data):
        assert False
