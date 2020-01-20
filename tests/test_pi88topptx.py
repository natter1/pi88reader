import pytest
import matplotlib.pyplot as plt
from pptx_tools.templates import TemplateExample

from pi88reader.pi88_importer import PI88Measurement
from pi88reader.pi88_to_pptx import PI88ToPPTX


@pytest.fixture(scope='class')
def pi88_to_pptx():
    pi88_to_pptx = PI88ToPPTX()
    yield pi88_to_pptx


@pytest.fixture(scope='session')
def matplotlib_figure():
    def create_demo_figure():
        result: plt.Figure = plt.figure(figsize=(3.4, 1.8), dpi=100, facecolor='w', edgecolor='w', frameon=True)
        result.suptitle('matplotlib figure', fontsize=14, fontweight='bold', color='red')
        return result

    matplotlib_figure = create_demo_figure()
    yield matplotlib_figure


class TestPI88ToPPTX:
    def test__init__args_no(self):
        pi88_to_pptx = None
        pi88_to_pptx = PI88ToPPTX()
        assert pi88_to_pptx is not None

    def test__init__args_path(self):
        measurements_path = '../resources/'
        template = TemplateExample()
        pi88_to_pptx = PI88ToPPTX(measurements_path=measurements_path, template=template)
        assert pi88_to_pptx.prs is template.prs
        assert len(pi88_to_pptx.measurements) > 0

    def test__init__args_template(self):
        template = TemplateExample()
        pi88_to_pptx = PI88ToPPTX(template=template)
        assert pi88_to_pptx.prs is template.prs


    def test__init__args_path_template(self):
        assert False

    def test_load_tdm_files(self, pi88_to_pptx):
        measurements_path = '../resources/'
        n_before = len(pi88_to_pptx.measurements)
        pi88_to_pptx.load_tdm_files(measurements_path)
        n_after = len(pi88_to_pptx.measurements)
        assert n_after > n_before

    def test_add_measurements(self, pi88_to_pptx):
        n_before = len(pi88_to_pptx.measurements)
        filename = '../resources/quasi_static_12000uN.tdm'
        measurement = PI88Measurement(filename)
        # check PI88Measurement
        pi88_to_pptx.add_measurements(measurement)
        n_after = len(pi88_to_pptx.measurements)
        assert n_after == n_before + 1
        # check Iterable of PI88Measurement
        pi88_to_pptx.add_measurements([measurement])
        n_after_iter = len(pi88_to_pptx.measurements)
        assert n_after_iter == n_before + 2

    def test_add_matplotlib_figure(self, pi88_to_pptx, matplotlib_figure):
        slide = pi88_to_pptx.pptx_creator.add_slide("Slide with matplotlib figure")
        n_before = len(slide.shapes)
        pi88_to_pptx.add_matplotlib_figure(matplotlib_figure, slide)
        n_after = len(slide.shapes)
        assert n_after == n_before + 1

    def test_create_summary_slide(self, pi88_to_pptx):
        n_before = len(pi88_to_pptx.prs.slides)
        pi88_to_pptx.create_summary_slide()
        n_after = len(pi88_to_pptx.prs.slides)
        assert n_after == n_before + 1

    def test_save(self, pi88_to_pptx):
        assert False
