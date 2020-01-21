"""This module allows National Instruments TDM/TDX files to be accessed like
NumPy structured arrays. Triboscan can save PI88 measurements in this file format.

==============================================================================
Inspired by the module tdm-loader (https://pypi.org/project/tdm-loader/):
from Josh Ayers and Florian Dobener
==============================================================================
"""
import os.path
import re
import warnings
import xml.etree.ElementTree
from dataclasses import dataclass, field, InitVar
from typing import Optional, List

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


def get_usi_from_string(string: str) -> list:
    if string is None or string.strip() == '':
        return []
    else:
        return re.findall("id\(\"(.+?)\"\)", string)


@dataclass()
class TDMChannel:
    xml_root: xml.etree.ElementTree.Element = field(repr=False)
    id: str
    name: str = None
    description: str = None
    unit: str = None
    inc: str = None
    data_type: str = None
    local_columns_usi: str = None

    def __post_init__(self):
        self.read()

    def read(self) -> None:
        element = self.xml_root.find(f'.//tdm_channel[@id=\'{self.id}\']')
        self.name: str = element.find("name").text
        self.description: str = element.find("description").text
        self.unit: str = element.find("unit_string").text
        self.data_type: str = element.find("datatype").text
        self.local_columns_usi: str = get_usi_from_string(element.findtext('local_columns'))[0]
        self.inc: str = self._get_inc()

    def _get_data_usi(self, root: xml.etree.ElementTree.Element) -> str:
        local_column = root.find(
            f".//localcolumn[@id='{self.local_columns_usi}']")
        return get_usi_from_string(local_column.findtext('values'))[0]

    def _get_inc(self) -> str:
        data_type = self.data_type.split('_')[1].lower() + '_sequence'
        data_usi = self._get_data_usi(self.xml_root)
        return self.xml_root.find(
            f".//{data_type}[@id='{data_usi}']/values").get('external')

    # def __str__(self):
    #     return f"TdmChannel object\n" \
    #            f"\tid: {self.id}\n" \
    #            f"\tName: {self.name}\n" \
    #            f"\tDescription: {self.description}\n" \
    #            f"\tUnit: {self.unit}\n" \
    #            f"\tdata type: {self.data_type}" \
    #            f"\tinc: {self.inc}"


@dataclass()
class TDMChannelGroup:
    id: str = field(default_factory=str, init=False)
    name: str = field(default_factory=str, init=False)
    description: str = field(default_factory=str, init=False)
    channel_ids: list = field(default_factory=list, init=False)
    channels: list = field(default_factory=list, init=False)
    root: InitVar[any]
    _id: InitVar[any]

    def __post_init__(self, root: xml.etree.ElementTree.Element, _id: str):
        self.read(root, _id)
        self.read_channels(root)

    def read(self, root: xml.etree.ElementTree.Element, _id: str):
        element = root.find(f'.//tdm_channelgroup[@id=\'{_id}\']')
        self.id = element.get('id')
        self.name = element.find("name").text
        self.description = element.find("description").text
        self.channel_ids = get_usi_from_string(element.findtext('channels'))

    def read_channels(self, root: xml.etree.ElementTree.Element):
        for channel_id in self.channel_ids:
            self.channels.append(TDMChannel(root, channel_id))

    def get_channel(self, channel_name: str) -> Optional[TDMChannel]:
        result = [x for x in self.channels if x.name == channel_name]
        if len(result) == 0:
            return None
        return result[0]

    def __str__(self):
        return f"TdmChannelGroup object\n" \
               f"\tid: {self.id}\n" \
               f"\tName: {self.name}\n" \
               f"\tDescription: {self.description}\n" \
               f"\tChannel ids: {self.channel_ids.__str__()}"


class TDMData:
    """Class for importing data from National Instruments TDM/TDX files."""

    def __init__(self, tdm_file: str):
        """
        :param tdm_file: The filename including full path to the .TDM xml-file.
        """
        self._folder, self._tdm_filename = os.path.split(tdm_file)
        self.root = xml.etree.ElementTree.parse(tdm_file).getroot()
        self._tdx_order = 'C'  # Set binary file reading to column-major style
        self._tdx_filename = self.root.find('.//file').get('url')
        self._tdx_path = os.path.join(self._folder, self._tdx_filename)

        self.channel_groups = []
        self.read_channel_groups()

    def read_channel_groups(self):
        ids = get_usi_from_string(self.root.findtext('.//tdm_root//channelgroups'))
        for _id in ids:
            self.channel_groups.append(TDMChannelGroup(self.root, _id))

    def get_channel_group_names(self) -> List[str]:
        """
        Returns a list with all channel_group names.
        """
        return [x.name for x in self.channel_groups
                if x.name is not None]

    def get_channel_names(self, channel_group_name: str) -> List[str]:
        """
        Returns a list with all channel names in channel_group.
        :param channel_group_name: str
        :return: list of str
        """
        channels = self.get_channel_group(channel_group_name).channels
        return [channel.name for channel in channels
                if channel.name is not None]

    def get_channel_dict(self, channel_group_name: str) -> dict:
        """Returns a dict with {channel: data} entries of a channel_group."""
        result = {}
        name_doublets = set()

        for channel_name in self.get_channel_names(channel_group_name):
            if channel_name in result:
                name_doublets.add(channel_name)
            inc = self.get_channel(channel_group_name, channel_name).inc
            data = self._get_data(inc)
            result[channel_name] = np.array(data)

        if len(name_doublets) > 0:
            warnings.warn(f"Duplicate channel name(s): {name_doublets}")
        return result

    def get_channel_group(self, group_name: str) -> Optional[TDMChannelGroup]:
        result = [x for x in self.channel_groups if x.name == group_name]
        if len(result) == 0:
            return None
        return result[0]

    def get_channel(self, channel_group_name: str, channel_name: str) -> Optional[TDMChannel]:
        channel_group = self.get_channel_group(channel_group_name)
        if channel_group:
            return channel_group.get_channel(channel_name)
        return None

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

    def _get_dtype_from_tdm_type(self, value_type):
        return np.dtype(self.get_endian_format() + DTYPE_CONVERTERS[value_type])

    def _get_data(self, inc: int):
        """Gets data binary tdx-file belonging to the given inc.

        :return: numpy data or None
            Returns None, if inc is None, else returns numpy data.
        """
        if inc is None:
            return None
        else:
            ext_attribs = self.root.find(f".//file/block[@id='{inc}']").attrib
            return np.memmap(
                self._tdx_path,
                offset=int(ext_attribs['byteOffset']),
                shape=(int(ext_attribs['length']),),
                dtype=self._get_dtype_from_tdm_type(ext_attribs['valueType']),
                mode='r',
                order=self._tdx_order
            ).view(np.recarray)

    def _read_data(self, channel, attribute_name, to_object):
        if channel:
            setattr(to_object, attribute_name, self._get_data(channel.inc))
            setattr(to_object, attribute_name + '_unit', channel.unit)
        else:
            setattr(to_object, attribute_name, None)

    def read_from_channel_group(self, group_name, name_tuples, to_object):
        """
        Read channels data (names given in name_tuples) from group_name into
        to_object, by setting the attribute names given via name_tuples.
        If some data wasn't found, the attribute is set to None.
        :param group_name: str
        :param name_tuples: (str, str)
            (attribute_name, channel_name)
        :param to_object: object
        :return: None
        """
        for name_tuple in name_tuples:
            channel = self.get_channel(group_name, name_tuple[1])
            self._read_data(channel, name_tuple[0], to_object)

    def get_instance_attributes_dict(self):
        """
        Function specific for PI88 measurement files
        :return: dict
        """

        def get_name_value_pair(element):
            if element.tag == 'string_attribute':
                return {element.get("name"): element.find("s").text}
            elif element.tag == 'double_attribute':
                return {element.get("name"): float(element.text)}
            elif element.tag == 'long_attribute':
                return {element.get("name"): int(element.text)}
            # todo: 'time_attribute'
            else:
                return {element.get("name"): element.text}

        result = {}
        attributes = self.root.find(".//tdm_root//instance_attributes")
        for child in attributes:
            result.update(get_name_value_pair(child))

        return result
