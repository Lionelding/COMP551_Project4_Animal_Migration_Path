'''preprocessing'''

from __future__ import print_function

import csv
import sys
import numpy as np

''' Struture
{
    year: {
        animal_id: {
            data: [data points]
        },
        ...
    },
    ...
}
'''

def get_col_index(col_titles, title):
    for curr_title, i in enumerate(col_titles):
        if curr_title == title:
            return i
    return -1

def read_data(fname, cols, organize):
    '''if organize=false, returns an array containing the data in the given cols of the file
    else returns a dictionary with the above structure'''
    if not organize:
        data = []
        with open(fname, 'rb') as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            # skip the header
            reader.next()
            for row in reader:
                feature_vec = []
                for col in cols:
                    feature_vec.append(row[col])
                data.append(feature_vec)
        return data
    else:
        data = {}
        with open(fname, 'rb') as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            # get the timestamp and individual-local-identifier columns
            col_titles = reader.next()
            timestamp_col = get_col_index(col_titles, 'timestamp')
            if timestamp_col == -1:
                print('Could not find column `timestamp`')
                sys.exit(1)
            ili_col = get_col_index(col_titles, 'individual-local-identifier')
            if ili_col == -1:
                print('Could not find column `individual-local-identifier`')
                sys.exit(1)
            # iterate row by row and create the data object

            # for each set of datapoints, ensure that it is sorted
            return data

def preprocess(fname, cols, organize=True):
    return np.array(read_data(fname, cols, organize))
