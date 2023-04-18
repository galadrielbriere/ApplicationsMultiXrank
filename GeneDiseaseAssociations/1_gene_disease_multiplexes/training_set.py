import pandas as pd
import numpy as np
import random
import os
path = os.path.dirname(os.path.realpath(__file__))
path = path + '/'
os.chdir(path)

disease_target = pd.read_csv('gene_disease_associations_2014/gene_disease_2014_0.5.gr', sep = '\t', header = None)
num_pos = len(disease_target)
factor = 1
num_neg = num_pos*factor

bip = pd.read_csv('networks/bipartite/1_2.gr', sep = '\t', header = None)
subset = bip[[0,1]]
bip_tuples = [tuple(x) for x in subset.to_numpy()]

set_prot = set(bip[0])
set_disease = set(bip[1])


compt = 0
list_neg = list()
while (compt < num_neg) :
    prot = random.choice(list(set_prot))
    disease = random.choice(list(set_disease))
    tuple_neg = (prot, disease)
    if (tuple_neg not in bip_tuples) and (tuple_neg not in list_neg) :
        list_neg.append(tuple_neg)
        compt += 1
    if (compt%100 == 0) :
        print(compt)
        
data_neg = pd.DataFrame(list_neg, columns=[0, 1])
data_neg[2] = pd.Series(np.zeros((len(data_neg))), dtype = int)
data_neg.to_csv('neg_training.tsv', sep = '\t', header = None, index = False)

data_pos = disease_target[[0,1]]
data_pos[2] = pd.Series(np.ones((len(data_pos))), dtype=int)
data_pos.to_csv('pos_training.tsv', sep = '\t', header = None, index = False)

training_data = pd.concat([data_pos, data_neg])
training_data.to_csv('training.tsv', sep = '\t', header = None, index = False)


