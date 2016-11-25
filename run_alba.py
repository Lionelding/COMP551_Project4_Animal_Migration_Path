# -*- coding: utf-8 -*-
"""
Created on Mon Nov 21 20:32:18 2016

@author: Alba
"""

import numpy as np
from numpy.linalg import norm
import matplotlib.pyplot as plt
from matplotlib import cm as cm
from dtw import dtw

from preprocess import preprocess

def plot_dist_matrix(df):

    fig = plt.figure()
    ax1 = fig.add_subplot(111)
    cmap = cm.get_cmap('Spectral', 30)
    cax = ax1.imshow(df, interpolation="nearest", cmap=cmap)    
    ax1.grid(False)
    plt.title('Similarity',fontsize=20)    
    ticks = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24]    
    plt.xticks(ticks, fontsize=12)
    plt.yticks(ticks, fontsize=12)
    fig.colorbar(cax)
    #plt.savefig('dist.pdf', format='pdf', bbox_inches='tight')
    plt.show()

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

def plot_migrations(animal1,animal2):
    migration1 = lat_lon[animal_id[animal1]]
    migration1 = np.asarray(migration1, dtype='float64')
    migration2 = lat_lon[animal_id[animal2]]
    migration2 = np.asarray(migration2, dtype='float64')
 
    plt.figure(1);plt.subplot(1,2,1); plt.plot(migration1[:,0],migration1[:,1]);plt.plot(migration2[:,0],migration2[:,1])
    distance, matrix, path = dtw(migration1, migration2, dist=lambda migration1, migration2: norm(migration1 - migration2, ord=1))
    print('\ndistance = %f' % distance)
    plt.subplot(1,2,2); plt.plot(path[0],path[1])

if __name__ == '__main__':        
    ## Data
    df = preprocess("Common_eider_preproc.csv", [2,3,4,28])
    df_2000 = [row for row in df if '2000' in row[0]]
    
    animal_id = []
    lat_lon = dict()
    for row in df_2000:
        if row[3] in lat_lon and float(row[1])<0:
            lat_lon[row[3]].append([row[1],row[2]])
        elif float(row[1])<0:
            animal_id.append(row[3])
            lat_lon[row[3]] = [[row[1],row[2]]]
    
    dist_matrix_2000 = create_dist_matrix(animal_id, lat_lon)
    plot_dist_matrix(dist_matrix_2000)
    plot_migrations(1,2)