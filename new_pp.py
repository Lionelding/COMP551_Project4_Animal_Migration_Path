'''Example using new preprocessing technique'''
from __future__ import print_function

from argparse import ArgumentParser
import numpy as np
from argparse import ArgumentParser
import sys
import os

from preprocess import get_data_by_individual, get_time_series, RelativeDate, RelativeDateRange
from utils import plot_series

parser = ArgumentParser()
parser.add_argument('fpath', type=str, action='store',
                    help='the path of the csv to load')

args = parser.parse_args()

if not os.path.exists(args.fpath):
    if 'data/' in args.fpath:
        parser.error('The file %s does not exist' % args.fpath)
        sys.exit(1)
    else:
        # try appending preprocessed_data/
        args.fpath = 'data/' + args.fpath
        if not os.path.exists(args.fpath):
            parser.error('The file %s does not exist' % args.fpath)
            sys.exit(1)

print(__doc__)
parser.print_help()
print()

def organize(tsos):
    '''organizes a list of time series objects into a dictionary'''
    id_to_series = {}
    for tso in tsos:
        if tso.id not in id_to_series:
            id_to_series[tso.id] = []
        id_to_series[tso.id].append(tso.series)
    return id_to_series

if __name__ == '__main__':

    # get a map of individual id to all its data, ordered by time
    indiv_to_ts = get_data_by_individual(args.fpath)

    print('Number of individuals')
    print(len(indiv_to_ts))
    print()

    # let's plot out Irma's latitude against time
    print('Plotting Irma\'s latitude over time')
    plot_series(indiv_to_ts['Irma'], 2, 1)
    print()

    # optionally define a relative date range, e.g.
    start = RelativeDate(3, 1)
    end = RelativeDate(11, 1)
    rdr = RelativeDateRange(start, end)

    # get all the time series (splits)
    tsos = get_time_series(indiv_to_ts, rdr)
    print()

    print('Total number of time series')
    print(len(tsos))
    print()

    # let's plot Irma's time series now
    # organize the series by id
    id_to_series = organize(tsos)
    # get Irma's time series
    irma_series = id_to_series['Irma']
    # plot them
    print('Plotting Irma\'s latitude over time, after splitting')
    plot_series(irma_series, 2, 1, variable_length=True)
    print()
    
    # Do whatever you need to do with them
