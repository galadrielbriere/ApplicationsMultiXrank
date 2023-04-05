#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import pandas as pd
import re
import os
path = os.path.dirname(os.path.realpath(__file__))
path = path + '/'
os.chdir(path)

# Needed to replace "::" with "_" in node names
def replace_double_colon(text):
    return re.sub(r'::', '_', text)

# Get metadata associated to nodes
name = pd.read_csv("../HetionetDB_to_MultiXrankDB/HetionetDB/hetionet-v1.0-nodes.tsv", sep = '\t')
name["mapping_id"] = name["id"].apply(replace_double_colon)

# Read MultiXrank results and map nodes to their metadata in Hetionet
# MultiXrank results are stored in directories starting with search_string in search_dir
search_dir = "../"
search_string = "results_multiXrank_param"

# Loop through directories in search_dir and search for search_string to get multiXrank results
for dirpath, dirnames, filenames in os.walk(search_dir):
    for dirname in dirnames:
        if dirname.startswith(search_string):
            dir_path = os.path.join(dirpath, dirname)
            dest_path = os.path.join("./", "merged_"+dirname)
            os.makedirs(dest_path, exist_ok=True)
            files_in_dir = os.listdir(dir_path)
            for filename in files_in_dir:
                file_path = os.path.join(dir_path, filename)
                dest_file_path = os.path.join(dest_path, filename)

                # Map node names to multiXrank results
                temp = pd.read_csv(file_path, sep = '\t', header = 0)
                merge = pd.merge(temp, name, left_on = "node", right_on = 'mapping_id')
                # Write results
                merge[["node", "score", 'name']].to_csv(dest_file_path, sep = '\t', header = None, index = False)
                
