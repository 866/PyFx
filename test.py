import data.stooq_major_daily.load as load
import mainAPI.plotting as plot
import datetime as dt
import data_structuring.frame_class as fc
frag = fc.cut_by_datetime(db['eurusd'],dt.datetime(2010,2,1),dt.datetime(2010,2,15))
db = load.db_last_5years()
frag = fc.cut_by_datetime(db['eurusd'],dt.datetime(2010,2,1),dt.datetime(2010,2,9))
frag1 = fc.cut_by_datetime(db['eurusd'],dt.datetime(2010,12,3),dt.datetime(2010,12,17))
frag2 = fc.cut_by_datetime(db['eurusd'],dt.datetime(2009,1,26),dt.datetime(2009,2,10))
plot.plot_chart(frag, frag1, frag2)