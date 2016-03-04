import numpy
import csv
import sys
import glob
import argparse
from os import listdir

class CSVAnalyser:
    def __init__(self, directories = []):
        self.directories = directories

    def find_csv_filenames(self,path_to_dir, suffix=".csv" ):
        filenames = listdir(path_to_dir)
        return [ filename for filename in filenames if filename.endswith( suffix ) ]

    def open_csv_file (self,path_to_file):
        csv_file = open(path_to_file, 'r')
        return csv_file

    def analyse_file(self,file_handler):
        try:
            reader = csv.reader(file_handler)
            valid = False
            for row in reader:
                #print row
                if len(row) != 0:
                    if row[0] == "Week":
                        valid = True
                    elif row[0] == "Month":
                        valid = True
            if not valid:
                print "file: " + file_handler.name +" is NOT valid. Skipping file"
            else:
                None


        finally:
            file_handler.close()

    def analyse(self):
        for directory in self.directories:
                csv_files_in_directory = self.find_csv_filenames(directory)
                for csv_file in csv_files_in_directory:
                    file_handler = self.open_csv_file(directory + "/" + csv_file)
                    self.analyse_file(file_handler)


def main(arguments):
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)

    parser.add_argument('-dir', nargs='+')
    args = parser.parse_args(arguments)

    csv_analyser = CSVAnalyser(args.dir)
    csv_analyser.analyse()
    #get all the file names and save them


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))