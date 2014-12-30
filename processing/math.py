import numpy as np
import data_structuring.frame_class as fc

def find_correlation_by_C(tf1, tf2):
    tf1, tf2 = fc.mutual_time_frames(tf1, tf2)
    if not (len(tf1) == 0 or len(tf2) == 0):
        return np.corrcoef(tf1.get_C_list(), tf2.get_C_list())[0][1]
    else:
        return None