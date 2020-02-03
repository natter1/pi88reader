from pi88reader.pi88_to_pptx import PI88ToPPTX
from pptx_tools.templates import TemplateExample


def main():
    run()

def run():
    filename = '..\\resources\\quasi_static_12000uN.tdm'
    # measurements_path = '..\\resources\\creep_example\\'
    measurements_path = '..\\resources\\'

    pptx = PI88ToPPTX(measurements_path, TemplateExample())
    pptx.create_title_slide()
    pptx.create_measurement_slides()
    pptx.create_summary_slide()
    pptx.pptx_creator.add_content_slide()
    pptx.save("example_pi88_to_pptx.pptx")

if __name__ == '__main__':
    main()
