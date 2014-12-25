import numpy as np
from matplotlib import pyplot as plt
import data_aggregation.ticks_csv_parser as tcp
import data_structuring.frame_class as fc

x = fc.only_working_days(tcp.parse_csv_dukascopy("EURUSD_H.csv"))
#OY = np.array(fc.cut_by_OC_param(x).get_HL_distribution())
OY = np.array(x.get_HL_distribution())
print(OY)
OX = range(len(OY))
fig = plt.figure()

width = 0.35
ind = np.arange(len(OY))
print(OY)
plt.bar(ind, OY)
plt.xticks(ind + width / 2, OX)
plt.grid()
fig.autofmt_xdate()

plt.show()

