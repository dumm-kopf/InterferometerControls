# -*- coding: utf-8 -*-
"""
This code is the first attempt at getting a intensity vs. displacement plot
of a SHG Inteferometer.It is not well written but it works.
"""

import pyvisa as visa
import OscpVISA
import numpy
import matplotlib.pyplot as plt
from tqdm import tqdm
from pylablib.devices import Thorlabs

#%% 
rm = visa.ResourceManager()
print(rm.list_resources())

# Initializes Oscilloscope
OSCP = OscpVISA.SiglentOSCP(name = 'USB0::0xF4ED::0xEE3A::SDS1ECDQ2R5643::INSTR')


OSCP.ID()
print(OSCP.return_meanV())

Thorlabs.list_kinesis_devices()

stage_scale = 233472/0.5 

stage = Thorlabs.KinesisMotor('80840262', scale = stage_scale) 
stage.get_status()


# Movement Parameters

# disp = 0.000024
#%%

dx = 80    #displacement per step/measurement in internal units
nn = 200   #number of steps/measurement

# Initialize arrays for data
position_data = numpy.zeros(nn)
oscp_data = numpy.zeros(nn)

# Moves stage to a initial position
stage.move_to(-10000, scale = False)
stage.wait_move()

#%% Every iteration moves the stage by dx and records position and OSCP.meanV
for i in tqdm(range(0, nn, 1), desc="Measureing"): 

    
    stage.wait_move()
    
    position_data[i] = stage.get_position(scale = True)
    oscp_data[i] = OSCP.return_meanV()
    
    # print(str(OSCP.return_meanV()) + " at " + str(stage.get_position(scale = False)))
    
    # print(position_data[i])
    # print(stage.get_position(scale = False))
     
    stage.move_by(dx, scale = False)
    
#%%  Plot the stage.Position vs OSCP.meanV
plt.plot(position_data, oscp_data)




#%%
stage.close()





