from pi88reader.pi88_to_pptx import PI88ToPPTX
from pptx_tools.templates import TemplateExample


def main():
    run()

def run():
    filename = '../resources/quasi_static_12000uN.tdm'
    filename = '../resources/AuSn_Creep/1000uN 01 LC.tdm'
    # measurements_path = '../resources/AuSn_Creep/'
    # measurements_path = '../resources/creep_example/'
    measurements_path = '../resources/'
    #measurement = PI88Measurement(filename)

    pptx = PI88ToPPTX(measurements_path, TemplateExample())
    for m in pptx.measurements:
        dummy = m.settings.dict
        print(dummy)
    pptx.create_title_slide()
    pptx.create_summary_slide()
    pptx.save("example_pi88_to_pptx.pptx")

if __name__ == '__main__':
    main()