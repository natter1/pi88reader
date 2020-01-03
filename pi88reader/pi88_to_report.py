import numpy as np
import matplotlib.pyplot as plt
import numpy as np
import pylatex
import tornado.web

from pi88reader.pi88_importer import PI88Measurement, SegmentType


def main():
    filename = '..\\resources\\quasi_static_12000uN.tdm'
    measurement = PI88Measurement(filename)

    plot = plt.scatter(measurement.time, measurement.depth)
    plt.scatter(measurement.time, measurement.load)
    # plt.scatter(measurement.depth, measurement.load)
    plt.show()


if __name__ == "__main__":
    main()
