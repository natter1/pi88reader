import pi88reader.tdm_importer as tdm


class PI88Segments:
    def __init__(self):
        self.timestamp_begin = None
        self.timestamp_end = None
        self.time = None
        self.begin_demand = None
        self.end_demand = None

        self.fb_mode = None
        self.points = None
        self.points_compressed = None
        self.lia_status = None


class PI88Measurement:
    def __init__(self, filename):
        self.time = None
        self.depth = None
        self.load = None
        self.depth_v = None
        self.load_v = None

        self.segments = PI88Segments()

        self.average_dynamic_depth = None
        self.average_dynamic_load = None
        self.average_dynamic_time = None

        self.average_dynamic_freq = None
        self.average_dynamic_disp_amp = None
        self.average_dynamic_phase_shift = None
        self.average_dynamic_load_amp = None
        self.average_dynamic_dyn_comp = None

        self.average_dynamic_storage_mod = None
        self.average_dynamic_loss_mod = None
        self.average_dynamic_tan_delta = None
        self.average_dynamic_complex_mod = None
        self.average_dynamic_hardness = None

        # todo: how to make it work with 'with' statement
        data = tdm.TdmData(filename)

        self._read_quasi_static(data)
        self._read_segemnts(data)
        self._read_average_dynamic(data)

    def _read_quasi_static(self, data):
        group_name = "Indentation All Data Points"
        if group_name not in data.get_channel_group_names():
            return
        self.time = data.get_channel_data(group_name, "Test Time")
        self.depth = data.get_channel_data(group_name, "Indent Disp.")
        self.load = data.get_channel_data(group_name, "Indent Load")
        self.depth_v = data.get_channel_data(group_name, "Indent Disp. Volt.")
        self.load_v = data.get_channel_data(group_name, "Indent Act. Load Volt.")

    def _read_segemnts(self, data):
        group_name = "Segments"
        if group_name not in data.get_channel_group_names():
            return
        self.segments.timestamp_begin = data.get_channel_data(group_name, "Segment Begin Time")
        self.segments.timestamp_end = data.get_channel_data(group_name, "Segment End Time")
        self.segments.time = data.get_channel_data(group_name, "Segment Time")
        self.segments.begin_demand = data.get_channel_data(group_name, "Segment Begin Demand")
        self.segments.end_demand = data.get_channel_data(group_name, "Segment End Demand")
        # print(data.channel_dict("Segments"))

    def _read_average_dynamic(self, data):
        group_name = "Indentation Averaged Values"
        if group_name in data.get_channel_group_names():
            self.average_dynamic_depth = data.get_channel_data(group_name, "Indent Disp.")
            self.average_dynamic_load = data.get_channel_data(group_name, "Indent Load")
            self.average_dynamic_time = data.get_channel_data(group_name, "Test Time")

        group_name = "Basic Dynamic Averaged Values 1"
        if group_name in data.get_channel_group_names():
            self.average_dynamic_freq = data.get_channel_data(group_name, "Dynamic Freq.")
            self.average_dynamic_disp_amp = data.get_channel_data(group_name, "Disp. Amp.")
            self.average_dynamic_phase_shift = data.get_channel_data(group_name, "Phase Shift")
            self.average_dynamic_load_amp = data.get_channel_data(group_name, "Load Amp.")
            self.average_dynamic_phase_shift = data.get_channel_data(group_name, "Dynamic Comp.")

        group_name = "Visco-Elastic: Indentation Averaged Values 1"
        if group_name in data.get_channel_group_names():
            self.average_dynamic_storage_mod = data.get_channel_data(group_name, "Storage Mod.")
            self.average_dynamic_loss_mod = data.get_channel_data(group_name, "Loss Mod.")
            self.average_dynamic_tan_delta = data.get_channel_data(group_name, "Tan-Delta")
            self.average_dynamic_complex_mod = data.get_channel_data(group_name, "Complex Mod.")
            self.average_dynamic_hardness = data.get_channel_data(group_name, "Hardness")


measurement = PI88Measurement('D:\\py_projects\\pi88reader\\resources\\12000uN 01 LC.tdm')

# print("time:", measurement.time)
# print("depth:", measurement.depth)
# print("load:", measurement.load)
# print("depth_v:", measurement.depth_v)
# print("load_v:", measurement.load_v)
#
# print("segments begin time:", measurement.segments.timestamp_begin)
# print("segments end time:", measurement.segments.timestamp_end)
# print("time:", measurement.segments.time)
# print("begin demand:", measurement.segments.begin_demand)
# print("end demand:", measurement.segments.end_demand)
print("average dynamic depth:", measurement.average_dynamic_depth)
print("average dynamic load:", measurement.average_dynamic_load)
print("average dynamic time:", measurement.average_dynamic_time)
# // -------------------
# // av
# dyn
# data
# // -------------------
#
# removeNAN();
# for (tdx_eInt32Usi_data & data : tdx_eInt32Usi_datas){
# if (data.channelGroupName == "Segments"){
# if (data.name == "Segment FB Mode"){
# measurement.segments.FBMode = data.data;
# }
# if (data.name == "Segment Points"){
# measurement.segments.points = data.data;
# measurement.segments.points_compressed = data.data; // values will be overwritten, if compressing data
# }
# if (data.name == "Segment LIA Status"){
# measurement.segments.LIAStatus = data.data;
# }
# }
# }
#
# if (measurement.depth.size() > maxDataSize){
# maxDataSize = measurement.depth.size();
# }