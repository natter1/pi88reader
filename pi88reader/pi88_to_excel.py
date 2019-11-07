"""
todo: check pandas -> can write excel (?)
"""
import numpy as np
from openpyxl import Workbook
from openpyxl.styles import Font
import time as timer

from pi88reader.pi88importer import PI88Measurement, SegmentType


def main():
    filename = '..\\resources\\quasi_static_12000uN.tdm'
    to_excel = PI88ToExcel(filename)
    # print(to_excel.measurement.get_segment_curve(SegmentType.LOAD))
    # print(to_excel.measurement.settings.dict)

    to_excel.write("delme.xlsx")


class PI88ToExcel:
    def __init__(self, tdm_filename):
        self.measurement = PI88Measurement(tdm_filename)
        self.tdm_filename = tdm_filename

    def write(self, filename):
        wb = Workbook()
        self.write_quasi_static_data(wb.active)

        ws2 = wb.create_sheet(title="load_unload")
        self.write_segment_data(ws2)
        wb.save(filename=filename)

    def write_quasi_static_data(self, ws):
        ws.title = self.tdm_filename.split('.')[2].split('\\')[2]
        data = self.measurement.get_quasi_static_curve()
        self.write_data(ws, data)

    def write_segment_data(self, ws):
        ws.title = "segments"
        ws.cell(row=1, column=1).value = "LOAD:"
        data = self.measurement.get_segment_curve(SegmentType.LOAD)
        self.write_data(ws, data, row=1, col=2)

        ws.cell(row=1, column=5).value = "HOLD:"
        data = self.measurement.get_segment_curve(SegmentType.HOLD)
        self.write_data(ws, data, row=1, col=6)

        ws.cell(row=1, column=9).value = "UNLOAD:"
        data = self.measurement.get_segment_curve(SegmentType.UNLOAD)
        self.write_data(ws, data, row=1, col=10)

    def write_row(self, ws, data, row, col):
        font = Font(bold=True)
        for i, value in enumerate(data):
            ws.cell(row=row, column=col+i).value = value
            ws.cell(row=row, column=col + i).font = font

    def write_cols(self, ws, data, row, col):
        for i, value in enumerate(data[0]):
            for j, column in enumerate(data):
                ws.cell(row=row+i, column=col+j).value = column[i]

    def write_data(self, ws, data, row=1, col=1):
        header = data[0]
        if header:
            self.write_row(ws, header, row, col)
            row+=1
        self.write_cols(ws, data[1:], row, col)
        # for i, value in enumerate(data[1]):
        #     for j, column in enumerate(data[1:]):
        #         ws.cell(row=row+i, column=col+j).value = column[i]

if __name__ == "__main__":
    main()
