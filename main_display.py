import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style

style.use('fivethirtyeight')

fig = plt.figure()
ax1 = fig.add_subplot(2,2,1)            
ax2 = fig.add_subplot(2,2,2)
ax3 = fig.add_subplot(2,2,3)                                              

def animate(i):
    graph_data = open('example.txt','r').read()
    lines = graph_data.split('\n')
    t1s = []
    x1s = []
    y1s = []
    z1s = []
    for line in lines:
        if len(line) > 1:
            t1, x1, y1, z1 = line.split(',')
            t1s.append(float(t1))
            if len(t1s) > 20:
                del_var = int(len(t1s)) - 20
                del t1s[0:del_var - 1]
            x1s.append(float(x1))
            if len(x1s) > 20:
                del_var = int(len(x1s)) - 20
                del x1s[0:del_var - 1]
            y1s.append(float(y1))
            if len(y1s) > 20:
                del_var = int(len(y1s)) - 20
                del y1s[0:del_var - 1]
            z1s.append(float(z1))
            if len(z1s) > 20:
                del_var = int(len(z1s)) - 20
                del z1s[0:del_var - 1]
    ax1.clear()
    ax1.plot(t1s, x1s)
    ax1.plot(t1s, y1s)
    ax1.plot(t1s, z1s)
    ax1.set_xlabel('Time')
    ax1.set_ylabel('Euler')

def animate2(i):
    graph_data = open('example2.txt','r').read()
    lines = graph_data.split('\n')
    t2s = []
    x2s = []
    y2s = []
    z2s = []
    for line in lines:
        if len(line) > 1:
            t2, x2, y2, z2 = line.split(',')
            t2s.append(float(t2))
            if len(t2s) > 20:
                del_var = int(len(t2s)) - 20
                del t2s[0:del_var - 1]
            x2s.append(float(x2))
            if len(x2s) > 20:
                del_var = int(len(x2s)) - 20
                del x2s[0:del_var - 1]
            y2s.append(float(y2))
            if len(y2s) > 20:
                del_var = int(len(y2s)) - 20
                del y2s[0:del_var - 1]
            z2s.append(float(z2))
            if len(z2s) > 20:
                del_var = int(len(z2s)) - 20
                del z2s[0:del_var - 1]
    ax2.clear()
    ax2.plot(t2s, x2s)
    ax2.plot(t2s, y2s)
    ax2.plot(t2s, z2s)
    ax2.set_xlabel('Time')
    ax2.set_ylabel('Y-Axis')

def animate3(i):
    graph_data = open('example3.txt','r').read()
    lines = graph_data.split('\n')
    t3s = []
    x3s = []
    y3s = []
    z3s = []
    for line in lines:
        if len(line) > 1:
            t3, x3, y3, z3 = line.split(',')
            t3s.append(float(t3))
            if len(t3s) > 20:
                del_var = int(len(t3s)) - 20
                del t3s[0:del_var - 1]
            x3s.append(float(x3))
            if len(x3s) > 20:
                del_var = int(len(x3s)) - 20
                del x3s[0:del_var - 1]
            y3s.append(float(y3))
            if len(y3s) > 20:
                del_var = int(len(y3s)) - 20
                del y3s[0:del_var - 1]
            z3s.append(float(z3))
            if len(z3s) > 20:
                del_var = int(len(z3s)) - 20
                del z3s[0:del_var - 1]
    ax3.clear()
    ax3.plot(t3s, x3s)
    ax3.plot(t3s, y3s)
    ax3.plot(t3s, z3s)
    ax3.set_xlabel('Time')
    ax3.set_ylabel('Y-Axis')

ani = animation.FuncAnimation(fig, animate, interval=1000)
ani2 = animation.FuncAnimation(fig, animate2, interval=1000)
ani3 = animation.FuncAnimation(fig, animate3, interval=1000)
plt.show()