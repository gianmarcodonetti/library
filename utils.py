# -*- coding: utf-8 -*-
"""
Created on Wed Jul 20 10:41:33 2016

@author: Giammi
"""

import time
import numpy as np
import matplotlib.pyplot as plt
from math import radians, cos, sin, asin, sqrt
from scipy.spatial.distance import euclidean
import itertools

def showExecTime(startPoint, initialString = "", verbose=True):
    """
    Compute the execution time from an initial starting point.
    You can also pass me a string to print out at the end of computation.
    
    Parameters
    ----------
    startPoint : float, timestamp of the starting point
    initialString : string to output on the console, before the execution time
    
    Returns
    -------
    endPoint - startPoint, the difference between the two timestamps
    """
    eex = time.time()
    seconds = round(eex - startPoint, 2)
    minutes = (seconds/60)
    hours = int(minutes/60)
    minutes = int(minutes % 60)
    seconds = round(seconds % 60, 2)
    if verbose:
        print("\n- "+initialString+" Execution time: %sh %sm %ss -" % (hours, minutes, seconds))
    return eex - startPoint

def haversine(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance between two points 
    on the earth (specified in decimal degrees).
    
    Parameters
    ----------
    lon1, lat1 : float, longitude and latitude of the first point
    lon2, lat2 : float, longitude and latitude of the second point
    
    Returns
    -------
    km : float, the distance between the two points, expressed in kilometers
    """
    # convert decimal degrees to radians 
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    # haversine formula 
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    km = 6367 * c
    return km

def manhattan_distance(cell1, cell2):
    """
    Parameters
    ----------
    cell1 : 2d tuple-like, the first cell in a 2-dimensional grid
    cell2 : 2d tuple-like, the second cell in a 2-dimensional grid
    
    Returns
    -------
    distance = horizontal steps + vertical steps, the total number of steps
    in order to get from cell1 to cell2 (or viceversa)
    """
    hor_steps = np.abs(cell1[0] - cell2[0])
    ver_steps = np.abs(cell1[1] - cell2[1])
    return hor_steps + ver_steps

def no_points_close_to_me(me, points, radius = 100):
    """
    Parameters
    ----------
    me : tuple-like, the coordinates of the considered point
    points : list-like of tuple-like, all the other point in the world
    radius : the radius where 'me' should be alone
    
    Returns
    -------
    result : true if the point is alone, false otherwise    
    """
    result = True
    number_of_close_points = 0
    for p in points:
        dist = np.linalg.norm(me - p)
        if dist <= radius:
            number_of_close_points += 1
    if number_of_close_points > 1:
        result = False    
    return result


def cluster_most_representative(cluster, center, field, n=1):
    """
    Find the most representative element in the cluster,
    in terms of euclidean distance from the center
    
    Parameters
    ----------
    cluster: list-like, set of all the elements in the cluster. Each element must be a dictionary
    center: center of the cluster above
    field: string, the key for obtaining the values used for the clustering
    n: default 1, number of representatives per cluster
    
    Returns
    -------
    element: the closest n elemente in the cluster to the center
    """    
    all_tuples = [] # will contain each element with its distance from the center
    for elem in cluster:
        dist = euclidean(elem[field], center)
        all_tuples.append((elem, dist))
    all_tuples = sorted(all_tuples, key = lambda x: x[1])
    most_representatives = [tup[0] for tup in all_tuples]
    return most_representatives[:n]
    

def compare_clusters(c1, c2):
    """
    Compare two different labellings on the same set of elements.
    Take into account only the co-appearing elements if there are some problems.
    
    Parameters
    ----------
    c1: first labelling, list of dict. Each dict should contain the name and the label
    c2: second labelling, as above
    
    Returns
    -------
    new_c1, new_c2: the new labellings (only the second could be modified)
    matchings: the name of such elements that are matching between the two clusterings
    accuracy: the accuracy between the two different labellings
    re_label: a dictionary for the renaming of the labels in the second clustering
    """
    # Mantain only the co-occurring names
    names_c1, names_c2 = [elem['name'] for elem in c1], [elem['name'] for elem in c2]
    c1 = [elem for elem in c1 if elem['name'] in names_c2]
    c2 = [elem for elem in c2 if elem['name'] in names_c1]
    labels = set([elem['label'] for elem in c2])
    # Evaluate each permutation
    permutations = itertools.permutations(labels)
    result = []
    for permutation in permutations:
        re_label = {}
        # Map for the new labelling
        for l in range(len(labels)):
            re_label[l] = permutation[l]
        matchings = 0
        for label in labels:
            from_c1 = [elem['name'] for elem in c1 if elem['label'] == label]
            from_c2 = [elem['name'] for elem in c2 if re_label[elem['label']] == label]
            matchings += len(set(from_c1) & set(from_c2))
        result.append({'permutation': permutation, 'matchings': matchings})
    # Get the best permutation
    best = [r for r in result if r['matchings'] == max([r['matchings'] for r in result])][0]
    re_label = {}
    for l in range(len(labels)):
        re_label[l] = best['permutation'][l]
    # Rebuild the second cluster
    c2 = [{'name': elem['name'], 'label': re_label[elem['label']]} for elem in c2]
    matchings = []
    for e1 in c1:
        label = e1['label']
        name = e1['name']
        for e2 in c2:
            if name == e2['name'] and label == e2['label']:
                matchings.append(name)
    # Returns the labellings, the matchings, the accuracy, and the renaming dictionary
    return (c1, c2, matchings, best['matchings']/len(c1), re_label)


def plot_confusion_matrix(cm, classes, normalize=False, title="",
                          cmap=plt.cm.Blues, cluster_names=['First', 'Second']):
    """
    This function prints and plots the confusion matrix.
    Normalization can be applied by setting `normalize=True`.
    """
    accuracy = sum(cm.diagonal())/sum([sum(row) for row in cm])
    plt.imshow(cm, interpolation='nearest', cmap=cmap)
    if title:
        plt.title(title + "\nAccuracy "+str(round(accuracy*100, 2))+"%")
    plt.colorbar()
    tick_marks = np.arange(len(classes))
    plt.xticks(tick_marks, classes)
    plt.yticks(tick_marks, classes)

    if normalize:
        cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
        print("Normalized confusion matrix")
    else:
        print('Confusion matrix, without normalization')

    print(cm)

    thresh = cm.max() / 2.
    for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
        plt.text(j, i, cm[i, j],
                 horizontalalignment="center",
                 color="white" if cm[i, j] > thresh else "black")

    plt.ylabel(cluster_names[0]+' cluster label')
    plt.xlabel(cluster_names[1]+' cluster label')
    plt.tight_layout()
    pass


def test_compare_cluster():
    """ Testing the function compare_clusters() """
    import os, pickle
    workspace = 'C:/Users/Giammi/OneDrive/Università/TESI/'
    os.chdir(workspace)    
    
    
    """ TEST 1.1 : Time VS Geo """
    time = open('./time_response/clustering/all_ftest.pickle', 'rb')
    all_ftest = pickle.load(time)
    accuracy = {}
    for PC in [2, 3, 4, 5, 6, 7, 8, 9, 10, 21, 42]:
        geo = open('./geo_response/clustering/all_features_final_map_PC'+str(PC)+'.pickle', 'rb')
        all_features = pickle.load(geo)
        
        c1 = [{'name': elem['brand'], 'label': elem['label']} for elem in all_ftest]
        c2 = [{'name': elem['name'], 'label': elem['label']} for elem in all_features]
        
        accuracy[PC] = compare_clusters(c1, c2)[3]
    
    
    """ TEST 1.2 : Location VS Summary """
    location = open('./geo_response/clustering/all_features_location_time.pickle', 'rb')
    location = pickle.load(location)
    summary = open('./brand_summary/all_features_brand_summary_PC2.pickle', 'rb')
    summary = pickle.load(summary)
    
    c1 = [{'name': elem['name'], 'label': elem['label']} for elem in location]
    c2 = [{'name': elem['name'], 'label': elem['label']} for elem in summary]
    
    compare_clusters(c1, c2)[3]
    
    
    """ TEST 1.3 : all together """
    PC = 6
    geo = open('./geo_response/clustering/all_features_final_map_PC'+str(PC)+'.pickle', 'rb')
    all_features = pickle.load(geo)
    
    c1 = [{'name': elem['brand'], 'label': elem['label']} for elem in all_ftest]
    c2 = [{'name': elem['name'], 'label': elem['label']} for elem in summary]
    compare_clusters(c1, c2)[3]
    
    
    """ TEST 2 """
    c1 = [
            {'name' : 'A', 'label': 0},
            {'name' : 'B', 'label': 0},
            {'name' : 'C', 'label': 1},
            {'name' : 'D', 'label': 1},
            {'name' : 'E', 'label': 2},
            {'name' : 'F', 'label': 2},
            {'name' : 'G', 'label': 3},   
            {'name' : 'H', 'label': 3},
            {'name' : 'I', 'label': 3}, 
    ]
    c2 = [
            {'name' : 'A', 'label': 1},
            {'name' : 'B', 'label': 1},
            {'name' : 'C', 'label': 2},
            {'name' : 'D', 'label': 2},
            {'name' : 'E', 'label': 3},
            {'name' : 'F', 'label': 3},
            {'name' : 'G', 'label': 0},   
            {'name' : 'H', 'label': 0},
            {'name' : 'I', 'label': 0}, 
    ]
    result = compare_clusters(c1, c2)
    assert(len(result[2]) == len(c1) and result[3] == 1)
    
    
    
    """ TEST 3 """
    c2 = [
            {'name' : 'A', 'label': 2},
            {'name' : 'B', 'label': 2},
            {'name' : 'C', 'label': 0},
            {'name' : 'D', 'label': 0},
            {'name' : 'E', 'label': 1},
            {'name' : 'F', 'label': 1},
            {'name' : 'G', 'label': 1},   
            {'name' : 'H', 'label': 3},
            {'name' : 'I', 'label': 3}, 
    ]
    result = compare_clusters(c1, c2)
    assert(len(result[2]) == len(c1) - 1 and result[3] == (len(c2)-1)/len(c1))
    
    
    
    """ TEST 4 """
    c1 = [
            {'name' : 'A', 'label': 0},
            {'name' : 'B', 'label': 0},
            {'name' : 'C', 'label': 1},
            {'name' : 'D', 'label': 1},
    ]
    c2 = [
            {'name' : 'A', 'label': 1},
            {'name' : 'B', 'label': 1},
            {'name' : 'C', 'label': 0},
            {'name' : 'D', 'label': 0},
    ]
    result = compare_clusters(c1, c2)
    assert(len(result[2]) == len(c1) and result[3] == (len(c2))/len(c1))
    
    # Exit the test case
    pass


