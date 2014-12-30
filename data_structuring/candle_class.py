class Candle:
    """ Class for candle information storing """
    def __init__(self, DateTime, Open, High, Low, Close, Volume):
        self.DateTime = DateTime
        self.Open = Open
        self.High = High
        self.Low = Low
        self.Close = Close
        self.Volume = Volume

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

    def getCL(self):
        """ Returns Close-Low """
        return self.Close-self.Low

    def getHC(self):
        """ Returns High-Close """
        return self.High-self.Close

    def print_description(self):
        """ Prints candle properties """
        print("\tDatetime: " + str(self.DateTime) +
            "\n\tOpen: " + str(self.Open) +
            "\n\tHigh: " + str(self.High) +
            "\n\tLow: " + str(self.Low) +
            "\n\tClose: " + str(self.Close) +
            "\n\tVolume: " + str(self.Volume))