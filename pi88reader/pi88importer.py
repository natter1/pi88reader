import tdm_loader


class PI88Measurement:
    time = None

data_file = tdm_loader.OpenFile('D:\\py_projects\\pi88reader\\resources\\12000uN 01 LC.tdm')
print(data_file)

print(data_file.channel_dict("Indentation All Data Points"))

PI88Measurement.time = data_file.channel("Indentation All Data Points", "Test Time")

print(PI88Measurement.time)

# for (tdx_eFloat64Usi_data & data : tdx_eFloat64Usi_datas){
#                                                          // -------------------
#                                                          // all quasi static
# // -------------------
# if (data.channelGroupName == "Indentation All Data Points"){
# if (data.name == "Test Time"){
# measurement.time = data.data;
# }
# if (data.name == "Indent Disp."){
# measurement.depth = data.data;
# }
# if (data.name == "Indent Load"){
# measurement.load = data.data;
# }
# if (data.name == "Indent Disp. Volt."){
# measurement.depth_V = data.data;
# }
# if (data.name == "Indent Act. Load Volt."){
# measurement.load_V = data.data;
# }
# }
# if (data.channelGroupName == "Segments"){
# if (data.name == "Segment Begin Time"){
# measurement.segments.timestamp_begin = data.data;
# }
# if (data.name == "Segment End Time"){
# measurement.segments.timestamp_end = data.data;
# }
# if (data.name == "Segment Time"){
# measurement.segments.time = data.data;
# }
# if (data.name == "Segment Begin Demand"){
# measurement.segments.begin_demand = data.data;
# }
# if (data.name == "Segment End Demand"){
# measurement.segments.end_demand = data.data;
# }
# }