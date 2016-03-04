import numpy as np
from sklearn import preprocessing
from sklearn import cross_validation
from sklearn.cross_validation import KFold
from sklearn import linear_model
import csv
import sys
import glob
import argparse
from os import listdir

class CSVAnalyser:
    def __init__(self, directories = []):
        self.directories = directories
        self.search_data = []
        self.data = None
        self.normalized_data = None


    def find_csv_filenames(self,path_to_dir, suffix=".csv" ):
        filenames = listdir(path_to_dir)
        return [ filename for filename in filenames if filename.endswith( suffix ) ]

    def open_csv_file (self,path_to_file):
        csv_file = open(path_to_file, 'r')
        #skip header
        return csv_file

    def analyse_file(self,file_handler):
        try:
            reader = csv.reader(file_handler)
            next(reader, None)  # skip the headers

            value_list = []

            for row in reader:
                value_list.append(float(row[1]))
            self.search_data.append(value_list)

        finally:
            file_handler.close()

    def analyse(self):
        for directory in self.directories:
                csv_files_in_directory = self.find_csv_filenames(directory)
                for csv_file in csv_files_in_directory:
                    file_handler = self.open_csv_file(directory + "/" + csv_file)
                    self.analyse_file(file_handler)


        self.data = np.array(self.search_data)
        self.normalized_data = preprocessing.normalize(self.data)
        print self.data

        #5-fold validation
        kf = KFold(len(self.data), n_folds=5)
        for train_index, test_index in kf:
            print("TRAIN:", train_index, "TEST:", test_index)
            X_train, X_test = self.data[train_index], self.data[test_index]
            print("X_TRAIN:", X_train, "X_TEST:", X_test)


        clf = linear_model.LinearRegression()


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