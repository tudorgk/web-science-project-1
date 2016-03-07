import numpy as np
from sklearn import preprocessing
import matplotlib.pyplot as plt
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
        return csv_file

    def analyse_file(self,file_handler):
        try:
            reader = csv.reader(file_handler)
            header = next(reader)  # check the headers
            #print header

            if header[0] == 'Month':
                value_list = []
                for row in reader:
                    value_list.append(float(row[1]))
                self.search_data.append(value_list)
            elif header[0] == 'Week':
                value_list = []
                aux_week_array = []
                aux_month = ""
                for row in reader:
                    if aux_month == "":
                        aux_month = row[0][:7]
                    if row[0][:7] == aux_month:
                        aux_week_array.append(float(row[1]))
                    else:
                        average_week_count = np.average(aux_week_array)
                        value_list.append(average_week_count)
                        del aux_week_array[:]
                        aux_week_array.append(float(row[1]))
                        aux_month = row[0][:7]
                self.search_data.append(value_list)

        finally:
            file_handler.close()

    def analyse(self):
        for directory in self.directories:
                csv_files_in_directory = self.find_csv_filenames(directory)
                for csv_file in csv_files_in_directory:
                    file_handler = self.open_csv_file(directory + "/" + csv_file)
                    self.analyse_file(file_handler)


        #need to pad the matrix with missing values
        length = len(sorted(self.search_data,key=len, reverse=True)[0])
        self.data=np.array([xi+[0]*(length-len(xi)) for xi in self.search_data])

        self.data = np.transpose(self.data)


        #get only the values until 12-2015 (to match the clinical data)
        self.data = self.data[:self.clinical_data.size,:]
        #print ("SMALL data = " , self.data.shape)
        #print ("Clinical data = ", self.clinical_data.size)

        self.normalized_data = preprocessing.normalize(self.data)
        #print self.data

        regr = linear_model.LinearRegression()

        coeficients_array = []
        rmse_array = []
        variance_array = []

        #5-fold validation
        kf = KFold(len(self.data), n_folds=5,shuffle=True)
        for train_index, test_index in kf:
            X_train, X_test = self.data[train_index], self.data[test_index]
            Y_train, Y_test = self.clinical_data[train_index], self.clinical_data[test_index]
            regr.fit(X_train, Y_train)

            #save data for averaging after 5 fold validation
            coeficients_array.append(regr.coef_)
            rmse_array.append(np.sqrt(mean_squared_error(regr.predict(X_test), Y_test)))
            variance_array.append(regr.score(X_test, Y_test))


        # The root mean square error
        print("%.3f" % np.average(rmse_array))
        # Explained variance score: 1 is perfect prediction
        # The best possible score is 1.0 and it can be negative (because the model can be arbitrarily worse).
        # A constant model that always predicts the expected value of y, disregarding the input features,
        # would get a R^2 score of 0.0.
        print('%.3f' % np.average(variance_array))



def main(arguments):
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)

    parser.add_argument('-dir', nargs='+')
    parser.add_argument('-t', nargs=1)

    args = parser.parse_args(arguments)

    csv_analyser = CSVAnalyser(args.dir)
    csv_analyser.import_clinical_data(args.t[0])
    csv_analyser.analyse()



if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))