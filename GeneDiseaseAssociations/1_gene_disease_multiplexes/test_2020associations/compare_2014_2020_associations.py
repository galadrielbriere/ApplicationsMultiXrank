#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import pandas as pd
import os

path = os.path.dirname(os.path.realpath(__file__))
path = path + '/'
os.chdir(path)
try : 
    os.mkdir('gene_disease_associations_2014_2020/')
except OSError : 
    pass

a2020 = pd.read_table("gene_disease_associations_2020/gene_disease_2020_0.5.gr", header=None)
a2020.columns = ["gene", "disease", "s2020"] 

a2014 = pd.read_table("../gene_disease_associations_2014/gene_disease_2014_0.5.gr", header=None)
a2014.columns = ["gene", "disease", "s2014"] 

# Find common associations
com_df = pd.merge(a2014, a2020, on=["gene", "disease"])
com_df[["gene", "disease", "s2014", "s2020"]].to_csv("gene_disease_associations_2014_2020/common_associations.tsv", sep="\t", index=False, header=True)

# Find depreciated associations
removed_df = pd.merge(a2014, a2020, on=["gene", "disease"], how="left", indicator=True)
removed_df = removed_df[removed_df["_merge"] == "left_only"]
removed_df = removed_df.drop(columns=["s2020", "_merge"])
removed_df.to_csv("gene_disease_associations_2014_2020/depreciated_associations.tsv", sep="\t", index=False, header=True)

# Find novel associations
new_df = pd.merge(a2020, a2014, on=["gene", "disease"], how="left", indicator=True)
new_df = new_df[new_df["_merge"] == "left_only"]
new_df = new_df.drop(columns=["s2014", "_merge"])
new_df[["gene", "disease", "s2020"]].to_csv("gene_disease_associations_2014_2020/novel_associations.tsv", sep="\t", index=False, header=True)
