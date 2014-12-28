import numpy as np
from matplotlib import pyplot as plt


def plot_distribution(dist_list, x_axis=None):
    if x_axis is None:
        x_axis = range(len(dist_list))
    fig = plt.figure()
    width = 0.35
    ind = np.arange(len(dist_list))
    plt.bar(ind, dist_list)
    plt.xticks(ind + width / 2, x_axis)
    plt.grid()
    fig.autofmt_xdate()
    plt.show()