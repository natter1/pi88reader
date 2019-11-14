"""
This file contains variables with names of important pptx template master_slide shapes
"""
# from pptx.enum.text import MSO_AUTO_SIZE


# todo: add something like this directly to python-pptx
def copy_font(_from, _to):
    _to.bold = _from.bold
    # todo: color is ColorFormat object
    # _to.set_color = _from.color
    # todo: fill is FillFormat object
    # _to.fill = _from.fill
    _to.italic = _from.italic
    _to.language_id = _from.language_id
    _to.name = _from.name
    _to.size = _from.size
    _to.underline = _from.underline


def remove_unpopulated_shapes(slide):
    """
    Removes empty placeholders (e.g. due to layout) from slide.
    Further testing needed.
    :param slide: pptx.slide.Slide
    :return:
    """
    for index in reversed(range(len(slide.shapes))):
        shape = slide.shapes[index]
        # if shape.is_placeholder and shape.text_frame.text == "":
        if shape.has_text_frame and shape.text_frame.text == "":
            shape.element.getparent().remove(shape.element)
            print(f"removed index {index}")


def change_paragraph_text_to(paragraph, text):
    """
    Change text of paragraph to text, but keep format.
    :param paragraph:
    :param text:
    :return:
    """
    font = paragraph.runs[0].font
    paragraph.text = text
    copy_font(font, paragraph.font)


def analyze_paragraphs(paragraphs):
    for index, para in enumerate(paragraphs):
        print(f"index: {index} - text: {para.text}")
        for run_index, run in enumerate(para.runs):
            print(f"\trun: {run.text}")

# master_slides[0] (large red header bar; no slide numbers)
class MasterSlideBig:
    def __init__(self, slide_master):
        self.slide_master = slide_master
        self.author_shape_name = "Rectangle 4"
        self.website_shape_name = "Rectangle 5"

    def set_author(self, name, city=None, date=None):
        text= ""
        spacer = " ∙ "
        if city:
            text += city + spacer
        if date:
            text += date + spacer
        text += name

        for shape in self.slide_master.shapes:
            if not shape.has_text_frame:
                continue
            if shape.name == self.author_shape_name:
                change_paragraph_text_to(shape.text_frame.paragraphs[0], text)


    def set_website(self, text):
        for shape in self.slide_master.shapes:
            if not shape.has_text_frame:
                continue
            if shape.name == self.website_shape_name:
                change_paragraph_text_to(shape.text_frame.paragraphs[0], text)