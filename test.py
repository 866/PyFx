import data.stooq_major_daily.load as load
import mainAPI.plotting as plot
import datetime as dt
import processing.mathalgs as mt
import data_structuring.frame_class as fc
symbol = 'gbpusd'
db = load.db_last_year()
frag = fc.cut_by_datetime(db['eurusd'], dt.datetime(2014,5,6),dt.datetime(2014,5,8))
x = mt.find_pattern_profitability(frag, db[symbol], 8, 0.86)
print("Total Profit/Num: ",sum(x.values()), len(x))
print("Ratio: ",sum(x.values())/len(x))
print("Max/Min: ",max(x.values()), min(x.values()))
mt.print_current_situation_daily(db)
