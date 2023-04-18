#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import multiprocessing as mp
import multixrank as mxk
import pandas as pd
import numpy as np
import os
import glob
import subprocess

path = os.path.dirname(os.path.realpath(__file__))
path = path + '/'
os.chdir(path)
try : 
    os.mkdir('seeds')
    os.mkdir('parameters')
    os.mkdir('results')
except OSError : 
    pass


def mxrank(k) :
    print(str(k) + '\n')
    multixrank_obj = mxk.Multixrank(config = "parameters/config_full_" + str(k) + ".yml", wdir = path)
    ranking = multixrank_obj.random_walk_rank()
    multixrank_obj.write_ranking(ranking, path = "results/seeds_" + str(k))

def new_bipartite(training_data, k):
    # For the kth pair of seed, create a specific bipartite network without bipartite relation between the seed nodes
    original_bipartite = "networks/bipartite/1_2.gr"
    out_bipartite = 'networks/bipartite/1_2_seeds_' + str(k) + '.gr' 
    gene = training_data.iloc[k][0]
    disease = training_data.iloc[k][1]
    sed_command = "sed '/%s\t%s/d' %s > %s" % (str(gene), str(disease), original_bipartite, out_bipartite)
    subprocess.call(sed_command, shell=True)

def create_parameters(k, path) : 
    r = 0.7
    eta = [1/2, 1/2]
    lamb = np.array([[0.5,0.5],\
            [0.5,0.5]])
    delta1 = 0.5
    delta2 = 0
    tau = [[1/3, 1/3, 1/3],
           [1]]
    file = open(path + 'parameters/' + 'config_full_' + str(k) + '.yml','w')
    file.write('seed: seeds/seeds_' + str(k) + '.txt' + '\n')
    file.write('self_loops: 1' + '\n')
    file.write('r: ' + str(r) + '\n')
    file.write('eta: ' + '[{},{}]'.format(eta[0],eta[1]) + '\n')
    file.write('lamb:' + '\n' + '    ' + \
               '- [{},{}]'.format(lamb[0,0], lamb[0,1]) + '\n' + '    '  + \
               '- [{},{}]'.format(lamb[1,0], lamb[1,1]) + '\n')
    file.write('multiplex:' + '\n' + '    ')
    file.write('protein:' + '\n' + '        ' + \
                       'layers:' + '\n' + '            ' + \
                           '- networks/multiplex/1/new_PPI.gr' + '\n' + '            ' + \
                           '- networks/multiplex/1/Complexes.gr' + '\n' + '            ' + \
                           '- networks/multiplex/1/Reactome.gr' + '\n' + '        ' + \
                        'delta: {}'.format(delta1) + '\n' + '        ' + \
                        'graph_type: ' + '[00, 00, 00]' + '\n' + '        ' + \
                        'tau: ' + str(tau[0]) + '\n')
    file.write('    ' + 'disease:' + '\n' + '        ' + \
                       'layers:' + '\n' + '            ' + \
                           '- networks/multiplex/2/new_disease.gr' + '\n' + '        ' + \
                        'delta: {}'.format(delta2) + '\n' + '        ' + \
                        'graph_type: ' + '[00]' + '\n' + '        ' + \
                        'tau: ' + str(tau[1]) + '\n')
    file.write('bipartite: ' + '\n' + '    ' + \
               'networks/bipartite/1_2_seeds_' + str(k) + '.gr: ' + '{source: protein, target: disease, graph_type: 01}')
    file.close
    
    
training_data = pd.read_csv('training.tsv', sep = '\t', header = None)
for k in range(len(training_data)) :
    file = open('seeds/seeds_' + str(k) + '.txt','w')
    file.write(training_data.iloc[k][0] + '\n' + training_data.iloc[k][1])
    file.close() 
    new_bipartite(training_data, k)
    
size = len(glob.glob("seeds/*.txt"))
for k in range(size) :
    create_parameters(k, path)
num_cpu = 20
p = mp.Pool(processes=num_cpu)
p.map(mxrank, [i for i in range(size)])  

