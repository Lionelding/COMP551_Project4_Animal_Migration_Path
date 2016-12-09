'''Load temporal clusterers and learn from them'''

from __future__ import print_function

import logging
import numpy as np
from argparse import ArgumentParser
import sys
from time import time
import os.path
import matplotlib.pylab as plt

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
        plot(plottable, 'number of clusters', 'error (avg Euclidean distance)', 'number of clusters vs. error for temporal clustering in %s' % plottable.name)

    # plot them together
    plot(plottables, 'number of clusters', 'error (avg Euclidean distance)', 'number of clusters vs. error for temporal clustering in all spatial clusters')
