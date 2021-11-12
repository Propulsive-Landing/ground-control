from rf import RF
from matplotlib import pyplot as plt

def main():
    file = open("run.csv", "w")
    plt.axis([0, 10, 0, 10])
    plt.ion()
    plt.show()

    global xArr
    xArr = []
    global yArr
    yArr = []

    def handler(frame):
        for x in frame:
            file.write(str(x) + ", ")
        file.write("\n")

        #Plotting
        xArr.append(frame[3])
        yArr.append(frame[46])

    def plot():
        global xArr
        global yArr
        if(len(xArr) > 10):
            xArr = xArr[-20:]
            yArr = yArr[-20:]
            plt.clf()
            plt.plot(xArr, yArr)
            plt.draw()
            plt.pause(0.001)


    rf = RF('COM3', 115200, handler, telem_string='=IhL4f4l26f19f20fI', backlog_threshold=6000)
    
    while(True):
        #plotting
        plot()


        #reading
        rf.read_binary()
    

if __name__ == "__main__":
   main()