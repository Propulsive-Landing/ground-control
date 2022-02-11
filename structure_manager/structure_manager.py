import tkinter as tk
from tkinter import ttk

import os
from pathlib import Path


class TypeManager():
  options = {
    "pad byte": "x",
    "char (1B)": "c", 
    "signed char (1B)": "b",
    "unsigned char (1B)": "B",
    "_Bool (1B)": "?",
    "short (2B)": "h",
    "unsigned short (2B)": "H",
    "int (4B)": "i",
    "unsigned int (4B)": "I",
    "long (4B)": "l",
    "unsigned long (4B)": "L",
    "long long (8B)": "q",
    "unsigned long long (8B)": "Q",
    "ssize_t": "n",
    "size_t": "N",
    "float (4B)": "f",
    "double (8B)": "d",
    "char[]": "s",
    "char[] Pascal String": "p",
    "void *": "P"
  } 
  ordering_options = {
    "native byte order, size, and alignment": "@",
    "native byte order, standard size, no alignment": "=",
    "Little endian, standard size, no alignment": "<",
    "Big endian, standard size, no alignment": ">",
    "network byteorder, standard size, no alignment": "!"
  }


  def __init__(self, frame, ordering, types, numbers, names):
    self.frame = frame
    self.ordering = ordering
    self.types = types
    self.numbers = numbers
    self.names = names
  
    self.rows = []

    self.script_path = Path(os.path.realpath(__file__)).parent
    self.structure_path = Path("./data/structure.txt")
    self.structure_string_path = Path("./data/struct_string.txt")

    self.structure_path = os.path.join(self.script_path, self.structure_path)
    self.structure_string_path = os.path.join(self.script_path, self.structure_string_path)



  def add_value(self, input_type, input_number, input_name):
    row = tk.Frame(self.frame)
  
    self.rows.append(row)

    selected = tk.StringVar()
    self.types.append(selected)
    selected.set(input_type)
    input1 = tk.OptionMenu(row, selected, *(self.options.keys()))
    input1.grid(row=0, column=0)
  
    number = tk.StringVar()
    number.set(input_number)
    input2 = tk.Entry(row, width=8, textvariable=number)
    input2.grid(row=0, column=1)
    self.numbers.append(number)

    
    name = tk.StringVar()
    name.set(input_name)
    input3 = tk.Entry(row, textvariable=name)
    input3.grid(row=0, column=2)
    self.names.append(name)
  
    row.pack()

  def remove_last_value(self):
    self.names.pop(len(self.names)-1)
    self.types.pop(len(self.types)-1)
    self.numbers.pop(len(self.numbers)-1)

    self.rows[-1].destroy()

  def add_section(self):
    self.add_value(list(self.options.keys())[0], 1, "")


  def update_from_file(self):
    try:
      with open(self.structure_path, 'r') as file:
        firstLine = file.readline()[:-1]
        self.ordering.set(firstLine)
        for line in file:
          line = line[:-1]
          arr = line.split(',')
          self.add_value(arr[0], arr[1], arr[2])
    except OSError as e:
      print(e)


  #This runs once window is closed
  def save_frame(self):
    for i in range(0, len(self.numbers)):
      if(not self.numbers[i].get().isnumeric()):
        return

    file = open(self.structure_path, "w")
    file.write(self.ordering.get() + "\n")
    for i in range(0, len(self.numbers)):
      file.write(self.types[i].get() + "," + self.numbers[i].get() + "," + self.names[i].get() + "\n")
    file.close()

  def generate_string_file(self):
    try:
      with open(self.structure_path, 'r') as structure_file, open(self.structure_string_path, 'w') as string_struct_file:
        string_struct_file.write(self.ordering_options[structure_file.readline()[:-1]])
        for line in structure_file:
          line = line[:-1]
          arr = line.split(',')
          if(not arr[1] == "1"):
            string_struct_file.write(arr[1])
          
          string_struct_file.write(self.options.get(arr[0]))
    except OSError as e:
      print(e)


def main():
  window = tk.Tk()
  window.title("Structure Initialization")
  window.geometry("400x600")

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

  ordering = tk.StringVar()
  types = []
  numbers = []
  names = []

  typeManager = TypeManager(frame, ordering, types, numbers, names)

  ordering.set(list(TypeManager.ordering_options.keys())[0])
  ordering_selection = tk.OptionMenu(frame, ordering, *(TypeManager.ordering_options.keys()))
  ordering_selection.pack()

  label_row = tk.Frame(frame)
  column_labels = tk.Label(label_row, text="Type  |  Number  |  Name", justify='center')
  column_labels.pack()
  label_row.pack()
  

  
  add_button = tk.Button(root, text="Add Type", command=typeManager.add_section)
  add_button.pack()

  remove_button = tk.Button(root, text="Remove Last", command=typeManager.remove_last_value)
  remove_button.pack()


  
  typeManager.update_from_file()

  tk.mainloop()
  
  typeManager.save_frame()
  typeManager.generate_string_file()

if __name__ == "__main__":
  main()