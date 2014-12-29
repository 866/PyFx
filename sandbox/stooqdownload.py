#daily http://stooq.com/db/d/?b=d_world_ms
#minutely http://stooq.com/db/d/?b=h_world_ms
import urllib.request
import datetime
import time
import os
filename = "tmp.zip"
try:
    success = False
    print(str(datetime.datetime.fromtimestamp(int(time.time())).strftime('%Y-%m-%d %H:%M:%S')) +
          "currently Pulling stooq")
    #Keep in mind this is close high low open data from Yahoo
    urlToVisit = 'http://stooq.com/db/d/?b=d_world_ms'
    try:
        file = urllib.request.urlopen(urlToVisit).read()
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
    print(str(datetime.datetime.fromtimestamp(int(time.time())).strftime('%Y-%m-%d %H:%M:%S')))
    print(filename + " had been downloaded successfully. Unzipping...")
    os.system("unzip -xoq "+filename)
    os.system("rm "+filename)
    os.system("Finished")