'''Clustering example'''
from __future__ import print_function
import numpy as np
import matplotlib.pylab as plt
import random
import sys
sys.path.append('./clustering/')
from ts_cluster import TsCluster

if __name__ == '__main__':
    train = np.genfromtxt('datasets/train.csv', delimiter='\t')
    test = np.genfromtxt('datasets/test.csv', delimiter='\t')
    print('Shape train')
    print(train.shape)
    print('Shape test')
    print(test.shape)
    data=np.vstack((train[:,:-1],test[:,:-1]))

    print('Shape data')
    print(data.shape)
    print(data[0])

    clusterer = TsCluster(4)

    clusterer.k_means_clust(data,4,10,4)

    centroids = clusterer.get_centroids()

    for i in centroids:

        plt.plot(i)

    plt.show()
