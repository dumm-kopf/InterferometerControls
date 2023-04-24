# -*- coding: utf-8 -*-
"""
Created on Mon Jan 30 13:18:48 2023

@author: lenovo
"""
import Interferometer
from matplotlib import pyplot as plt
import numpy as np
import scipy

import datatools
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
intensity = data[:, 3]

delt_t = 2 * data[:,1] * 10 ** 12 / (3 * 10 ** 8)  # converted to femtoseconds
intensity = data[:, 3]

plt.plot(delt_t, intensity)
plt.show()

fitted = dt.fit_gauss(delt_t, intensity)

plt.plot(delt_t, fitted)
plt.show()

pulse = dt.fwhm(delt_t, fitted)

x = int(pulse[0])
x2 = int(pulse[1])

width = 1.41 * (delt_t[x2] - delt_t[x])

# FWHM = datatools.fmhw(intensity)

# expected value, 35 fs * 1.5 = 53.5 fs


