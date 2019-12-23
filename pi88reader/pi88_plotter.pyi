import matplotlib.pyplot as plt
import numpy as np

class PI88Plotter:
    """
    Used to plot data from PI88 measuremnts with matplotlib
    :param pi88_measurements: pi88_measurement or list of pi88_measurements
    """
    def __init__(self, pi88_measurements):
        self.measurements = []
        self.add_measurements(pi88_measurements)
        self.figsize = (5.6, 5.0)

        self.marker_style = dict(marker='o', markeredgewidth=0, markersize=2)
        self.line_style = dict(linestyle='')
        self.colors = plt.cm.viridis(np.linspace(0, 1, len(self.measurements)))

    def add_measurements(self, measurements):
        """
        Adds a single PI88Measurement or a list o PI88Measurement's to the plotter.

        :param measurements: PI88Measurement or list of PI88Measurement
        :return:
        """
        try:
            self.measurements.extend(measurements)
        except:
            self.measurements.append(measurements)

    def create_figure_with_axes(self, x_label="", y_label=""):
        figure = plt.figure(figsize=self.figsize, dpi=150, facecolor='w', edgecolor='w', frameon=True)
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
