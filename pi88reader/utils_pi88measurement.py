"""
@author: Nathanael Jöhrmann
"""
from typing import Tuple, List

from pi88reader.ni_analyser import fit_unloading, calc_hardness, calc_Er, calc_unloading_data
from pi88reader.pi88_importer import SegmentType


def is_aborted_measurement(measurement) -> bool:
    result = False
    if measurement.settings.dict["Acquisition_Test_Aborted"]:
        result = True
    return result


def is_drift_corrected(measurement) -> bool:
    result = False
    if measurement.settings.dict["Current_Drift_Correction"]:
        result = True
    return result


def get_drift_rate(measurement) -> float:
    return measurement.settings.dict["Current_Drift_Rate__nm___s__"]

# def get_unloading_fit(measurement) -> float:
#     header, time, disp, load = measurement.get_segment_curve(SegmentType.UNLOAD, occurence=-1)  # -1 -> last one found
#     result = fit_unloading(disp, load)
#     return result


def get_measurement_result_table_data(measurement: "PI88Measurement", data: dict) -> List[List[str]]:
    """Get table like result data for a measurement. The data dict can be calculated via calc_unloading_data."""
    if measurement.settings.dict["Quasi_Analysis_Fit_Has_Been_Done"] == -1: #0:
        H_triboscan = "no fit done"
        Er_triboscan = "no fit done"
    else:
        print(measurement.settings.dict["Quasi_Analysis_Fit_Has_Been_Done"])
        H_triboscan = f"{measurement.settings.dict['Quasi_Analysis_Martens_Hardness__GPa__']:.2f}"
        Er_triboscan = f"{measurement.settings.dict['Quasi_Analysis_Reduced_Modulus__GPa__']:.2f}"

    return [["H [GPa] (TriboScan)", H_triboscan],
            ["Er [GPa] (TriboScan)", Er_triboscan],
            ["H [GPa]", f"{data['hardness']:.2f}"],
            [f"Er [GPa] (\u03B2={data['beta']})", f"{data['Er']:.2f}"],
            [f"E [GPa] (\u03BD={data['poisson_ratio']})", f"{data['E']:.2f}"]
            ]


def get_measurement_meta_table_data(measurement: "PI88Measurement") -> list:
    return [["Filename (original):", measurement.settings.dict["Acquisition_Quasi_File_Name"]],
            ["Measurement date:", measurement.settings.dict["Acquisition_Timestamp"].date()],
            ["Measurement aborted:", f"{is_aborted_measurement(measurement)}"],
            ["Drift correction:", f"{is_drift_corrected(measurement)}"],
            ["Drift rate:", f"{get_drift_rate(measurement):.2f} nm/s"]
            ]