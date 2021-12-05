from rf import RF

import tkinter as tk
from tkinter import filedialog

from multiprocessing import Process, cpu_count

import os
import math
from pathlib import Path
from shutil import copyfile

def log_handler(queue, path):
    print("Start log handling")

    file = open(path, 'w')

    while(True):
        message = queue.get()
        if(message == 'STOP'):
           break
        file.write(str(message) + '\n')
        print(message)
    file.close()
    print("end log handling")

def telem_frame_handler(queue, current_val, path):
    print("start frame handling")


    #============Text Output========#    
    # import tkinter as tk
    # window = tk.Tk()
    # window.title("DATA")
    # window.geometry("200x200")
    # window.after(1, lambda: window.focus_force())

    # x_axis = tk.StringVar()
    # x_axis.set('0')
    # y_axis = tk.StringVar()
    # y_axis.set('0')

    # x = tk.Entry(window, textvariable=x_axis)
    # x_label = tk.Label(window, text="X: ")
    # x_label.pack()
    # x.pack()

    # y = tk.Entry(window, textvariable=y_axis)
    # y.pack()

    #=========Graph Output===========#
    import matplotlib.pyplot as plt
    plt.ion()
    plt.show()
    xArr = []
    yArr = []

    #=========File Intiialization====#
    file = open(path, 'a')



    while(True):
        #=====Handling and file writing======#
        message = queue.get()
        if(message == 'STOP'):
           break

        for x in message:
            file.write(str(x) + ",")
        file.write('\n')

        try:
            #=========Text Output=========#
            # x_axis.set((180/math.pi)*current_val[2])
            # y_axis.set((180/math.pi)*current_val[3])
            # window.update()

            #=========Graph Output=========#
            yArr.append(float((current_val[2])))
            plt.clf()
            plt.plot(yArr[-40:])
            plt.draw()
            plt.pause(0.00001)
        except ValueError:
            pass
        except IndexError:
            pass


    # plt.close()
    file.close()
    # window.destroy()
    print("END Frame handling")


def main():
    #============Get struct string===============#
    script_path = Path(os.path.realpath(__file__)).parent.parent
    structure_string_path = Path("./structure_manager/data/struct_string.txt")

    structure_string_path = os.path.join(script_path, structure_string_path)
    
    try:
        struct_string = open(structure_string_path).readline()
    except FileNotFoundError:
        print("ERR")

    #======Check minimum core requirements=======#
    if(cpu_count() < 3):
        print(f'Only {cpu_count()} cores available while at least 3 are required')


    #=========Initialize GUI=====================#
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
    baud_input.set("9600")


    #===============Directory/File Management Setup=========#

    global parent_directory
    parent_directory = script_path
    def select_directory():
        global parent_directory
        parent_directory = Path(filedialog.askdirectory(title="Select Directory for Runs", initialdir=script_path))

    runs_directory_select = tk.Button(window, text="Select Data Directory", command=select_directory)
    runs_directory_select.pack()

    start_button = tk.Button(window, text="Start Recording", command=start_recording)
    start_button.pack(side=tk.BOTTOM)
    while(not start_condition):
        window.update()
    #============="Start Recording"==============#


    #====================File management after start==============#
    directory = os.path.join(parent_directory, Path('./run0'))
    index = 1
    while(os.path.isdir(directory)):
        directory = os.path.join(parent_directory, Path('./run' + str(index)))
        index += 1

    os.mkdir(directory)
    
    copyfile(os.path.join(script_path, Path('./structure_manager/data/structure.txt')), os.path.join(directory, Path('./structure.txt')))

    #============Get Number of Attributes in struct==================#
    attribute_num = 0
    with open(os.path.join(directory, Path('./structure.txt'))) as structure_file:
        structure_file.readline()
        lines = structure_file.readlines()
        for line in lines:
            attribute_num += int(line.split(',')[1])
    
    rf = RF(port_input.get(), baud_input.get(), telem_string=struct_string, telem_attibute_num=attribute_num)

    #==================Logging and Graphic Processes==================#

    with open(os.path.join(directory, Path('./data.csv')), 'w') as data_file, open(os.path.join(directory, Path('./structure.txt'))) as structure_file:
        names = []
        structure_file.readline()
        for line in structure_file.readlines():
            line = line.strip()
            arr = line.split(',')

            if(arr[1] == '1'):
                names.append(arr[2])
                continue
            else:
                for i in range(0, int(arr[1])):
                    names.append(arr[2] + "["+str(i)+"]")
        for x in names:
            data_file.write(x + ",")
        data_file.write("\n")

    telem_process = Process(target=telem_frame_handler, args=(rf.telem_frame_queue, rf.current_telem_frame, os.path.join(directory, Path('./data.csv'))))
    telem_process.start()

    log_process = Process(target=log_handler, args=(rf.log_queue, os.path.join(directory, Path('./output.log'))))
    log_process.start()


    #================Exit management=============================#
    global listening
    listening = True
    def stop_listening():
        rf.telem_frame_queue.put('STOP')
        rf.log_queue.put('STOP')
        telem_process.join()
        log_process.join()
        global listening
        listening = False

    stop_button = tk.Button(window, text="Save and Exit", command=stop_listening)
    stop_button.pack()

    while(listening):
        rf.read_binary()
        window.update()

    f = open(os.path.join(directory, Path('./bytes.log')), 'w')
    for elem in rf._history:
        f.write(str(elem) + " ")
    f.close()
    

if __name__ == "__main__":
   main()