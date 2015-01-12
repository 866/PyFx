def symbol_price(symbol):
    """
    returns symbols Open(day), Bid price from yahoo
    """
    import re
    import requests
    try:
        page = requests.get('http://finance.yahoo.com/q?s='+symbol+'=X')
        open_price = float(re.search('Open:</th><td class="yfnc_tabledata1">(.*)</td></tr><tr>', page.text).group(1))
        bid_price = float(re.search('<span class="time_rtq_ticker"><span id="(.*)">(.*)</span></span> <span class="(.*) time_rtq_content">', page.text).group(2))
    except Exception as e:
        print("Can not fetch " + symbol + " data. Exception"+str(e))
        open_price = 0
        bid_price = 0
    return open_price, bid_price