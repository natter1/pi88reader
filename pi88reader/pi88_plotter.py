"""
@author: Nathanael Jöhrmann
"""
import os
from enum import Enum, auto
from typing import Union, List, Tuple, Iterable, Optional
from matplotlib.figure import Figure
from matplotlib.pyplot import Axes
import matplotlib.pyplot as plt
import numpy as np

from pi88reader.pi88_importer import PI88Measurement, load_tdm_files
from pi88reader.plotter_styles import PlotterStyle


class Data(Enum):
    TIME = auto()
    LOAD = auto()
    DISPLACEMENT = auto()


class PI88Plotter:
    """
    Used to plot data from PI88 measuremnts with matplotlib
    """
    def __init__(self, pi88_measurements: Union[PI88Measurement, List[PI88Measurement]]):
        self.measurements = []
        self.add_measurements(pi88_measurements)
        self.figure_size = (5.6, 5.0)
        self.dpi = 150

        self.marker_style = dict(marker='o', markeredgewidth=0, markersize=2)
        self.line_style = dict(linestyle='')
        self.colors = plt.cm.viridis(np.linspace(0, 1, len(self.measurements)))

    def add_measurements(self, measurements: Union[PI88Measurement, Iterable[PI88Measurement]]) -> None:
        """
        Adds a single PI88Measurement or a list o PI88Measurement's to the plotter.
        """
        if measurements:
            try:
                self.measurements.extend(measurements)
            except TypeError:
                self.measurements.append(measurements)

    def load_tdm_files(self, path: str, sort_key=os.path.getctime):  # sorted by creation time (using windows)
        self.measurements.extend(load_tdm_files(path, sort_key))

    def create_figure_with_axes(self, x_label: str = "", y_label: str = "") -> Tuple[Figure, Axes]:
        figure = plt.figure(figsize=self.figure_size, dpi=self.dpi, facecolor='w', edgecolor='w', frameon=True)
        axes = figure.add_subplot()
        axes.set_xlabel(x_label)
        axes.set_ylabel(y_label)
        return figure, axes

    def add_curve_to_axes(self, x, y, axes):  # todo: kwargs? legend entry etc.?
        axes.plot(x, y, **self.marker_style, **self.line_style)

    def get_load_displacement_plot(self):
        return self.get_plot(Data.DISPLACEMENT, Data.LOAD)

    def get_load_time_plot(self):
        return self.get_plot(Data.TIME, Data.LOAD)

    def get_displacement_time_plot(self):
        pass

    def get_plot(self, data_x: Data, data_y: Data):
        data_type = { # name, unit, PI88Measurement attribute name
            Data.TIME: ("time", "s", "time"),
            Data.LOAD: ("load", "µN", "load"),
            Data.DISPLACEMENT: ("displacement", "nm", "depth")
        }
        x_name, x_unit , x_attr_name = data_type[data_x]
        y_name, y_unit , y_attr_name = data_type[data_y]

        figure, axes = self.create_figure_with_axes(x_label=f"{x_name} [{x_unit}]", y_label=f"{y_name} [{y_unit}]")
        axes.set_prop_cycle('color', self.colors)
        for measurement in self.measurements:
            x = getattr(measurement, x_attr_name)
            y = getattr(measurement, y_attr_name)
            self.add_curve_to_axes(x, y, axes)
        figure.tight_layout()
        return figure

    def set(self,
            plotter_style: Optional[PlotterStyle] = None,
            dpi: Optional[int] = None,
            figure_size: Optional[tuple[float, float]] = None
            ):
        if plotter_style:
            self.read_plotter_style(plotter_style)
        if dpi:
            self.dpi = dpi
        if figure_size:
            self.figure_size = figure_size

    def read_plotter_style(self, style: PlotterStyle):
        if style.dpi:
            self.dpi = style.dpi
        # ...
