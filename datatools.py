# -*- coding: utf-8 -*-
"""
Some data analysis functions
"""
import numpy
import pandas
from scipy.optimize import curve_fit


def import_csv(file_dir):
    """
    reads a .csv file and returns a numpyarray
    :param file_dir: file directory
    :return: a numpy array
    """
    dataF = pandas.read_csv(file_dir)
    dataA = pandas.DataFrame.to_numpy(dataF)
    return dataA


def gauss(x, H, A, x0, sigma):
    return H + A * numpy.exp(-(x - x0) ** 2 / (2 * sigma ** 2))


def fit_gauss(x_data, y_data):
    mean = sum(x_data * y_data) / sum(y_data)
    sigma = numpy.sqrt(sum(y_data * (x_data - mean) ** 2) / sum(y_data))
    output = curve_fit(gauss, x_data, y_data, p0=[min(y_data), max(y_data), mean, sigma])
    return output

