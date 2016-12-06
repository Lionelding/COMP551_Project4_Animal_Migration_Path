'''Try out some other preprocessing'''

from __future__ import print_function
import datetime
import sys

import numpy as np

from preprocess import get_data_by_individual
from utils import plot_series

from interpolation import normalize_time_series

'''
For each individual, look at all points
Print out the start time and end time for each animal
See if there are any for which we don't have a lot of points and throw them out
For the animals remaining, determine the latest start time and earliest end time over all the animals
Cut any points outside this range
Hopefully, the range could last for at least a couple of years
Plot longitude vs time for each animal and for each point we still have
Should look something like the below image
From this image, eyeball a couple of migrations, as shown in the image
Cut out all other points and just use the selected migrations for the algorithm
'''

def convert_unix_ts_to_date_string(ts):
    return datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')

class Individual(object):
    def __init__(self, id, start, end):
        self.id = id
        self.start = start
        self.end = end

def get_start_and_end_times_by_individual(data):
    indivs = []
    for id, pts in data.iteritems():
        indivs.append(Individual(id, pts[0][2], pts[-1][2]))
    return indivs

def max_subset(indivs, s):
  starts = sorted(indivs, key=lambda x: x.start)
  ends = sorted(indivs, key=lambda x: x.end)

  current_stack = []

  largest = []

  while len(starts) + len(ends) > 0:
    while len(starts) > 0 and starts[0].start <= ends[0].end:
      current_stack.append(starts.pop(0))

      for i in range(0, len(current_stack) - len(largest)):

        if current_stack[i].end - current_stack[-1].start >= s:

          amax = max(current_stack, key=lambda x: x.start)
          foo = filter(lambda x: (x.end >= amax.start + s), current_stack)
          if len(foo) > len(largest):
            largest = foo[:]
          continue

    if len(starts) == 0: break

    while ends[0].end < starts[0].start:
      current_stack.remove(ends.pop(0))

  return largest

def plot_lat_vs_time(data, individually=False):
    tss = [s for id, s in data.iteritems()]
    if individually:
        for ts in tss:
            plot_series(np.array(ts), 2, 1)
    else:
        plot_series(tss, 2, 1, variable_length=True)

SECONDS_PER_YEAR = 60 * 60 * 24 * 365
NUM_YEARS = .4

if __name__ == '__main__':

    # get all the data
    data = get_data_by_individual('data/white_geese.csv')

    print('total number of individuals')
    print(len(data))

    # print all the data
    plot_lat_vs_time(data)

    # get Individual objects for each of the individuals in the data set
    indivs = get_start_and_end_times_by_individual(data)

    print('id\tstart\tend')
    for indiv in indivs:
        print('%s\t%s\t%s' % (indiv.id, convert_unix_ts_to_date_string(indiv.start), convert_unix_ts_to_date_string(indiv.end)))

    print()

    # filter the individuals to get just those that have overlap in data points
    # for at least NUM_YEARS years
    filtered_indivs = max_subset(indivs, SECONDS_PER_YEAR * NUM_YEARS)

    print('individuals with overlapping time series for at least %.f years' % NUM_YEARS)
    print(len(filtered_indivs))

    # get the ids of the filtered individuals
    ids = [i.id for i in filtered_indivs]

    # get the time series of the filtered individuals
    filtered_tss = [v for k, v in data.iteritems() if k in ids]

    # interpolate for the filtered individual set
    normd_tss = normalize_time_series(filtered_tss)

    normd_tss = np.array(normd_tss)
    print('shape of all time series after normalization')
    print(normd_tss.shape)
    print()

    # plot lat vs time
    plot_series(normd_tss, 2, 1)

    # plot lat vs lon
    plot_series(normd_tss)
