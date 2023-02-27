# -*- coding: utf-8 -*-
"""
Some data analysis functions
"""
import numpy as np
import pandas
from matplotlib import pyplot as plt
from scipy.optimize import curve_fit
from scipy import stats


def import_csv(file_dir):
    """
    reads a .csv file and returns a numpy array
    :param file_dir: file directory
    :return: a numpy array
    """
    dataF = pandas.read_csv(file_dir)
    dataA = pandas.DataFrame.to_numpy(dataF)
    return dataA


def gauss(x, H, A, x0, sigma):
    return H + A * np.exp(-(x - x0) ** 2 / (2 * sigma ** 2))


def fmhw_gauss(xdata, ydata):

    plt.plot(xdata, ydata, '--r')
    mean = sum(xdata * ydata) / sum(ydata)
    sigma = np.sqrt(sum(ydata * (xdata - mean) ** 2) / sum(ydata))
    popt, pcov = curve_fit(gauss, xdata, ydata, p0=[min(ydata), max(ydata), mean, sigma])
    plt.plot(xdata, gauss(xdata, *popt), 'b', label='fit')
    plt.show()

    return 2.35482 * sigma