from pi88reader.pi88_importer import PI88Measurement
from pi88reader.pi88_to_excel import PI88ToExcel


def main():
    run()

def run():
    # measurements_path = '../resources/creep_example/'
    # measurements_path = '../resources/'
    filename = '..\\resources\\quasi_static_12000uN.tdm'
    measurement = PI88Measurement(filename)
    to_excel = PI88ToExcel(measurement)
    to_excel.write("example_pi88_to_excel.xlsx")


if __name__ == '__main__':
    main()