import glob
import os
from bisect import bisect

import matplotlib.pyplot as plt
import numpy as np
import matplotlib.ticker as ticker

import pi88reader.my_styles as my_styles
import pi88reader.pptx_creator as pptx_creator
from pi88reader.pi88_matplotlib_tools import PlotStyle
from pi88reader.pi88importer import PI88Measurement
from pi88reader.pi88importer import SegmentType
import pi88reader.pptx_template as pptx_template


def main():
    # path = "..\\resources\\AuSn_Creep\\"
    # path = "..\\resources\\AuSn_Creep\\1000uN\\"
    # path = "..\\resources\\AuSn_Creep\\4000uN\\"
    # path = "..\\resources\\AuSn_Creep\\10000uN\\"
    # path = "..\\resources\\AuSn_Creep\\12500uN\\"
    # path = "..\\resources\\AuSn_Creep\\12500uN_2\\"
    # path = "..\\resources\\AuSn_Creep\\DMA\\"
    path = "..\\resources\\creep_example\\"

    files = get_tdm_files(path)
    # files.extend(get_tdm_files(path_2))

    figure, axes = create_figure(x_label=r"F/A [$N/m^2$]", y_label="creep rate [1/s]")
    dlog_figure, dlog_axes = create_figure(x_label=r"F/A [$N/m^2$]", y_label="creep rate [1/s]")
    load_disp_figure, load_disp_axes = create_figure(x_label="displacement [nm]", y_label=r"load [$\mathrm{\mu N}$]")
    style = PlotStyle(len(files))
    print(style.cmap)
    style.cmap = my_styles.CMAP_BERNHARD
    style.marker_map = my_styles.MARKER_BERNHARD
    axes.set_prop_cycle(color=style.cmap, marker=style.marker_map)
    dlog_axes.set_prop_cycle(color=style.cmap, marker=style.marker_map)

    for file in files:
        measurement = PI88Measurement(file)
        creep_rate_avg, load_over_area_avg = get_avg_strain_rate_and_sigma(measurement)

        # add_dlog_plot(dlog_axes, x=load_over_area_avg, y=creep_rate_avg, style=style, label=measurement.filename, fit_deg=1)
        add_dlog_plot(dlog_axes, x=load_over_area_avg, y=creep_rate_avg, style=style, label="", fit_deg=1)
        axes.plot(load_over_area_avg, creep_rate_avg, **style.marker, **style.line, label=measurement.filename)
        load_disp_axes.plot(measurement.depth, measurement.load, **style.marker, **style.line, label=measurement.filename)
    # for measurement in self.measurements:
    #     x = measurement.depth
    #     y = measurement.load
    #     axes.plot(x, y, **marker_style, **line_style)
    #     # axes.scatter(x, y, **marker_style)
    axes.legend()
    dlog_axes.legend()
    load_disp_axes.legend()
    figure.tight_layout()
    dlog_figure.tight_layout()
    load_disp_figure.tight_layout()
    figure.savefig(path + "stress_strain.png")
    dlog_figure.savefig(path + "dlog_stress_strain.png")
    load_disp_figure.savefig(path + "load_disp.png")

    # pptx = pptx_creator.PPTXCreator(template=pptx_template.TemplateETIT169(), title="Creep via Ni on AuSn")
    pptx = pptx_creator.PPTXCreator(template=pptx_template.TemplateExample(), title="Creep Example")
    pptx.add_matplotlib_figure(dlog_figure, slide_index=0, top_rel=0.22)
    pptx.add_matplotlib_figure(load_disp_figure, slide_index=0, top_rel=0.22, left_rel=0.5)
    pptx.save(path+"NI_on_AuSn.pptx")


def get_tdm_files(path):
    files = glob.glob(os.path.join(path, '*.tdm'))
    files.sort(key=os.path.getctime)  # sorted by creation time (in windows)
    return files


def create_figure(x_label="", y_label=""):
    figsize = (5.6, 5.0)
    figure = plt.figure(figsize=figsize, dpi=150, facecolor='w', edgecolor='w', frameon=True)
    axes = figure.add_subplot()
    axes.set_xlabel(x_label)
    axes.set_ylabel(y_label)

    return figure, axes


def get_avg_strain_rate_and_sigma(measurement):
    header, time, disp, load = measurement.get_segment_curve(SegmentType.HOLD)
    # for DMA:
    header, time, disp, load = measurement.get_segment_curve(SegmentType.HOLD, occurence=2)

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

        averaged_area = measurement.area_function.get_area(avg_disp[-1]) * 1e-18
        area_avg.append(averaged_area)
        averaged_load_over_area = avg_load[-1] * 1e-6 / averaged_area
        load_over_area_avg.append(averaged_load_over_area)
        creep_rate_avg.append((delta_disp[-1] / avg_disp[-2]) / delta_time[-1])

    return creep_rate_avg, load_over_area_avg


def add_dlog_plot(axes, x, y, style, label="", fit_deg=0):
    axes.loglog(x, y, **style.marker, **style.line, label=label,
                color=style.color, fillstyle="none")

    if fit_deg:
        log_x = np.log(x)
        log_y = np.log(y)
        coeffs = np.polyfit(log_x, log_y, deg=fit_deg)
        poly_1d = np.poly1d(coeffs)
        yfit = lambda x: np.exp(poly_1d(np.log(x)))
        # label = rf"$y = {coeffs[0]:.2f}x {coeffs[1]:+.2f}$"
        label = rf"$n = {coeffs[0]:.2f}$"
        axes.plot(x, yfit(x), color=style.color, marker="", label=label)

    # needed to prevent overlapping labels:
    locs = axes.get_xticklabels(minor=True)
    if len(locs)>5:
        axes.xaxis.set_minor_formatter(ticker.NullFormatter())
        axes.xaxis.set_major_locator(ticker.MaxNLocator(nbins=5))

    style.next_style()


if __name__ == "__main__":
    main()