import pandas as pd
import numpy as np
import random
import os
path = os.path.dirname(os.path.realpath(__file__))
path = path + '/'
os.chdir(path)

disease_target = pd.read_csv('gene_disease_associations_2014/gene_disease_2014_0.5.gr', sep = '\t', header = None)
num_pos = len(disease_target)

# Twice as many negative associations that will be selected randomly
factor = 2
num_neg = num_pos*factor

bip = pd.read_csv('networks/bipartite/1_2.gr', sep = '\t', header = None)
subset_bip = bip[[0,1]]
bip_tuples = [tuple(x) for x in subset_bip.to_numpy()]

# We don't want to train on associations that could appear in DisGeNet 2020
disgenet_2020 =  pd.read_csv('test_2020associations/pos_associations_2020.tsv', sep = '\t', header = None)
subset_disgenet2020 = disgenet_2020[[0,1]]

disgenet2020_tuples = [tuple(x) for x in subset_disgenet2020.to_numpy()]

skip_tuples = bip_tuples + disgenet2020_tuples

set_prot = set(bip[0])
set_disease = set(bip[1])

compt = 0
list_neg = list()
while (compt < num_neg) :
    prot = random.choice(list(set_prot))
    disease = random.choice(list(set_disease))
    tuple_neg = (prot, disease)
    if (tuple_neg not in skip_tuples) and (tuple_neg not in list_neg) :
        list_neg.append(tuple_neg)
        compt += 1
    if (compt%100 == 0) :
        print(compt)
        
data_neg = pd.DataFrame(list_neg, columns=[0, 1])
data_neg[2] = pd.Series(np.zeros((len(data_neg))), dtype = int)
data_neg.to_csv('neg_training_f' + str(factor) + '.tsv', sep = '\t', header = None, index = False)

data_pos = disease_target[[0,1]]
data_pos[2] = pd.Series(np.ones((len(data_pos))), dtype=int)
data_pos.to_csv('pos_training_f' + str(factor) + '.tsv', sep = '\t', header = None, index = False)

training_data = pd.concat([data_pos, data_neg])
training_data['seed'] = range(len(training_data))
training_data.to_csv('training_f' + str(factor) + '.tsv', sep = '\t', header = None, index = False)


