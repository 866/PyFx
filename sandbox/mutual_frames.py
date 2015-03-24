import processing.mathalgs as mt
import data_structuring.frame_class as fc
import data_aggregation.dbms as dbms
import data_aggregation.ticks_csv_parser as tcp
import datetime

audusd = tcp.parse_txt_stooq_daily("/home/victor/Desktop/data/daily/world/currencies\major/audusd.txt", 'audusd')
xauusd = tcp.parse_txt_stooq_daily("/home/victor/Desktop/data/daily/world/currencies\major/xauusd.txt", 'xauusd')

print(len(audusd))
print(len(xauusd))
mt1, mt2 = fc.mutual_time_frames(audusd, xauusd)
mt1.print_description()
mt2.print_description()
