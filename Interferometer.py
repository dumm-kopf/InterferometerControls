# -*- coding: utf-8 -*-
"""
Created on Wed Jan 18 16:11:13 2023
@author: Jason Shao
"""

import OscpVISA
import pandas
import matplotlib.pyplot as plt
import numpy
from datetime import datetime
from tqdm import tqdm
from pylablib.devices import Thorlabs


class interferometer:
    """Interferometer class containing operations
    that involve the oscilloscope and motor"""

    def __init__(self, motor_serial='80840262', stage_scale=None,
                 oscilloscope_name='USB0::0xF4ED::0xEE3A::SDS1ECDQ2R5643::INSTR'):
        """Initializes both the motor and oscilloscope

        Args:
            motor_serial: the serial number of the ThorLabs motor to connect
            stage_scale:
        """
        #%% Instantiate variables
        # Measurement parameters
        self.initial_position = self.stage.get_position       # position to start measuring
        self.final_position = self.initial_position           # position to stop measuring
        # default values prevent excessive movement incase position hasn't been zeroed properly

        # displacement between each measurement for desired precision
        self.precision = 45       # 45 internal units this is just under 100nm

        # currently used displacement between each measurement
        self.increment = self.precision

        # Maintain scale option for pylablib methods, so it doesn't have to be included in every method call
        self.scale = False
        # Relative directories for data and plots
        self.data_dir = '/data'
        self.plot_dir = '/plot'
        # Dictionary for data array index
        self.data_dic = {
            "pos": 0,
            "pos_scaled": 1,
            "time": 2,
            "volt": 3
        }

        self.date_string = (datetime.now()).strftime('%d-%m-%YT%H%M%S')     # keeps track of when data is taken
        self.mc_data = numpy.empty(200)         # most recent data array
        self.laser_bw = "None"                  # laser bandwidth
        self.laser_wl = "None"                  # laser wavelength
        if motor_serial == '80840262':          # scale for known devices
            self.stage_scale = 2.14e-6
        else:
            self.stage_scale = stage_scale

        #%% Initialize devices
        # initialize oscilloscope
        self.oscilloscope = OscpVISA.oscilloscope(name=oscilloscope_name)

        # Initialize Kinesis Motor as stage w/ given scale
        try:
            self.stage = Thorlabs.KinesisMotor(motor_serial, scale=self.stage_scale)
            self.stage._scale_units = "nm"
        # Error for if the stage wasn't closed after previous operation
        except Thorlabs.base.ThorlabsError:
            raise Exception("Operation interrupted, stage not closed \n "
                            "Enter 'interferometer.close()' in console")

    def convert(self, val):
        """Converts between internal units and physical units based on given scale factor

        Automatically determines if input is in internal units or physical units
        since internal units are always of the type int and physical units are always of the type floats

        :param val: value to be converted
        """
        if isinstance(val, int):
            return val / self.stage_scale
        else:
            return val * self.stage_scale

    def set_measure_param(self, initial_position, final_position, increment, scale):
        """ Set measuring parameters

        :param initial_position: position to start measuring
        :param final_position: position to stop measuring
        :param increment: displacement between each measurement
        :param scale: True for physical units, False for internal units
        """
        self.initial_position = initial_position
        self.final_position = final_position
        self.increment = increment
        self.scale = scale

    def get_measure_param(self, scale=None):
        """
        Returns current initial_position, final_position, and increment

        :param scale: False for internal unit, True for physical unit
        :return: measurement parameter values
        """
        if scale is None:
            scale = self.scale
        if scale:
            return {
                    self.convert(self.initial_position),
                    self.convert(self.final_position),
                    self.convert(self.increment)
                    }
        else:
            return self.initial_position, self.final_position, self.increment

    # def center_to_max(self, position_range):
    #     """
    #     Locates and positions the stage for maximum SHG
    #
    #     This is done by taking quick and scrappy measurements that
    #     recursively decrease in range and increase in precision
    #
    #     :param position_range: the position range in which max SHG occurs
    #     :return: the position the stage has been moved to
    #     """
    #     increment = position_range / 20
    #     IvD = numpy.zeros((20, 2))
    #     while increment > self.increment:
    #         for i in range(0, 20, 1):
    #             self.stage.wait_move()
    #             self.stage.move_by(increment, scale=False)
    #             IvD[i][0] = self.stage.get_position(scale=False)
    #             IvD[i][1] = self.oscilloscope.return_meanV()
    #         center = IvD[numpy.argmax(a=IvD[:, 1])][1]
    #         self.stage.move_to(center, scale=False)
    #         self.stage.wait_move()
    #         self.center_to_max(position_range=position_range/2)
    #     return self.stage.get_position()

    def measure_IvP(self, initial_position=None, final_position=None, increment=None,
                    scale=None, laser_bw=None, laser_wl=None, save_data=False):
        """
        Takes a measurement and plots IvD data, exports a .csv file if save_data=True

        :param initial_position: position to start measuring
        :param final_position: position to stop measuring
        :param increment: displacement between measurements
        :param scale: True if inputs are in physical units, false if in internal units
        :param save_data: save data as .csv or not
        :param laser_bw: record laser bandwidth of this measurement
        :param laser_wl: record laser wavelength of this measurement
        """
        if initial_position==None: initial_position = self.initial_position
        if final_position==None: final_position = self.final_position
        if increment==None: increment = self.increment
        if scale==None: scale = self.scale
        if laser_bw==None: laser_bw = self.laser_bw
        if laser_wl==None: laser_wl = self.laser_wl

        #%% Set parameters and record values

        # instantiate data array
        array_size = abs(int((self.initial_position - self.final_position) / self.increment))
        data_IvP = numpy.zeros((array_size, 4))

        # prep for measurement
        self.stage.move_to(initial_position, scale=scale)
        self.stage.wait_move()
        print('Stage at initial position ' + str(self.stage.get_position(scale=scale)))

        #%% Measuring
        print('Measurement started')

        # updates time of measurement
        now = datetime.now()
        self.date_string = now.strftime("%d-%m-%YT%H%M%S")

        for i in tqdm(range(0, array_size, 1), desc="Measuring"):

            self.stage.wait_move()
            self.stage.move_by(increment, scale=scale)

            data_IvP[i][0] = self.stage.get_position(scale=False)
            data_IvP[i][1] = self.convert(data_IvP[i][0])
            data_IvP[i][2] = data_IvP[i][1] * 3e-8
            data_IvP[i][3] = self.oscilloscope.return_meanV()
        self.mc_data = data_IvP
        #%% Plot data
        self.plot_IvP(data=self.mc_data)

        #%% export .csv
        if save_data:
            self.export_csv(data_IvP)

    def plot_IvP(self, data=None, save=False):
        """
        A method that plots given data

        :param data: 2D numpy array to be plotted
        :return: a plot
        """
        if data==None: data = self.mc_data

        plt.style.use('_mpl-gallery')
        fig, ax = plt.subplots()
        ax.plot(data[:, 1], data[:, 3])
        ax.set(xlabel='position (nm)', ylabel='intensity (V)',
               title='SHG Intensity vs. Position')
        plt.grid()
        info_string = 'Bandwidth: ' + self.laser_bw + 'Wavelength: ' + self.laser_wl
        plt.figtext(s=info_string)

        if save==True: plt.savefig('\plot\info_string')


    def export_csv(self, data, name=None):
        """ A method that exports the current data to a .csv file

        :param data: data to be exported, should be numpy array
        :param name: filename
        :return: exports .cvs
        """
        if data==None: data = self.mc_data

        dataframe = pandas.DataFrame(
            data=data,
            columns=['pos', 'scaled_pos', 'time', 'intensity']
        )
        laser_info = "|" + str(self.laser_wl) + "," + str(self.laser_bw) + "|"

        if name==None:
            filename = data + self.date_string + laser_info
        else:
            filename = self.data_dir + name + laser_info

        dataframe.to_csv(filename + ".csv")

    def move_by(self, x, scale=None):
        if scale==None: scale = self.scale
        self.stage.move_by(x, scale)

    def move_to(self, x, scale=None):
        if scale==None: scale = self.scale
        self.stage.move_to(x, scale)

    def get_pos(self, scale=None):
        if scale==None: scale = self.scale
        return self.stage.get_position(scale=scale)

    def close(self): self.stage.close()

    def open(self): self.stage.open()

    def get_mean(self): self.oscilloscope.return_meanV()