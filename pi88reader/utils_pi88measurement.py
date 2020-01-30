"""
@author: Nathanael Jöhrmann
"""

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


def get_measurement_result_data(measurement: "PI88Measurement", poisson_ratio = 0.3, beta = 1.0) -> list:
    """Get table like result data for a measurement."""
    return [["H [GPa] (TriboScan)", f"{measurement.settings.dict['Quasi_Analysis_Hardness__GPa__']:.2f}"],
            ["Er [GPa] (Triboscan)",  f"{measurement.settings.dict['Quasi_Analysis_Reduced_Modulus__GPa__']:.2f}"],
            ["H [GPa]", None],
            ["Er [GPa]", None],
            [f"E [GPa] (PN={poisson_ratio}, Beta={beta}", None]
            ]


def get_measurement_meta_data(measurement: "PI88Measurement") -> list:
    return [["Filename (original):", measurement.settings.dict["Acquisition_Quasi_File_Name"]],
            ["Measurement date:", measurement.settings.dict["Acquisition_Timestamp"].date()],
            ["Measurement aborted:", f"{is_aborted_measurement(measurement)}"],
            ["Drift correction:", f"{is_drift_corrected(measurement)}"],
            ["Drift rate:", f"{get_drift_rate(measurement):.2f} nm/s"]
            ]