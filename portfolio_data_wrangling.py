from stock import *
from etf_info_extractor import *
import datetime

etf_info = extract_etf_data(50)


for idx in etf_info.index:
    print idx
    etf = etf_info.loc[idx]
    ref_date = etf["Prezzo di riferimento"][0]
    ref_price = etf["Prezzo di riferimento"][1]
    print idx, etf["Codice Alfanumerico"], ref_date, ref_price
    stocks = get_stock_data([etf["Codice Alfanumerico"]], datetime.datetime(2017,5,1),ref_date + datetime.timedelta(days=2))
    if len(stocks) > 0:
        try:
            price = stocks[0].get_prices().loc[etf["Prezzo di riferimento"][0].date()]
            print str(ref_price) + " ?= " + str(price)
        except Exception as e:
            print "etf not corresponding"
            print str(ref_date) + " != \n" + str(stocks[0].get_prices())

#stock_list = get_stock_data(etf_codes, datetime.datetime(2017,1,1), datetime.datetime(2017,2,1))

# etfs = load_etf_name_list()
# etfs_name = etfs["Symbol"]
# etfs_list = etfs_name.tolist()

# stock_list = get_stock_data(etfs_list, datetime.datetime(2016,1,1), datetime.datetime(2016,6,1))

# found = []
# for stock in stock_list:
    # found.append(stock.get_name())

# with open("test.txt", "wb") as fp:
    # pickle.dump(found, fp)

# with open('test.txt', 'rb') as handle:
        # found = pickle.load(handle)

# print found

# stock_list = get_stock_data(["AMZN", "GOOG"], datetime.datetime(2016,1,1), datetime.datetime(2016,12,31))
# stock_list = get_stock_data(["EPA:EBBB"], datetime.datetime(2016,1,1), datetime.datetime(2016,12,31))

# rr = get_rr_from_stock_list(stock_list)

