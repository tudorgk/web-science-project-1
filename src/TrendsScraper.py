import urllib
from selenium import webdriver

class TrendsScraper:
    def __init__(self, search_words = None):
        self.search_words = search_words
        self.baseURL = "http://www.google.com/trends/trendsReport?q="
        self.tailURL = "&date=01/2011%2062m&geo=DK&hl=en-US&tz=Etc/GMT-1&cmpt=q&content=1&export=1"

    def scrapeGoogleTrends(self):
        for query_word in self.search_words:
            browser = webdriver.Chrome()

            urlString = self.baseURL + query_word + self.tailURL
            print urlString

            browser.get(urlString)

            #report_file.retrieve(urlString, "download/" + query_word + ".csv")
            print "Downloading: " + query_word + ".csv file"

