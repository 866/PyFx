import csv
import data_structuring.candle_class as candle_class
import data_structuring.frame_class as frame_class
from datetime import datetime

def parse_csv(filename):
    try:
        with open(filename) as csvfile:
            strings = csv.reader(csvfile,delimiter=',')
            frame = []
            timeset = set()
            for row in strings:
                # CSV format DD.MM.YYYY HH:MI:SS.MIC
                time = datetime(int(row[0][6:10]), #year
                                int(row[0][3:5]), #month
                                int(row[0][0:2]), #day
                                int(row[0][11:13]), #hour=0
                                int(row[0][14:16]), #minute=0
                                int(row[0][17:19]), #second=0
                                int(float(row[0][20:]))) #microsecond=0
                if time not in timeset:
                    candle = candle_class.Candle(time,float(row[1]),
                                            float(row[2]),
                                            float(row[3]),
                                            float(row[4]),
                                            float(row[5]))
                    timeset.add(time)
                    frame.append((time, candle))
            return frame_class.TimeFrame(frame)
    except IOError:
        print("Error opening file "+filename)
