#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import multixrank
import os

pwd = os.path.dirname(os.path.realpath(__file__))
pwd = pwd + '/'
os.chdir(pwd)

multixrank_obj = multixrank.Multixrank(config=pwd+"config_full_param1.yml", wdir=pwd)
ranking_df = multixrank_obj.random_walk_rank()
multixrank_obj.write_ranking(ranking_df, path=pwd+"results_multiXrank_param1", top=None)

multixrank_obj = multixrank.Multixrank(config=pwd+"config_full_param2.yml", wdir=pwd)
ranking_df = multixrank_obj.random_walk_rank()
multixrank_obj.write_ranking(ranking_df, path=pwd+"results_multiXrank_param2", top=None)

multixrank_obj = multixrank.Multixrank(config=pwd+"config_full_param3.yml", wdir=pwd)
ranking_df = multixrank_obj.random_walk_rank()
multixrank_obj.write_ranking(ranking_df, path=pwd+"results_multiXrank_param3", top=None)

multixrank_obj = multixrank.Multixrank(config=pwd+"config_full_param4.yml", wdir=pwd)
ranking_df = multixrank_obj.random_walk_rank()
multixrank_obj.write_ranking(ranking_df, path=pwd+"results_multiXrank_param4", top=None)
