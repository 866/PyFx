import csv
import data_structuring.candle_class as candle_class
import data_structuring.frame_class as frame_class
from datetime import datetime

def parse_csv_dukascopy(filename):
    try:
        with open(filename) as csvfile:
            strings = csv.reader(csvfile, delimiter=',')
            frame = []
            timeset = set()
            for row in strings:
                # CSV format DD.MM.YYYY HH:MI:SS.MIC
                time = datetime.strptime(row[0], "%d.%m.%Y %H:%M:%S.%f")
                if time not in timeset:
                    candle = candle_class.Candle(time,
                                            float(row[1]),
                                            float(row[2]),
                                            float(row[3]),
                                            float(row[4]),
                                            float(row[5]))
                    timeset.add(time)
                    frame.append(candle)
            return frame_class.TimeFrame(frame)
    except IOError:
        print("Error opening file "+filename)


def parse_csv_yahoo(filename):
    try:
        with open(filename) as csvfile:
            strings = csv.reader(csvfile, delimiter=',')
            frame = []
            timeset = set()
            for row in strings:
                # CSV format YYYY-MM-DD
                time = datetime.strptime(row[0], "%Y-%m-%d")
                if time not in timeset:
                    candle = candle_class.Candle(time,
                                            float(row[1]),
                                            float(row[2]),
                                            float(row[3]),
                                            float(row[4]),
                                            float(row[5]))
                    timeset.add(time)
                    frame.append(candle)
            return frame_class.TimeFrame(frame)
    except IOError:
        print("Error opening file "+filename)

def parse_csv_metatrader(filename):
    try:
        with open(filename) as csvfile:
            strings = csv.reader(csvfile, delimiter=',')
            frame = []
            timeset = set()
            for row in strings:
                # CSV format YYYY-MM-DD
                time = datetime.strptime(row[0]+row[1], "%Y.%m.%d%H:%M")
                if time not in timeset:
                    candle = candle_class.Candle(time,
                                            float(row[2]),
                                            float(row[3]),
                                            float(row[4]),
                                            float(row[5]),
                                            float(row[6]))
                    timeset.add(time)
                    frame.append(candle)
            return frame_class.TimeFrame(frame)
    except IOError:
        print("Error opening file "+filename)

def parse_txt_stooq_daily(filename, period=None, symbol=None):
    try:
        with open(filename) as csvfile:
            strings = csv.reader(csvfile, delimiter=',')
            frame = []
            timeset = set()
            next(strings)
            for row in strings:
                # CSV format YYYY-MM-DD
                time = datetime.strptime(row[0], "%Y%m%d")
                if time not in timeset:
                    candle = candle_class.Candle(time,
                                                 float(row[1]),
                                                 float(row[2]),
                                                 float(row[3]),
                                                 float(row[4]),
                                                 float(row[5]))
                    timeset.add(time)
                    frame.append(candle)
            return frame_class.TimeFrame(frame, symbol=symbol, period=period)
    except IOError:
        print("Error opening file "+filename)

def parse_txt_stooq_hourly(filename, period=None, symbol=None):
    try:
        with open(filename) as csvfile:
            strings = csv.reader(csvfile, delimiter=',')
            frame = []
            timeset = set()
            next(strings)
            for row in strings:
                # CSV format YYYY-MM-DD
                time = datetime.strptime(row[0]+row[1], "%Y-%m-%d%H:%M:%S")
                if time not in timeset:
                    candle = candle_class.Candle(time,
                                                 float(row[2]),
                                                 float(row[3]),
                                                 float(row[4]),
                                                 float(row[5]),
                                                 float(row[6]))
                    timeset.add(time)
                    frame.append(candle)
            return frame_class.TimeFrame(frame, symbol=symbol, period=period)
    except IOError:
        print("Error opening file "+filename)

def download_from_yahoo_to_file(stock, filename):
    import urllib.request
    import time
    try:
        print('Currently Pulling', stock)
        print(str(datetime.fromtimestamp(int(time.time())).strftime('%Y-%m-%d %H:%M:%S')))
        #Keep in mind this is close high low open data from Yahoo
        urlToVisit = 'http://chartapi.finance.yahoo.com/instrument/1.0/'+stock+'/chartdata;type=quote;range=10y/csv'
        try:
            sourceCode = urllib.request.urlopen(urlToVisit).read().decode("utf-8")
            try:
                with open(filename, 'w') as f:
                    f.write(sourceCode)
            except IOError as e:
                print("Error writing file: " + str(e))
        except Exception as e:
            print(str(e), 'failed to organize pulled data.')
    except Exception as e:
        print(str(e), 'failed to pull pricing data')

#daily http://stooq.com/db/d/?b=d_world_txt
#hourly http://stooq.com/db/d/?b=h_world_txt
def download_from_stooq(url_to_visit, path):
    import urllib.request
    import datetime
    import time
    import os
    filename = "tmp.zip"
    try:
        success = False
        print(str(datetime.datetime.fromtimestamp(int(time.time())).strftime('%Y-%m-%d %H:%M:%S')) +
              " Currently pulling stooq")
        #Keep in mind this is close high low open data from Yahoo
        urlToVisit = 'http://stooq.com/db/d/?b=d_world_ms'
        try:
            file = urllib.request.urlopen(url_to_visit).read()
            try:
                with open(filename, 'wb') as f:
                    f.write(file)
                    success = True
            except IOError as e:
                print("Error writing file: " + str(e))
        except Exception as e:
            print(str(e), 'failed to organize pulled data.')
    except Exception as e:
        print(str(e), 'failed to pull pricing data')
    if success is True:
        print(str(datetime.datetime.fromtimestamp(int(time.time())).strftime('%Y-%m-%d %H:%M:%S ')) + url_to_visit + " had been downloaded successfully. Unzipping...")
        os.system("unzip -xoq "+filename+" -d "+path)
        os.system("rm "+filename)
        print(str(datetime.datetime.fromtimestamp(int(time.time())).strftime('%Y-%m-%d %H:%M:%S ')) + "Finished")