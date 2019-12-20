import io
from datetime import datetime

import matplotlib.pyplot as plt
from pptx import Presentation
from pptx.util import Inches

import pi88reader.pptx_template as pptx_template
from pi88reader.pi88_matplotlib_tools import PI88Plotter as PI88Plotter
from pi88reader.pptx_creator import PPTXCreator as PPTXCreator

# todo: - use layout example file
# todo: - create title slide (contact data, creation date ...)

def main():
    TEMPLATE_FILENAME = '..\\resources\pptx\\example-template.pptx'
    analyze_ppt(TEMPLATE_FILENAME)


class PI88ToPPTX:
    def __init__(self, measurement, use_tamplate=True, title="Title"):
        slides = []
        self.measurement = measurement
        self.plotter = PI88Plotter()
        self.plotter.add_measurements(measurement)

        # self.pptx = PPTXCreator(use_tamplate, title=title)
        # fig_width = 8
        # fig_height = 4.5
        # fig = self.plotter.get_load_displacement_plot((fig_width,fig_height))
        # zoom = 1.0
        # picture = self.add_matplotlib_figure(fig, self.prs.slides[0], width=Inches(fig_height*zoom))
        # picture.left = Inches(1)
        # picture.top = Inches(3)

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