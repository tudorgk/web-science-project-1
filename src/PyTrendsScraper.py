import os
from pytrends.pyGTrends import pyGTrends
import time
from random import randint

class PyTrendsScraper:
    def __init__(self, search_words = None, file_name = "report.csv"):
        self.save_path = "pytrends/" + file_name
        self.search_words = search_words
        self.connector = pyGTrends("websciencebot@gmail.com", "gotneedforspeed")

    def scrapeGoogleTrends(self):

        defaultReportName = "report"
        i = 1

        for word in self.search_words:

            report = self.connector.request_report(word, hl='en-US', geo="DK", date="01/2011 60m")

            # wait a random amount of time between requests to avoid bot detection
            time.sleep(randint(1, 5))

            self.connector.save_csv(self.save_path,word)
            i+=1