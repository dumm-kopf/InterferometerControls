# -*- coding: utf-8 -*-
"""
Some data analysis functions
"""
import numpy as np
import pandas
from matplotlib import pyplot as plt
from scipy.optimize import curve_fit
from scipy import signal


def import_csv(file_dir):
    """
    reads a .csv file and returns a numpy array
    :param file_dir: file directory
    :return: a numpy array
    """
    dataF = pandas.read_csv(file_dir)
    dataA = pandas.DataFrame.to_numpy(dataF)
    return dataA


def gauss(x, H, A, mean, sigma):
    """
    Gaussian Distribution function
    :param x:
    :param H:
    :param A:
    :param mean: mean
    :param sigma: standard distribution
    :return:
    """
    return H + A * np.exp(-(x - mean) ** 2 / (sigma ** np.sqrt(2 * np.pi)))


def fit_gauss(xdata, ydata):
    """
    Determines parameters for Gaussian distribution
    :param xdata: x data
    :param ydata: y data
    :return: fitted y data
    """

    # plt.plot(xdata, ydata, 'or')
    mean = sum(xdata) / xdata.size
    sigma = np.std(xdata)
    popt, pcov = curve_fit(gauss, xdata, ydata, p0=[min(ydata), max(ydata), mean, sigma])
    # plt.plot(xdata, gauss(xdata, *popt), 'b', label='fit')
    # plt.show()
    return gauss(xdata, *popt)


def fwhm(xdata, ydata):
    """
    Determines the Full Width at Half Max of given data
    :param xdata: x data
    :param ydata: y data
    :return: the x indices of fwhm of peaks
    """

    index_max, _ = signal.find_peaks(ydata)

    half_widths = signal.peak_widths(ydata, index_max, rel_height=0.5)

    x1 = int(half_widths[2])
    x2 = int(half_widths[3])

    plt.plot(xdata, ydata)
    # plt.plot(index_max, ydata[index_max], "x")
    plt.hlines(half_widths[1], xdata[x1], xdata[x2], color="C2")
    plt.show()

    return x1, x2
