import numpy as np
import matplotlib.pyplot as plt
import numpy as np


class PI88Plotter:
    def __init__(self):
        self.measurements = []

    def add_measurement(self, measurement):
        self.measurements.append(measurement)

    def get_load_displacement_plot(self, figsize=(6.4, 6.8)):
        figure = plt.figure(figsize=figsize, dpi=100, facecolor='w', edgecolor='w', frameon=True)
        # axes = figure.add_axes([0.15, 0.1, 0.8, 0.8])
        axes = figure.add_subplot()
        axes.set_xlabel("displacement [nm]")
        axes.set_ylabel("load [µN]")
        for measurement in self.measurements:
            x = measurement.depth
            y = measurement.load
            axes.scatter(x, y)
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
