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
import pandas
from datetime import datetime
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
# As of now, peak SHG at x = 5456650

init_x = -15000      
final_x = 15000
dx = 200   #displacement between each measurement


#%% Define measurement function
def IVDmeasure(init, fin, dx=1, scale=False):
    
    # Initialize arrays for data
    nn = int((fin - init) / dx)
    global PvI_data
    PvI_data= numpy.zeros((nn, 2))


    
    stage.wait_move()
    stage.move_to(init, scale=scale)
    stage.wait_move()
    print('Stage at initial position ' + str(stage.get_position(scale=scale)))
    
    
    print('Mesurement begins')
    for i in tqdm(range(0, nn, 1), desc="Measuring"):
        
        stage.wait_move()
        stage.move_by(dx, scale=scale)
        
        PvI_data[i][0] = stage.get_position(scale=False)
        PvI_data[i][1] = OSCP.return_meanV()
    
        
#%%
IVDmeasure(init_x, final_x, dx=dx, scale=False)

#%%  Plot the stage.Position vs OSCP.meanV
plt.plot(PvI_data[:,0], PvI_data[:,1])

#%% Saves Data to .csv file
convert = pandas.DataFrame(PvI_data)
now = datetime.now()
dt_string = now.strftime("%d-%m-%YT%H%M%S")
addrs = "C:/Users/lenovo/Documents/Beam Characterization Project/Data/PvI"

convert.to_csv(addrs + dt_string + ".csv") 


#%% Close stage
stage.close()

    

    
    