'''Clustering example'''
from __future__ import print_function

import sys
import os.path
import random
from time import time
from argparse import ArgumentParser
import logging

import numpy as np
from numpy.linalg import norm

sys.path.append('./clustering/')
from ts_cluster0 import TsCluster

from preprocess import load
from interpolation import normalize_time_series
from utils import plot_series, extract_lat_and_lon

################################################################################
# logging and options
################################################################################

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(levelname)s %(message)s')

parser = ArgumentParser()
parser.add_argument('--n_clusts', type=int, action='store', default=1,
                    help='the number of clusters to use; will be ignored if --clust_range is also used')
parser.add_argument('--clust_range', type=int, action='store', nargs=3,
                    help='stop, start, and step -- number of clusters to cross-validate over')
parser.add_argument('--ds_factor', type=int, action='store',
                    help='the downsampling factor')
parser.add_argument('--norm', type=int, action='store', default=1,
                    help='the norm to use in DTW; valid values are 1 or 2, for L1 and L2 norms respectively')
parser.add_argument('--st', type=float, action='store', default=.2,
                    help='the stopping threshold to use during clustering')

args = parser.parse_args()

if args.norm not in [1, 2]:
    parser.error('norm must be 1 or 2')
    sys.exit(1)

print(__doc__)
parser.print_help()
print()

################################################################################
# core logic
################################################################################

if __name__ == '__main__':

    # load the data
    # TODO make the data to load a parameter
    data_obj = load('preprocessed_data/prd.pkl')
    # TODO choose whether to load data by year or by animal
    # if by year, select year, else select animal - print out options
    data_by_year = data_obj.get_data_by_year()
    year, indivs = data_by_year[0]

    print('year')
    print(year)
    print('num individuals for the year')
    print(len(indivs))
    print()

    # get the time series of interest from the loaded data
    tss = []
    for indiv_id, pts in indivs:
        tss.append(pts)

    # normalize the series!!! (optionally downsampling)
    normd_tss = normalize_time_series(tss, downsample_factor=args.ds_factor)

    print('Shape of normalized data')
    print(normd_tss.shape)
    print()

    # extract just the lat and lon coordinates since this is all we want to use for DTW
    ptss = extract_lat_and_lon(normd_tss)

    print('Shape of data without time')
    print(ptss.shape)
    print()

    # instantiate a clusterer
    print('Instantiating a clusterer')
    clusterer = TsCluster(args.n_clusts, args.norm, stopping_threshold=args.st)
    print('done')
    print()

    print('Clustering')
    t0 = time()
    clusterer.k_means_clust(ptss, 100, verbose=True)
    dur = time() - t0
    print('done in %fs' % dur)
    print()

    centroids = clusterer.get_centroids()

    print('plotting centroids')
    plot_series(centroids)
