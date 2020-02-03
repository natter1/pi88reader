from pi88reader.pi88_importer import load_tdm_files
from pi88reader.pi88_plotter import PI88Plotter
from pi88reader.plotter_styles import get_plotter_style_bernhard_4


def main():
    measurements = load_tdm_files('../resources/creep_example/')
    plotter = PI88Plotter(measurements)
    plotter.get_load_time_plot().savefig("fig1.png")
    plotter.get_displacement_time_plot().savefig("fig2.png")
    plotter.read_plotter_style(get_plotter_style_bernhard_4())
    plotter.get_displacement_time_plot().savefig("fig3.png")


if __name__ == '__main__':
    main()


measurements = load_tdm_files('../resources/creep_example/')
plotter = PI88Plotter(measurements)
plotter.get_load_time_plot().savefig("fig1.png")
plotter.get_displacement_time_plot().savefig("fig2.png")
plotter.read_plotter_style(get_plotter_style_bernhard_4())
plotter.get_displacement_time_plot().savefig("fig3.png")


# measurements = load_tdm_files('../resources/creep_example/')
# measurements = load_tdm_files('../resources/nanobruecken2020/')
# plotter = PI88Plotter(measurements)
# fig = plotter.get_load_displacement_plot()
# plotter.read_plotter_style(get_plotter_style_bernhard_4())
# fig = plotter.get_displacement_time_plot()