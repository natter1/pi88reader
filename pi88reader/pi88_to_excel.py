"""
todo: check pandas -> can write excel (?)
"""
import numpy as np
from openpyxl import Workbook

from pi88reader.pi88importer import PI88Measurement, SegmentType


def main():
    filename = '..\\resources\\quasi_static_12000uN.tdm'
    to_excel = PI88ToExcel(filename)
    print(to_excel.measurement.get_segment_curve(SegmentType.LOAD))
    print(to_excel.measurement.settings.dict)

    to_excel.write_to_excel("delme.xlsx")


class PI88ToExcel:
    def __init__(self, tdm_filename):
        self.measurement = PI88Measurement(tdm_filename)
        self.tdm_filename = tdm_filename

    def write_to_excel(self, filename):
        wb = Workbook()

        ws1 = wb.active
        ws1.title = self.tdm_filename.split('.')[2].split('\\')[2]
        # print(self.tdm_filename.split('.')[2].split('\\')[2])
        quasi_static_data = np.column_stack(
            (self.measurement.time,
             self.measurement.depth,
             self.measurement.load
             )
        )
        quasi_static_header = [
            "time [s]",
            "depth [nm]",
            "load [µN]"
        ]
        ws1.append(quasi_static_header)

        for row in quasi_static_data.tolist():
            ws1.append(row)

        ws2 = wb.create_sheet(title="todo")

        print(ws1['AA10'].value)
        wb.save(filename=filename)


if __name__ == "__main__":
    main()
