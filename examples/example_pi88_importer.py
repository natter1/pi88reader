from pprint import pprint
from pi88reader.pi88_importer import PI88Measurement

# filename = '..\\resources\\nanobruecken2020\\Conti_Al_Silver_02_2500uN_001 LC.tdm'
filename = '..\\resources\\quasi_static_12000uN.tdm'

measurement = PI88Measurement(filename)
pprint(len(measurement.settings.dict))
pprint(measurement.area_function.get_area(100))