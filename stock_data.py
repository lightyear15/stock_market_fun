import pandas
from BeautifulSoup import BeautifulSoup as BS
import urllib2


etfs = {}
WEBSITE = "http://www.borsaitaliana.it"
PAGES = range(31,39)
COLUMNS = ["Codice Alfanumerico", "Codice Isin", "Reuters Ric Strumento", "Bloomberg Ticker Strumento", "iNAV - Bloomberg Ticker"]
for page in PAGES:
    print "analysing page " + str(page)
    html = urllib2.urlopen( WEBSITE + "/borsa/etf.html?&page=" + str(page))
    soup = BS(html)
    for row in soup.findAll("table")[0].tbody.findAll("tr"):
        link = row.findAll("a")[1]["href"]
        final_link = WEBSITE + link
        link_html = urllib2.urlopen( final_link)
        etf_soup = BS(link_html)
        etf_name = etf_soup.find("h1").find("a").contents[0]
        print "retrieving data for " + etf_name
        etf_data = {}
        for table in etf_soup.findAll("table"):
            for row in table.findAll("tr"):
                key = None
                for cell in row.findAll("td"):
                    if key:
                        code = str(cell).split("<span class=\"t-text -right\">")[1].split("</span>")[0].strip()
                        etf_data[key] = code
                        key = None
                    for elem in COLUMNS:
                        if elem in str(cell):
                            key = elem
        etfs[etf_name] = etf_data
etf_dataframe = pandas.DataFrame.from_dict(etfs, orient="index")
etf_dataframe.index.name = "etf"
print etf_dataframe.shape
print etf_dataframe
etf_dataframe.to_csv("etf_italy_3.csv")
