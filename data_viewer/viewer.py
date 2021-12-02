import tkinter as tk
from tkinter import filedialog

import os
from pathlib import Path

import matplotlib.pyplot as plt

def main():
    script_path = Path(os.path.realpath(__file__)).parent

    #=============================Setup Window and scrollbar============================#
    window = tk.Tk()
    window.title("Data Viewer")
    window.geometry("500x300")

    frame = tk.Frame(window)
    frame.pack()

    #==========================================Directory Selection=============================================#
    
    global parent_directory
    parent_directory = script_path
    global variables
    variables = {}


    def update_dropdown_from_variables():
        independent_selection['menu'].delete(0, 'end')
        independent_index_selection['menu'].delete(0, 'end')
        dependent_selection['menu'].delete(0, 'end')
        dependent_index_selection['menu'].delete(0, 'end')
        independent.set('')
        independent_index.set('')
        dependent.set('')
        dependent_index.set('')

        dependent_index_selection['menu'].add_command(label=1, command=tk._setit(dependent_index, 1))
        independent_index_selection['menu'].add_command(label=1, command=tk._setit(independent_index, 1))

        for choice in variables.keys():
            independent_selection['menu'].add_command(label=choice, command=tk._setit(independent, choice))
            dependent_selection['menu'].add_command(label=choice, command=tk._setit(dependent, choice))

    def select_directory():
        global parent_directory
        parent_directory = Path(filedialog.askdirectory(title="Select Run Directory", initialdir=script_path))

        global variables
        variables.clear()

        try:
            with open(Path.joinpath(parent_directory, './structure.txt'), 'r') as struct_file:
                struct_file.readline()
                for line in struct_file.readlines():
                    line = line.strip()
                    arr = line.split(',')
                    name = arr[2]
                    num = arr[1]

                    variables[name] = int(num)
            
            update_dropdown_from_variables()

        except:
            with open(Path.joinpath(parent_directory, './data.csv'), 'r') as data_file:
                line = data_file.readline()
                arr = line.strip().split(',')
                variables = {a: 1 for a in arr}
                
            update_dropdown_from_variables()

    runs_directory_select = tk.Button(frame, text="Select Data Directory", command=select_directory)
    runs_directory_select.pack()

    #==========================================Variable Selection==================================#

    independent_selections = tk.Frame(frame)
    dependent_selections = tk.Frame(frame)
    independent_selections.pack()
    dependent_selections.pack()

    independent = tk.StringVar()
    independent_index = tk.StringVar()
    dependent = tk.StringVar()
    dependent_index = tk.StringVar()

    independent_selection = tk.OptionMenu(independent_selections, independent, value='', *(variables.keys()))
    independent_index_selection = tk.OptionMenu(independent_selections, independent_index, value='')

    dependent_selection = tk.OptionMenu(dependent_selections, dependent, value='', *(variables.keys()))
    dependent_index_selection = tk.OptionMenu(dependent_selections, dependent_index, value='')
    

    tk.Label(independent_selections, text="Independent Variable: ").grid(row=0, column=0)
    independent_selection.grid(row=0, column=1)
    tk.Label(independent_selections, text="Index: ").grid(row=0, column=2)
    independent_index_selection.grid(row=0, column=3)

    tk.Label(dependent_selections, text="Dependent Variable: ").grid(row=0, column=0)
    dependent_selection.grid(row=0, column=1)
    tk.Label(dependent_selections, text="Index: ").grid(row=0, column=2)
    dependent_index_selection.grid(row=0, column=3)


    #======================Variable Index Management========================================#
    
    def independent_changed(*args):
        if(independent.get() not in variables.keys()):
            return

        independent_index_selection['menu'].delete(0, 'end')
        for i in range(0, variables[independent.get()]):
            independent_index_selection['menu'].add_command(label=i, command=tk._setit(independent_index, i))

    def dependent_changed(*args):
        if(dependent.get() not in variables.keys()):
            return

        dependent_index_selection['menu'].delete(0, 'end')
        for i in range(0, variables[dependent.get()]):
            dependent_index_selection['menu'].add_command(label=i, command=tk._setit(dependent_index, i))

    independent.trace('w', independent_changed)
    dependent.trace('w', dependent_changed)

        
    #=====================================Graph Generation==========================================#

    
    def generate_graph():
        xArr = []
        yArr = []

        xIndex = 0
        for key, value in variables.items():
            if(key == independent.get()):
                xIndex+=int(independent_index.get())
                break
            xIndex+=value

        yIndex = 0
        for key, value in variables.items():
            if(key == dependent.get()):
                yIndex+=int(dependent_index.get())
                break
            yIndex+=value
                
        print(xIndex, yIndex)

        with open(Path.joinpath(parent_directory, './data.csv'), 'r') as data_file:
            for line in data_file.readlines():
                arr = line.split(',')
                try:
                    xArr.append(float(arr[xIndex]))
                    yArr.append(float(arr[yIndex]))
                except ValueError:
                    pass

        plt.plot(xArr, yArr)
        plt.show()

    generate = tk.Button(frame, text="Generate Graph", command=generate_graph)
    generate.pack()

    #===========================Main====================#

    tk.mainloop()

if __name__ == "__main__":
  main()