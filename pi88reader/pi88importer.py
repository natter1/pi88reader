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
        if group_name not in data.get_channel_group_names():
            return
        self.average_dynamic_depth = data.get_channel_data(group_name, "Indent Disp.")


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
# print("average dynamic depth:", measurement.average_dynamic_depth)

# // -------------------
# // av
# dyn
# data
# // -------------------
# if (data.channelGroupName == "Indentation Averaged Values"){
# if (data.name == "Indent Disp."){
# measurement.avDyn_Depth = data.data;
# }
# if (data.name == "Indent Load"){
# measurement.avDyn_Load = data.data;
# }
# if (data.name == "Test Time"){
# measurement.avDyn_Time = data.data;
# }
# }
# if (data.channelGroupName == "Basic Dynamic Averaged Values 1"){
# if (data.name == "Dynamic Freq."){
# measurement.avDyn_Freq = data.data;
# }
# if (data.name == "Disp. Amp."){
# measurement.avDyn_Disp_Amp = data.data;
# }
# if (data.name == "Phase Shift"){
# measurement.avDyn_Phase_Shift = data.data;
# }
# if (data.name == "Load Amp."){
# measurement.avDyn_Load_Amp = data.data;
# }
# if (data.name == "Dynamic Comp."){
# measurement.avDyn_dyn_Comp = data.data;
# }
# }
# if (data.channelGroupName == "Visco-Elastic: Indentation Averaged Values 1"){
# if (data.name == "Storage Mod."){
# measurement.avDyn_Storage_Mod = data.data;
# }
# if (data.name == "Loss Mod."){
# measurement.avDyn_Loss_Mod = data.data;
# }
# if (data.name == "Tan-Delta"){
# measurement.avDyn_Tan_Delta = data.data;
# }
# if (data.name == "Complex Mod."){
# measurement.avDyn_Complex_Mod = data.data;
# }
# if (data.name == "Hardness"){
# measurement.avDyn_Hardness = data.data;
# }
# }
# }