from pptx_tools.templates import TemplateExample
from pi88reader.pi88_importer import PI88Measurement
from pi88reader.pi88_plotter import PI88Plotter
from pptx_tools.creator import PPTXPosition, PPTXCreator
from pptx.util import Inches

def test_pptx_creator():


    # pptx = PPTXCreator()  # create pptx without using a template file
    pptx = PPTXCreator(TemplateExample())
    title_slide = pptx.create_title_slide(title="PPTXCreator Demo")
    slide2 = pptx.add_slide(title="Normal slide")

    plotter = PI88Plotter(PI88Measurement("../resources/AuSn_Creep/1000uN 01 LC.tdm"))
    fig = plotter.get_load_displacement_plot()
    fig_width = fig.get_figwidth()
    zoom = 1
    picture = pptx.add_matplotlib_figure(fig, title_slide, PPTXPosition(0.2, 0.25),
                                         width=Inches(fig_width * zoom))


    zoom = 0.2
    pptx.add_matplotlib_figure(fig, title_slide, PPTXPosition(0.7, 0.25), width=Inches(fig_width * zoom))

    pptx.add_text_box(slide2, "This is the first paragraph\n... and here comes the second", PPTXPosition(0.7, 0.7))
    pptx.save("delme_pptx_creator_demo.pptx")

