"""
This module provides an easier Interface to create *.pptx presentations using the module python-pptx.
@author: Nathanael Jöhrmann
"""
import io

from pptx import Presentation
from pptx.util import Inches

import pi88reader.pptx_template as pptx_template


# todo: template_file to Enum in pptx_template with all available templates
class PPTXCreator:
    """
    This Class provides an easy interface to create a PowerPoint presentation.
        - position elements as fraction of slide height/width
        - add matplotlib figures
        - use pptx templates (in combination with pptx_template.py)
    """
    def __init__(self, template=None, title="Title"):
        """

        :param template:
        :param title:
        """
        self.slides = []
        self.template = None
        self.prs = None
        self.create_presentation(template)
        self.default_layout = self.prs.slide_masters[0]
        # self.template_file = template_file
        self.set_first_slide(title=title)

        # picture = self.add_matplot_figure(fig, self.prs.slides[0], width=Inches(fig_height*zoom))

        # picture.left = Inches(1)
        # picture.top = Inches(3)

    def fraction_width_to_inch(self, fraction):
        """
        Returns a width in inches calculated as a fraction of total slide-width.
        :param fraction: float
        :return: Calculated Width in inch
        """
        result = Inches(self.prs.slide_width.inches * fraction)
        return result

    def fraction_height_to_inch(self, fraction):
        """
        Returns a height in inches calculated as a fraction of total slide-height.
        :param fraction: float
        :return: Calculated Width in inch
        """
        return Inches(self.prs.slide_height.inches * fraction)

    def save(self, filename="delme.pptx"):
        """
        Saves the presentation under the given filename.
        :param filename: string
        :return: None
        """
        self.prs.save(filename)

    def create_presentation(self, template=None):
        """

        :param template:
        :return:
        """
        if template:
            self.template = template  # pptx_template.TemplateETIT169()
            self.prs = self.template.prs
        else:
            self.prs = Presentation()

    def set_first_slide(self, title):
        layout = self.prs.slide_masters[1].slide_layouts[0]
        slide = self.prs.slides.add_slide(layout)
        # slide.shapes[2].element.getparent().remove(slide.shapes[2].element)
        title_shape = slide.shapes.title
        title_shape.text = title  # self.measurement.filename
        pptx_template.remove_unpopulated_shapes(slide)

    def write_position_in_kwargs(self, left_rel=0.0, top_rel=0.0, kwargs={}):
        """
        This method modifies(!) the argument kwargs by adding or changing the entries "left" and "top".
        :param left_rel:
        :param top_rel:
        :param kwargs:
        :return: None
        """
        left = self.fraction_width_to_inch(left_rel)
        top = self.fraction_height_to_inch(top_rel)

        if not "left" in kwargs:
            kwargs["left"] = left
        else:
            kwargs["left"] = kwargs["left"] + left
        if not "top" in kwargs:
            kwargs["top"] = top
        else:
            kwargs["top"] = kwargs["top"] + top

    def add_matplotlib_figure(self, fig, slide_index, left_rel=0.0, top_rel=0.0, **kwargs):
        """
        Add a motplotlib figure fig to slide with index slide_index. With top_rel and left_rel
        it is possible to position the figure in Units of slide height/width (float in range [0, 1].
        :param fig: a matplolib figure
        :param slide_index: index of slide in presentation on which to insert fig
        :param left_rel: distance from slide left (relative to slide width)
        :param top_rel: distance from slide top (relative to slide height)
        :param kwargs: e.g. "left" and "top" to position figure [inches] starting from (rel_left, rel_top)
        :return: pptx.shapes.picture.Picture
        """
        self.write_position_in_kwargs(left_rel=left_rel, top_rel=top_rel, kwargs=kwargs)
        # todo: check slide_index
        slide = self.prs.slides[slide_index]
        with io.BytesIO() as output:
            fig.savefig(output, format="png")
            pic = slide.shapes.add_picture(output, **kwargs)  # 0, 0)#, left, top)
        return pic
