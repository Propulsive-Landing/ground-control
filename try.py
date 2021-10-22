import matplotlib.pyplot as plt

data_list = [0]

def update_list(input):
    data_list.append(input)



def printing_func(lst, new_input):
    graph = plt.axes()
    graph.scatter3D(0, 0, 0, color = 'b')
    update_list(float(new_input))
    fig, ax = plt.subplots()
    ax.plot = (1, lst[-1])
    plt.show()

printing_func(data_list, 7)