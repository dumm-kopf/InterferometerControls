# -*- coding: utf-8 -*-
"""
Created on Wed Jan 18 16:11:13 2023

@author: Jason Shao
"""

# import pyvisa as visa
import OscpVISA
import numpy
import sys
import matplotlib.pyplot as plt
from tqdm import tqdm
from pylablib.devices import Thorlabs

class Interferometer:
    
    def __init__(self, name, stage_serial = '80840262', stage_scale = 233472/0.5,
                 oscilloscope_name = 'USB0::0xF4ED::0xEE3A::SDS1ECDQ2R5643::INSTR'):
        
        array_size = 0
        
        self.name = name
        self.stage_serial = stage_serial
        self.oscilloscope_name = oscilloscope_name
        self.stage_scale = stage_scale
        #%% Initialize Devices
        # Initialize oscilloscope
        self.OSCP = OscpVISA.SiglentOSCP(name = oscilloscope_name)
        # Initialize Kinesis Motor as stage w/ scale
        try: 
            self.stage = Thorlabs.KinesisMotor(stage_serial, scale = stage_scale) 
        except Thorlabs.base.ThorlabsError:
            print("Operation interrupted, stage not closed")
            print('Enter "stage.close()" in console')
            sys.exit(0)
            
    def set_measure_param(self, initial_position = 0, final_position = 0, increment = 1, scale = False):
        
        self.initial_position = initial_position
        self.final_position =   final_position
        self.increment = increment
        self.scale = scale
        
    def get_measure_param(self, scale = False):
        
        return (self.initial_position, self.final_position, self.increment, self.scale)
   
    def center_to_max(self, position_range):
        original_p = self.stage.get_position()
        increment = position_range / 20
        
        for i in range(0, 20, 1):
            
            self.stage.move_by
        
        
    
    def zero_position(self):
        
        oscp = numpy.zeros(-10000)
        stage = numpy.zeros(10000)
        
        self.stage.move_to(self.stage.get_position(scale = False) - 5000, scale = False)
        self.stage.wait_move()
        for i in tqdm(range(0, array_size, 1), desc="Measureing"):
            self.stage.wait_move()
            self.stage.move_by(dx, scale=scale)
            
            position_data[i] = self.stage.get_position(scale=False)
            oscp_data[i] = self.OSCP.return_meanV()
        
        
        
    def IVDmeasure(self, initial_position, final_position, dx=1, scale=False):
        
        # Initialize arrays for data
        array_size = int((final_position - initial_position) / dx)
        global position_data
        position_data= numpy.zeros(array_size)
        global oscp_data
        oscp_data = numpy.zeros(array_size)

        
        self.stage.wait_move()
        self.stage.move_to(initial_position, scale=scale)
        self.stage.wait_move()
        print('Stage at initial position ' + str(self.stage.get_position(scale=scale)))
        
        i = 0
        
        print('Mesurement begins')
        for i in tqdm(range(0, array_size, 1), desc="Measureing"):
            
            self.stage.wait_move()
            self.stage.move_by(dx, scale=scale)
            
            position_data[i] = self.stage.get_position(scale=False)
            oscp_data[i] = self.OSCP.return_meanV()
        
            i = i + 1
            
            
            
