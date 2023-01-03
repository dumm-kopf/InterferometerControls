# -*- coding: utf-8 -*-
"""
This is a better code for measuring and plotting
intensity vs. displacement of a SHG Oscilloscope
"""

# import pyvisa as visa
import OscpVISA
import numpy
import sys
import matplotlib.pyplot as plt
from tqdm import tqdm
from pylablib.devices import Thorlabs

#%% Initialize Devices
# Initialize oscilloscope
OSCP = OscpVISA.SiglentOSCP(name = 'USB0::0xF4ED::0xEE3A::SDS1ECDQ2R5643::INSTR')
# OSCP.ID()

# Initialize Kinesis Motor as stage w/ scale
stage_scale = 233472/0.5 

try: 
    stage = Thorlabs.KinesisMotor('80840262', scale = stage_scale) 
except Thorlabs.base.ThorlabsError:
    print("Operation interrupted, stage not closed")
    print('Enter "stage.close()" in console')
    sys.exit(0)

#%% Set IVDmeasure Parameters 
#   (Optional, can be entered directly into func)

init_x = 0        
final_x = 24000
dx = 1000    #displacement between each measurement


#%% Define measurement function
def IVDmeasure(init, fin, dx=1, scale=False):
    
    # Initialize arrays for data
    nn = int((fin - init) / dx)
    global position_data
    position_data= numpy.zeros(nn)
    global oscp_data
    oscp_data = numpy.zeros(nn)

    
    stage.wait_move()
    stage.move_to(init, scale=scale)
    stage.wait_move()
    print('Stage at initial position' + str(stage.get_position(scale=scale)))
    
    i = 0
    
    print('Mesurement begins')
    for i in tqdm(range(0, nn, 1), desc="Measureing"):
        
        stage.wait_move()
        stage.move_by(dx, scale=scale)
        
        position_data[i] = stage.get_position(scale=True)
        oscp_data[i] = OSCP.return_meanV()
    
        i = i + 1
        
#%%
IVDmeasure(init_x, final_x, dx=dx, scale=False)

#%%  Plot the stage.Position vs OSCP.meanV
plt.plot(position_data, oscp_data)

stage.close()
    
    
    
    
    
    
    
    