import data_aggregation.ticks_csv_parser as tcp
import data_structuring.frame_class as fc

def load_stooq_db(path, cut_dy_date=None):
    import glob
    if "daily" in path:
        read_func = tcp.parse_txt_stooq_daily
        period = "D"
    elif "hourly" in path:
        read_func = tcp.parse_txt_stooq_hourly
        period = "H"
    if not path[-1] == '/':
        path += "/"
    files = glob.glob(path+"*")
    res = {}
    for file in files:
        symbol = file.split("/")[len(file.split("/"))-1].split('.')[0]
        if cut_dy_date is None:
            res[symbol] = read_func(file, period=period, symbol=symbol)
        else:
            res[symbol] = fc.cut_by_datetime(read_func(file, period=period, symbol=symbol), cut_dy_date)
    return res
