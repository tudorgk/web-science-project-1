import numpy as np
from sklearn import preprocessing
from sklearn import cross_validation
from sklearn.cross_validation import KFold
from sklearn import linear_model
import csv
import sys
import glob
import argparse
import json
from os import listdir

from sklearn.metrics import mean_squared_error


class CSVAnalyser:
    def __init__(self, directories = []):
        self.directories = directories
        self.search_data = []
        self.data = None
        self.normalized_data = None
        self.clinical_data = None


    def import_clinical_data (self,path_to_file):
        json_file = open(path_to_file,'r')
        json_data = json.load(json_file)
        self.clinical_data = np.array(json_data[1])
        #print self.clinical_data


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
        self.data = self.data.transpose()

        #get only the values until 12-2015 (to match the clinical data)
        #print ("BIG data = " , self.data.shape)
        self.data = self.data[:len(self.clinical_data),:]
        #print ("SMALL data = " , self.data.shape)
        #print ("Clinical data = ", self.clinical_data.shape)

        self.normalized_data = preprocessing.normalize(self.data)
        #print self.data

        regr = linear_model.LinearRegression()

        #5-fold validation
        kf = KFold(len(self.data), n_folds=5,shuffle=False)
        for train_index, test_index in kf:
            #print("TRAIN:", train_index, "TEST:", test_index)
            X_train, X_test = self.data[train_index], self.data[test_index]
            Y_train, Y_test = self.clinical_data[train_index], self.clinical_data[test_index]
            regr.fit(X_train, Y_train)
            #print("X_TRAIN:", X_train, "X_TEST:", X_test)

            # The coefficients
            print('Coefficients: \n', regr.coef_)
            # The mean square error
            #print("Residual sum of squares: %.2f" % np.mean((regr.predict(X_test) - Y_test) ** 2))
            print("Residual sum of squares: %.2f" % np.sqrt(mean_squared_error(regr.predict(X_test), Y_test)))
            # Explained variance score: 1 is perfect prediction
            print('Variance score: %.2f' % regr.score(X_test, Y_test))





def main(arguments):
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)

    parser.add_argument('-dir', nargs='+')
    parser.add_argument('-t', nargs=1)

    args = parser.parse_args(arguments)

    csv_analyser = CSVAnalyser(args.dir)
    csv_analyser.import_clinical_data(args.t[0])
    csv_analyser.analyse()
    #get all the file names and save them


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))