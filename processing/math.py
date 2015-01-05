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

