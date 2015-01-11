"""
def main():
    coef_dict = {}
    for i in %len(coef_dict.keys()):
        coef_dict[%coef.dict.key] = coef_dict.value
    return coef_dict
"""

def correlation_data(file, func, coef_dict):
    """
    Writes data in python script that returns corr_coef_dict.
    :param file - path to file:
    :param corr_coef - correlation dictionary:
    :return: nothing
    """
    with open(file, 'a') as f:
        f.write("\n#Automatically generated script for correlation_dictionary\n\n\n")
        f.write("def "+func+"():\n\tcoef_dict = {}\n\t")
        for key, value in coef_dict.items():
            f.write("\tcoef_dict["+str(key)+"] = "+str(value)+"\n")
        f.write("\treturn coef_dict")


def database(file, func, db):
    """
    Writes data in python script that returns db.
    :param file - path to file:
    :param db - db dictionary:
    :return: nothing
    """
    with open(file, 'a') as f:
        f.write("\n\n\n#Automatically generated script for database\n\n\n")
        f.write("def "+func+"():\n\tdb = {}\n\t"
                            "import data_structuring.frame_class as fc\n\t"
                            "import data_structuring.candle_class as cc\n\t"
                            "import datetime\n\t")
        for key, value in db.items():
            f.write("candle_list = []\n\t")
            for candle in value.container:
                f.write("candle_list.append(cc.Candle(datetime.datetime(" +
                        str(candle.DateTime.year) + ", " +
                        str(candle.DateTime.month) + ", " +
                        str(candle.DateTime.day) + ", " +
                        str(candle.DateTime.hour) + ", " +
                        str(candle.DateTime.minute) + "), " +
                        str(candle.Open) + ", " +
                        str(candle.High) + ", " +
                        str(candle.Low) + ", " +
                        str(candle.Close) + ", " +
                        str(candle.Volume) + "))\n\t")
            f.write("db['" + str(key) + "'] = fc.TimeFrame(candle_list, symbol='" + str(value.symbol) +
                    "', period='" + str(value.period) + "')\n\t")
        f.write("return db")
