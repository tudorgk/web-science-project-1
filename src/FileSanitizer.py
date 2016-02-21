#!/usr/bin/env python

"""

"""

import sys
import argparse
import string
import re



def tokenize_file(input_file):
    review = input_file.read()
    tokens = [e.lower()
              for e in
              map(string.strip, re.compile("(\s)").split(review))
              if len(e) > 0 and not re.match("\s",e)]

    return tokens


def sanitize_stopwords(input_file):
    all_input = input_file.read()
    array = []
    lines = all_input.split('\n')
    for line in lines:
        first_word = line.split('|')[0].strip()
        array.append(first_word)
    return array


def remove_stop_words(tokenized_strings, stop_words):
    print stop_words


def main(arguments):

    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)

    parser.add_argument('file', type=argparse.FileType('r'), nargs='+')
    parser.add_argument('-d', action='store', type=argparse.FileType('r'), nargs=1, help='stop words file')

    args = parser.parse_args(arguments)
    # print args

    # get stop words file
    stop_words_file = args.d
    stop_words_list = sanitize_stopwords(stop_words_file[0])
    print stop_words_list

    # get files
    for f in args.file:
        # print f
        tokenized_words = tokenize_file(f)
        print tokenized_words


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))


# File analyzer




