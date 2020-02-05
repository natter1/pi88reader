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


.. |image01| image:: https://github.com/natter1/pi88reader/raw/master/docs/images/plotter01_default_style.png
    :width: 240pt
.. |image02| image:: https://github.com/natter1/pi88reader/raw/master/docs/images/plotter01_bernhard_4_style.png
    :width: 240pt

+-----------+-----------+
| |image01| | |image02| |
+-----------+-----------+
| default   | bernhard_4|
+-----------+-----------+

The class PI88Plotter is based on matplotlib  and generates figures for typical nanoindentation plotting tasks.
These include, load-displacement, load-time, displacement-time, hardness or  reduced modulus.
The style of the plots can be customized with plotter styles (plotter_styles.py).
This includes dpi, figure size, line and marker style.

class PI88ToPPTX
----------------

The class PI88PToPPTX helps to create PowerPoint reports based on PI88Measurement data.
It uses python-pptx--interface module and so doesn't need an installed version of PowerPoint to create a pptx-file.
Its possible to use a template file as base to get e.g. coorperate design. There are methods to create slides add tables,
(matplotlib-) figures and textboxes to the slides. Tables and text can be formated using style sheets. For some common
tasks, there are convenient functions:

    * create_title_slide() ... create a slide with load-displacement plot and table with meta data of measurements
    * create_measurement_slides() ... create a slide for each measurement including plot and calculated results
    * create_summary_slide() ... summary of all measurements (including calculated Er, H)
    * add_content_slide() ... creates a content slide with hyperlinks to all other slides


class PI88ToExcel
-----------------

...

ni_analyser.py
--------------

...

License and Acknowledgments
---------------------------
``pi88reader`` is licensed under the MIT license.
