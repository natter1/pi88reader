from pi88reader.pi88_importer import load_tdm_files
from pi88reader.pi88_plotter import PI88Plotter
from pi88reader.plotter_styles import get_plotter_style_bernhard_4


def main():
    measurements = load_tdm_files('../resources/creep_example/')
    plotter = PI88Plotter(measurements)
    fig = plotter.get_load_displacement_plot()
    fig.show()
    fig = plotter.get_load_time_plot()
    fig.show()
    plotter.read_plotter_style(get_plotter_style_bernhard_4())
    fig = plotter.get_displacement_time_plot()
    fig.show()

if __name__ == '__main__':
    main()