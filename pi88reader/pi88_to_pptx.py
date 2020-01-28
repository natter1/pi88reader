"""
@author: Nathanael Jöhrmann
"""
import glob
import os
from datetime import datetime
from typing import Union, Iterable

import matplotlib.pyplot as plt
from pptx.enum.dml import MSO_THEME_COLOR_INDEX
from pptx.util import Inches

from pptx_tools.templates import analyze_pptx
from pi88reader.pi88_importer import PI88Measurement, load_tdm_files
from pi88reader.pi88_plotter import PI88Plotter
from pptx_tools.creator import PPTXCreator, PPTXPosition
import pptx_tools.style_sheets as style_sheets


# todo: - create title slide (contact data, creation date ...)
from pptx_tools.table_style import PPTXTableStyle
from pi88reader.utils_pi88measurements import get_date_intervall_string, get_aborted_measurements, \
    get_transducer_serials_string, get_triboscan_versions_string, get_feedback_modes_string, get_measurements_meta_data


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
        self.add_matplotlib_figure(fig, result, PPTXPosition(0.02, 0.15))
        return result

    def create_title_slide(self, title=None, layout=None):
        if title is None:
            title = f"NI results {self.path}"
        result = self.pptx_creator.add_title_slide(title, layout)

        table_data = get_measurements_meta_data(self.measurements)

        table_shape = self.pptx_creator.add_table(result, table_data, PPTXPosition(0.05, 0.3))
        dummy = table_shape.table

        table_style = style_sheets.table_no_header()  # PPTXTableStyle()
        table_style.set_width_as_fraction(self.prs, 0.52)
        table_style.write_shape(table_shape)
        return result


    def save(self, filename="delme.prs"):
        self.prs.save(filename)

    # def set_first_slide(self):
    #     layout = self.prs.slide_layouts[0]
    #     slide = self.prs.slides.add_slide(layout)
    #     # slide.shapes[2].element.getparent().remove(slide.shapes[2].element)
    #     title = slide.shapes.title
    #     title.text = self.measurement.filename
    #     pptx_templates.remove_unpopulated_shapes(slide)

    # def add_matplotlib_figure(self, fig, slide, **kwargs):
    #     """
    #     kwargs["left"] = 0
    #     kwargs["top"] = 0
    #     :param fig:
    #     :param slide:
    #     :return: prs.shapes.picture.Picture
    #     """
    #     #left = top = Inches(1)
    #     if not "left" in kwargs:
    #         kwargs["left"] = 0
    #     if not "top" in kwargs:
    #         kwargs["top"] = 0
    #
    #     with io.BytesIO() as output:
    #         fig.savefig(output, format="png")
    #         pic = slide.shapes.add_picture(output, **kwargs) #0, 0)#, left, top)
    #     return pic




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