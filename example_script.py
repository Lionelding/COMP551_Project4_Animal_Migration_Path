'''example script that uses preprocessed data'''
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
    if 'preprocessed_data/' in args.source_path:
        parser.error('The file %s does not exist' % args.source_path)
        sys.exit(1)
    else:
        # try appending preprocessed_data/
        args.source_path = 'preprocessed_data/' + args.source_path
        if not os.path.exists(args.source_path):
            parser.error('The file %s does not exist' % args.source_path)
            sys.exit(1)

print(__doc__)
parser.print_help()
print()

if __name__ == '__main__':
    print('file path: %s' % args.source_path)
    print()

    data = load(args.source_path)

    data_by_year = data.get_data_by_year()
    print('num years')
    print(len(data_by_year))
    year_0, indivs = data_by_year[0]

    print('year')
    print(year_0)
    print('number of indiviuals')
    print(len(indivs))
    indiv_0, pts = indivs[0]
    print('individual')
    print(indiv_0)
    print('shape of path')
    print(pts.shape)

    tss = []
    for individual_id, individual_data in indivs:
        tss.append(individual_data)

    # print the data prior to normalization
    ptss = []
    for ts in tss:
        ptss.append(([pt[0] for pt in ts], [pt[1] for pt in ts]))

    # plot one path
    plt.plot(ptss[0][0], ptss[0][1])

    plt.show()

    # plot all paths
    for lats, lons in ptss:
        plt.plot(lats, lons)

    plt.show()

    # now we can normalize
    normd_tss = normalize_time_series(tss)

    # lets plot the paths to see how they look

    # remove time from the paths
    ptss = []
    for ts in tss:
        ptss.append(([pt[0] for pt in ts], [pt[1] for pt in ts]))

    # plot one path
    plt.plot(ptss[0][0], ptss[0][1])

    plt.show()

    # plot all paths
    for lats, lons in ptss:
        plt.plot(lats, lons)

    plt.show()
