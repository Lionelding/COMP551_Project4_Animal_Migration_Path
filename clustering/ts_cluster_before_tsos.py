'''uses dtw package DTW implementation'''
from __future__ import print_function

import matplotlib.pylab as plt
import numpy as np
from numpy.linalg import norm
import random
import sys
sys.path.append('../')
from dtw import dtw

def l1_norm(x, y):
    return norm(x - y, ord=1)

def l2_norm(x, y):
    return norm(x - y)

class TsCluster(object):

    def __init__(self, num_clust, dist_norm, max_iterations, stopping_threshold=1.):
        '''
        num_clust is the number of clusters for the k-means algorithm
        assignments holds the assignments of data points (indices) to clusters
        centroids holds the centroids of the clusters
        '''
        if dist_norm == 1:
            self.dist_norm = l1_norm
        else:
            self.dist_norm = l2_norm
        self.num_clust = num_clust
        self.max_iterations = max_iterations
        self.assignments = {}
        self.centroids = []
        self.stopping_threshold = stopping_threshold

    # Euclidean distance measures -- to be continued TODO -- finish/use this later

    def point_dist(self, x1, x2):
        '''returns the distance between two points in 2d'''
        return math.sqrt((x1[0] - x2[0])**2 + (x1[1] - x2[1])**2)

    def seq_dist(self, s1, s2):
        '''returns the total Euclidean distance between two series'''
        pass

    def error(self):
        '''returns the mean squared error of the assignments with respect to the centroids'''
        total = 0.
        for i, c in enumerate(self.centroids):
            clust = self.assignments[i]
            for s_idx, _ in clust:
                total += seq_dist(self.data[s_idx], c)**2
        return total / self.num_time_series

    # end Euclidean distance stuff

    def get_assignment_error(self):
        '''returns the total assignment error, which is equal to the average DTW distance
        between a time series and its centroid'''
        total = 0.
        for _, cluster in self.assignments.iteritems():
            for _, dist in cluster:
                total += dist
        return total / self.num_time_series

    def print_clusters(self):
        for centroid_idx, clust in self.assignments.iteritems():
            print('Cluster %d:' % centroid_idx, end='')
            print([series_idx for series_idx, _ in clust])

    def detect_oscillation(self, errs):
        if len(errs) < 4:
            return False
        else:
            errs.reverse()
            epsilon = 0.001
            if abs(errs[0] - errs[2]) < epsilon and abs(errs[1] - errs[3]) < epsilon:
                return True
            return False

    # each centroid is a line, rather than a point!!!
    def k_means_clust(self, data, verbose=False):
        '''
        k-means clustering algorithm for time series data.  dynamic time warping Euclidean distance
         used as default similarity measure.
        '''
        self.data = data
        self.num_time_series = len(data)
        self.centroids = random.sample(data, self.num_clust)

        err_hist = [float('inf')]
        for n in range(self.max_iterations):
            if verbose:
                print('iteration ' + str(n + 1))
            # assign data points to clusters
            self.assignments = {}
            # assignments has the following structure:
            # {
            #   centroid_idx: [(idx of a time series, its dist from the centroid), ...]
            # }
            for ind, i in enumerate(data):
                # ind is the data series number, i is the data series
                # define the minimum distance for the data series
                min_dist = float('inf')
                # define the index of the closest centroid
                closest_clust = None
                for c_ind, j in enumerate(self.centroids):
                    # c_ind is the index of the centroid, j is the centroid
                    cur_dist, matrix, path = dtw(i, j, dist=self.dist_norm)
                    if cur_dist < min_dist:
                        min_dist = cur_dist
                        closest_clust = c_ind
                # add the index of the current data series to a cluster
                if closest_clust not in self.assignments:
                    self.assignments[closest_clust] = []
                self.assignments[closest_clust].append((ind, min_dist))

            # print the current clusters status
            if verbose:
                self.print_clusters()

            # calculate the error of the assignment
            curr_err = self.get_assignment_error()

            if verbose:
                print('Average error: %f' % curr_err)
                print()

            err_diff = abs(err_hist[len(err_hist) - 1] - curr_err)
            err_hist.append(curr_err)

            # if the error difference is less than the threshold, then stop
            # else, update centroids and continue
            if err_diff < self.stopping_threshold or self.detect_oscillation(err_hist):
                break

            # now that we've updated the clusters that each series is part of,
            # we recalculate the centroids of the clusters
            for key in self.assignments:
                # key is the index of a centroid in the centroids list
                clust_sum = 0.
                for k, _ in self.assignments[key]:
                    # k is the index of a time series in the current cluster
                    # add the time series to the cluster sum
                    clust_sum = clust_sum + data[k]
                # update each point in the centroid with the average of all points in the cluster of time
                # series around the centroid
                self.centroids[key] = [m / len(self.assignments[key]) for m in clust_sum]

    def get_centroids(self):
        return np.array(self.centroids)

    def get_assignments(self):
        return self.assignments

    def plot_centroids(self):
        for i in self.centroids:
            plt.plot(i)
        plt.show()
