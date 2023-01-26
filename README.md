# Interferometer Controls 
This provides basic controls necessary for taking inteferometry measurements. A translational stage is controlled by a ThorLabs Kinesis motor and the instensity is measured using a Siglent Oscilloscope.

## Dependencies
- The main dependencies are [PyLabLib](https://pylablib.readthedocs.io/en/latest/) for communicating with the motor and [PyVISA](https://pyvisa.readthedocs.io/en/latest/) for communicating with the oscilloscope.

  - For the ThorLabs module in PyLabLib, there is a dependency on a package that can only be installed through pip, not conda, ***if working in a conda virtual environment use pip to install PyLabLib and its dependencies*** or the code will not work. It might be a good idea to use alternatives for setting up a virtual environment, although conda has other benefits and using pip in a conda environment isn't always problematic.

- Other dependencies are [numbpy](https://numpy.org), [matplotlib](https://matplotlib.org) for arrays and plots (usually included in a conda python installation); the [tqdm](https://pypi.org/project/tqdm/) package is for the progress bar.

## Features
- OscpVISA.py creates a class for the oscilloscope with some basic methods, this makes it easier to type read/query commands.

- Measure.py initializes all devices and has a function to take a intensity vs. position with input arguments initial and final position, parameters dx for distance between each measurement and scale for whether the inputs are in real units or internal units of the device.

## Next Steps
- [ ] Fine tune certain parameters for current set-up such as determining the position where the motor makes contact with the stage and the position for max SHG.
- [ ] Convert the data into the time domain, fit Gaussian, determine FWHM
