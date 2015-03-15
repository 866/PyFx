import numpy as np
import data_structuring.frame_class as fc
import mainAPI.print as prt


def find_correlation_by_C(tf1, tf2, shift=0): #shift is the shift of tf1
    tf1, tf2 = fc.mutual_time_frames(tf1, tf2)
    if not (len(tf1) == 0 or len(tf2) == 0):
        if shift == 0:
            return np.corrcoef(tf1.get_C_list(), tf2.get_C_list())[0][1]
        else:
            return np.corrcoef(tf1.get_C_list()[shift:], tf2.get_C_list()[:-shift])[0][1]
    else:
        return None

def find_correlation_by_OHLC(tf1, tf2, shift=0): #shift is the shift of tf1
    tf1, tf2 = fc.mutual_time_frames(tf1, tf2)
    if not (len(tf1) == 0 or len(tf2) == 0):
        if shift == 0:
            tf1_list = tf1.get_O_list()+tf1.get_H_list()+tf1.get_L_list()+tf1.get_C_list()
            tf2_list = tf2.get_O_list()+tf2.get_H_list()+tf2.get_L_list()+tf2.get_C_list()
        else:
            tf1_list = tf1.get_O_list()[shift:]+tf1.get_H_list()[shift:]+tf1.get_L_list()[shift:]+tf1.get_C_list()[shift:]
            tf2_list = tf2.get_O_list()[:-shift]+tf2.get_H_list()[:-shift]+tf2.get_L_list()[:-shift]+tf2.get_C_list()[:-shift]
        return np.corrcoef(tf1_list, tf2_list)[0][1]
    else:
        return None

def find_fragment_in_tf_by_C(fragment, tf, threshold = 0.9):
    res = {}
    fragc = fragment.get_C_list()
    framec = tf.get_C_list()
    len_frag, len_frame = len(fragc), len(framec)
    if len_frame<len_frag:
        res = None
    else:
        for i in range(len_frame-len_frag):
            corr_coef = np.corrcoef(fragc, framec[i:i+len_frag])[0][1]
            if corr_coef >= threshold:
                res[tf.container[i].DateTime] = corr_coef
    return res

def find_fragment_in_tf_by_OHLC(fragment, tf, threshold = 0.9):
    res = {}
    fragc, framec = [], []
    for i in range(len(fragment)):
        fragc.append(fragment.container[i].Open)
        fragc.append(fragment.container[i].High)
        fragc.append(fragment.container[i].Low)
        fragc.append(fragment.container[i].Close)
    for i in range(len(tf)):
        framec.append(tf.container[i].Open)
        framec.append(tf.container[i].High)
        framec.append(tf.container[i].Low)
        framec.append(tf.container[i].Close)
    len_frag, len_frame = len(fragc), len(framec)
    if len_frame < len_frag:
        res = None
    else:
        for i in range(int((len_frame-len_frag)/4)):
            corr_coef = np.corrcoef(fragc, framec[i*4:i*4+len_frag])[0][1]
            if corr_coef >= threshold:
                res[tf.container[i].DateTime] = corr_coef
    return res

def find_pattern_profitability(fragment, tf, days, threshold=0.9):
    res = {}
    found = find_fragment_in_tf_by_OHLC(fragment, tf, threshold)
    for date in found.keys():
        dummy, itr = tf.is_in_frame(date)
        try:
            for i in range(len(fragment)-1):
                next(itr)
            open_price = next(itr).Open
            for i in range(days-1):
                candle = next(itr)
            close_price = next(itr).Open
            res[date] = close_price-open_price
        except StopIteration:
            pass
    return res

def find_correlation_dict_by_C(db, shift=0):
    corr_dict = {}
    progress = 0
    prt.print_progress(progress)
    div = len(db.keys())*(len(db.keys())-1)/200
    for pair1 in db.keys():
        for pair2 in db.keys():
            if (pair2 is not pair1) and ((pair2, pair1) not in corr_dict):
                corr_dict[(pair1, pair2)] = find_correlation_by_C(db[pair1], db[pair2], shift)
                progress += 1
                prt.print_progress(progress/div)
    prt.print_progress(100)
    print("\nCalculating is finished")
    return corr_dict

def find_best_corr_in_dict(corr_dict, threshold=0.95):
    best_corr_dict = {}
    for key, value in corr_dict.items():
        if value > threshold or value < -threshold:
            best_corr_dict[key] = value
    return best_corr_dict

def print_current_situation_daily(db):
    import data_aggregation.fetch as fetch
    import math
    print("Pair       Avr_OC        Curr_OC        Ratio        Probability")
    for key, item in db.items():
        open_price, current_price = fetch.symbol_price(str(key))
        if open_price is not 0:
            oc_avr = item.get_average_OC_range()
            oc_today = math.fabs(current_price-open_price)
            prob = len(fc.cut_by_OC_point(item, oc_today)) / len(item)
            if prob < .2:
                prob_str = "\033[91m{0:.2f}".format(prob)+"\033[0m"
            elif prob > .8:
                prob_str = "\033[92m{0:.2f}".format(prob)+"\033[0m"
            else:
                prob_str = "{0:.2f}".format(prob)
            print(str(key)+("     {0:f}      {1:f}       {2:f}     "+prob_str).format(oc_avr, oc_today, oc_today/oc_avr))

def print_current_situation_to_current_hour(db): #TODO: check it
    import data_aggregation.fetch as fetch
    import math
    import datetime
    print("Current hour is " + str(datetime.datetime.now().hour))
    print("Pair       Avr_OC        Curr_OC        Ratio        Probability")
    for key, item in db.items():
        open_price, current_price = fetch.symbol_price(str(key))
        if open_price is not 0:
            hour_dist = item.get_hourly_distribution()
            oc_avr = 0
            for hour in range(datetime.datetime.now().hour):
                oc_avr += hour_dist[hour]
            oc_today = math.fabs(current_price-open_price)
            print(str(key)+("     {0:f}      {1:f}       {2:f}     ").format(oc_avr, oc_today, oc_today/oc_avr))
