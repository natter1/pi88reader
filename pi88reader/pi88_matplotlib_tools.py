import numpy as np
import matplotlib.pyplot as plt
import numpy as np
import pi88reader.my_styles as my_styles

class PlotStyle:
    def __init__(self, n_colors=4):
        self.line = dict(linestyle='')
        self.cmap = plt.cm.viridis(np.linspace(0, 1, n_colors))
        self.marker_map = ["x", "+", "1"]  # my_styles.MARKER_BERNHARD
        self.current_color_index = 0
        self.current_marker_index = 0

    @property
    def color(self):
        assert 0 <= self.current_color_index < len(self.cmap), "current_color_index invalid!"
        return self.cmap[self.current_color_index % len(self.cmap)]

    @property
    def marker(self):
        assert 0 <= self.current_color_index < len(self.cmap), "current_marker_index invalid!"
        marker = self.marker_map[self.current_marker_index % len(self.marker_map)]
        return dict(marker=marker, markeredgewidth=1, markersize=6)

    def next_color(self):
        self.current_color_index = (self.current_color_index + 1) % len(self.cmap)

    def next_marker(self):
        self.current_marker_index = (self.current_marker_index + 1) % len(self.marker_map)

    def next_style(self):
        self.next_color()
        self.next_marker()

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


def main():
    # todo: possible circular import!
    from pi88reader.pi88importer import PI88Measurement, SegmentType

    filename = '..\\resources\\quasi_static_12000uN.tdm'
    measurement = PI88Measurement(filename)

    plot = plt.scatter(measurement.time, measurement.depth)
    plt.scatter(measurement.time, measurement.load)
    # plt.scatter(measurement.depth, measurement.load)
    plt.show()


if __name__ == "__main__":
    main()
