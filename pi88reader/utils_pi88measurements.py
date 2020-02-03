"""
Functions to handle a collection of measurements.
@author: Nathanael Jöhrmmann
"""
from typing import Iterable, Collection, Union, ValuesView


def get_set_by_setting_name(name: str, measurements: Iterable) -> set:
    result = set()
    for m in measurements:
        result.add(m.settings.dict[name])
    return result


def get_summary_by_set(my_set: set) -> str:
    result = ""
    for text in my_set:
        if result:
            result += ", "
        result += text
    return result


def get_transducer_serials_string(measurements: Iterable) -> str:
    serials = get_set_by_setting_name("Acquisition_Transducer_Serial", measurements)
    return get_summary_by_set(serials)


def get_triboscan_versions_string(measurements: Iterable) -> str:
    versions = get_set_by_setting_name("Acquisition_TriboScan_Version", measurements)
    return get_summary_by_set(versions)


def get_feedback_modes(measurements: Iterable) -> set:
    # 1 ... ? displacement controlled (careful! first segments with in contact always DC)
    # 5 ... load controlled
    result = set()
    for measurement in measurements:
        result.add(measurement.segments.fb_mode[-1])
    return result


def get_feedback_modes_string(measurements: Iterable) -> str:
    result = ""
    modes = get_feedback_modes(measurements)
    if 1 in modes:
        result += "displacement controlled"
    if 5 in modes:
        if result:
            result += ", "
        result += "load controlled"
    return result


def get_measurement_dates(measurements: Iterable) -> set:
    result = set()
    for m in measurements:
        result.add(m.settings.dict["Acquisition_Timestamp"].date())
    return result


def get_date_intervall_string(measurements: Iterable) -> str:
    dates = get_measurement_dates(measurements)
    if len(dates) == 1:
        return min(dates).__str__()
    elif len(dates) > 1:
        return min(dates).__str__() + " ... " + max(dates).__str__()
    return ""


def get_aborted_measurements(measurements: Iterable) -> list:
    result = []
    for m in measurements:
        if m.settings.dict["Acquisition_Test_Aborted"]:  # todo: check with aborted measurement
            print(m.settings.dict["Acquisition_Test_Aborted"])
            result.append(m)
    return result


def get_measurements_meta_table_data(measurements: Collection) -> list:
    """Get table like meta data for a collection of measurements."""
    return [["Number of measurements:", len(measurements)],
            ["Feedback modes: ", get_feedback_modes_string(measurements)],
            ["Measurements aborted:", len(get_aborted_measurements(measurements))],
            ["Measurement dates: ", get_date_intervall_string(measurements)],
            ["Transducer serials: ", get_transducer_serials_string(measurements)],
            ["Triboscan versions: ", get_triboscan_versions_string(measurements)]]


def get_measurements_result_table_data(data_list: Union[ValuesView, Iterable[dict]]) -> list:
    result = [["Name", "Er [GPa]", "E [GPa]", "H [GPa"]]

    for data in data_list:
        result.append([data['base_name'], f"{data['Er']:.2f}", f"{data['E']:.2f}", f"{data['hardness']:.2f}"])

    return result

