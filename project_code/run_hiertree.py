# -*- coding: utf-8 -*-
"""
Hierarchical clustering
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.cluster.hierarchy import fcluster
from sklearn.metrics import silhouette_score

from preprocess import *
from functions import *
from example_npp import organize
from interpolation import normalize_time_series_objects

def process_data(animal_year, norm_id_to_series):
    lon_lat = dict()
    for i in range(len(animal_year)):
        lon_lat[animal_year[i]] = norm_id_to_series[animal_year[i]]
    
    dist_matrix = create_dist_matrix(animal_year, lon_lat)
    plot_dist_matrix(dist_matrix)
    ytdist, Z = plot_hier_tree(dist_matrix,animal_year)
    K = []
    thr = []
    sil_score = []    
    for t in range(int(np.ceil(np.min(ytdist))),int(np.ceil(np.max(ytdist)))):    
        clusters = fcluster(Z, t, 'distance')
        k = len(set(clusters))
        if k is not 1:
            thr.append(t)
            K.append(k)
            sil_score.append(silhouette_score(dist_matrix, clusters, metric='precomputed'))    
    plt.figure(3)
    plt.plot(K,sil_score)
    plt.xlabel('Clusters')
    plt.ylabel('Silhouette score')
    return dist_matrix

if __name__ == '__main__':        
    ## Dataset
    # get a map of individual id to all its data, ordered by time
    indiv_to_ts = get_data_by_individual('turkey_vultures.csv')
        
    print('Number of individuals')
    print(len(indiv_to_ts))
    print()

    rdr = None
    # optionally define a relative date range, e.g.
    #start = RelativeDate(rdr[0], rdr[1])
    #end = RelativeDate(rdr[2], rdr[3])
    #rdr = RelativeDateRange(start, end)
    
    # get all the time series (splits)
    tsos = get_time_series(indiv_to_ts, rdr)
    print()

    print('Total number of time series')
    print(len(tsos))
    print()

    # organize the series by id
    animal_year,id_to_series = organize(tsos)

    # let's normalize them so that we have one point per day
    interval = 3
    normalize_time_series_objects(tsos, interval, rdr)

    animal_year,norm_id_to_series = organize(tsos, True)    
    
    dist_matrix = process_data(animal_year,norm_id_to_series) 

    
