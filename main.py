from rf import RF
import tkinter as tk
from multiprocessing import Process
import os
from pathlib import Path

def telem_frame_handler(queue, path):
    print("start")

    import matplotlib.pyplot as plt
    plt.axis([0, 10, 0, 10])
    plt.ion()
    plt.show()
    file = open(path, 'w')

    xArr = []
    yArr = []

    while(True):
        message = queue.get()
        if(message == 'STOP'):
           break

        xArr.append(message[3])
        yArr.append(message[46])

        
        plt.clf()
        plt.plot(xArr[-20:], yArr[-20:])
        plt.draw()
        plt.pause(0.001)

        for x in message:
           file.write(str(x) + ",")
        file.write('\n')

    file.close()
    print("END")


def main():
    #======Get struct string=====#
    script_path = Path(os.path.realpath(__file__)).parent
    structure_string_path = Path("./structure_manager/data/struct_string.txt")

    structure_string_path = os.path.join(script_path, structure_string_path)
    
    try:
        struct_string = open(structure_string_path).readline()
    except FileNotFoundError:
        print("ERR")
    

    window = tk.Tk()
    window.title("RF Communication")
    window.geometry("200x200")
    
    global start_condition
    start_condition = False

    def start_recording():
        global start_condition
        start_condition = True

    options = tk.Frame(window)
    options.pack()

    tk.Label(options, text="Port: ").grid(row=0, column=0)
    port_input = tk.StringVar()
    port = tk.Entry(options, width=8, textvariable=port_input)
    port.grid(row=1, column=0)

    tk.Label(options, text="Baud rate: ").grid(row=0, column=1)
    baud_input = tk.StringVar()
    baud = tk.Entry(options, width=8, textvariable=baud_input)
    baud.grid(row=1, column=1)

    start_button = tk.Button(window, text="Start Recording", command=start_recording)
    start_button.pack()

    while(not start_condition):
        window.update()

    
        
    
    rf = RF(port_input.get(), baud_input.get(), telem_string=struct_string)

    telem_process = Process(target=telem_frame_handler, args=(rf.telem_frame_queue,'run1.csv'))
    telem_process.start()


    global listening
    listening = True
    def stop_listening():
        rf.telem_frame_queue.put('STOP')
        telem_process.join()
        global listening
        listening = False

    stop_button = tk.Button(window, text="Save and Exit", command=stop_listening)
    stop_button.pack()

    while(listening):
        rf.read_binary()
        window.update()
    

if __name__ == "__main__":
   main()