"""
@author: Nathanael Jöhrmann
"""
import glob
import os
from datetime import datetime

import matplotlib.pyplot as plt

import pi88reader.pptx_template as pptx_template
from pi88reader.pi88_importer import PI88Measurement
from pi88reader.pi88_plotter import PI88Plotter
from pi88reader.pptx_creator import PPTXCreator


# todo: - create title slide (contact data, creation date ...)
def main():
    TEMPLATE_FILENAME = '..\\resources\pptx_template\\example-template.pptx'
    pptx_template.analyze_pptx(TEMPLATE_FILENAME)


class PI88ToPPTX:
    def __init__(self, measurements_path=None, template=None):
        self.path = measurements_path
        self.measurements = []
        if self.path:
            self.load_tdm_files(measurements_path)
        self.plotter = PI88Plotter(self.measurements)
        self.pptx_creator = None
        self.pptx = None
        self.create_pptx(template=template)
        self.position = self.pptx_creator.default_position

        # fig_width = 8
        # fig_height = 4.5
        # fig = self.plotter.get_load_displacement_plot((fig_width,fig_height))
        # zoom = 1.0
        # picture = self.add_matplotlib_figure(fig, self.prs.slides[0], width=Inches(fig_height*zoom))
        # picture.left = Inches(1)
        # picture.top = Inches(3)

    def create_pptx(self, template=None):
        self.pptx_creator = PPTXCreator(template=template)
        self.pptx = self.pptx_creator.prs

    def load_tdm_files(self, path):
        files = glob.glob(os.path.join(path, '*.tdm'))
        files.sort(key=os.path.getctime)  # sorted by creation time (using windows)
        for file in files:
            self.measurements.append(PI88Measurement(file))

    def add_matplotlib_figure(self, fig, slide_index, pptx_position=None, **kwargs):
        """
        :param fig:
        :param slide_index:
        :param pptx_position:
        :param kwargs: e.g. width and height
        :return: pptx.shapes.picture.Picture
        """
        return self.pptx_creator.add_matplotlib_figure(fig, slide_index, pptx_position, **kwargs)

    def create_summary_slide(self, layout=None):
        result = self.pptx_creator.add_slide("Summary", layout)
        return result


    def save(self, filename="delme.pptx"):
        self.prs.save(filename)

    # def set_first_slide(self):
    #     layout = self.prs.slide_layouts[0]
    #     slide = self.prs.slides.add_slide(layout)
    #     # slide.shapes[2].element.getparent().remove(slide.shapes[2].element)
    #     title = slide.shapes.title
    #     title.text = self.measurement.filename
    #     pptx_template.remove_unpopulated_shapes(slide)

    # def add_matplotlib_figure(self, fig, slide, **kwargs):
    #     """
    #     kwargs["left"] = 0
    #     kwargs["top"] = 0
    #     :param fig:
    #     :param slide:
    #     :return: pptx.shapes.picture.Picture
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


def setup_master_slide_big(slide_master):
    """
    This function is just an example. It has to be customized
    to fit with the used template.
    :param slide_master:
    :return:
    """
    date_time = datetime.now()

    master = pptx_template.MasterSlideBig(slide_master)
    master.set_author("Nathanael Jöhrmann", city="Chemnitz", date=date_time.strftime("%d %B, %Y"))
    master.set_website("https://www.tu-chemnitz.de/etit/wetel/")


def setup_master_slide_small(slide_master):
    pass




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