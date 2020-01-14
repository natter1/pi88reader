"""
@author: Nathanael Jöhrmann
"""
from enum import Enum

import numpy as np

import pi88reader.tdm_importer as tdm


def main():
    """
    Called at end of file, if __name__ == "__main__"
    """
    import pi88reader.pi88_to_pptx as pi88_to_pptx  # import PI88ToPPTX
    measurement_path = "..\\resources\\AuSn_Creep\\1000uN 01 LC.tdm"

    presentation = pi88_to_pptx.PI88ToPPTX(measurement_path)
 #   to_excel = PI88ToExcel(filename)

    # measurement = PI88Measurement('..\\resources\\quasi_static_12000uN.tdm')
    # measurement = PI88Measurement('..\\resources\\AuSn_Creep\\1000uN 01 LC.tdm')
    measurement = PI88Measurement('..\\resources\\nan_error_dyn_10000uN.tdm')
    print(measurement.filename)

    print(measurement.settings.dict)
    print(measurement.area_function.b)
    for name_tuple in PI88Measurement.static_name_tuples:
        print(name_tuple[0], getattr(measurement, name_tuple[0]))
    for name_tuple in PI88Segments.name_tuples:
        print(name_tuple[0], getattr(measurement.segments, name_tuple[0]))
    for name_tuple in PI88Measurement.dynamic_name_tuples:
        print(name_tuple[0], getattr(measurement, name_tuple[0]))


class PI88AreaFunction:
    data_names = [
        ("filename", "Acquisition_Area_Function_Name"),
        ("b", "Current_Area_Function_B"),
        ("c0", "Current_Area_Function_C0"),
        ("c1", "Current_Area_Function_C1"),
        ("c2", "Current_Area_Function_C2"),
        ("c3", "Current_Area_Function_C3"),
        ("c4", "Current_Area_Function_C4"),
        ("c5", "Current_Area_Function_C5")
    ]

    def __init__(self, settings_dict={}):
        # only needed, to make pycharm code completion work:
        self.b = None
        self.c0 = None
        # --------------------------------------------------
        self.read(settings_dict)

    def read(self, settings):
        """
        Read area function parameters from a dictionary (settings).
        :param settings: dict
        :return: None
        """
        for data_name in PI88AreaFunction.data_names:
            if data_name[1] in settings:
                setattr(self, data_name[0], settings[data_name[1]])
            else:
                setattr(self, data_name[0], None)

    def get_area(self, h):
        return (self.c0 * h**2
                + self.c1 * h
                + self.c2 * h**(1/2)
                + self.c3 * h**(1/4)
                + self.c4 * h**(1/8)
                + self.c5 * h**(1/16)
                )


class SegmentType(Enum):
    LOAD = 1
    UNLOAD = 2
    HOLD = 3
    UNKNOWN = 4


class PI88Segments:
    # (attribute_name, TDM-channelname)
    name_tuples = [
        ("timestamp_begin", "Segment Begin Time"),
        ("timestamp_end", "Segment End Time"),
        ("time", "Segment Time"),
        ("begin_demand", "Segment Begin Demand"),
        ("end_demand", "Segment End Demand"),

        ("fb_mode", "Segment FB Mode"),
        ("points", "Segment Points"),
        ("lia_status", "Segment LIA Status")
    ]

    def __init__(self, data):
        self.points_compressed = None
        self.segment_type = []
        # only to make code completition in pycharm work:
        self.timestamp_begin = None
        self.timestamp_end = None
        self.time = None
        self.begin_demand = None
        self.end_demand = None

        self.fb_mode = None
        self.points = None
        self.lia_status = None
        # -------------------------------------------------

        self._read(data)
        self.calc_segment_types()

    def _read(self, data):
        group_name = "Segments"
        data.read_from_channel_group(group_name, PI88Segments.name_tuples, self)
        # print(data.get_channel_dict(group_name))

    def calc_segment_types(self):
        for index, value in enumerate(self.time):
            self.segment_type.append(self.get_segment_type(index))

    def get_segment_type(self, index):
        """
        :param index: int
        :return: SegmentType
        """
        if self.begin_demand[index] < self.end_demand[index]:
            return SegmentType.LOAD
        if self.begin_demand[index] > self.end_demand[index]:
            return SegmentType.UNLOAD
        if self.begin_demand[index] == self.end_demand[index] > 0:
            return SegmentType.HOLD
        return SegmentType.UNKNOWN

    def get_segment_mask(self, array, segment_type, occurence=1):
        """
        Returns a boolean mask for selection from measurement data array
        using the condition_function to select segment of interest.
        :param array:
        :param segment_type:
        :param occurence: int, optional
        :return: numpy.recarray
        """
        counter = 0
        for i in range(len(self.begin_demand)):
            if segment_type == self.segment_type[i]:
                begin = self.timestamp_begin[i]
                end = self.timestamp_end[i]
                counter += 1
            if counter == occurence:
                break

        return (begin <= array) & (array <= end)


class PI88Settings:
    # self.settings dictonary names for important settings
    important_settings_names = [
        "Current_Machine_Compliance__nm___mN__",
        "Current_Tip_Modulus__MPa__",
        "Current_Tip_Poissons_Ratio",
        "Acquisition_Tare",
        "Acquisition_Transducer_Type",
        "Acquisition_Test_Aborted",
        "Current_Drift_Correction",
        "Current_Drift_Rate__nm___s__"
    ]

    def __init__(self, data):
        self.dict = {}
        self._read(data)

    def _read(self, data):
        self.dict = data.get_instance_attributes_dict()


class PI88Measurement:
    # (attribute_name, TDM-channelname)
    static_name_tuples = [
        ("time", "Test Time"),
        ("depth", "Indent Disp."),
        ("load", "Indent Load"),
        ("load_actual", "Indent Act. Load"),
        ("depth_v", "Indent Disp. Volt."),
        ("load_v", "Indent Act. Load Volt."),
        ("output_v", "Indent Act. Output Volt.")
    ]
    # (attribute_name, TDM-channelname)
    dynamic_name_tuples = [
        # channel groupname: Indentation Averaged Values
        ("average_dynamic_time", "Test Time"),
        ("average_dynamic_depth", "Indent Disp."),
        ("average_dynamic_load", "Indent Load"),
        ("average_dynamic_load_actual", "Indent Act. Load"),
        ("average_dynamic_depth_v", "Indent Disp. Volt."),
        ("average_dynamic_load_v", "Indent Act. Load Volt."),
        ("average_dynamic_output_v", "Indent Act. Output Volt."),

        # channel groupname: "Basic Dynamic Averaged Values 1"
        ("average_dynamic_freq", "Dynamic Freq."),
        ("average_dynamic_disp_amp", "Disp. Amp."),
        ("average_dynamic_phase_shift", "Phase Shift"),
        ("average_dynamic_load_amp", "Load Amp."),
        ("average_dynamic_dyn_comp", "Dynamic Comp."),
        ("average_dynamic_disp_amp_v", "Disp. Amp. Volt."),
        ("average_dynamic_load_amp_v", "Load Amp. Volt."),

        # channel groupname: "Visco-Elastic: Indentation Averaged Values 1"
        ("average_dynamic_storage_mod", "Storage Mod."),
        ("average_dynamic_loss_mod", "Loss Mod."),
        ("average_dynamic_tan_delta", "Tan-Delta"),
        ("average_dynamic_complex_mod", "Complex Mod."),
        ("average_dynamic_hardness", "Hardness"),
        ("average_dynamic_contact_area", "Contact Area"),
        ("average_dynamic_contact_depth", "Contact Depth")
    ]

    def __init__(self, filename):
        self.filename =filename
        # only to make code completition in pycharm work:
        self.time = None
        self.depth = None
        self.load = None
        self.time_unit = None
        self.depth_unit = None
        self.load_unit = None
        # -------------------------------------------------

        # todo: how to make it work with 'with' statement
        data = tdm.TdmData(filename)

        self.segments = PI88Segments(data)
        self.settings = PI88Settings(data)
        self.area_function = PI88AreaFunction(self.settings.dict)
        self._read_quasi_static(data)
        self._read_average_dynamic(data)

        for name_tuple in PI88Measurement.dynamic_name_tuples:
            self.remove_nans(name_tuple[0])

    def _read_quasi_static(self, data):
        group_name = "Indentation All Data Points"
        data.read_from_channel_group(group_name, PI88Measurement.static_name_tuples, self)
        # print(data.channel_dict(group_name))

    def _read_average_dynamic(self, data):
        group_name = "Indentation Averaged Values"
        data.read_from_channel_group(group_name, PI88Measurement.dynamic_name_tuples[0:7], self)
        # print(data.channel_dict(group_name))

        group_name = "Basic Dynamic Averaged Values 1"
        data.read_from_channel_group(group_name, PI88Measurement.dynamic_name_tuples[7:14], self)

        group_name = "Visco-Elastic: Indentation Averaged Values 1"
        data.read_from_channel_group(group_name, PI88Measurement.dynamic_name_tuples[14:], self)

    def remove_nans(self, attribute_name):
        """
        Sometimes it happens in dynamic mode, that measurement values are invalid (-> nan).
        Those invalid values can be removed with this method.

        :param attribute_name: Name (self.attribute_name) to be cleaned.
        :return: None
        """
        array = getattr(self, attribute_name, None)
        if array is not None:
            mask = np.invert(np.isnan(array))
            setattr(self, attribute_name, array[mask])

    def get_quasi_static_curve(self):
        """
        Returns data for time, depth and load.
        :return: list, list, list, list
            header, time_data, depth_data, load_data
        """
        # todo: check, if it is right measurement type (e.g. quasi static)
        header = [f"time [{self.time_unit}]",
                  f"depth[{self.depth_unit}]",
                  f"load[{self.load_unit}]"]
        return header, self.time, self.depth, self.load

    def get_segment_curve(self, segment_type, occurence=1):
        """
        Returns data for time, depth and load belonging to segment_type.
        :param segment_type: SegmentType
        :return: list, list, list, list
            header, time_data, depth_data, load_data
        """
        # todo: check, if it is right measurement type (e.g. quasi static, not aborted ...)
        mask = self.segments.get_segment_mask(self.time, segment_type, occurence=occurence)
        header = [f"time [{self.time_unit}]",
                  f"depth[{self.depth_unit}]",
                  f"load[{self.load_unit}]"]
        return header, self.time[mask], self.depth[mask], self.load[mask]


if __name__ == "__main__":
    main()
