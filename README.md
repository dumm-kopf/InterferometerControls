# Interferometer Controls 
This provides basic controls necessary for taking inteferometry measurements. A translational stage is controlled by a ThorLabs Kinesis motor and the instensity is measured using a Siglent Oscilloscope.

## Dependencies
The main dependencies are PyLabLib for communicating with the motor and PyVISA for communicating with the oscilloscope.

For the ThorLabs module in PyLabLib, there is a dependency on a package that can only be installed through pip, not anaconda, *if working in a conda virtual environment use pip to install all packages* or the code will not work. It might be a good idea to use alternatives for setting up a virtual environment.

Other dependencies are numbpy, matplotlib for arrays and plots; the tqdm package is for the progress bar.

## Features
OscpVISA.py creates a class for the oscilloscope with some basic methods, this makes it easier to type read/query commands.

Measure.py initializes all devices and has a function to take a intensity vs. position with input arguments initial and final position, parameters dx for distance between each measurement and scale for whether the inputs are in real units or internal units of the device.

## Next Steps
1. Fine tune certain parameters for current set-up such as determining the position where the motor makes contact with the stage and the position for max SHG.
2. Convert the data into the time domain, fit Gaussian, determine FWHM
