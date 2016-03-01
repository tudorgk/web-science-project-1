#!/usr/bin/env python

"""

"""

import argparse
import string
import re
import sys
import urllib as ul
import os
from TrendsScraper import TrendsScraper

def tokenize_file(input_file):
    review = input_file.read()
    tokens = [e.lower()
              for e in
              map(string.strip, re.compile("(\s)").split(review))
              if len(e) > 0 and not re.match("\s",e)]

    tokens = [re.split(r'[-()\n ,:.]', x) for x in tokens]
    flattened = [val for sublist in tokens for val in sublist]
    return flattened


def sanitize_stopwords(input_file):
    all_input = input_file.read()
    array = []
    lines = all_input.split('\n')
    for line in lines:
        first_word = line.split('|')[0].strip()
        array.append(first_word)
    return array


def remove_stop_words(tokenized_strings, stop_words):
    sanitized_list = [x for x in tokenized_strings if x not in stop_words]

    #remove empty chars
    sanitized_list = filter(None, sanitized_list)

    #remove numbers
    sanitized_list = [x for x in sanitized_list if not any(c.isdigit() for c in x)]

    return sanitized_list

def main(arguments):

    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)

    parser.add_argument('file', type=argparse.FileType('r'), nargs='+')
    parser.add_argument('-d', action='store', type=argparse.FileType('r'), nargs=1, help='stop words file')

    args = parser.parse_args(arguments)

    # get stop words file
    stop_words_file = args.d
    stop_words_list = sanitize_stopwords(stop_words_file[0])

    sanitiezed_file_list = []
    # get files
    for f in args.file:
        tokenized_words = tokenize_file(f)
        sanitiezed_words = remove_stop_words(tokenized_words,stop_words_list)
        sanitiezed_file_list.append(sanitiezed_words)

    # now we have the sanitized words for each file
    #print sanitiezed_file_list

    query_words = []

    # find the words that appear in both
    for i in range(0,len(sanitiezed_file_list)):
        for j in range(0,len(sanitiezed_file_list)):
            if i != j:
                for k in range(0,len(sanitiezed_file_list[i])):
                    if sanitiezed_file_list[i][k] in sanitiezed_file_list[j]:
                        query_words.append(sanitiezed_file_list[i][k])

    query_words = list(set(query_words))

    query_words =map(lambda x:ul.quote(x),query_words)
    print query_words

    file_name = args.file[0].name.rsplit('/',1)[-1]

    scraper = TrendsScraper(query_words,file_name)
    scraper.scrapeGoogleTrends()


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))


# File analyzer




