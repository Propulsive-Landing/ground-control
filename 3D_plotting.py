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

plt.figure()                                    #tried to display two graphs
graph = plt.axes(projection = '3d')             #first graph above popped up 
graph.set_xlabel('z-coordinate')                #As soon as closed the first graph, second one popped up
graph.set_ylabel('y-coordinate')                #appear to not show two seperate graphs at the same time
graph.set_zlabel('z-coordinate')
graph.autoscale(False)                          #copy and pasting this code (left) into another window and trying to run both 
graph.set_xlim([-5, 5])                         #at the same time also failed, one than the other
graph.set_ylim([-5, 5])
graph.set_zlim([0,10])
graph.scatter3D(1, 1, 1, color = 'b')
plt.show()