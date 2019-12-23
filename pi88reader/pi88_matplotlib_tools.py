"""
@author: Nathanael Jöhrmann
"""
import matplotlib.pyplot as plt
import numpy as np


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




def main():
    # todo: possible circular import!
    from pi88reader.pi88_importer import PI88Measurement

    filename = '..\\resources\\quasi_static_12000uN.tdm'
    measurement = PI88Measurement(filename)

    plotter = PI88Plotter(measurement)
    figure = plotter.get_load_displacement_plot()
    figure.show()


if __name__ == "__main__":
    main()
