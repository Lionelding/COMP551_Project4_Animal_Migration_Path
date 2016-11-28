'''preprocessing'''

from __future__ import print_function

import csv
import sys
import numpy as np
import cPickle as pickle
import time
import datetime

''' Struture
{
    year: {
        individual_id: [data points],
        ...
    },
    ...
}
'''
def get_col_index(col_titles, title):
    for i, curr_title in enumerate(col_titles):
        if curr_title == title:
            return i
    return -1

def get_unix_ts(ts_str):
    '''converts a string timestamp to a unix timestamp
    string format: 2015-06-19 12:34:42.000 or 2001-07-31 2:37:41'''
    year_str, month_str, rest = ts_str.split('-')
    day_str, rest = rest.split(' ')
    if '.' in rest:
        clock_time, milliseconds = rest.split('.')
    else:
        clock_time = rest
    hour_str, minute_str, second_str = clock_time.split(':')

    day = int(day_str)
    month = int(month_str)
    year = int(year_str)
    hour = int(hour_str)
    minute = int(minute_str)
    second = int(second_str)

    dt = datetime.datetime(year, month, day, hour, minute, second)

    return time.mktime(dt.timetuple())

def read_data(fname):
    '''if organize=false, returns an array containing (lat, lon, time) datapoints
    else returns a dictionary with the above structure'''
    '''
    if not organize:
        data = []
        with open(fname, 'rb') as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            # skip the header
            reader.next()
            for row in reader:
                feature_vec = []
                for col in cols:
                    feat_val = row[col]
                    # attempt to cast feat_val to a float
                    try:
                        feat_val = float(feat_val)
                    except ValueError:
                        print('unable to cast feature to float')
                        sys.exit(1)
                    feature_vec.append(feat_val)
                data.append(feature_vec)
        return data
    '''
    data_by_year = {}
    data_by_individual = {}
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
        lat_col = get_col_index(col_titles, 'location-lat')
        lon_col = get_col_index(col_titles, 'location-long')
        # iterate row by row and create the data object
        for row in reader:
            # get the year
            timestamp = row[timestamp_col]
            try:
                year = int(timestamp.split('-')[0])
            except ValueError:
                print('Unable to cast year to an integer')
                sys.exit(1)

            # get the individual
            individual = row[ili_col]

            if year not in data_by_year:
                data_by_year[year] = {}

            if individual not in data_by_year[year]:
                data_by_year[year][individual] = []

            if individual not in data_by_individual:
                data_by_individual[individual] = {}

            if year not in data_by_individual:
                data_by_individual[individual][year] = []

            # get the data
            lat = float(row[lat_col])
            lon = float(row[lon_col])
            # convert the timestamp string into a utc timestamp
            time = get_unix_ts(timestamp)

            feature_vec = [lat, lon, time]

            data_by_year[year][individual].append(feature_vec)
            data_by_individual[individual][year].append(feature_vec)
            '''
            for col in cols:
                feat_val = row[col]
                # attempt to cast feat_val to a float
                try:
                    feat_val = float(feat_val)
                except ValueError:
                    print('unable to cast feature to float')
                    sys.exit(1)
                feature_vec.append(feat_val)
            '''
        return data_by_year, data_by_individual

# Note: this is a pretty inefficient data structure - stores the same data twice
class Data(object):
    '''A wrapper class for data'''

    def __init__(self, data_by_year, data_by_individual):
        self.data_by_year = data_by_year
        self.data_by_individual = data_by_individual

    def get_data(self):
        return self.get_data_by_year, self.get_data_by_individual

    def get_year(year):
        '''returns the data for all the individuals for a single year'''
        if year not in self.data:
            raise Exception('No such year')
        return self.data[year]

    def get_data_by_year(self):
        '''returns an iterable over all the years according to the following format
        [(year, [(individual_id, data) for each individual]) for each year]'''
        retval = []
        for year, individuals in self.data_by_year.iteritems():
            l_indivs = []
            for individual_id, data in individuals.iteritems():
                l_indivs.append((individual_id, np.array(data)))
            retval.append((year, l_indivs))
        retval.sort()
        return retval

    def get_data_by_individual(self):
        '''returns data for individuals across years according to the following format
        [(individual_id, [(year, data) for each year]) for each individual]'''
        retval = []
        for individual, years in self.data_by_individual.iteritems():
            l_years = []
            for year, data in years.iteritems():
                l_years.append((year, np.array(data)))
            l_years.sort()
            retval.append((individual, l_years))
        return retval

def load_pickle(name):
    with open(name, 'rb') as f:
        p = pickle.load(f)
    return p

def save_pickle(name, content):
    if '.pkl' not in name:
        name = 'preprocessed_data/' + name + '.pkl'
    else:
        name = name = 'preprocessed_data/' + name
    print('saving data as %s' % name)
    with open(name, 'wb') as f:
        pickle.dump(content, f)

def preprocess(source_name, dest_name):
    '''creates a Data object from csv'''
    # get the data
    data_by_year, data_by_individual = read_data(source_name)
    # wrap the data in an object
    data = Data(data_by_year, data_by_individual)
    # save it to disk
    save_pickle(dest_name, data)

def load(fname):
    '''returns a pre-pickled Data object'''
    return load_pickle(fname)
