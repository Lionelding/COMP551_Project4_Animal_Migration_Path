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
from interpolation import normalize_time_series
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

if __name__ == '__main__':
    print('file path: %s' % args.source_path)
    print()

    # Load the clusterers
    clusterers = load(args.source_path)

    print('Summary of number of clusters to average error')
    print('n_clusts\tavg_err')
    for n_clusts, err, _ in clusterers:
        print('%d\t%.4f' % (n_clusts, err))
    print()

    # print a cluster
    # best assignment and lowest error for the 6th clusterer (used 6 clusters)
    best_assignment, lowest_err = clusterers[5][2].get_best_assignment()
    for centroid, cluster in best_assignment.iteritems():
        print('Centroid %d: ' % centroid.id, end='')
        print([tso.id for tso, _ in cluster])
        print([tso.year for tso, _ in cluster])
    print('Error: %f' % lowest_err)
    print()



    for _, err in clusterers[5][2].assignments_history:
        print(err)
    print()

    # TODO -- figure out what the best number of clusters is

    # TODO -- for the best number of clusters, get the assignments

    # TODO -- cluster within each cluster temporally!

    # TODO -- analyze the final clusters
