#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
import random
import os
import glob
path = os.path.dirname(os.path.realpath(__file__))
path = path + '/'
os.chdir(path)

# Load novel gene disease associations
novel = pd.read_csv('gene_disease_associations_2014_2020/novel_associations.tsv', sep = '\t', header = 0)

# Load depreciated gene disease associations
depreciated = pd.read_csv('gene_disease_associations_2014_2020/depreciated_associations.tsv', sep = '\t', header = 0)

# Load training associations
training = pd.read_csv('../training_f2.tsv', sep = '\t', header = None)
training.columns = ["gene", "disease", "association", "num"] 

# Extract only a subset that are in the protein multiplex and disease multiplex
disease = pd.read_csv('networks/multiplex/2/new_disease.gr', sep = '\t', header = None)
set_disease = set(disease[0]).union(set(disease[1]))
path_prot = glob.glob('networks/multiplex/1/*gr')
set_prot = set()
for k in path_prot :
    temp = pd.read_csv(k, sep = '\t', header = None)
    set_temp = set(temp[0]).union(set(temp[1]))
    set_prot = set_prot.union(set_temp)

novel_in_graph = novel[(novel['gene'].isin(set_prot)) & (novel['disease'].isin(set_disease))]
novel_in_graph.loc[:, 'association'] = 1

# All associations already considered (in training.tsv or in novel_in_graph)
all_assoc = pd.concat([novel_in_graph[['gene', "disease"]], training[['gene', "disease"]]])
all_assoc = [tuple(x) for x in all_assoc.to_numpy()]

# Sample negative associations
factor = 1
num_neg = len(novel_in_graph)*factor
compt = 0
list_neg = list()
while (compt < num_neg) :
    prot = random.choice(list(set_prot))
    disease = random.choice(list(set_disease))
    tuple_neg = (prot, disease)
    if (tuple_neg not in all_assoc):
        list_neg.append(tuple_neg)
        compt += 1
    if (compt%1000 == 0) :
        print(compt)
        
neg_assoc = pd.DataFrame(list_neg, columns=[0, 1])
neg_assoc[2] = pd.Series(np.zeros((len(neg_assoc))), dtype = int)
neg_assoc.columns = ["gene", "disease", "association"]

# Save positive and negative sets
novel_in_graph[['gene', "disease", "association"]].to_csv('pos_associations_2020.tsv', sep = '\t', header = None, index = False)
neg_assoc.to_csv('neg_associations_2020.tsv', sep = '\t', header = None, index = False)
training_data_2020 = pd.concat([novel_in_graph, neg_assoc])
training_data_2020[['gene', "disease", "association"]].to_csv('test_set_2020.tsv', sep = '\t', header = None, index = False)