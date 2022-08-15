from pathlib import Path
from pprint import pprint

import matplotlib.pyplot as plt
import numpy as np
import numpy.typing as npt
from numpy.polynomial import Polynomial
from scipy import optimize

from pi88reader.ni_analyser import calc_unloading_data
from pi88reader.pi88_importer import PI88Measurement, SegmentType


def polynomial_fit(m: PI88Measurement,  segment_type: SegmentType, polynom_deg=5) -> npt.NDArray:
    """
    Polynomial fit for given SegmentType. Returns polynom coef.
    """
    def f(x, *p):
        return Polynomial(p)(x)

    result = np.ndarray(0)
    _, _, depth, load = m.get_segment_curve(segment_type)
    # x_data, y_data = m.depth, m.load
    if len(depth) == 0:
        return result

    polynom = Polynomial.fit(depth, load, polynom_deg, domain=[])  # using domain=[] gives correct coef., otherwise there is some shift/stretching
    plt.plot(*polynom.linspace(domain=[depth.min(), depth.max()]), label="Polynom")
    plt.plot(depth, load, '.', label="exp.")


    sigma = np.ones(len(depth))
    sigma[-1] = 0.001
    result, _ = optimize.curve_fit(f, depth, load, np.zeros(polynom_deg+1), sigma=sigma)

    plt.plot(depth, f(depth, *result), label="Polynom through max load/disp")
    plt.legend()
    plt.show()

    return result


def powerlaw_fit_unloading_dict(m: PI88Measurement, upper=0.95, lower=0.20, beta=1, poisson_ratio=0.3):
    result = calc_unloading_data(m, upper=upper, lower=lower, beta=beta, poisson_ratio=poisson_ratio)
    return result


def max_displacement_during_load(m: PI88Measurement) -> float:
    _, _, loading_depth, _ = m.get_segment_curve(SegmentType.LOAD)
    return loading_depth[-1]


def displacement_after_unload(m: PI88Measurement) -> float:
    _, _, depth, _ = m.get_segment_curve(SegmentType.UNLOAD)
    return depth[-1]


def hold_displacement(m: PI88Measurement) -> float:
    """Returns displacement change during hold."""
    _, _, unloading_depth, _ = m.get_segment_curve(SegmentType.UNLOAD)
    return unloading_depth[0] - max_displacement_during_load(m)


def create_ni_sim_input_file(measurement: PI88Measurement, poisson_ratio=0.3):
    result = ""
    af = measurement.area_function
    result += "TIP area function coefficients (start row 2; N=6)\n"
    result += f"{af.c0}\n{af.c1}\n{af.c2}\n{af.c3}\n{af.c4}\n{af.c5}\n"

    result += "polynom fit loading curve (start row 9; N=7)\n"
    for c in polynomial_fit(measurement, segment_type=SegmentType.LOAD, polynom_deg=6):
        result += f"{c}\n"

    result += "polynom fit unloading curve (start row 17; N=7)\n"
    for c in polynomial_fit(measurement, segment_type=SegmentType.UNLOAD, polynom_deg=6):
        result += f"{c}\n"

    result += "fit unloading curve P=A*(h-hf)^m (start row 25; N=3)\n"
    unloading_dict = powerlaw_fit_unloading_dict(measurement, poisson_ratio=poisson_ratio)
    result += f"{unloading_dict['fit_A']}\n"
    result += f"{unloading_dict['fit_hf']}\n"
    result += f"{unloading_dict['fit_m']}\n"

    result += "poisson ratio sample (also used to calc E below) (row 29)\n"
    result += f"{unloading_dict['poisson_ratio']}\n"

    result += "calculated E [GPa] (not Er!) (row 31)\n"
    result += f"{unloading_dict['E']}\n"

    result += "beta\n"
    result += f"{unloading_dict['beta']}\n"
    # todo: change later after implementing creep during hold in FEM
    displacement_during_hold = hold_displacement(measurement)
    result += "delta displacement during hold (row 33)\n"
    result += f"{displacement_during_hold}\n"

    result += "max. displacement [nm] (row 35)\n"
    result += f"{max_displacement_during_load(measurement)}\n"

    result += "unload displacement end (~zero load) [nm] (row 37)\n"
    result += f"{displacement_after_unload(measurement)}\n"

    _, _, unloading_depth, unloading_load = measurement.get_segment_curve(SegmentType.UNLOAD)
    result += "exp. unloading curve (disp;load) row(39ff)\n"
    for i, depth in enumerate(unloading_depth):
        result += f"{depth};{unloading_load[i]}\n"

    result += "END"

    save_path = Path(measurement.filename).parent/(measurement.base_name + "_DATA.txt")
    text_file = open(save_path, "w")
    text_file.write(result)
    text_file.close()


filename = Path("D:\\PI88\\2022\\220506_Al_DeltaCanti\\delta_cantilever_500nm_Al")/"1000uN 01 LC.tdm"  # "'..\\resources\\quasi_static_12000uN.tdm'

measurement = PI88Measurement(filename)
create_ni_sim_input_file(measurement)
# pprint((m.settings.dict))
# pprint(m.area_function.get_area(100))