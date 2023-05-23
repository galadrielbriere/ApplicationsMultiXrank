#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import pandas as pd
import os

path = os.path.dirname(os.path.realpath(__file__))
path = path + '/'
os.chdir(path)

original_bipartite = pd.read_table("networks/bipartite/1_2_prop0.gr", header=None)
original_bipartite.columns = ["gene", "disease", "score"] 

last_bipartite = pd.read_table("gene_disease_associations_2020/gene_disease_2020.tsv", header=None)
last_bipartite = last_bipartite[[1,0,2]]
last_bipartite.columns = ["gene", "disease", "score"] 

uncovered = pd.merge(original_bipartite, last_bipartite, on=["gene", "disease"], how="right", indicator=True)
uncovered = uncovered[["gene","disease", "score_y"]]
uncovered.columns = ["gene", "disease", "score"] 


for prop in range(10,80,10):
    keep = uncovered.sample(n=round(len(uncovered)*prop/100))
    new_bip = pd.concat([original_bipartite, keep])
    new_bip.to_csv("networks/bipartite/1_2_prop"+str(prop)+".gr", sep="\t", index=False, header=False)