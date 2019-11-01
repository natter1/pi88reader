import pi88reader.tdm_importer as tdm
import numpy as np


class PI88Segments:
    # (attribute_name, TDM-channelname)
    array_names = [
        ("timestamp_begin", "Segment Begin Time"),
        ("timestamp_end", "Segment End Time"),
        ("time", "Segment Time"),
        ("begin_demand", "Segment Begin Demand"),
        ("end_demand", "Segment End Demand"),

        ("fb_mode", "Segment FB Mode"),
        ("points", "Segment Points"),
        ("lia_status", "Segment LIA Status")
    ]

    def __init__(self):
        for name_tuple in PI88Segments.array_names:
            setattr(self, name_tuple[0], None)

        self.points_compressed = None


class PI88Measurement:
    # (attribute_name, TDM-channelname)
    static_array_names = [
        ("time", "Test Time"),
        ("depth", "Indent Disp."),
        ("load", "Indent Load"),
        ("load_actual", "Indent Act. Load"),
        ("depth_v", "Indent Disp. Volt."),
        ("load_v", "Indent Act. Load Volt."),
        ("output_v", "Indent Act. Output Volt.")
    ]
    # (attribute_name, TDM-channelname)
    dynamic_array_names = [
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

        ("average_dynamic_storage_mod", "Storage Mod."),
        ("average_dynamic_loss_mod", "Loss Mod."),
        ("average_dynamic_tan_delta", "Tan-Delta"),
        ("average_dynamic_complex_mod", "Complex Mod."),
        ("average_dynamic_hardness", "Hardness"),
        ("average_dynamic_contact_area", "Contact Area"),
        ("average_dynamic_contact_depth", "Contact Depth")
    ]

    def __init__(self, filename):
        for name_tuple in PI88Measurement.static_array_names:
            setattr(self, name_tuple[0], None)

        for name_tuple in PI88Measurement.dynamic_array_names:
            setattr(self, name_tuple[0], None)

        self.segments = PI88Segments()

        # todo: how to make it work with 'with' statement
        data = tdm.TdmData(filename)

        self._read_quasi_static(data)
        self._read_segemnts(data)
        self._read_average_dynamic(data)

        for name_tuple in PI88Measurement.dynamic_array_names:
            self.remove_nans(name_tuple[0])

    def _read_data(self, data, group_name, array_names, to_object):
        if group_name not in data.get_channel_group_names():
            return
        for name_tuple in array_names:
            try:
                setattr(to_object, name_tuple[0], data.get_channel_data(group_name, name_tuple[1]))
            except Exception as inst:
                print(inst)

    def _read_quasi_static(self, data):
        group_name = "Indentation All Data Points"
        self._read_data(data, group_name, PI88Measurement.static_array_names, self)
        # print(data.channel_dict(group_name))

    def _read_segemnts(self, data):
        group_name = "Segments"
        self._read_data(data, group_name, PI88Segments.array_names, self.segments)
        # print(data.channel_dict(group_name))

    def _read_average_dynamic(self, data):
        group_name = "Indentation Averaged Values"
        self._read_data(data, group_name, PI88Measurement.dynamic_array_names[0:7], self)
        # print(data.channel_dict(group_name))

        group_name = "Basic Dynamic Averaged Values 1"
        self._read_data(data, group_name, PI88Measurement.dynamic_array_names[7:14], self)
        # print(data.channel_dict(group_name))

        group_name = "Visco-Elastic: Indentation Averaged Values 1"
        self._read_data(data, group_name, PI88Measurement.dynamic_array_names[14:], self)
        # print(data.channel_dict(group_name))

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
        else:
            print(f"Given attribute name {attribute_name} does not exist.")


# measurement = PI88Measurement('D:\\py_projects\\pi88reader\\resources\\10000uN 06.tdm')
# measurement = PI88Measurement('D:\\py_projects\\pi88reader\\resources\\12000uN 01 LC.tdm')


measurement = PI88Measurement('D:\\myAnsys\\pi88reader\\resources\\12000uN 01 LC.tdm')
# print("time:", measurement.time)
# print("depth:", measurement.depth)
# print("load:", measurement.load)
# print("depth_v:", measurement.depth_v)
# print("load_v:", measurement.load_v)

# for name_tuple in PI88Measurement.static_array_names:
#     print(name_tuple[0], getattr(measurement, name_tuple[0]))

# for name_tuple in PI88Segments.array_names:
#     print(name_tuple[0], getattr(measurement.segments, name_tuple[0]))

# for name_tuple in PI88Measurement.dynamic_array_names:
#     print(name_tuple[0], getattr(measurement, name_tuple[0]))


# // -------------------
# if (measurement.depth.size() > maxDataSize){
# maxDataSize = measurement.depth.size();
# }