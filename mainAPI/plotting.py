import numpy as np
from matplotlib import pyplot as plt
from matplotlib.finance import candlestick

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

def plot_chart(*tfs, norm=True, realtime=True):
    import matplotlib.dates as mdt
    fig, ax = plt.subplots()
    if len(tfs) == 1 and norm is True:
        y = [(mdt.date2num(candle.DateTime), candle.Open, candle.Close, candle.High, candle.Low) for candle in tfs[0].container]
        candlestick(ax, y, width=0.4, colorup='r', colordown='b')
        ax.xaxis_date()
        plt.title(tfs[0].symbol + " chart")
    else:
        for tf in tfs:
            if realtime is True:
                x = tf.get_Time_list()
            else:
                x = range(len(tf))
            y = np.array(tf.get_C_list())
            if norm is True:
                y -= y.min()
                y /= y.max()
            plt.plot(x, y, label=tf.symbol)
            plt.title("Charts graph")
    plt.legend(loc='upper center', shadow=True)
    plt.xlabel("Time")
    plt.ylabel("Price")
    plt.grid()
    plt.show()
