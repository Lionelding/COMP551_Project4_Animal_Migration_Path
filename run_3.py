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
from utils import make_all_plottable
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

if __name__ == '__main__':
    print('file path: %s' % args.source_path)
    print()

    # Load the clusterers
    centroid_id_to_clusterers = load(args.source_path)

    print_all_errors(centroid_id_to_clusterers)

    # TODO implement windowing for euclidean distance -- well, this is dynamic time warping (with windowing)!!!
    # Try temporal clustering using windowing :) (augment run_2 to allow for windowing as an option - will need to
    # modify k_means_clust so that windowing is an option)

    # TODO -- analyze the final clusters
    # i.e. print some graphs!!!
