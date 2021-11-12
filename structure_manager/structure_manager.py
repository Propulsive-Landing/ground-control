import tkinter as tk
import os
from pathlib import Path

root = tk.Tk()
root.title("Structure Initialization")
root.geometry("400x400")

frame = tk.Frame(root)
frame.pack()

script_path = Path(os.path.realpath(__file__)).parent
structure_path = Path("./data/structure.txt")
structure_string_path = Path("./data/struct_string.txt")

structure_path = os.path.join(script_path, structure_path)
structure_string_path = os.path.join(script_path, structure_string_path)

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

ordering = tk.StringVar()
ordering.set(list(ordering_options.keys())[0])
ordering_selection = tk.OptionMenu(frame, ordering, *(ordering_options.keys()))
ordering_selection.pack()


types = []
numbers = []

def add_section():
  add_value(list(options.keys())[0], 1)

def add_value(input_type, input_number):
  row = tk.Frame(frame)
  
  selected = tk.StringVar()
  types.append(selected)
  selected.set(input_type)
  input1 = tk.OptionMenu(row, selected, *(options.keys()))
  input1.grid(row=0, column=0)
  
  number = tk.StringVar()
  number.set(input_number)
  input2 = tk.Entry(row, textvariable=number)
  input2.grid(row=0, column=1)
  numbers.append(number)
  
  row.pack()

add_button = tk.Button(root, text="Add Type", command=add_section)
add_button.pack()


def update_from_file():
  try:
    with open(structure_path, 'r') as file:
      firstLine = file.readline()[:-1]
      ordering.set(firstLine)
      for line in file:
        line = line[:-1]
        arr = line.split(',')
        add_value(arr[0], arr[1])
  except OSError as e:
    print(e)

update_from_file()


tk.mainloop()

#This runs once window is closed
def save_frame():
  file = open(structure_path, "w")
  file.write(ordering.get() + "\n")
  for i in range(0, len(numbers)):
    file.write(types[i].get() + "," + numbers[i].get() + "\n")
  file.close()

def generate_string_file():
  try:
    with open(structure_path, 'r') as structure_file, open(structure_string_path, 'w') as string_struct_file:
      string_struct_file.write(ordering_options[structure_file.readline()[:-1]])
      for line in structure_file:
        line = line[:-1]
        arr = line.split(',')
        string_struct_file.write(arr[1] + options.get(arr[0]))
  except OSError as e:
    print(e)

save_frame()
generate_string_file()