import urllib
from selenium import webdriver
import os

class TrendsScraper:
    def __init__(self, search_words = None, virus_name = ""):
        self.virus_name = virus_name
        self.search_words = search_words
        self.baseURL = "http://www.google.com/trends/trendsReport?q="
        self.tailURL = "&date=01/2011%2062m&geo=DK&hl=en-US&tz=Etc/GMT-1&cmpt=q&content=1&export=1"
        self.setUp()

    def setUp(self):
        self.profile = webdriver.FirefoxProfile('/Users/tudorgk/Library/Application Support/Firefox/Profiles/38mtquy7.default')
        self.profile.set_preference("browser.download.folderList", 2)
        self.profile.set_preference("browser.download.manager.showWhenStarting", False)

        path_directory = "/Users/tudorgk/Documents/University/WS/web-science-project-1/downloads/" + self.virus_name
        if not os.path.exists(path_directory):
            os.makedirs(path_directory)

        self.profile.set_preference("browser.download.dir", path_directory )
        self.profile.set_preference('browser.helperApps.neverAsk.saveToDisk', ('application/vnd.ms-excel'))
        self.driver = webdriver.Firefox(self.profile)

    def scrapeGoogleTrends(self):
        for query_word in self.search_words:

            urlString = self.baseURL + query_word + self.tailURL
            print urlString

            self.driver.get(urlString)
            print "Downloading: " + query_word + ".csv file"

