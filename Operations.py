# -*- coding: utf-8 -*-
"""
Created on Mon Jan 30 13:18:48 2023

@author: lenovo
"""

from Interferometer import interferometer
import datatools as dt

og = dt.import_csv('/Users/jason/Documents/BeamCharacterizationProject/Data/PvI18-01-2023T190315.csv')

data = og[:,1:]
FWHM = dt.fmhw_gauss(data[:,0] / 300000000, data[:,1])
print(FWHM)