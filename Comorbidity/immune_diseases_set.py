#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import pandas as pd
import networkx as nx
import numpy as np
import os
path = os.path.dirname(os.path.realpath(__file__))
path = path + '/'
os.chdir(path)

disease = pd.read_csv('autoimmune_disease.txt', sep = '\t', header = None)
disease_net = pd.read_csv('diseases_monoplex_no_self_loop.tsv', sep = '\t', header = None)
list_disase_net = list(set(disease_net[0]).union(set(disease_net[1])))

sub_disease = disease[disease[1].isin(list_disase_net)]
sub_disease.to_csv('disease_set.tsv', sep  = '\t', header = None, index = False)
