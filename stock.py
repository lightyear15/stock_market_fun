import pandas
import datetime
import pandas_datareader as pdr
import fix_yahoo_finance
import os

PRICE_REFERENCE = "Close"
DEFAULT_ARCHIVE_FOLER = "./stocks/"

class Stock():
    def __init__(self,stock_name, data, start = None, end = None):
        self.name = stock_name
        self.data = data
        self.start = start
        self.end = end
    def get_name(self):
        return self.name
    def get_prices(self):
        mask = (self.data.index >= self.get_first_day()) & (self.data.index <= self.get_last_day())
        tmp = self.data[PRICE_REFERENCE].loc[mask]
        tmp.name = self.name
        tmp.index = pandas.to_datetime(tmp.index)
        return tmp
    def set_dates(self, start, end):
        self.start = start
        self.end = end
    def join(self, stock_obj):
        if stock_obj is None:
            return
        if (self.name is not stock_obj.name):
            raise Error("joining two different stocks")
        res = pandas.concat([self.data, stock_obj.data]).drop_duplicates().sort_index()
        self.data = res
    def get_first_day(self):
        if self.start is None:
            self.start = self.data.index[0]
        return self.start
    def get_last_day(self):
        if self.end is None:
            self.end = self.data.index[-1]
        return self.end

def download_data(stock_name, start, end):
    try:
        temp = pdr.get_data_yahoo(stock_name, start, end)
        temp.fillna(method="ffill", inplace=True)
        stock = Stock(stock_name, temp, start, end)
        return stock
    except Exception as e:
        print (e)
        return None

def get_stock_data(stock_name_list, start, end, archive_path = DEFAULT_ARCHIVE_FOLER):
    stock_list = []
    for stock_name in stock_name_list:
        stock = None
        start_date = start
        end_date= end
        stock_fname = get_fname_from_stock(stock_name)
        stock_abs_fname = os.path.expanduser(os.path.join(archive_path, stock_fname))
        if os.path.exists(stock_abs_fname):
            stock = Stock(stock_name, pandas.DataFrame.from_csv(stock_abs_fname))
            if stock.get_first_day() < start:
                start_date = stock.get_last_day()
            if stock.get_last_day() > end:
                end_date = stock.get_first_day()
            stock.set_dates(start, end)
        new_data = None
        if start_date < end_date:
            new_data = download_data (stock_name, start_date, end_date)
        if stock and new_data:
            stock.join(new_data)
        elif new_data:
            stock = new_data
        if stock and len(stock.data.index) > 0:
            stock_list.append(stock)
            stock.data.to_csv(stock_abs_fname)
    return stock_list

def get_rr_from_stock_list(stocks):
    prices = pandas.DataFrame()
    start = stocks[0].get_first_day()
    end = stocks[0].get_last_day()
    prices[stocks[0].get_name()] = stocks[0].get_prices()
    for stock in stocks:
        if stock.get_first_day() != start and stock.get_last_day() != end:
            raise Error ("Dates do not match")
        prices[stock.get_name()] = stock.get_prices()
    prices.fillna(method="ffill", inplace=True)
    prices_i = prices.iloc[:-1]
    prices_i_1 = prices.iloc[1:]
    rr = np.divide(prices_i_1.as_matrix() - prices_i.as_matrix(), prices_i.as_matrix()) * 100
    rate_of_returns = pandas.DataFrame(rr)
    rate_of_returns.columns = prices.columns.values
    rate_of_returns.set_index(prices_i_1.index, inplace=True)
    return rate_of_returns

def get_fname_from_stock(stock_name):
    return stock_name + ".csv"
