from pandas_datareader import data as pdr
import fix_yahoo_finance


with open ("etf_italy_codes.csv") as file:
    etf_list = file.readlines()
    for etf in etf_list:
        filename = etf.strip().replace(".","_") + ".csv"
        data = pdr.get_data_yahoo(etf.strip(), start="2016-01-01", end="2017-06-01")
        if len(data.index) > 200:
            data.to_csv("./stocks/" + filename)
            print (etf.strip())
            print (data.head())
