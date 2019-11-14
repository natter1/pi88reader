import numpy as np
import matplotlib.pyplot as plt
import numpy as np


class PI88Plotter:
    def __init__(self):
        self.measurements = []

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

    def get_load_displacement_plot(self, figsize=(6.4, 6.8)):
        marker_style = dict(marker='o', markeredgewidth=0, markersize=2)
        line_style = dict(linestyle='')

        figure = plt.figure(figsize=figsize, dpi=300, facecolor='w', edgecolor='w', frameon=True)
        # axes = figure.add_axes([0.15, 0.1, 0.8, 0.8])
        axes = figure.add_subplot()
        colors = plt.cm.viridis(np.linspace(0, 1, 30))
        axes.set_prop_cycle('color', colors)
        axes.set_xlabel("displacement [nm]")
        axes.set_ylabel("load [µN]")
        for measurement in self.measurements:
            x = measurement.depth
            y = measurement.load
            axes.plot(x, y, **marker_style, **line_style)
            #axes.scatter(x, y, **marker_style)
        figure.tight_layout()
        return figure



from pi88reader.pi88importer import PI88Measurement, SegmentType


def main():
    filename = '..\\resources\\quasi_static_12000uN.tdm'
    measurement = PI88Measurement(filename)

    plot = plt.scatter(measurement.time, measurement.depth)
    plt.scatter(measurement.time, measurement.load)
    # plt.scatter(measurement.depth, measurement.load)
    plt.show()


if __name__ == "__main__":
    main()
