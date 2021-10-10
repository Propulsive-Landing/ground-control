from data_packet import *
from rf import *

import matplotlib.pyplot as plt

#rf = RF('COM1')                                #Com1 error because Com1 is not recognized
#packet = rf.read()

plt.figure()                                    #Correctly graphs 3D plot
graph = plt.axes(projection = '3d')             #input data set to (0,0,0) in line 19
graph.set_xlabel('z-coordinate')
graph.set_ylabel('y-coordinate')
graph.set_zlabel('z-coordinate')
graph.autoscale(False)
graph.set_xlim([-5, 5])
graph.set_ylim([-5, 5])
graph.set_zlim([0,10])
graph.scatter3D(0, 0, 0, color = 'b')
plt.show()

