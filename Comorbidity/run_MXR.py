#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import multixrank
import pandas as pd
import networkx as nx
import numpy as np
import shutil
import os
path = os.path.dirname(os.path.realpath(__file__))
path = path + '/'
os.chdir(path)

disease = pd.read_csv('disease_set.tsv', sep = '\t', header = None)
tissue = ['Ery', 'Mac0', 'MK', 'Mon', 'nB', 'nCD4', 'nCD8', 'Neu']

os.makedirs('results', exist_ok = True)
for i in range(len(disease)) :
    print(disease)
    os.makedirs('results/' + str(i), exist_ok = True)
    for j in range(len(tissue)) :
        print(tissue)
        file = open(tissue[j] + '/seeds.txt', 'w+')
        file.write(disease[1].iloc[i])
        file.close()
        newpath = path + tissue[j]
        multixrank_obj = multixrank.Multixrank(config = newpath + "/config_full.yml", wdir = newpath)
        ranking_df = multixrank_obj.random_walk_rank()
        multixrank_obj.write_ranking(ranking_df, path = newpath + "/output")
        original = newpath + '/output'
        target = path + 'results/' + str(i) + '/' + tissue[j]
        shutil.move(original,target)
        os.chdir(path)
        
