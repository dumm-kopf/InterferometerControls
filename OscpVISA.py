# This code acts as a wrapper on top of pyvisa wrappers for a Siglent Oscilloscope
import pyvisa as visa

rm = visa.ResourceManager()

# print(rm.list_resources())


class oscilloscope:
        
    def __init__(self, name):
        self.name = name
        self.instr = rm.open_resource(self.name)
        self.instr.read_termination = '\n'
        self.instr.write_termination = '\n'
        
    # Identifies device
    def ID(self):
        print('This device is')       
        print(self.instr.query('*IDN?'))
        
    # returns the mean voltage measurement from the oscilloscope channel 1
    def return_meanV(self):
        
        # retrieves str returned by oscilloscope
        og_str = self.instr.query('C1:PARAMETER_VALUE? MEAN') 
        # characters before the numerical value
        prefix_len = len("C1:PAVA MEAN,")
        
        # extract numerical value from returned str
        num_str = og_str[prefix_len : len(og_str) - 1]
        
        return float(num_str)
        

        
        
        
        
            
             
