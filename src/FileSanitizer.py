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
              map(string.strip, re.split("(\W+)", review))
              if len(e) > 0 and not re.match("\W",e)]

    return tokens


def main(arguments):

    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)

    parser.add_argument('file', type=argparse.FileType('r'), nargs='+')

    # args = parser.parse_args(arguments)
    # print args

    # get args
    args = parser.parse_args()
    for f in args.file:
        # print f
        tokenized_words = tokenize_file(f)
        print tokenized_words


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))


# File analyzer




