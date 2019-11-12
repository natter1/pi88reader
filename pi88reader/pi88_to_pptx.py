from pptx import Presentation
from pptx.util import Inches
import matplotlib.pyplot as plt
import io


# todo: - use layout example file
# todo: - create title slide (contact data, creation date ...)



# class _BaseMaster(_BaseSlide):
#     """
#     Base class for master objects such as |SlideMaster| and |NotesMaster|.
#     Provides access to placeholders and regular shapes.
#     """
#
#     __slots__ = ("_placeholders", "_shapes")
#
#     @lazyproperty
#     def placeholders(self):
#         """
#         Instance of |MasterPlaceholders| containing sequence of placeholder
#         shapes in this master, sorted in *idx* order.
#         """
#         return MasterPlaceholders(self._element.spTree, self)
#
#     @lazyproperty
#     def shapes(self):
#         """
#         Instance of |MasterShapes| containing sequence of shape objects
#         appearing on this slide.
#         """
#         return MasterShapes(self._element.spTree, self)



def analyze_ppt(input):
    """ Take the input file and analyze the structure.
    The output file contains marked up information to make it easier
    for generating future powerpoint templates.
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

    output_file = '..\\resources\pptx\\ETIT_16-9_names.pptx'
    prs.save(output_file)

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

template_file = '..\\resources\pptx\\ETIT_16-9.pptx'
analyze_ppt(template_file)
# prs = Presentation(template_file)
# title_slide_layout = prs.slide_layouts[0]
# slide = prs.slides.add_slide(title_slide_layout)
# title = slide.shapes.title
# # subtitle = slide.placeholders[1]
#
# title.text = "Hello, World!"
# # subtitle.text = "python-pptx was here!"
#
# fig = create_demo_figure()
# left = top = Inches(1)
# with io.BytesIO() as output:
#     fig.savefig(output, format="png")
#     pic = slide.shapes.add_picture(output, left, top)
#     pic.rotation=30
#     print(type(pic))
# prs.save('delme.pptx')