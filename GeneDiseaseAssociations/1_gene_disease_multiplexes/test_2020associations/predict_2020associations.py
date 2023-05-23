#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from sklearn import metrics
import pandas as pd
import numpy as np
import scipy as sp
import itertools
import pickle
import os
import logging
import re
import glob
import multiprocessing as mp

path = os.path.dirname(os.path.realpath(__file__))
path = path + '/'
os.chdir(path)

logging.basicConfig(filename='results_models_SVM_GB_RF_2020associations_all.log', level=logging.INFO)


def split_size(tot_size, piece) :
    num = int(tot_size/piece)
    size = round(((tot_size/piece) - num)*piece)
    piece_size = [piece for i in range(num)]
    piece_size.append(size)
    return piece_size


def define_sparse_matrix(prop, piece_size, num_multi, list_net, label) :
    try : 
        os.makedirs('results_sparse_' + str(prop))
    except OSError : 
        pass
    label[3] = '('+label[0]+','+label[1]+')'
    list_nodes = list()
    for k in range(num_multi) :
        temp = list(pd.read_csv('results_prop' + str(prop) + '/seeds_0/multiplex_' + str(list_net[k]) + '.tsv', sep = '\t').set_index('node').sort_index().index)
        list_nodes.append(temp)
    index = list(itertools.chain(*list_nodes))
    for i in range(len(piece_size)) :
        list_rwr = [list() for i in range(num_multi)]
        colname = list(label[3])[i*piece_size[i]:(i+1)*piece_size[i]]
        data_rwr = pd.DataFrame(columns=colname)
        for j in range(piece_size[i]) :
            for l in range(num_multi) :
                temp = pd.read_csv('results_prop' + str(prop) + '/seeds_' + str((i)*piece_size[i] + j)  + '/multiplex_' + str(list_net[l]) + '.tsv', sep = '\t')
                temp = temp.set_index('node')
                temp = temp.sort_index()
                list_rwr[l].append(temp)  
        for k in range(piece_size[i]) :
            data_rwr[colname[k]] = pd.concat([list_rwr[l][k] for l in range(num_multi)])['score']
        data_rwr = data_rwr.T
        data_rwr_sparse = sp.sparse.csr_matrix(data_rwr.values).astype(float)
        sp.sparse.save_npz('results_sparse_' + str(prop) + '/data_rwr_sparse_' + str(i), data_rwr_sparse)
        del data_rwr_sparse
    return index


def read_sparse_matrix(prop):
    num = len(glob.glob('results_sparse_' + str(prop) + '/*.npz'))
    list_sparse = list()
    for i in range(num) :
        temp = sp.sparse.load_npz('results_sparse_' + str(prop) + '/data_rwr_sparse_' + str(i) + '.npz')
        list_sparse.append(temp)
    data = sp.sparse.vstack([i for i in list_sparse])
    del list_sparse
    return data

def get_classif_metrics(y_test, y_pred):
    accuracy = metrics.accuracy_score(y_test, y_pred)
    balanced_accuracy = metrics.balanced_accuracy_score(y_test, y_pred)
    f1_score = metrics.f1_score(y_test, y_pred)
    tn, fp, fn, tp = metrics.confusion_matrix(y_test, y_pred).ravel()
    m_dict = {"accuracy": accuracy, "balanced_accuracy": balanced_accuracy, "f1_score": f1_score, 
              "tp": tp, "fp": fp, "tn": tn, "fn":fn}
    return m_dict

def predict(k):
    filename = path_classifier[k]

    pattern = r"GB"
    match_GB = re.search(pattern, filename)

    clf = pickle.load(open(filename,'rb'))
    X_processed = X

    if match_GB:
        X_processed = X_processed.toarray()

    y_pred = clf.predict(X_processed)

    quality = get_classif_metrics(y, y_pred)
    
    return(path_classifier[k], quality)
    
for prop in range(1):
    list_net = ['protein', 'disease']
    tot_size = int(len(glob.glob('results_prop' + str(prop) + '/*')))
    piece = 600
    num_multi = len(list_net)
    piece_size = split_size(tot_size, piece)

    label = pd.read_csv('test_set_2020.tsv', sep = '\t', header = None)

    index = define_sparse_matrix(prop, piece_size, num_multi, list_net, label)
    X = read_sparse_matrix(prop)
    y = label[2]
    y[0:int(len(y)/2)] = pd.Series(np.ones(int(len(y)/2)), dtype = int)


    path_classifier = sorted(glob.glob('../classifiers_f2_SVM_GB_RF/*.sav'))
    size = len(path_classifier)

    num_cpu = 5
    p = mp.Pool(processes=num_cpu)
    results = p.map(predict, [k for k in range(size)])  

    logging.info(f'########### Results for proportion = {prop}')
    for k in range(len(results)):
        logging.info(f'####### {results[k][0]} \t {results[k][1]}')
        print(f'####### {results[k][0]} \t {results[k][1]}')