# -*- coding: utf-8 -*-
"""
Created on Mon Jan 30 13:18:48 2023

@author: lenovo
"""
import Interferometer
from matplotlib import pyplot as plt
import numpy as np
import scipy
from Interferometer import interferometer
import datatools as dt

# maitai = Interferometer.interferometer()
# maitai.set_measure_param(-15000, 15000, 80, False)
# maitai.laser_bw = 40
# maitai.laser_wl = 800
# maitai.measure_IvP(laser_bw=60, laser_wl=800)
# maitai.export_csv()
# maitai.close()


data = dt.import_csv('/Users/jason/Documents/BeamCharacterizationProject/Repo/data/27-02-2023T15475640800.csv')
t = (data[:, 1]) * 10 ** 9 / (3 * 10 ** 8) * 2 * (800 * 10 ** -9)
i = data[:, 3] * 1

FWHM = dt.fmhw_gauss(t, i)
print(FWHM)

# expected value, 35 fs
