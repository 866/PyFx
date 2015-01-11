import data_aggregation.ticks_csv_parser as tcp
import data_structuring.frame_class as fc

def load_stooq_db(path, cut_dy_date=None):
    import mainAPI.print as prt
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
    div = len(files)
    progress = 0
    div = len(files)/100
    for file in files:
        progress += 1
        if 'txt' in file:
            prt.print_progress(progress/div)
            symbol = file.split("/")[len(file.split("/"))-1].split('.')[0]
            if cut_dy_date is None:
                res[symbol] = read_func(file, period=period, symbol=symbol)
            else:
                res[symbol] = fc.cut_by_datetime(read_func(file, period=period, symbol=symbol), cut_dy_date)
    prt.print_progress(100)
    print("\nParsing is finished")
    return res