"""
todo: check pandas -> can write excel (?)
"""
from pi88reader.pi88importer import PI88Measurement
import numpy as np
from openpyxl import Workbook

def main():
    filename = '..\\resources\\quasi_static_12000uN.tdm'
    to_excel = PI88ToExcel(filename)
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
#
#
# pi88TDMToExcel
#
# pi88TDMToExcel
# excelCreator;
# for (int i =0;i < fileNames.count();i++)
# {
#     emit
# newStatus("<b>" + QString::number(i + 1) + "/" + QString::number(fileNames.count()) + ":</b> " + "load " + fileNames.at(
#     i));
# excelCreator.importTDMFile(fileNames.at(i));
# qInfo() << "<br>***** " + fileNames.at(i) + " *****";
# if (analysisType == atNoiseTest)
# {
#     emit
# newStatus("<b>" + QString::number(i + 1) + "/" + QString::number(
#     fileNames.count()) + ":</b> " + "FFT for " + fileNames.at(i));
# excelCreator.addDCCreepComparisonExcelSheet();
# }
#
# if (ui->tryUnloadingFitCheckBox->isChecked()){// do fit before compression!
# emit newStatus("<b>" + QString::
#     number(i + 1) + "/" + QString::number(fileNames.count()) + ":</b> " + "unloading fit for " + fileNames.at(i));
# excelCreator.measurement.tryUnloadingFit();
# }
# if (analysisType == atFESimulation){// do seperation befor compression
# excelCreator.measurement.polyFitLoadingCurve();
# excelCreator.measurement.polyFitUnloadingCurve();
# excelCreator.addSeperatedLoadUnloadCurve();
# excelCreator.writeAnsysTXT(excelCreator.measurement.areaFunction, ui->poissonDoubleSpinBox->value());
# }
# if (ui->compressCheckBox->isChecked()){
# emit newStatus("<b>" + QString::
#     number(i + 1) + "/" + QString::number(fileNames.count()) + ":</b> " + "compress data for " + fileNames.at(i));
# excelCreator.measurement.compressData(ui->compressMaxNSpinBox->value(), ui->compressMaxRelChangeDoubleSpinBox->value());
# }
# emit
# newStatus("<b>" + QString::number(i + 1) + "/" + QString::number(
#     fileNames.count()) + ":</b> " + "add settings sheet for " + fileNames.at(i));
# excelCreator.addMeasurementSettingsExcelSheet();
#
# if (analysisType == atCreepDC)
# {
#     emit
# newStatus("<b>" + QString::number(i + 1) + "/" + QString::number(
#     fileNames.count()) + ":</b> " + "add DC creep sheet for " + fileNames.at(i));
# excelCreator.addDCCreepExcelSheet();
# }
#
# if (analysisType == atCreepLC){
# emit newStatus("<b>" + QString::
#     number(i + 1) + "/" + QString::number(fileNames.count()) + ":</b> " + "add LC creep sheet for " + fileNames.at(i));
# excelCreator.addLCCreepExcelSheet();
# }
# emit
# newStatus("<b>" + QString::number(i + 1) + "/" + QString::number(
#     fileNames.count()) + ":</b> " + "add measurement data sheet for " + fileNames.at(i));
# excelCreator.addMeasurementDataExcelSheet(ui->poissonDoubleSpinBox->value());
# if (excelCreator.hasDynamicData()){
# emit newStatus("<b>" + QString::
#     number(i + 1) + "/" + QString::number(fileNames.count()) + ":</b> " + "add settings sheet for " + fileNames.at(i));
# excelCreator.addAvDynamicDataExcelSheet();
# }
# }
# // optional
# result
# file
# einlesen
# if (ui->loadResultsCheckBox->isChecked()){
# if ( !resultsFileName.isEmpty() )
# {
# excelCreator.triboscanResults.importResultsTxt(resultsFileName);
# if (excelCreator.triboscanResults.resultsLoaded){
# emit newStatus("<b>add results sheet from:</b> " + resultsFileName);
# excelCreator.addTriboscanResultsExcelSheet();
# // qDebug() << "";
# }
# }
# }
#
# // optional
# create
# comparison
# sheet
# if (ui->createComparisonCheckBox->isChecked())
# {
# / * statusLabel->setText("add comparison sheet");
# statusLabel->adjustSize();
# statusLabel->repaint();
# * / excelCreator.addComparisonExcelSheet(analysisType);
# }
#
# if (analysisType == atCreepDC){
# / * statusLabel->setText("add DCCreep comparison sheet");
# statusLabel->adjustSize();
# statusLabel->repaint();
# * / excelCreator.addDCCreepComparisonExcelSheet();
# }
#
# excelCreator.save(ui->comparisonStyleBox->currentText());
# / *statusLabel->setText("done");
# statusLabel->adjustSize();
# statusLabel->repaint();