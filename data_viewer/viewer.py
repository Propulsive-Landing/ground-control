import tkinter as tk
from tkinter import ttk
from tkinter import filedialog

import os
from pathlib import Path


def main():
    script_path = Path(os.path.realpath(__file__)).parent

    #=============================Setup Window and scrollbar============================#
    window = tk.Tk()
    window.title("Data Viewer")
    window.geometry("400x400")

    main_frame = tk.Frame(window)
    main_frame.pack(fill = tk.BOTH, expand=1)

    my_canvas = tk.Canvas(main_frame)
    my_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)

    my_scrollbar = ttk.Scrollbar(main_frame, orient=tk.VERTICAL, command=my_canvas.yview)
    my_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    my_canvas.configure(yscrollcommand=my_scrollbar.set)
    my_canvas.bind('<Configure>', lambda e: my_canvas.configure(scrollregion=my_canvas.bbox("all")))
  

    root = tk.Frame(my_canvas)
    my_canvas.create_window((0,0), window=root, anchor="nw")

    frame = tk.Frame(root)
    frame.bind('<Configure>', lambda e: my_canvas.configure(scrollregion=my_canvas.bbox("all")))  

    frame.pack()

    #==========================================Variable Selection=============================================#
    global parent_directory
    parent_directory = script_path
    global variables
    variables = {}

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
    

    independent_selection.grid(row=0, column=0)
    independent_index_selection.grid(row=0, column=1)

    dependent_selection.grid(row=0, column=0)
    dependent_index_selection.grid(row=0, column=1)

    def select_directory():
        global parent_directory
        parent_directory = Path(filedialog.askdirectory(title="Select Run Directory", initialdir=script_path))

        with open(Path(Path.joinpath(parent_directory, './structure.txt')), 'r') as struct_file:
            struct_file.readline()
            for line in struct_file.readlines():
                line = line.strip()
                arr = line.split(',')
                name = arr[2]
                num = arr[1]

                variables[name] = int(num)

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

        


    runs_directory_select = tk.Button(window, text="Select Data Directory", command=select_directory)
    runs_directory_select.pack(side=tk.TOP)



    tk.mainloop()

if __name__ == "__main__":
  main()