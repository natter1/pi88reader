"""
@author: Nathanael Jöhrmann
"""
from typing import Iterable

import numpy as np
from scipy.optimize import curve_fit


def calc_S(A, hf, m, h_max):
    S = A * m * (h_max - hf) ** (m - 1)
    return S


def get_power_law_fit(x_data: Iterable, y_data: Iterable, start_values: list,
                      bounds: tuple = ((0, 0, 1), (np.inf, np.inf, np.inf))
                      ) -> dict:

    def fit_function(x, _A, _hf, _m):
        return _A * (x - _hf) ** _m

    result = {}

    x_data = np.array(x_data)
    y_data = np.array(y_data)
    start_values = np.array(start_values)

    popt, pcov = curve_fit(fit_function, x_data, y_data, p0=start_values,
                           bounds=bounds, maxfev=100000)

    result["A"] = popt[0]
    result["hf"] = popt[1]
    result["m"] = popt[2]
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


def fit_unloading(displacement: Iterable, load: Iterable, upper=0.95, lower=0.20) -> dict:
    """
    Power law fit for unloading curve. Returns a dictionary with fit parameters and calculated S, Er and H
    """
    # *************************************
    # =======  (S = A * (x-_hf)**m) =======
    # *************************************
    result = {"S": 0}
    if len(displacement) == 0:
        return result
    h_max = max(displacement)
    x_data, y_data = get_subset_by_y(displacement, load, upper, lower).values()
    if len(x_data) == 0:
        return result
    A_estimate = 0.1
    hf_estimate = h_max * 0.9
    m_start = 1.8

    start_values = [A_estimate, hf_estimate, m_start]

    bounds = ((0, 0, 1),
              (1e6, h_max, 1e6)
              )  # don't use np.inf instead of 1e6! - somehow this leads to curve_fit-failure

    result = get_power_law_fit(x_data, y_data, start_values, bounds)
    result["S"] = calc_S(**result, h_max=h_max)

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
