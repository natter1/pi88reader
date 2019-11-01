"""This module allows National Instruments TDM/TDX files to be accessed like
NumPy structured arrays.

==============================================================================
Inspired by the module tdm-loader (https://pypi.org/project/tdm-loader/):
from Josh Ayers and Florian Dobener
==============================================================================
"""
import os.path
import re
import warnings
import xml.etree.ElementTree as ET

import numpy as np

# dictionary for converting from NI to NumPy datatypes
DTYPE_CONVERTERS = {'eInt8Usi': 'i1',
                    'eInt16Usi': 'i2',
                    'eInt32Usi': 'i4',
                    'eInt64Usi': 'i8',
                    'eUInt8Usi': 'u1',
                    'eUInt16Usi': 'u2',
                    'eUInt32Usi': 'u4',
                    'eUInt64Usi': 'u8',
                    'eFloat32Usi': 'f4',
                    'eFloat64Usi': 'f8',
                    'eStringUsi': 'U'}


class XmlTdmData:  # helper class used to keep TdmData interface tidy
    """
    Helper class for TdmData containing xml-related data-handling.
    """

    def __init__(self, element_tree):
        self.tree = element_tree
        self.root = element_tree.getroot()
        self.tdm_root = self.root.find('.//tdm_root')
        ids = XmlTdmData.get_usi_from_string(self.tdm_root.findtext('channelgroups'))
        self.channelgroups = list(map(self.get_channelgroup_by_id, ids))

    @staticmethod
    def get_usi_from_string(string):
        if string is None or string.strip() == '':
            return []
        else:
            return re.findall("id\(\"(.+?)\"\)", string)

    def get_channelgroup_by_id(self, id):
        return self.root.find('.//tdm_channelgroup[@id=\'{0}\']'.format(id))

    def get_endian_format(self):
        """
        Returns '<' for littleEndian and '>' for bigEndian
        :return: '<' or '>'
        """
        order = self.root.find('.//file').get('byteOrder')
        if order == 'littleEndian':
            return '<'
        elif order == 'bigEndian':
            return '>'
        else:
            raise TypeError('Unknown endian format in TDM file')

    def get_tdx_filename(self):
        return self.root.find('.//file').get('url')

    def channel(self, group_name, channel_name, occurrence=0, ch_occurrence=0):
        """
        Returns a xml channel_name element with name 'channel_name' in 'group_name'.
        :param group_name:  str
        :param channel_name: str
        :param occurrence: int, optional
        :param ch_occurrence: int, optional
        :return: xml.etree.ElementTree.Element
        """
        channels = self.channels(group_name, occurrence)
        result = list(filter(lambda x: x.findtext('name') == channel_name, channels))
        if len(result) < ch_occurrence:
            raise IndexError(f'Channel {channel_name} (occurrence {ch_occurrence}) not found')
        return result[ch_occurrence]

    def channels(self, group_name, occurrence=0):
        """
        Returns a list of xml elements belonging to 'group_name'.
        :param group_name: str
        :param occurrence: int, optional
        :return: list of xml.etree.ElementTree.Element
        """
        channel_groups = list(filter(lambda x: x.findtext('name') == group_name, self.channelgroups))
        if len(channel_groups) <= occurrence:
            raise IndexError(f'Channel group {group_name} (occurrence {occurrence}) not found')
        group_name = channel_groups[occurrence]

        return list(map(lambda usi: self.root.find(".//tdm_channel[@id='{0}']".format(usi)),
                        XmlTdmData.get_usi_from_string(
                            group_name.findtext('channels'.format(group_name.get('id'))))
                        )
                    )

    def get_channel_inc(self, group_name, channel_name, group_occurrence=0, channel_occurrence=0):
        channel_xml = self.channel(group_name, channel_name, group_occurrence, channel_occurrence)
        datatype = channel_xml.findtext('datatype').split('_')[1].lower() + '_sequence'
        local_columns_usi = XmlTdmData.get_usi_from_string(channel_xml.findtext('local_columns'))[0]
        local_column_xml = self.root.find(f".//localcolumn[@id='{local_columns_usi}']")
        data_usi = XmlTdmData.get_usi_from_string(local_column_xml.findtext('values'))[0]
        return self.root.find(f".//{datatype}[@id='{data_usi}']/values").get('external')


class TdmData:
    """Class for importing data from National Instruments TDM/TDX files."""

    def __init__(self, tdm_file):
        """
        :param tdm_file: str
            The filename including full path to the .TDM xml-file.
        """
        self._folder, self._tdm_filename = os.path.split(tdm_file)
        self.xml = XmlTdmData(ET.parse(tdm_file))
        self._tdx_order = 'C'  # Set binary file reading to column-major style
        self._tdx_path = os.path.join(self._folder, self.xml.get_tdx_filename())

    def get_channel_group_names(self):
        """
        Returns a list with all channel_group names.
        :return: list of str
        """
        result = [name.text for name in self.xml.root.findall(".//tdm_channelgroup/name")
                  if name.text is not None]
        return result

    def get_channel_names(self, channel_group):
        """
        Returns a list with all channel names in channel_group.
        :param channel_group: str
        :return: list of str
        """
        channels = self.xml.channels(channel_group)
        return [channel.findtext('name') for channel in channels
                if channel.findtext('name') is not None]

    def get_channel_data(self, group_name, channel_name, group_occurrence=0, channel_occurrence=0):
        """Returns data of a channel_name by its channel_name group and channel_name name.
        
        :param group_name: str
        :param channel_name: str
        :param group_occurrence: int, optional
            Gives the nth occurrence of the channel_name group name. By default the first occurrence is returned.
        :param channel_occurrence: int, optional
            Gives the nth occurrence of the channel_name name. By default the first occurrence is returned.
        :return: numpy data
        """
        try:
            inc = self.xml.get_channel_inc(group_name, channel_name, group_occurrence, channel_occurrence)
        except Exception as inst:
            raise ValueError(f"{inst}\nNo binary data inc found for groupname: {group_name}; channel_name: {channel_name}")

        ext_attribs = self.xml.root.find(f".//file/block[@id='{inc}']").attrib
        return np.memmap(self._tdx_path,
                         offset=int(ext_attribs['byteOffset']),
                         shape=(int(ext_attribs['length']),),
                         dtype=np.dtype(self.xml.get_endian_format() + DTYPE_CONVERTERS[ext_attribs['valueType']]),
                         mode='r',
                         order=self._tdx_order).view(np.recarray)

    def channel_dict(self, channel_group, occurrence=0):
        """Returns a dict with {channel: data} entries of a channel_group.

        :param channel_group: str
        :param occurrence: int
        :return: dict
        """
        channel_dict = {}
        name_doublets = set()

        for channel_name in self.get_channel_names(channel_group):
            if channel_name in channel_dict:
                name_doublets.add(channel_name)
            data = self.get_channel_data(channel_group, channel_name)
            channel_dict[channel_name] = np.array(data)

        if len(name_doublets) > 0:
            warnings.warn(f"Duplicate channel name(s): {name_doublets}")
        return channel_dict

    def get_channel_unit(self, channel_group, channel, occurrence=0, ch_occurrence=0):
        """Returns the unit of the channel at given channel_group.

        :param channel_group: str
        :param channel: str
        :param occurrence: int
        :param ch_occurrence: int
        :return: str
        """
        channel_xml = self.xml.channel(channel_group, channel, occurrence, ch_occurrence)
        return channel_xml.findtext('unit_string')

    def channel_description(self, channel_group_name, channel_name, occurrence=0, ch_occurrence=0):
        """Returns the description of the channel at given channel_group.

        :param channel_group_name: str
        :param channel_name: str
        :param occurrence: int, optional
        :param ch_occurrence: int, optional
        :return: str
        """
        channel_xml = self.xml.channel(channel_group_name, channel_name, occurrence, ch_occurrence)
        return channel_xml.findtext('description')

    def get_instance_attributes_dict(self):
        """
        Function specific for PI88 measurement files
        :return: dict
        """
        result = {}
        element = self.xml.tdm_root.find("instance_attributes")
        for child in element:
            # print(child)
            if child.tag == 'string_attribute':
                result[child.get("name")] = child.find("s").text
                #result.append({child.get("name"), child.find("s").text})
                # print(child.get("name"), child.find("s").text)
            elif child.tag == 'double_attribute':
                result[child.get("name")] = float(child.text)
            elif child.tag == 'long_attribute':
                result[child.get("name")] = int(child.text)
            # todo: 'time_attribute'
            else:
                result[child.get("name")] = child.text
        return result