"""

"""
from pptx.util import Inches
from pptx import Presentation
import io
from datetime import datetime
import pi88reader.pptx_template as pptx_template


class PPTXCreator:
    def __init__(self, use_tamplate=True, template_file = '..\\resources\pptx\\ETIT_16-9.pptx', title="Title"):
        slides = []
        self.template_file = template_file
        self.create_presentation(use_tamplate)
        self.set_first_slide(title=title)

        # picture = self.add_matplot_figure(fig, self.prs.slides[0], width=Inches(fig_height*zoom))

        # picture.left = Inches(1)
        # picture.top = Inches(3)

    def relative_width_to_inch(self, value):
        result = Inches(self.prs.slide_width.inches * value)
        return result

    def relative_height_to_inch(self, value):
        return Inches(self.prs.slide_height.inches * value)

    def save(self, filename="delme.pptx"):
        self.prs.save(filename)

    def create_presentation(self, use_template=True):
        if use_template:
            self.prs = Presentation(self.template_file)
            self.setup_master_slide_big(self.prs.slide_masters[0])
            # todo: slide_small
            self.setup_master_slide_small(self.prs.slide_masters[1])
        else:
            self.prs = Presentation()

    def setup_master_slide_big(self, slide_master):
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

    def setup_master_slide_small(self, slide_master):
        pass

    def set_first_slide(self, title):
        layout = self.prs.slide_layouts[0]
        slide = self.prs.slides.add_slide(layout)
        # slide.shapes[2].element.getparent().remove(slide.shapes[2].element)
        title_shape = slide.shapes.title
        title_shape.text = title  # self.measurement.filename
        pptx_template.remove_unpopulated_shapes(slide)

    def add_matplot_figure(self, fig, slide_index, top_rel = 0.0, left_rel = 0.0, **kwargs):
        """
        Add a motplotlib figure fig to slide with index slide_index
        :param fig:
        :param slide_index:
        :param top_rel: distance from slide top (relative to slide height)
        :param left_rel: distance from slide left (relative to slide width)
        :param kwargs:
        :return: pptx.shapes.picture.Picture
        """
        # left = top = Inches(1)
        left = self.relative_width_to_inch(left_rel)
        top = self.relative_height_to_inch(top_rel)

        if not "left" in kwargs:
            kwargs["left"] = left  # 0
        if not "top" in kwargs:
            kwargs["top"] = top  # 0
        # todo: check slide_index
        slide = self.prs.slides[slide_index]
        with io.BytesIO() as output:
            fig.savefig(output, format="png")
            pic = slide.shapes.add_picture(output, **kwargs)  # 0, 0)#, left, top)
        return pic
