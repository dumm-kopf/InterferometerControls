from pylablib.devices import Thorlabs
import pyvisa as visa
import OSCPcomm
import numpy
import matplotlib.pyplot as plt


rm = visa.ResourceManager()

print(rm.list_resources())

OSCP = OSCPcomm.SiglentOSCP(name = 'USB0::0xF4ED::0xEE3A::SDS1ECDQ2R5643::INSTR')

OSCP.ID()
print(OSCP.return_meanV())

Thorlabs.list_kinesis_devices()

stage_scale = 233472/0.5 

stage = Thorlabs.KinesisMotor('80840262', scale = stage_scale) 
stage.get_status()




# Movement

disp = 0.000024

increment = 80
dx = 200

# Initialize arrays for data
position_data = numpy.zeros(dx)
oscp_data = numpy.zeros(dx)

stage.move_to(-10000, scale = False)
stage.wait_move()

for i in range(0, dx, 1): 
    
    stage.wait_move()
    
    position_data[i] = stage.get_position(scale = True)
    oscp_data[i] = OSCP.return_meanV()
    
    print(str(OSCP.return_meanV()) + " at " + str(stage.get_position(scale = False)))
    # print(position_data[i])
    # print(stage.get_position(scale = False))
     
    stage.move_by(increment, scale = False)
    
    
plt.plot(position_data, oscp_data)
    
stage.close()





