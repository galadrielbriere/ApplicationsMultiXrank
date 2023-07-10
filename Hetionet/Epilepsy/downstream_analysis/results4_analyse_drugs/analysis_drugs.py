#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np

drugs = pd.read_csv('drugs.tsv', sep = '\t', header = None)
drugs_dict = dict()
for k in range(len(drugs)) :
    drugs_dict[drugs[0].iloc[k]] = drugs[1].iloc[k].split(',')
    
drugs_class_dict = dict()
for k in drugs_dict.keys() :
    temp = drugs_dict[k]
    for l in temp :
        if l not in drugs_class_dict :
            drugs_class_dict[l] = [k]
        else :
            drugs_class_dict[l].append(k)

drugs_class_count = dict()
for k in drugs_class_dict.keys() :
    drugs_class_count[k] = len(drugs_class_dict[k])
    
sub_count = [(k,v) for k,v in drugs_class_count.items() if v >= 7]
sub_count = sorted(sub_count, key=lambda x: x[1], reverse = True)


cyt = 'Cytochrome P-450 Substrates'
ana = 'Analgesics'
# ant = 'Antidepressive Agents'
ind = 'Indoles'

cyt_drugs = drugs_class_dict[cyt]
ana_drugs = drugs_class_dict[ana]
# ant_drugs = drugs_class_dict[ant]
ind_drugs = drugs_class_dict[ind]
tot_drugs = (set(cyt_drugs).union(set(ana_drugs))).union(set(ind_drugs))

print(sub_count)
print(len(set(cyt_drugs))) # 23
print(len(set(ana_drugs))) # 16
# print(len(set(ant_drugs)))
print(len(set(ind_drugs))) # 8

print(len(set(tot_drugs))) # 23/26
print(len(set(cyt_drugs).intersection(ana_drugs))) # 13/16
# print(len(set(cyt_drugs).intersection(ant_drugs)))
print(len(set(cyt_drugs).intersection(ind_drugs))) # 5/8


# print(len(set(ana_drugs).intersection(ant_drugs)))
print(len(set(ana_drugs).intersection(ind_drugs))) # 8

# print(len(set(ant_drugs).intersection(ind_drugs)))
