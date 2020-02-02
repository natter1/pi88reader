"""
@author: Nathanael Jöhrmann
"""
import os
from typing import Union, Iterable, Optional, List

import matplotlib.pyplot as plt
import pptx_tools.style_sheets as style_sheets
from pptx.shapes.autoshape import Shape
from pptx_tools.creator import PPTXCreator, PPTXPosition
# todo: - create title slide (contact data, creation date ...)
from pptx_tools.table_style import PPTXTableStyle
from pptx_tools.templates import analyze_pptx

from pi88reader.pi88_importer import PI88Measurement, load_tdm_files
from pi88reader.pi88_plotter import PI88Plotter
from pi88reader.plotter_styles import GraphStyler
from pi88reader.pptx_styles import table_style_summary
from pi88reader.utils_pi88measurement import get_measurement_result_data, get_measurement_meta_data
from pi88reader.utils_pi88measurements import get_measurements_meta_data, \
    get_measurements_result_data


def main():
    TEMPLATE_FILENAME = '..\\resources\\pptx_template\\example-template.pptx'
    analyze_pptx(TEMPLATE_FILENAME)


class PI88ToPPTX:
    def __init__(self, measurements_path=None, template=None):
        self.path = measurements_path
        self.measurements = []
        if self.path:
            self.load_tdm_files(measurements_path)
        self.plotter = PI88Plotter(self.measurements)
        self.pptx_creator = PPTXCreator(template=template)
        self.prs = self.pptx_creator.prs
        self.position = self.pptx_creator.default_position

        self.poisson_ratio = 0.3
        self.beta = 1.0

        # fig_width = 8
        # fig_height = 4.5
        # fig = self.plotter.get_load_displacement_plot((fig_width,fig_height))
        # zoom = 1.0
        # picture = self.add_matplotlib_figure(fig, self.prs.slides[0], width=Inches(fig_height*zoom))
        # picture.left = Inches(1)
        # picture.top = Inches(3)

    def load_tdm_files(self, path: str, sort_key=os.path.getctime):  # sorted by creation time (using windows)
        self.measurements.extend(load_tdm_files(path, sort_key))

    def add_measurements(self, measurements: Union[PI88Measurement, Iterable[PI88Measurement]]) -> None:
        """
        Adds a single PI88Measurement or a list o PI88Measurement's to the plotter.
        """
        if measurements:
            try:
                self.measurements.extend(measurements)
            except TypeError:
                self.measurements.append(measurements)

    def add_matplotlib_figure(self, fig, slide, pptx_position=None, **kwargs):
        """
        :param fig:
        :param slide_index:
        :param pptx_position:
        :param kwargs: e.g. width and height
        :return: prs.shapes.picture.Picture
        """
        return self.pptx_creator.add_matplotlib_figure(fig, slide, pptx_position, **kwargs)

    def create_summary_slide(self, layout=None):
        result = self.pptx_creator.add_slide(f"Summary - {self.path}", layout)

        plotter = PI88Plotter(self.measurements)
        fig = plotter.get_load_displacement_plot()
        fig.axes[0].legend(loc="best")
        self.add_matplotlib_figure(fig, result, PPTXPosition(0.02, 0.15))
        self.create_measurements_result_data_table(result)
        return result

    def create_title_slide(self, title=None, layout=None, default_content=False):
        if title is None:
            title = f"NI results {self.path}"
        result = self.pptx_creator.add_title_slide(title, layout)
        self.create_measurements_meta_table(result)

        plotter = PI88Plotter(self.measurements)
        fig = plotter.get_load_displacement_plot()
        self.add_matplotlib_figure(fig, result, PPTXPosition(0.57, 0.24))
        return result

    def create_measurement_slide(self, measurement: PI88Measurement, layout = None, graph_styler = None):
        title = measurement.base_name  # filename[:-4].split("/")[-1].split("\\")[-1]
        result = self.pptx_creator.add_slide(title, layout)

        plotter = PI88Plotter(measurement)
        if graph_styler is not None:
            plotter.graph_styler = graph_styler
        fig = plotter.get_load_displacement_plot()
        self.add_matplotlib_figure(fig, result, PPTXPosition(0.02, 0.15))

        self.create_measurement_result_table(result, measurement)
        self.create_measurement_meta_data_table(result, measurement)
        return result

    def create_measurement_slides(self, measurements: Optional[List[PI88Measurement]] = None, layout = None) -> list:
        result = []
        if measurements is None:
            measurements = self.measurements

        graph_styler = GraphStyler(len(self.measurements))

        for measurement in measurements:
            result.append(self.create_measurement_slide(measurement, layout, graph_styler))

        return result

    def create_measurement_meta_data_table(self, slide, measurement, table_style: PPTXTableStyle = None) -> Shape:
        table_data = get_measurement_meta_data(measurement)
        result = self.pptx_creator.add_table(slide, table_data, PPTXPosition(0.521, 0.16))
        if table_style is None:
            table_style = style_sheets.table_no_header()
            table_style.set_width_as_fraction(0.4)
        table_style.write_shape(result)
        return result

    def create_measurement_result_table(self, slide, measurement, table_style: PPTXTableStyle = None) -> Shape:
        table_data = get_measurement_result_data(measurement, self.poisson_ratio, self.beta)

        result = self.pptx_creator.add_table(slide, table_data, PPTXPosition(0.521, 0.56))
        if table_style is None:
            table_style = style_sheets.table_no_header()
            table_style.set_width_as_fraction(0.4)
        table_style.write_shape(result)
        return result

    def create_measurements_meta_table(self, slide, table_style: PPTXTableStyle = None):
        table_data = get_measurements_meta_data(self.measurements)

        result = self.pptx_creator.add_table(slide, table_data, PPTXPosition(0.021, 0.26))
        if table_style is None:
            table_style = style_sheets.table_no_header()
            table_style.set_width_as_fraction(0.52)
        table_style.write_shape(result)
        return result

    def create_measurements_result_data_table(self, slide, table_style: PPTXTableStyle = None):
        table_data = get_measurements_result_data(self.measurements)
        result = self.pptx_creator.add_table(slide, table_data)
        if table_style is None:
            table_style = table_style_summary()
        table_style.write_shape(result)
        return result

    def save(self, filename="delme.prs"):
        self.prs.save(filename)



def create_demo_figure():
    figure = plt.figure(figsize=(6.4, 6.8), dpi=100, facecolor='w', edgecolor='w', frameon=True)
    # figure.patch  # The Rectangle instance representing the figure background patch.
    # figure.patch.set_visible(False)
    figure.patch.set_alpha(0.5)
    supertitle = figure.suptitle('suptitle', fontsize=14, fontweight='bold', color='red')
    supertitle.set_color('green')
    supertitle.set_rotation(5)
    supertitle.set_size(18)

    textstr = '\n'.join((
        fr'$\mu={5}^{5}$',
        r'$\mathrm{median}=3_3$',
        r'$median=3_3$',
        fr'$\sigma=$'))
    return figure


if __name__ == "__main__":
    main()