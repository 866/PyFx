import data_aggregation.ticks_csv_parser as tcp
import data_structuring.frame_class as fc
from mainAPI.plotting import plot_distribution
import math

x = fc.only_working_days(tcp.parse_csv_metatrader("EURUSD1440.csv"))
num_of_bars = 30
avr_range = x.get_average_HL_range()
left_bound = 0
right_bound = avr_range*3
delta = (right_bound-left_bound)/num_of_bars
median = delta/2
res_list = []
res_list_x = []

while median < right_bound:
    res_list.append(len(fc.cut_by_HL_range(x, median-delta/2, median+delta/2)))
    res_list_x.append(math.ceil((median-delta/2)*10000))
    median += delta

print(res_list_x)
print("Average range: ", avr_range)
print("Delta: ", delta)
print("Left bound: " + str(left_bound) + " Right bound: " + str(right_bound))
print("Distribution",  res_list)

plot_distribution(res_list, res_list_x)
plot_distribution(x.get_weekdaily_distribution())