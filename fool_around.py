import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style
from example_data import *

style.use('fivethirtyeight')

fig = plt.figure()
ax1 = fig.add_subplot(1, 1, 1)

def animate(i):
    graph_data = open(ExampleData, 'r').read()                  #ExampleData is a class from another file that we can update reguraly
    lines = graph_data.split(',')                               #Coordinate pairs on other file are than split and graphed every time interval
    xs = []                                                     #Won't dispaly data on the graph
    ys = []
    for line in lines:
        if len(line) > 1:
            x, y = line.split(',')
            xs.append(float(x))
            ys.append(float(y))
    ax1.clear()
    ax1.plot(xs, ys)




ani = animation.FuncAnimation(fig, animate, interval = 1000)    #1000 ms
plt.show()
