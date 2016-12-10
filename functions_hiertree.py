# -*- coding: utf-8 -*-
"""
Functions for hierarchical clustering
"""
import numpy as np
from numpy.linalg import norm
import matplotlib.pyplot as plt
from matplotlib import cm as cm
from dtw import dtw
from scipy.cluster.hierarchy import linkage
from scipy.cluster.hierarchy import dendrogram
from scipy.spatial.distance import pdist

def create_dist_matrix(animal_id, lat_lon):   
    dist_matrix = np.zeros((len(animal_id),len(animal_id)))
    for ind1 in range(0,len(animal_id)):
        migration1 = lat_lon[animal_id[ind1]]
        migration1 = np.asarray(migration1, dtype='float64')
        for ind2 in range(ind1+1,len(animal_id)):
            if animal_id[ind1] != animal_id[ind2]:
                migration2 = lat_lon[animal_id[ind2]]
                migration2 = np.asarray(migration2, dtype='float64')
                distance, matrix, path = dtw(migration1, migration2, dist=lambda migration1, migration2: norm(migration1 - migration2, ord=1))
                dist_matrix[ind1][ind2] = distance
                dist_matrix[ind2][ind1] = distance
    
    return dist_matrix
    
def plot_dist_matrix(df):
    fig = plt.figure()
    ax1 = fig.add_subplot(111)
    cmap = cm.get_cmap('Spectral', 30)
    cax = ax1.imshow(df, interpolation="nearest", cmap=cmap)    
    ax1.grid(False)
    plt.title('Similarity',fontsize=20)    
    fig.colorbar(cax)
    plt.show()

def plot_hier_tree(dist_matrix,animal_year):
    ytdist = pdist(dist_matrix)
    Z = linkage(ytdist, 'complete')
    plt.figure(2)
    dendrogram(Z, distance_sort='ascending', show_leaf_counts=True, labels=animal_year,orientation='right')    
    return ytdist, Z

def plot_migrations(animal1,animal2, lon_lat, animal_year):
    migration1 = lon_lat[animal_year[animal1]]
    migration1 = np.asarray(migration1, dtype='float64')
    migration2 = lon_lat[animal_year[animal2]]
    migration2 = np.asarray(migration2, dtype='float64')
 
    plt.figure(1);plt.subplot(1,2,1); plt.plot(migration1[:,0],migration1[:,1]);plt.plot(migration2[:,0],migration2[:,1])
    distance, matrix, path = dtw(migration1, migration2, dist=lambda migration1, migration2: norm(migration1 - migration2, ord=1))
    print('\ndistance = %f' % distance)
    plt.subplot(1,2,2); plt.plot(path[0],path[1])