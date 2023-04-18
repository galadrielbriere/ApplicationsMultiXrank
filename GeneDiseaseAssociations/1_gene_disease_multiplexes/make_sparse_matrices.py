#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import pandas as pd
import scipy as sp
import itertools
import os
import glob

path = os.path.dirname(os.path.realpath(__file__))
path = path + '/'
os.chdir(path)
    
def split_size(tot_size, piece) :
    num = int(tot_size/piece)
    size = round(((tot_size/piece) - num)*piece)
    piece_size = [piece for i in range(num)]
    piece_size.append(size)
    return piece_size


def define_sparse_matrix(piece_size, num_multi, label) :
    try : 
        os.makedirs('results_sparse')
    except OSError : 
        pass
    label[3] = '('+label[0]+','+label[1]+')'
    list_nodes = list()
    for k in range(num_multi) :
        temp = list(pd.read_csv('results/seeds_0/multiplex_' + str(list_net[k]) + '.tsv', sep = '\t').set_index('node').sort_index().index)
        list_nodes.append(temp)
    index = list(itertools.chain(*list_nodes))
    for i in range(len(piece_size)) :
        list_rwr = [list() for i in range(num_multi)]
        colname = list(label[3])[i*piece_size[i]:(i+1)*piece_size[i]]
        data_rwr = pd.DataFrame(columns=colname)
        for j in range(piece_size[i]) :
            for l in range(num_multi) :
                temp = pd.read_csv('results/seeds_' + str((i)*piece_size[i] + j)  + '/multiplex_' + str(list_net[l]) + '.tsv', sep = '\t')
                temp = temp.set_index('node')
                temp = temp.sort_index()
                list_rwr[l].append(temp)  
        for k in range(piece_size[i]) :
            data_rwr[colname[k]] = pd.concat([list_rwr[l][k] for l in range(num_multi)])['score']
        data_rwr = data_rwr.T
        data_rwr_sparse = sp.sparse.csr_matrix(data_rwr.values).astype(float)
        sp.sparse.save_npz('results_sparse/data_rwr_sparse_' + str(i), data_rwr_sparse)
        del data_rwr_sparse
    return index


def read_sparse_matrix():
    num = len(glob.glob('results_sparse/*.npz'))
    list_sparse = list()
    for i in range(num) :
        temp = sp.sparse.load_npz('results_sparse/data_rwr_sparse_' + str(i) + '.npz')
        list_sparse.append(temp)
    data = sp.sparse.vstack([i for i in list_sparse])
    del list_sparse
    return data

list_net = ['protein', 'disease']
tot_size = int(len(glob.glob('results/*')))
piece = 600
num_multi = len(list_net)
piece_size = split_size(tot_size, piece)
label = pd.read_csv('training.tsv', sep = '\t', header = None)

define_sparse_matrix(piece_size, num_multi, label) 