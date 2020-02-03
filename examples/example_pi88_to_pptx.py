from pi88reader.etit169_pptx_template import TemplateETIT169
from pi88reader.pi88_to_pptx import PI88ToPPTX
from pptx_tools.templates import TemplateExample


def main():
    run()

def run():
    filename = '../resources/quasi_static_12000uN.tdm'
    filename = '../resources/AuSn_Creep/1000uN 01 LC.tdm'
    # measurements_path = '../resources/AuSn_Creep/'
    # measurements_path = '../resources/creep_example/'
    measurements_path = '../resources/nanobruecken2020/'
    # measurements_path = '../resources/dc/'
    # measurements_path = '../resources/'
    # measurements_path = '../resources/190829_Cu_400-867-03-Nr16/'


    pptx = PI88ToPPTX(measurements_path, TemplateETIT169())
    pptx.create_title_slide()
    pptx.create_measurement_slides()
    pptx.create_summary_slide()
    pptx.pptx_creator.add_content_slide()
    pptx.save("nanobruecken2020_pi88_to_pptx.pptx")

if __name__ == '__main__':
    main()