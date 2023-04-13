#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import multixrank
import os

pwd = os.path.dirname(os.path.realpath(__file__))
pwd = pwd + '/'
os.chdir(pwd)

multixrank_obj = multixrank.Multixrank(config=pwd+"config_full_param1.yml", wdir=pwd)
ranking_df = multixrank_obj.random_walk_rank()
multixrank_obj.write_ranking(ranking_df, path=pwd+"results_multiXrank_param1_t100", top=100)
multixrank_obj.write_ranking(ranking_df, path=pwd+"results_multiXrank_param1_t200", top=200)
multixrank_obj.write_ranking(ranking_df, path=pwd+"results_multiXrank_param1_t500", top=500)

multixrank_obj = multixrank.Multixrank(config=pwd+"config_full_param2.yml", wdir=pwd)
ranking_df = multixrank_obj.random_walk_rank()
multixrank_obj.write_ranking(ranking_df, path=pwd+"results_multiXrank_param2_t100", top=100)
multixrank_obj.write_ranking(ranking_df, path=pwd+"results_multiXrank_param2_t200", top=200)
multixrank_obj.write_ranking(ranking_df, path=pwd+"results_multiXrank_param2_t500", top=500)

multixrank_obj = multixrank.Multixrank(config=pwd+"config_full_param3.yml", wdir=pwd)
ranking_df = multixrank_obj.random_walk_rank()
multixrank_obj.write_ranking(ranking_df, path=pwd+"results_multiXrank_param3_t100", top=100)
multixrank_obj.write_ranking(ranking_df, path=pwd+"results_multiXrank_param3_t200", top=200)
multixrank_obj.write_ranking(ranking_df, path=pwd+"results_multiXrank_param3_t500", top=500)

multixrank_obj = multixrank.Multixrank(config=pwd+"config_full_param4.yml", wdir=pwd)
ranking_df = multixrank_obj.random_walk_rank()
multixrank_obj.write_ranking(ranking_df, path=pwd+"results_multiXrank_param4_t100", top=100)
multixrank_obj.write_ranking(ranking_df, path=pwd+"results_multiXrank_param4_t200", top=200)
multixrank_obj.write_ranking(ranking_df, path=pwd+"results_multiXrank_param4_t500", top=500)