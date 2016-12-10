'''Load temporal clusterers and learn from them'''

from __future__ import print_function

import logging
import numpy as np
from argparse import ArgumentParser
import sys
from time import time
import os.path
import matplotlib.pylab as plt
from mpl_toolkits.mplot3d import Axes3D

from preprocess import load
from utils import Plottable, plot
sys.path.append('./clustering/')
from ts_cluster import TsClusterer

################################################################################
# logging and options
################################################################################

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(levelname)s %(message)s')

parser = ArgumentParser()
parser.add_argument('source_path', type=str, action='store',
                    help='the filepath of the data source file')

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

def print_all_errors(centroid_id_to_clusterers):
    for centroid_id, clusterers in centroid_id_to_clusterers.iteritems():
        print('-' * 40)
        print('Spatial cluster %d' % centroid_id)
        print('_' * 40)
        print_errors(clusterers)

def get_plottable(clusterers, name):
    for n_clusts, err, _ in clusterers:
        print('%d\t%.4f' % (n_clusts, err))

class TemporalClusteringCandidate(object):
    '''An object to make dealing with the data a bit nicer'''

    def __init__(self, n_clusts, avg_err, clusterer):
        self.n_clusts = n_clusts
        self.avg_err = avg_err
        self.clusterer = clusterer

def reformat(centroid_id_to_clusterers):
    dic = {}
    for spatial_clust_id, cands in centroid_id_to_clusterers.iteritems():
        dic[spatial_clust_id] = []
        for n_clusts, err, clusterer in cands:
            dic[spatial_clust_id].append(TemporalClusteringCandidate(n_clusts, err, clusterer))
    return dic

def get_cand(candidates, n_clusts):
    for cand in candidates:
        if cand.n_clusts == n_clusts:
            return cand
    return None

def get_final_clustering(s_clust_to_t_cands, n_clusts):
    final_clustering = {}
    for spatial_clust_id, temporal_candidates in s_clust_to_t_cands.iteritems():
        final_clustering[spatial_clust_id] = {}
        best_n_clusts = n_clusts[spatial_clust_id]
        cand = get_cand(temporal_candidates, best_n_clusts)
        if cand:
            clusterer = cand.clusterer
            assignments, _ = clusterer.get_best_assignment()
            i = 0
            for _, cluster in assignments.iteritems():
                tsos = [tso for tso, _ in cluster]
                final_clustering[spatial_clust_id][i] = tsos
                i += 1
        else:
            print('Error')
            sys.exit(1)
    return final_clustering

def print_clusters(final_clustering):
    for spatial_clust_id, temporal_clusts in final_clustering.iteritems():
        print('>>>>>>spatial clust %d' % spatial_clust_id)
        for temporal_clust_id, tsos in temporal_clusts.iteritems():
            print('>>>temporal clust %d' % temporal_clust_id)
            for tso in tsos:
                print('%s_%d' % (tso.id, tso.year), end=', ')
            print()

if __name__ == '__main__':
    print('file path: %s' % args.source_path)
    print()

    # Load the clusterers
    centroid_id_to_clusterers = load(args.source_path)

    print_all_errors(centroid_id_to_clusterers)

    # convert to TemporalCandidate objects
    # centroid id really represents a spatial cluster so...
    spatial_cluster_to_temporal_candidates = reformat(centroid_id_to_clusterers)

    # plot all the errors
    plottables = []
    for spatial_clust_id, cands in spatial_cluster_to_temporal_candidates.iteritems():
        n_clusts = []
        errs = []
        for cand in cands:
            n_clusts.append(cand.n_clusts)
            errs.append(cand.avg_err)
        plottables.append(Plottable(n_clusts, errs, 'spatial cluster %d' % spatial_clust_id))

    # plot them one at a time
    for plottable in plottables:
        plot(plottable, 'number of clusters', 'error (avg DTW distance)', 'number of clusters vs. error for temporal clustering in %s' % plottable.name)

    # plot them together
    plot(plottables, 'number of clusters', 'error (avg DTW distance)', legend=True)

    # use two temporal clusters for spatial cluster 0, 1, 2, 4, and 3 for spatial cluster 3

    # get the final clustering
    n_clusts = [2,2,2,3,2]
    final_clustering = get_final_clustering(spatial_cluster_to_temporal_candidates, n_clusts)

    total = 0
    for spatial_clust_id, temporal_clusts in final_clustering.iteritems():
        for temporal_clust_id, tsos in temporal_clusts.iteritems():
            print(len(tsos))
            total += len(tsos)
    print(total)

    print_clusters

    # select two lines in the same temporal cluster and plot them
    one = final_clustering[0][0][2]
    two = final_clustering[0][0][3]
    one.time_normalize()
    two.time_normalize()

    fig = plt.figure()
    ax = fig.gca(projection='3d')

    x = [lon for lon, _, _ in one.normalized_interpolated_series]
    y = [lat for _, lat, _ in one.normalized_interpolated_series]
    z = [time for _, _, time in one.normalized_interpolated_series]
    ax.plot(x, y, z, label='%s_%d' % (one.id, one.year))

    x = [lon for lon, _, _ in two.normalized_interpolated_series]
    y = [lat for _, lat, _ in two.normalized_interpolated_series]
    z = [time for _, _, time in two.normalized_interpolated_series]
    ax.plot(x, y, z, label='%s_%d' % (two.id, two.year))
    ax.set_xlabel('longitude')
    ax.set_ylabel('latitude')
    ax.set_zlabel('time (seconds)')

    ax.legend()
    plt.show()

    # select two lines in the same spatial cluster but different temporal clusters and plot them
    one = final_clustering[0][0][2]
    two = final_clustering[0][1][5]
    one.time_normalize()
    two.time_normalize()

    fig = plt.figure()
    ax = fig.gca(projection='3d')

    x = [lon for lon, _, _ in one.normalized_interpolated_series]
    y = [lat for _, lat, _ in one.normalized_interpolated_series]
    z = [time for _, _, time in one.normalized_interpolated_series]
    ax.plot(x, y, z, label='%s_%d' % (one.id, one.year))

    x = [lon for lon, _, _ in two.normalized_interpolated_series]
    y = [lat for _, lat, _ in two.normalized_interpolated_series]
    z = [time for _, _, time in two.normalized_interpolated_series]
    ax.plot(x, y, z, label='%s_%d' % (two.id, two.year))
    ax.set_xlabel('longitude')
    ax.set_ylabel('latitude')
    ax.set_zlabel('time (seconds)')

    ax.legend()
    plt.show()

    print_clusters(final_clustering)
