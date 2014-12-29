class TimeFrame(object):
    """ Representation of an ordered set of candles """
    def __init__(self, container=None, symbol=None, period=None):
        if container is None:
            container = []
        self.container = container
        self.symbol = str(symbol)
        self.period = str(period)

    def __str__(self):
        return str(self.container)

    def __repr__(self):
        return str(self.container)

    def __getitem__(self, key):
        return TimeFrame(self.container[key])

    def __len__(self):
        return len(self.container)

    def set_description(self, symbol=None, period=None):
        self.symbol = str(symbol)
        self.period = str(period)

    def append(self, candle):
        self.container.append(candle)

    def get_average_OC_range(self):
        """
        Returns average OC for whole set
        """
        import math
        range_sum = 0
        for unit in self.container:
            range_sum += math.fabs(unit.getCO())
        return range_sum/len(self)

    def get_average_HL_range(self):
        """
        Returns average HL for whole set
        """
        range_sum = 0
        for unit in self.container:
            range_sum += unit.getHL()
        return range_sum/len(self)

    
    def get_monthly_distribution(self):
        """
        Returns volatility(High-Low) distribution by days in list [MO, TU, WE, TH, FR]
        Warning: works only with monthly ticks!
        """
        m_vol = 12*[0]
        m_num = 12*[0]
        m_dist_vol = 12*[0]
        for elem in self.container:
            m_num[elem.DateTime.month-1] += 1
            m_vol[elem.DateTime.month-1] += elem.getHL()
        for i in range(12):
            if not m_num[i] == 0:
                m_dist_vol[i] = m_vol[i]/m_num[i]
        print(m_vol)
        print(m_num)
        return m_dist_vol        

    def get_weekdaily_distribution(self):
        """
        Returns volatility(High-Low) distribution by days in list [MO, TU, WE, TH, FR]
        Warning: works only with daily ticks!
        """
        day_vol = 7*[0]
        day_num = 7*[0]
        day_dist_vol = 7*[0]
        for elem in self.container:
            day_num[elem.DateTime.weekday()] += 1
            day_vol[elem.DateTime.weekday()] += elem.getHL()
        for i in range(7):
            if not day_num[i] == 0:
                day_dist_vol[i] = day_vol[i]/day_num[i]
        print(day_vol)
        print(day_num)
        return day_dist_vol

    def get_hourly_distribution(self):
        """
        Returns volatility(High-Low) distribution by days in list [0,1,2,3,...,23]
        Warning: works only with hourly ticks!
        """
        h_vol = 24*[0]
        h_num = 24*[0]
        h_dist_vol = 24*[0]
        for elem in self.container:
            h_num[elem.DateTime.hour] += 1
            h_vol[elem.DateTime.hour] += elem.getHL()
        for i in range(24):
            if not h_num[i] == 0:
                h_dist_vol[i] = h_vol[i]/h_num[i]
        return h_dist_vol

    def get_minutely_distribution(self):
        """
        Returns volatility(High-Low) distribution by minutes in list [0,1,2,3,...,59]
        Warning: works only with minutely ticks!
        """
        m_vol = 60*[0]
        m_num = 60*[0]
        m_dist_vol = 60*[0]
        for elem in self.container:
            m_num[elem.DateTime.minute] += 1
            m_vol[elem.DateTime.minute] += elem.getHL()
        for i in range(60):
            if not m_num[i] == 0:
                m_dist_vol[i] = m_vol[i]/m_num[i]
        return m_dist_vol

    def get_HL_hourly_distribution(self):
        """
        Works only with hour ticks
        Returns a list with 24 elements. Each element represent number of Lows/Highs for
        corresponding hour in a frame
        """
        hour_dist = 24*[0]
        min, max = 0, 0
        curr_day = self[0].container.DateTime.day
        for i in range(len(self.container)):
                if self[i].container.DateTime.day == curr_day:
                    if self[i].container.High > self[max].container.High:
                        max = i
                    if self[i].container.Low < self[max].container.Low:
                        min = i
                else:
                    hour_dist[self[min].container.DateTime.hour] += 1
                    hour_dist[self[max].container.DateTime.hour] += 1
                    curr_day = self[i].container.DateTime.day
                    min = i
                    max = i
        return hour_dist

    def get_avr_OC_HL_ratio(self):
        import math
        ratio_sum, num = 0, 0
        for element in self.container:
            if element.getHL() > 0:
                ratio_sum = math.fabs(element.getCO())/element.getHL()
                num += 1
        print(ratio_sum, num)
        if num == 0:
            res = 0
        else:
            res = ratio_sum/num
        return res

    def get_avr_OC_HL_dist(self):
        dist_sum, num = 0, 0
        for element in self.container:
            if element.getCO() > 0:
                dist_sum += element.getHC()
                dist_sum += element.getOL()
            else:
                dist_sum += element.getHO()
                dist_sum += element.getCL()
            num += 2
        if num == 0:
            res = 0
        else:
            res = dist_sum/num
        return res

    def get_O_list(self):
        res = []
        for element in self.container:
            res.append(element.Open)
        return res

    def get_H_list(self):
        res = []
        for element in self.container:
            res.append(element.High)
        return res

    def get_L_list(self):
        res = []
        for element in self.container:
            res.append(element.Low)
        return res

    def get_C_list(self):
        res = []
        for element in self.container:
            res.append(element.Close)
        return res

    def get_DT_list(self):
        res = []
        for element in self.container:
            res.append(element.DateTime)
        return res

    def is_in_frame(self, date):
        for element in self.container:
            if date == element.DateTime:
                return True
        else:
            return False

    def print_description(self):
        print("Timeframe data description")
        print("Symbol: " + self.symbol)
        print("Period: " + self.period)
        print("Length: " + str(len(self)))
        print("First-Last frame: " + str(self.container[0].DateTime) + " -- " +
              str(self.container[len(self.container)-1].DateTime))

def cut_by_OC_point(tf, threshold=None, param="e"):#e means exceeds
    import math
    if param == "e":
        sign = 1
    else:
        sign = -1
    if threshold==None:
        threshold = tf.get_average_OC_range()
    cut = TimeFrame()
    for element in tf.container:
        if math.fabs(element.getCO())*sign > threshold*sign:
            cut.append(element)
    return cut

def only_working_days(tf):
    wtf = TimeFrame()
    for element in tf.container:
        if element.DateTime.weekday() <= 4:
            wtf.append(element)
    return wtf

def cut_by_OC_range(tf, threshold1, threshold2):
    import math
    cut = TimeFrame()
    for element in tf.container:
        if threshold1 < math.fabs(element.getCO()) < threshold2:
            cut.append(element)
    return cut

def cut_by_HL_range(tf, threshold1, threshold2):
    cut = TimeFrame()
    for element in tf.container:
        if threshold1 < element.getHL() < threshold2:
            cut.append(element)
    return cut

def cut_by_datetime(tf, datetime_begin, datetime_end=None):
    import datetime
    if datetime_end is None:
        datetime_end = datetime.datetime.now()
    res = TimeFrame()
    for element in tf.container:
        if datetime_begin <= element.DateTime <= datetime_end:
            res.append(element)
    return res

