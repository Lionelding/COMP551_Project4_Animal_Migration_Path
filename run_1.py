'''Example using new preprocessing technique'''
from __future__ import print_function

from argparse import ArgumentParser
import numpy as np
from argparse import ArgumentParser
import sys
import os

from preprocess import get_data_by_individual, get_time_series, RelativeDate, RelativeDateRange
from utils import plot_series
from interpolation import normalize_time_series_objects
from cross_validation import CrossValidator
sys.path.append('./clustering/')
from ts_cluster import TsClusterer
from postprocess import to_pickle

parser = ArgumentParser()
parser.add_argument('fpath', type=str, action='store',
                    help='the path of the csv to load')
parser.add_argument('--rdr', type=int, nargs=4,
                    help='start_month start_day end_month end_day --> defines the range of dates '
                    'for which to include points each year')
parser.add_argument('--interval', type=float, default=1.,
                    help='the interpolation time interval to use (in days)')
parser.add_argument('--n_clusts', type=int, action='store', default=1,
                    help='the number of clusters to use; will be ignored if --clust_range is also used')
parser.add_argument('--clust_range', type=int, action='store', nargs=3,
                    help='start stop step --> number of clusters to cross-validate over')
parser.add_argument('--norm', type=int, action='store', default=1,
                    help='the norm to use in DTW; valid values are 1 or 2, for L1 and L2 norms respectively')
parser.add_argument('--max_iters', type=int, action='store', default=15,
                    help='the maximum number of centroid updates to use in clustering')
parser.add_argument('--st', type=float, action='store', default=.05,
                    help='the stopping threshold to use during clustering')
parser.add_argument('--dt', type=float, action='store', default=.5,
                    help='the difference threshold to use in determining the best number of clusters')
parser.add_argument('--it', type=float, action='store', default=.5,
                    help='points need to cover at least this fraction of the desired time interval to be considered')
parser.add_argument('--plot', action='store_true',
                    help='if set, will plot some things')

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

if args.norm not in [1, 2]:
    parser.error('norm must be 1 or 2')
    sys.exit(1)

print(__doc__)
parser.print_help()
print()

def organize(tsos, interpolated=False):
    '''organizes a list of time series objects into a dictionary'''
    id_to_series = {}
    for tso in tsos:
        if tso.id not in id_to_series:
            id_to_series[tso.id] = []
        id_to_series[tso.id].append(tso.interpolated_series if interpolated else tso.series)
    return id_to_series

def get_errs_by_num_clusts(clust_range, tsos, n_restarts, dist_norm, max_iterations, stopping_threshold):
    # Create a cross validator
    clust_sizes = range(clust_range[0], clust_range[1]+1, clust_range[2])
    cv =  CrossValidator(n_restarts, tsos)
    errs = []
    for n_clusts in clust_sizes:
        print('-' * 80)
        print('Number of clusters: %d' % n_clusts)
        print('_' * 80)
        # create a clusterer
        clusterer = TsClusterer(n_clusts, dist_norm, max_iterations, stopping_threshold)
        avg_err = cv.cross_validate(clusterer)
        errs.append((n_clusts, avg_err, clusterer))
        print('Average error of %f achieved using %d clusters' % (avg_err, n_clusts))
        print()
    return errs

def get_best_num_clusts_idx(errs, threshold):
    '''Decides the `best` number of clusters according to some threshold'''
    if len(errs) == 1:
        return errs[0][0]
    prev_err = errs[0][1]
    lowest_err = prev_err
    lowest_err_idx = 0
    for i in range(1, len(errs)):
        curr_err = errs[i][1]
        if curr_err < prev_err:
            lowest_err = curr_err
            lowest_err_idx = i
        if curr_err <= prev_err and (prev_err - curr_err) <= threshold:
            return i-1
        prev_err = curr_err
    return lowest_err_idx

if __name__ == '__main__':

    # get a map of individual id to all its data, ordered by time
    indiv_to_ts = get_data_by_individual(args.fpath)

    print('Number of individuals')
    print(len(indiv_to_ts))
    print()

    if args.plot:
        # let's plot out Irma's latitude against time
        print('Plotting Irma\'s latitude over time')
        plot_series(indiv_to_ts['Irma'], 2, 1)
        print()

    rdr = None

    # optionally define a relative date range, e.g.
    if args.rdr:
        start = RelativeDate(args.rdr[0], args.rdr[1])
        end = RelativeDate(args.rdr[2], args.rdr[3])
        rdr = RelativeDateRange(start, end)

    # get all the time series (splits)
    tsos = get_time_series(indiv_to_ts, rdr, args.it)
    print()

    print('Total number of time series')
    print(len(tsos))
    print()

    if args.plot:
        # let's plot Irma's time series now
        # organize the series by id
        id_to_series = organize(tsos)
        # get Irma's time series
        irma_series = id_to_series['Irma']
        # plot them
        print('Plotting Irma\'s latitude over time, after splitting')
        plot_series(irma_series, 2, 1, variable_length=True)
        print()

    ############################################################################
    # Do whatever else you might need to do with the tsos
    ############################################################################

    # let's normalize them so that we have one point per day
    normalize_time_series_objects(tsos, args.interval, rdr)

    # now each tso should have a property interpolated_series that contains its
    # interpolated points
    itss = np.array([tso.interpolated_series for tso in tsos])

    print('Shape of all time series after normalization')
    print(itss.shape)
    print()

    if args.plot:
        # let's plot Irma's interpolated time series
        id_to_interpolated_series = organize(tsos, interpolated=True)
        irma_interpolated_series = id_to_interpolated_series['Irma']
        print('Plotting Irma\'s latitude over time, after splitting and interpolating')
        plot_series(irma_interpolated_series, 2, 1)
        print()

    # cluster all the time series objects
    if args.clust_range:
        errs = get_errs_by_num_clusts(args.clust_range, tsos, 3, args.norm, args.max_iters, args.st)

        print('Summary of number of clusters to average error')
        print('n_clusts\tavg_err')
        for n_clusts, err, _ in errs:
            print('%d\t%.4f' % (n_clusts, err))
        print()

        # get the best number of clusters
        idx = get_best_num_clusts_idx(errs, args.dt)
        best_n_clusts, avg_err, clusterer = errs[idx]
        print('Best number of clusters: %d' % best_n_clusts)
        print('Average error: %f' % avg_err)
        print()

        # Finally, query the assignments for more information

        # get the assignments
        assignments = clusterer.get_assignments()

        # query the assignment object for information
        # TODO

        # store the errs for later use
        to_pickle('clusterers', errs)

    else:
        clusterer = TsClusterer(args.n_clusts, args.norm, args.max_subset, args.st)

        clusterer.k_means_clust(tsos, verbose=True)

        # Finally, query the assignments for more information

        # get the assignments
        assignments = clusterer.get_assignments()

        # query the assignment object for information
        # TODO

        # store the clusterer for later use
        to_pickle('clusterer', clusterer)
