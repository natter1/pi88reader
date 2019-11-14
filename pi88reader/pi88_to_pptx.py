from pptx import Presentation
from pptx.util import Inches
import matplotlib.pyplot as plt
import io
from datetime import datetime


import pi88reader.pptx_template as pptx_template
from pi88reader.pi88_matplotlib_tools import PI88Plotter as PI88Plotter


# todo: - use layout example file
# todo: - create title slide (contact data, creation date ...)

def main():
    TEMPLATE_FILENAME = '..\\resources\pptx\\ETIT_16-9.pptx'
    analyze_ppt(TEMPLATE_FILENAME)


class PI88ToPPTX:
    TEMPLATE_FILENAME = '..\\resources\pptx\\ETIT_16-9.pptx'
    def __init__(self, measurement, use_tamplate=True):
        slides = []
        self.measurement = measurement
        self.plotter = PI88Plotter()
        self.plotter.add_measurements(measurement)

        self.create_presentation(use_tamplate)
        self.set_first_slide()
        fig_width = 8
        fig_height = 4.5
        fig = self.plotter.get_load_displacement_plot((fig_width,fig_height))
        zoom = 1.0
        picture = self.add_matplot_figure(fig, self.prs.slides[0], width=Inches(fig_height*zoom))
        picture.left = Inches(1)
        picture.top = Inches(3)


        self.prs.save("delme.pptx")

    def create_presentation(self, use_tamplate=True):
        if use_tamplate:
            self.prs = Presentation(self.TEMPLATE_FILENAME)
            setup_master_slide_big(self.prs.slide_masters[0])
            setup_master_slide_small(self.prs.slide_masters[1])
        else:
            self.prs = Presentation()

    def set_first_slide(self):
        layout = self.prs.slide_layouts[0]
        slide = self.prs.slides.add_slide(layout)
        # slide.shapes[2].element.getparent().remove(slide.shapes[2].element)
        title = slide.shapes.title
        title.text = self.measurement.filename
        pptx_template.remove_unpopulated_shapes(slide)

    def add_matplot_figure(self, fig, slide, **kwargs):
        """
        kwargs["left"] = 0
        kwargs["top"] = 0
        :param fig:
        :param slide:
        :return: pptx.shapes.picture.Picture
        """
        #left = top = Inches(1)
        if not "left" in kwargs:
            kwargs["left"] = 0
        if not "top" in kwargs:
            kwargs["top"] = 0

        with io.BytesIO() as output:
            fig.savefig(output, format="png")
            pic = slide.shapes.add_picture(output, **kwargs) #0, 0)#, left, top)
        return pic


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


def analyze_ppt(input):
    """ Take the input file and analyze the structure of master slides.
    Prints shape names/ids and texts for SlideMaster-shapes
    To get an output file contains marked up information
    remove comment on last two lines of function.
    This is helpful when manipulating template-files.
    """
    prs = Presentation(input)
    # Each powerpoint file has multiple layouts
    # Loop through them all and  see where the various elements are
    slide_masters = prs.slide_masters
    for index, slide_master in enumerate(prs.slide_masters):
        print('------------------------------------')
        print('------------------------------------')
        print(f"slide master indexed: {index}")
        print(slide_master)
        print("text boxes:")
        for shape in slide_master.shapes:
            try:
                dummystring = f"shape name: {shape.name} - shape text: {shape.text}"
                shape.text = shape.name
                print(dummystring)
            except:
                pass
            #shape.text = 'hahahaha'
        # for shape in slide_master.slideshapes:
        #     print(shape)
        print('------------------------------------')
        for index, slide_layout in enumerate(slide_master.slide_layouts):
            print(f"\tslide layout: {slide_layout.name}")
            slide = prs.slides.add_slide(slide_master.slide_layouts[index])
            # Not every slide has to have a title
            try:
                title = slide.shapes.title
                title.text = 'Title for Layout {}'.format(index)
            except AttributeError:
                print("No Title for Layout {}".format(index))
            # Go through all the placeholders and identify them by index and type
            for shape in slide.placeholders:
                if shape.is_placeholder:
                    phf = shape.placeholder_format
                    # Do not overwrite the title which is just a special placeholder
                    try:
                        if 'Title' not in shape.text:
                            shape.text = 'Placeholder index:{} type:{}'.format(phf.idx, shape.name)
                    except AttributeError:
                        print("{} has no text attribute".format(phf.type))
                    print(f"\t\tid: {phf.idx} - name: {shape.name}")
    # output_file = '..\\resources\pptx\\template_names.pptx'
    # prs.save(output_file)

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