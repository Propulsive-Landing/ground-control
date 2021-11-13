from rf import RF
import tkinter as tk

import os
from pathlib import Path

def main():
    #======Get struct string=====#
    script_path = Path(os.path.realpath(__file__)).parent
    structure_string_path = Path("./structure_manager/data/struct_string.txt")

    structure_string_path = os.path.join(script_path, structure_string_path)
    
    struct_string = '=IhL4f4l26f19f20fI'
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

    start_button = tk.Button(window, text="Start Recording", command=start_recording)
    start_button.pack()

    while(not start_condition):
        window.update()

    
    print(struct_string)
    rf = RF('COM3', 115200, telem_string=struct_string, backlog_threshold=6000)

    #add save_and_exit button, live plot. 
    rf.loop_for_data(window)
    

if __name__ == "__main__":
   main()