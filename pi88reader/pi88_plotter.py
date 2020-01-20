"""
@author: Nathanael Jöhrmann
"""
from typing import Union, List, Tuple, Iterable, Optional
from matplotlib.figure import Figure
from matplotlib.pyplot import Axes
import matplotlib.pyplot as plt
import numpy as np

from pi88reader.pi88_importer import PI88Measurement


class PI88Plotter:
    """
    Used to plot data from PI88 measuremnts with matplotlib
    """
    def __init__(self, pi88_measurements: Union[PI88Measurement, List[PI88Measurement]]):
        self.measurements = []
        self.add_measurements(pi88_measurements)
        self.figsize = (5.6, 5.0)
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

    def create_figure_with_axes(self, x_label: str = "", y_label: str = "") -> Tuple[Figure, Axes]:
        figure = plt.figure(figsize=self.figsize, dpi=self.dpi, facecolor='w', edgecolor='w', frameon=True)
        axes = figure.add_subplot()
        axes.set_xlabel(x_label)
        axes.set_ylabel(y_label)
        return figure, axes

    def add_curve_to_axes(self, x, y, axes):  # todo: kwargs? legend entry etc.?
        axes.plot(x, y, **self.marker_style, **self.line_style)

    def get_load_displacement_plot(self):
        figure, axes = self.create_figure_with_axes(x_label="displacement [nm]", y_label="load [µN]")
        axes.set_prop_cycle('color', self.colors)
        for measurement in self.measurements:
            x = measurement.depth
            y = measurement.load
            self.add_curve_to_axes(x, y, axes)
        figure.tight_layout()
        return figure

    def set(self, dpi: Optional[int] = None):#, figsize: Optional[tuple[float, float]] = None):
        pass