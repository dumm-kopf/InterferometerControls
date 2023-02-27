# -*- coding: utf-8 -*-
"""
Created on Mon Jan 30 13:18:48 2023

@author: lenovo
"""
import Interferometer
from matplotlib import pyplot as plt
import numpy
import scipy
from Interferometer import interferometer
import datatools as dt

maitai = Interferometer.interferometer()
maitai.set_measure_param(-15000, 15000, 80, False)
maitai.laser_bw = 40
maitai.laser_wl = 800
maitai.measure_IvP(laser_bw=60,laser_wl=800)
maitai.export_csv()
maitai.close()


# og = dt.import_csv('/Users/jason/Documents/BeamCharacterizationProject/Data/PvI18-01-2023T190315.csv')
#
# data = og[:,1:]
# FWHM = dt.fmhw_gauss(data[:,0] / 300000000, data[:,1])
# print(FWHM)

# expected value, 35 fs