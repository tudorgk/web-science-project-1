#!/usr/bin/env python

"""

"""

import sys
import argparse


def main(arguments):

    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)

    parser.add_argument('file', type=argparse.FileType('r'), nargs='+')
    args = parser.parse_args()
    for f in args.file:
        for line in f:
            print line
    args = parser.parse_args(arguments)

    print args

if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))