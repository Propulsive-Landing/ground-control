import matplotlib.pyplot as plt

x = range(10)
y = range(10)

x2 = [1,2,3]
y2 = [3,2,1]

plt.subplot(1,2,1)                  #plots two different lines
plt.plot(x,y, 'b')                  #In theory, update x and y and then animate the plotting
plt.plot(x2,y2, 'r')                #using plt.func.animation
plt.xlabel('Time')
plt.ylabel('Angle')
plt.title('X vs X2')

plt.subplot(1,2,2)
plt.plot(0,0,'b')
plt.xlabel('Time')
plt.ylabel('Angle')

plt.title('one vs two')

plt.show()