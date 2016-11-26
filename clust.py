'''Clustering example'''
from __future__ import print_function

import numpy as np
import matplotlib.pylab as plt
import random
import sys
sys.path.append('./clustering/')
from ts_cluster import TsCluster

from preprocess import load

if __name__ == '__main__':

    data_obj = load('preprocessed_data/prd.pkl')
    data_by_year = data_obj.get_data_by_year()
    year, indivs = data_by_year[0]

    print('year')
    print(year)
    print('num individuals for the year')
    print(len(indivs))

    data = []
    for indiv_id, pts in indivs:
        data.append(pts)

    data = np.array(data)

    print('Shape data')
    print(data.shape)

    print(data[0])
    print(data[0].shape)
    print(data[1].shape)

    clusterer = TsCluster(4)

    clusterer.k_means_clust(data,4,10,4)

    centroids = clusterer.get_centroids()

    for i in centroids:

        plt.plot(i)

    plt.show()
