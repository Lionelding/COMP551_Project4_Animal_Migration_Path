'''preprocessing'''

from __future__ import print_function

import csv
import sys
import numpy as np

def read_data(fname, cols):
    '''returns an array containing the data in the given cols of the file'''
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

def preprocess(fname, cols):
    return np.array(read_data(fname, cols))
