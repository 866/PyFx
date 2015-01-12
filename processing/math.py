import numpy as np
import data_structuring.frame_class as fc
import mainAPI.print as prt


def find_correlation_by_C(tf1, tf2, shift=0): #shift is the shift of the tf1
    tf1, tf2 = fc.mutual_time_frames(tf1, tf2)
    if not (len(tf1) == 0 or len(tf2) == 0):
        if shift == 0:
            return np.corrcoef(tf1.get_C_list(), tf2.get_C_list())[0][1]
        else:
            return np.corrcoef(tf1.get_C_list()[shift:], tf2.get_C_list()[:-shift])[0][1]
    else:
        return None


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
