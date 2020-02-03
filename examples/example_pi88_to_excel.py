from pi88reader.pi88_importer import PI88Measurement
from pi88reader.pi88_to_excel import PI88ToExcel


def main():
    run()

def run():
    filename = '../resources/quasi_static_12000uN.tdm'
    filename = '../resources/AuSn_Creep/1000uN 01 LC.tdm'
    # measurements_path = '../resources/AuSn_Creep/'
    # measurements_path = '../resources/creep_example/'
    measurements_path = '../resources/d/'
    # measurements_path = '../resources/delme/'
    # measurements_path = '../resources/'
    # measurements_path = '../resources/190829_Cu_400-867-03-Nr16/'



    filename = '..\\resources\\quasi_static_12000uN.tdm'
    filename = '..\\resources\\AuSn_Creep\\1000uN 01 LC.tdm'

    filename = '..\\resources\\d\\Conti_Al_Silver_02_2500uN_006 LC.tdm'
    filename = '..\\resources\\dc\\500nm 02 DC.tdm'
    measurement = PI88Measurement(filename)

    to_excel = PI88ToExcel(measurement)
    to_excel.write("example_pi88_to_excel.xlsx")


if __name__ == '__main__':
    main()