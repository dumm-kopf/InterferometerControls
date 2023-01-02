# This code acts as a wrapper on top of pyvisa wrappers for a Siglent Oscilloscope
import pyvisa as visa

rm = visa.ResourceManager()

# print(rm.list_resources())

class SiglentOSCP:
        
    def __init__(self, name):
        self.name = name
        self.instr = rm.open_resource(self.name)
        self.instr.read_termination = '\n'
        self.instr.write_termination = '\n'
        
    
    def ID(self):
        print('This device is')       
        print(self.instr.query('*IDN?'))
         
    def return_meanV(self):
        
        og_str = self.instr.query('C1:PARAMETER_VALUE? MEAN') 
        prefix_len = len("C1:PAVA MEAN,")
        
        num_str = og_str[prefix_len : len(og_str) - 1]
        
        return float(num_str)
        
        
    def test(self):
        print('This is a test message')

        
        
        
        
            
             
