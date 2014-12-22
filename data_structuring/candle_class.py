class Candle:
    """ Class for candle information storing """
    def __init__(self, DateTime, Open, High, Low, Close, Volume):
        self.DateTime = DateTime
        self.Open = Open
        self.High = High
        self.Low = Low
        self.Close = Close
        self.Open = Open
   
    def getCO(self):
        """ Returns Close-Open """
        return self.Close-self.Open
        
    def getHL(self):
        """ Returns High-Low """
        return self.High-self.Low
        
    def getOL(self):
        """ Returns Open-Low """
        return self.Open-self.Low
        
    def getHO(self):
        """ Returns High-Open """
        return self.High-self.Open

def get_average_range(timeframe):
    range_sum = 0
    for unit in timeframe:
        range_sum += unit[1].getHL()
    return range_sum/len(timeframe)
