import data_aggregation.ticks_csv_parser as tcp
import data_structuring.frame_class as fc
x = fc.only_working_days(tcp.parse_csv_metatrader("sandbox/EURUSD1400.csv"))
num_of_bars = 20
avr_range = x.get_average_range()
left_bound = 0
right_bound = avr_range*2
delta = (right_bound-left_bound)/num_of_bars
median = delta/2
res_list = []

while median < right_bound:
    res_list.append(fc.cut_by_OC_range(x, median-delta/2, median+delta/2).get_avr_OC_HL_ratio())
    median += delta