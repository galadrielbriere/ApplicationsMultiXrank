#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import multixrank
import os

pwd = os.path.dirname(os.path.realpath(__file__))
pwd = pwd + '/'
os.chdir(pwd)

# Run with gene and drug seeds
multixrank_obj = multixrank.Multixrank(config=pwd+"config_full.yml", wdir=pwd)
ranking_df = multixrank_obj.random_walk_rank()
multixrank_obj.write_ranking(ranking_df, path=pwd+"multiXrank_results/", top=None)
multixrank_obj.to_sif(ranking_df, path=pwd+"multiXrank_results/top20.sif", top=20)

# Run with only gene as seed
multixrank_obj = multixrank.Multixrank(config=pwd+"config_full_gene.yml", wdir=pwd)
ranking_df = multixrank_obj.random_walk_rank()
multixrank_obj.write_ranking(ranking_df, path=pwd+"multiXrank_results_gene/", top=None)
multixrank_obj.to_sif(ranking_df, path=pwd+"multiXrank_results_gene/top20.sif", top=20)

# Run with only drug as seed
multixrank_obj = multixrank.Multixrank(config=pwd+"config_full_drug.yml", wdir=pwd)
ranking_df = multixrank_obj.random_walk_rank()
multixrank_obj.write_ranking(ranking_df, path=pwd+"multiXrank_results_drug/", top=None)
multixrank_obj.to_sif(ranking_df, path=pwd+"multiXrank_results_drug/top20.sif", top=20)