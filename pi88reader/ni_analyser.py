"""
@author: Nathanael Jöhrmann
"""
import math
from typing import Iterable

import numpy as np
from scipy.optimize import curve_fit

from pi88reader.pi88_importer import SegmentType


def calc_stiffness(fit_A, fit_hf, fit_m, h_max, **_):
    S = fit_A * fit_m * (h_max - fit_hf) ** (fit_m - 1)
    return S


def calc_hc(h_max: float, P_max: float, stiffness: float, **_):
    # hc = h - 0.75*Pmax/S
    return h_max - 0.75 * P_max / stiffness


def calc_hardness(P_max: float, Ac_max: float, **_) -> float:
    return P_max / Ac_max * 1e3


def calc_Er(Ac_max: float, stiffness: float, beta: float, **_) -> float:
    return 0.5 / beta * (math.pi / Ac_max) ** 0.5 * stiffness * 1000


def calc_E(Er: float, poisson_ratio: float, E_tip: float = 1140, poisson_ratio_tip: float = 0.07, **_):
    return (1 - poisson_ratio ** 2) / (1 / Er - (1 - poisson_ratio_tip ** 2) / (E_tip))  # * 1e9))

def get_power_law_fit(x_data: Iterable, y_data: Iterable, start_values: list,) -> dict:

    def fit_function(x, _A, _hf, _m):
        return _A * (x - _hf) ** _m

    result = {}

    x_data = np.array(x_data)
    y_data = np.array(y_data)
    start_values = np.array(start_values)

    try:
        popt, pcov = curve_fit(fit_function, x_data, y_data, p0=start_values, maxfev=10000, method='lm')
        result.update({"fit_failed": False, "fit_A": popt[0], "fit_hf": popt[1], "fit_m": popt[2]})
    except ValueError as e:
        result.update({"fit_failed": True, "fit_A": 0, "fit_hf": 0, "fit_m": 0})
    except RuntimeError:  # no solution with maxfev (maximal number of function evaluations) iterations
        result.update({"fit_failed": True, "fit_A": 0, "fit_hf": 0, "fit_m": 0})
    return result


def get_subset_by_y(x_data: Iterable, y_data: Iterable, upper: float, lower: float) -> dict:
    """Get a subset of given data by using upper and lower limit on y_data."""
    result = {"x": [], "y": []}
    y_max = max(y_data)

    for x, y in zip(x_data, y_data):
        if lower*y_max <= y <= upper*y_max:
            result["x"].append(x)
            result["y"].append(y)

    return result


def fit_unloading(displacement: Iterable, load: Iterable, upper, lower) -> dict:
    """
    Power law fit for unloading curve. Returns a dictionary with fit parameters
    """
    result = {}
    x_data, y_data = get_subset_by_y(displacement, load, upper, lower).values()
    if len(x_data) == 0:
        return result
    A_estimate = 0.1
    hf_estimate = min(displacement) * 0.9
    m_start = 1.8

    start_values = [A_estimate, hf_estimate, m_start]

    result = get_power_law_fit(x_data, y_data, start_values)


    return result


def calc_unloading_data(measurement, upper=0.95, lower=0.20, beta=1, poisson_ratio=0.3) -> dict:
    result = {
        "base_name": measurement.base_name,
        "upper": upper,
        "lower": lower,
        "beta": beta,
        "poisson_ratio": poisson_ratio,
        "h_max": 0, "P_max": 0,
        "fit_A": 0, "fit_hf": 0, "fit_m": 0, "fit_failed": True,
        "stiffness": 0,
        "hc_max": 0, "Ac_max": 0,
        "hardness": 0,
        "Er": 0, "E": 0
    }
    header, time, displacement, load = measurement.get_segment_curve(SegmentType.UNLOAD, occurence=-1)
    if len(displacement) == 0:
        return result
    result["h_max"] = max(displacement)
    result["P_max"] = max(load)
    result.update(fit_unloading(displacement, load, upper, lower))
    if result["fit_failed"]:
        return result
    result["stiffness"] = calc_stiffness(**result)
    result["hc_max"] = calc_hc(**result)
    result["Ac_max"] = measurement.area_function.get_area(result["hc_max"])
    result["hardness"] = calc_hardness(**result)
    result["Er"] = calc_Er(**result)
    result["E"] = calc_E(**result)
    return result


# ********************************************************************************
# in development
# ********************************************************************************
# from pi88reader.pi88_importer import SegmentType
from bisect import bisect


def get_avg_strain_rate_and_sigma(time, disp, load, area_function):  # todo: area_function; -> PI88Measurement.get_dict_for_creep_analyse
    """
    Uses data from a hold segment (time, displacement, load) and an area-function,
     to calculate avg. strain rate and sigma
    """
    # QS
    # header, time, disp, load = measurement.get_segment_curve(SegmentType.HOLD)
    # for DMA:
    # header, time, disp, load = measurement.get_segment_curve(SegmentType.HOLD, occurence=2)

    # find index with t > 50
    min_index = bisect(time, 50)

    # divide in roughly 130 parts
    parts = 10  # 4
    n = len(time[min_index:]) // parts  # average over n values; // -> floor division

    avg_time = []
    avg_disp = []
    avg_load = []

    delta_time = []  # [s]
    delta_disp = []  # [m]

    area_avg = []  # [m^2]
    load_over_area_avg = []  # [N/m^2]
    creep_rate_avg = []  # [m/s]

    start_index = min_index - n
    end_index = start_index + n
    avg_time.append(np.mean(time[start_index:end_index]))
    avg_disp.append(np.mean(disp[start_index:end_index]))
    avg_load.append(np.mean(load[start_index:end_index]))

    for i in range(0, parts):
        start_index = min_index + i * n
        end_index = start_index + n
        avg_time.append(np.mean(time[start_index:end_index]))
        avg_disp.append(np.mean(disp[start_index:end_index]))
        avg_load.append(np.mean(load[start_index:end_index]))
        # avg_load.append(np.mean(load[min_index:]))
        # avg_disp.append(np.mean(disp[min_index:]))

        delta_time.append(avg_time[-1] - avg_time[-2])
        delta_disp.append((avg_disp[-1] - avg_disp[-2]) * 1e-9)

        averaged_area = area_function(avg_disp[-1]) * 1e-18
        area_avg.append(averaged_area)
        averaged_load_over_area = avg_load[-1] * 1e-6 / averaged_area
        load_over_area_avg.append(averaged_load_over_area)
        creep_rate_avg.append((delta_disp[-1] / avg_disp[-2]) / delta_time[-1])

    return creep_rate_avg, load_over_area_avg
