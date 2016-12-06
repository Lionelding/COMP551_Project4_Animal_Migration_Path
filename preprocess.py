'''preprocessing'''

from __future__ import print_function

import csv
import sys
import numpy as np
import cPickle as pickle
import time
import datetime

from constants import SECS_PER_DAY, SECS_PER_YEAR

################################################################################
# New preprocessing
################################################################################

#---------------------
# downsampling helpers
#---------------------

def downsample(ts, factor):
    '''Takes a time series and returns a downsampling where only one point every
    factor points is kept'''
    if factor < 1:
        raise Exception("Downsampling factor must be >= 1")
    return ts[0:len(ts):factor]

def downsample_all(tss, factor):
    '''wrapper to downsample a bunch of time series using the above method'''
    new_tss = []
    for ts in tss:
        new_tss.append(downsample(ts, factor))
    return new_tss

#--------------
# Other helpers
#--------------
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

def sort_by_time(data):
    '''for each individual in data, sorts the time series by time'''
    for indiv_id in data:
        data[indiv_id].sort(key=lambda x: x[2])
    return data

def get_data_by_individual(fname):
    '''given a filename, returns a map of individual to data'''
    data = []
    with open(fname, 'rb') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
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
        if lat_col == -1:
            print('Could not find column `location-lat`')
            sys.exit(1)
        lon_col = get_col_index(col_titles, 'location-long')
        if lon_col == -1:
            print('Could not find column `location-long`')
            sys.exit(1)

        # create a map of individual-local-identifier to time series
        data = {}
        for row in reader:
            # get the timestamp
            timestamp = row[timestamp_col]
            # convert the timestamp string into a utc timestamp
            time = get_unix_ts(timestamp)
            # get the individual
            individual = row[ili_col]
            # get the location
            # get the data
            try:
                lat = float(row[lat_col])
                lon = float(row[lon_col])
                pt = [lon, lat, time]
                # add the point to the time series of the appropriate individual
                if individual not in data:
                    data[individual] = []
                data[individual].append(pt)
            except ValueError:
                print('cannot cast `%s` to float' % row[lat_col])

        # let's be sure that all the data is properly sorted...
        return sort_by_time(data)

def pretty_time(ts):
    return datetime.datetime.fromtimestamp(ts).strftime('%d/%m/%Y')

class TimeSeries(object):
    def __init__(self, id, series):
        self.id = id
        self.series = series

    def set_interpolated_series(self, interpolated_series):
        self.interpolated_series = interpolated_series

    def __str__(self):
        return self.id + ', ' + pretty_time(self.series[0][2]) + ' - ' + pretty_time(self.series[-1][2])

class RelativeDate(object):
    def __init__(self, month, day):
        self.month = month
        self.day = day

class RelativeDateRange(object):
    def __init__(self, start, end):
        self.start = start
        self.end = end

    def contains(self, date):
        if date.month > self.start.month and date.month < self.end.month:
            return True
        elif date.month == self.start.month:
            if date.month == self.end.month:
                return date.day >= self.start.day and date.day <= self.end.day
            else:
                return date.day >= self.start.day
        elif date.month == self.end.month:
            return date.day <= self.end.day
        else:
            return False

    def get_total_time(self):
        # Assume 30 day months
        num_months = self.end.month - self.start.month
        num_days = self.end.day - self.start.day
        return float((num_months*30 + num_days) * SECS_PER_DAY)

def get_total_time(series):
    return series[-1][2] - series[0][2]

def should_add(series, rdr=None):
    if len(series) == 0:
        return False
    series_time = get_total_time(series)
    if rdr:
        range_time = rdr.get_total_time()
    else:
        range_time = SECS_PER_YEAR

    if (series_time / range_time) > 0.8:
        return True

    return False

def split_time_series(indiv_id, time_series, relative_date_range=None):
    '''given an id and a time series, splits the time series according to the
    relative date range and returns a list of the splits. Uses some extrapolation if need be'''
    if relative_date_range:
        split = []
        curr_series = []
        for pt in time_series:
            curr_date = datetime.datetime.fromtimestamp(pt[2])
            if relative_date_range.contains(curr_date):
                curr_series.append(pt)
            elif len(curr_series) != 0:
                # decide if curr_series contains enough points to be added
                if should_add(curr_series, relative_date_range):
                    split.append(TimeSeries(indiv_id, curr_series))
                else:
                    print('Rejecting series for individual %s' % indiv_id)
                curr_series = []
        if should_add(curr_series):
            split.append(curr_series)
        else:
            print('Rejecting series for individual %s' % indiv_id)
        return split
    else:
        # split according to years
        year_to_series = {}
        for pt in time_series:
            curr_date = datetime.datetime.fromtimestamp(pt[2])
            if curr_date.year not in year_to_series:
                year_to_series[curr_date.year] = []
            year_to_series[curr_date.year].append(pt)
        split = []
        for year, series in year_to_series.iteritems():
            if should_add(series):
                split.append(TimeSeries(indiv_id, series))
            else:
                print('Rejecting series for individual %s' % indiv_id)
        return split

def get_time_series(data, relative_date_range=None):
    '''takes an mapping of individual id to the time series for the individual and
    returns a list of TimeSeries objects constructed according to the relative date range'''
    tsos = []   # time series objects
    for indiv_id, time_series in data.iteritems():
        tsos += split_time_series(indiv_id, time_series, relative_date_range)
    return tsos

################################################################################
# Old preprocessing
################################################################################

''' Struture
{
    year: {
        individual_id: [data points],
        ...
    },
    ...
}
'''

def read_data(fname):
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
            try:
                lat = float(row[lat_col])
                lon = float(row[lon_col])
                # convert the timestamp string into a utc timestamp
                time = get_unix_ts(timestamp)

                feature_vec = [lon, lat, time]

                data_by_year[year][individual].append(feature_vec)
                data_by_individual[individual][year].append(feature_vec)
            except ValueError:
                print('cannot cast %s to float' % row[lat_col])

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

################################################################################
# Pickling
################################################################################

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

## End
