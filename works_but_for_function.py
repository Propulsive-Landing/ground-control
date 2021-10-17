import matplotlib.pyplot as plt
import matplotlib.animation as anim

def plot_cont(xmax):
    y = []
    fig = plt.figure()
    ax = fig.add_subplot(1,1,1)

    def update(i):
        while i < 30:
            yi = i
            y.append(yi)
            x = range(len(y))
            ax.clear()
            ax.plot(x, y)
            i += 1

    a = anim.FuncAnimation(fig, update, frames=xmax, repeat=False)
    plt.show()

plot_cont(30)