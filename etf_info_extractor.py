import pandas
from BeautifulSoup import BeautifulSoup as BS
import urllib2
import datetime

WEBSITE = "http://www.borsaitaliana.it"
PAGES = range(1,39)
COLUMNS = ["Codice Alfanumerico", "Codice Isin", "Reuters Ric Strumento", "Bloomberg Ticker Strumento", "iNAV - Bloomberg Ticker", "Prezzo di riferimento"]

def extract_etf_data( max_etfs=-1):
    etfs = {}
    for page in PAGES:
        html = urllib2.urlopen( WEBSITE + "/borsa/etf.html?&page=" + str(page))
        soup = BS(html)
        for row in soup.findAll("table")[0].tbody.findAll("tr"):
            link = row.findAll("a")[1]["href"]
            final_link = WEBSITE + link
            link_html = urllib2.urlopen( final_link)
            etf_soup = BS(link_html)
            etf_name = etf_soup.find("h1").find("a").contents[0]
            etf_data = {}
            for table in etf_soup.findAll("table"):
                for row in table.findAll("tr"):
                    key = None
                    for cell in row.findAll("td"):
                        if key:
                            code = extract_info_from_cell(key, str(cell))
                            etf_data[key] = code
                            key = None
                        for elem in COLUMNS:
                            if elem in str(cell):
                                key = elem
            etfs[etf_name] = etf_data
            if max_etfs > 0 and len(etfs) >= max_etfs:
                break;
        if max_etfs > 0 and len(etfs) >= max_etfs:
            break;
    etf_dataframe = pandas.DataFrame.from_dict(etfs, orient="index")
    etf_dataframe.index.name = "etf"
    return etf_dataframe

def extract_info_from_cell(key, content):
    code = str(content).split("<span class=\"t-text -right\">")[1].split("</span>")[0].strip()
    if key == "Prezzo di riferimento":
            price = code.split("-")[0].strip()
            date = code.split("-")[1].strip()
            price = float(price.replace(",", "."))
            date = datetime.datetime.strptime(date, "%d/%m/%y")
            code = (date, price)
    return code
