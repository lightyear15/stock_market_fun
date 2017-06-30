from pandas_datareader import data as pdr
import fix_yahoo_finance


with open ("etf_italy_codes.csv") as file:
    etf_list = file.readlines()
    for etf in etf_list:
        print (etf.strip())
        filename = etf.strip().replace(".","_") + ".csv"
        data = pdr.get_data_yahoo(etf.strip(), start="2012-01-01", end="2017-06-01")
        print (data.head())
        data.to_csv("./stocks/" + filename)
