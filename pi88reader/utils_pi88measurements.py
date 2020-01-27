"""
Collection of functions to handle list of measurements
@author: Nathanael Jöhrmmann
"""
from typing import Iterable


# 'Acquisition_Transducer_Serial'
# 'Acquisition_TriboScan_Version'


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

# ----------------------------------------------------------------------------------------------------------------------


def get_transducer_serials_string(measurements: Iterable) -> str:
    serials = get_set_by_setting_name("Acquisition_Transducer_Serial", measurements)
    return get_summary_by_set(serials)

# ----------------------------------------------------------------------------------------------------------------------


def get_triboscan_versions_string(measurements: Iterable) -> str:
    versions = get_set_by_setting_name("Acquisition_TriboScan_Version", measurements)
    return get_summary_by_set(versions)

# ----------------------------------------------------------------------------------------------------------------------


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

def get_measurement_types(measurements: Iterable):
    pass


