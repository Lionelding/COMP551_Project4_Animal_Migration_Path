'''Clustering example'''
from __future__ import print_function

import numpy as np
import matplotlib.pylab as plt
import random
import sys
sys.path.append('./clustering/')
from ts_cluster1 import TsCluster
from numpy.linalg import norm

from preprocess import load
from interpolation import normalize_time_series

if __name__ == '__main__':

    data_obj = load('preprocessed_data/prd.pkl')
    data_by_year = data_obj.get_data_by_year()
    year, indivs = data_by_year[0]

    print('year')
    print(year)
    print('num individuals for the year')
    print(len(indivs))
    print()

    tss = []
    for indiv_id, pts in indivs:
        tss.append(pts)

    # normalize the series
    normd_tss = normalize_time_series(tss)

    print('Shape of normalized data')
    print(normd_tss.shape)
    print()

    # extract just the lat and lon coordinates
    ptss = []
    for pts in normd_tss:
        ptss.append([pt[:2] for pt in pts])

    ptss = np.array(ptss)

    print('Shape of data without time')
    print(ptss.shape)
    print()

    clusterer = TsCluster(4)

    clusterer.k_means_clust(ptss, 4, progress=True)

    centroids = clusterer.get_centroids()

    for i in centroids:

        plt.plot(i)

    plt.show()
