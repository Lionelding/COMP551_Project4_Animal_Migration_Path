'''Load spatial clusterers and learn from them'''

from __future__ import print_function

import logging
import numpy as np
from argparse import ArgumentParser
import sys
from time import time
import os.path
import matplotlib.pylab as plt

from preprocess import load
from utils import make_all_plottable, plot, Plottable
from cross_validation import CrossValidator
sys.path.append('./clustering/')
from ts_cluster import TsClusterer
from postprocess import to_pickle

################################################################################
# logging and options
################################################################################

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(levelname)s %(message)s')

parser = ArgumentParser()
parser.add_argument('source_path', type=str, action='store',
                    help='the filepath of the data source file')
parser.add_argument('--best_n_clusts', type=int, action='store',
                    help='the number of clusters to consider as the best number')
parser.add_argument('--norm', type=int, action='store', default=1,
                    help='the norm to use in DTW; valid values are 1 or 2, for L1 and L2 norms respectively')
parser.add_argument('--max_iters', type=int, action='store', default=15,
                    help='the maximum number of centroid updates to use in clustering')
parser.add_argument('--st', type=float, action='store', default=.05,
                    help='the stopping threshold to use during clustering')
parser.add_argument('--print_clusts', type=int, action='store',
                    help='print the individuals in each cluster, for the given number of clusters')
parser.add_argument('--window', type=int, action='store',
                    help='If set, DTW with windowing will be used rather than Euclidean distance. The window used will be twice the value passed.')

args = parser.parse_args()

if not os.path.exists(args.source_path):
    if 'postprocessed_data/' in args.source_path:
        parser.error('The file %s does not exist' % args.source_path)
        sys.exit(1)
    else:
        # try appending preprocessed_data/
        args.source_path = 'postprocessed_data/' + args.source_path
        if not os.path.exists(args.source_path):
            parser.error('The file %s does not exist' % args.source_path)
            sys.exit(1)

print(__doc__)
parser.print_help()
print()

def print_errors(clusterers):
    '''prints number of clusters vs error'''
    print('Summary of number of clusters to average error')
    print('n_clusts\tavg_err')
    for n_clusts, err, _ in clusterers:
        print('%d\t%.4f' % (n_clusts, err))
    print()

def plot_errors(clusterers):
    n_clusts = []
    errs = []
    for n, err, _ in clusterers:
        n_clusts.append(n)
        errs.append(err)

    plot(Plottable(n_clusts, errs), 'number of clusters', 'error (avg DTW distance)')

def print_clusters(assignments):
    for centroid, cluster in assignments.iteritems():
        print('Cluster %d: ' % centroid.id, end='')
        print([tso.id for tso, _ in cluster])
    print('Error: %f' % lowest_err)
    print()

def get_clusterer_for_best_n_clusts(clusterers, best_n_clusts):
    for n_clusts, err, clusterer in clusterers:
        if n_clusts == best_n_clusts:
            return clusterer
    return None

def sub_cluster(assignments, dist_metric, window, dist_norm, max_iterations, stopping_threshold):
    '''for each cluster in assignments, sub-cluster temporally (using Euclidean distance)'''
    centroid_id_to_clusterers = {}
    for centroid, cluster in assignments.iteritems():
        tsos = [tso for tso, _ in cluster]
        clust_range = [1, len(tsos), 1]
        n_restarts = 3
        clusterers = get_errs_by_num_clusts(clust_range, tsos, 3, dist_metric, window, dist_norm, max_iterations, stopping_threshold)
        centroid_id_to_clusterers[centroid.id] = clusterers
    return centroid_id_to_clusterers

def plot_centroids(assignments):
    plottables = []
    centroids = []
    for centroid, _ in assignments.iteritems():
        centroids.append(centroid)
    centroids.sort(key=lambda c: c.id)
    for centroid in centroids:
        loc_series = centroid.loc_series
        x = [pt[0] for pt in loc_series]
        y = [pt[1] for pt in loc_series]
        plottables.append(Plottable(x, y, name='centroid %d' % centroid.id))
    plot(plottables, 'longitude', 'latitude', legend=True)

def plot_clusters(assignments):
    clusters = []
    for centroid, cluster in assignments.iteritems():
        clusters.append((centroid.id, cluster))
    clusters.sort(key=lambda c: c[0])
    plottables = []
    colors = ['b', 'g', 'r', 'c', 'm']
    cluster_sizes = []
    for id, cluster in clusters:
        cluster_sizes.append(len(cluster))
        for tso, _ in cluster:
            loc_series = tso.interpolated_loc_series
            x = [pt[0] for pt in loc_series]
            y = [pt[1] for pt in loc_series]
            plottables.append(Plottable(x, y, color=colors[id]))
    plot(plottables, 'longitude', 'latitude', color=True, cluster_sizes=cluster_sizes)

def get_errs_by_num_clusts(clust_range, tsos, n_restarts, dist_metric, window, dist_norm, max_iterations, stopping_threshold):
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
        avg_err = cv.cross_validate(clusterer, distance_metric=dist_metric, window=window)
        errs.append((n_clusts, avg_err, clusterer))
        print('Average error of %f achieved using %d clusters' % (avg_err, n_clusts))
        print()
    return errs

if __name__ == '__main__':
    print('file path: %s' % args.source_path)
    print()

    # Load the clusterers
    clusterers = load(args.source_path)

    print_errors(clusterers)

    plot_errors(clusterers)

    if args.best_n_clusts:
        print('Getting the clusterer for %d clusters' % args.best_n_clusts)
        clusterer = get_clusterer_for_best_n_clusts(clusterers, args.best_n_clusts)
        if not clusterer:
            print('No clusterer found for %d clusters' % args.best_n_clusts)
            sys.exit(1)
        print('Done')
        print()

        assignments, lowest_err = clusterer.get_best_assignment()

        print('Clusters for the best assignment:')
        print_clusters(assignments)

        plot_centroids(assignments)

        plot_clusters(assignments)

        # Cluster temporally within each spatial cluster
        if args.window:
            dist_metric = 'dtw'
        else:
            dist_metric = 'euclidean'
        centroid_id_to_clusterers = sub_cluster(assignments, dist_metric, args.window, args.norm, args.max_iters, args.st)

        to_pickle('sub_clusterers', centroid_id_to_clusterers)
    elif args.print_clusts:
        clusterer = get_clusterer_for_best_n_clusts(clusterers, args.print_clusts)
        if not clusterer:
            print('No clusterer found for %d clusters' % args.print_clusts)
            sys.exit(1)
        print('Done')
        print()

        assignments, lowest_err = clusterer.get_best_assignment()

        print('Clusters:')
        print_clusters(assignments)
