pi88reader
==========
..
 .. image:: https://img.shields.io/pypi/v/pyansystools.svg
     :target: https://pypi.org/project/pyansystools/

.. image:: http://img.shields.io/:license-MIT-blue.svg?style=flat-square
    :target: http://badges.mit-license.org

Rewrite of C++ tool PI88ToExcel as python app (currently its only a collection of scripts)

Features
--------

* import \*.tdm files created with TriboScan (Nanoindenter software for Bruker PI88) into python
* do basic calculations (reduced modules ...)
* process several measurements together (folder based)
* create customizeable output
    * excel files with summary, tables for each measurement and settings
* customizeable plots using matplotlib
* creating automated powerpoint reports (including use of template \*.pptx)

class PI88Measurement
---------------------

.. code:: python

    from pi88reader.pi88_importer import PI88Measurement

    filename = '..\\resources\\quasi_static_12000uN.tdm'
    measurement = PI88Measurement(filename)

The class PI88Measurment is used to import TriboScan \*.tdm files created with a PI88 nanoindenter.
After loading a file it has quasi static time/load/depth data, area function, segment data and in case of a dynamic
measurement the average dynamic data (complex modulus, phase shift ...).

class PI88Plotter
-----------------

.. code:: python

    from pi88reader.pi88_importer import load_tdm_files
    from pi88reader.pi88_plotter import PI88Plotter
    from pi88reader.plotter_styles import get_plotter_style_bernhard_4

    measurements = load_tdm_files('../resources/creep_example/')
    plotter = PI88Plotter(measurements)
    plotter.get_displacement_time_plot().savefig("plotter01_default_style.png")
    plotter.read_plotter_style(get_plotter_style_bernhard_4())
    plotter.get_displacement_time_plot().savefig("plotter01_bernhard_4_style.png")


.. image:: https://github.com/natter1/pi88reader/raw/master/docs/images/plotter01_default_style.png
    :width: 240pt
.. image:: https://github.com/natter1/pi88reader/raw/master/docs/images/plotter01_bernhard_4_style.png
    :width: 240pt


License and Acknowledgments
---------------------------
``pi88reader`` is licensed under the MIT license.
