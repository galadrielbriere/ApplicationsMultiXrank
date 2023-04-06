#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import pandas as pd
import os
import matplotlib.pyplot as plt
path = os.path.dirname(os.path.realpath(__file__))
path = path + '/'
os.chdir(path)

# # Creating autocpt arguments 
# def func(pct): 
#     return "{:.1f}%\n".format(pct) 

result_dirs = [f"merged_results_multiXrank_param{i}_t{j}/" for i in range(1,5) for j in [100, 200, 500]]
article_score = pd.read_csv("Hetionet_prioritization_results/epilepsy_case_study_top100.txt", sep = '\t')
article_score = article_score.reset_index()

for dir in result_dirs:
    RWR_score = pd.read_csv(dir+"multiplex_3.tsv", sep = '\t', header = None)
    RWR_score = RWR_score.reset_index()
    
    # Map Hetionet and MultiXrank top results
    check = pd.merge(RWR_score, article_score, left_on = 2, right_on = 'name')
    check = check[[0, 2, 1, 'index_x', 'prediction', 'index_y', 'category', 'phcodb']]
    check = check.rename(columns={0:'node_id', 1:'MXR_score', 2:'name', 'index_x':'MXR_rank', 'index_y':'Hetionet_rank',
                                  'prediction':'Hetionet_score'})
    check.to_csv(dir+'check.tsv', sep = '\t', header = True, index = False)

    # Get prioritized nodes that don't overlap between Hetionet and MultiXrank
    diff = pd.merge(RWR_score, article_score, left_on = 2, right_on = 'name', how='outer', indicator=True)
    # MultiXrank nodes not prioritized by Hetionet
    mxr_not_in_het = diff.loc[diff['_merge'] == 'left_only'].rename(columns={0:'node_id', 1:'MXR_score', 2:'name', 'index_x':'MXR_rank'})
    mxr_not_in_het = mxr_not_in_het[["node_id", "name", "MXR_score", "MXR_rank"]]
    mxr_not_in_het.to_csv(dir+'MXR_not_in_Hetionet.tsv', sep = '\t', header = True, index = False)
    # Hetionet nodes not prioritized by MultiXrank
    het_not_in_mxr = diff.loc[diff['_merge'] == 'right_only'].rename(columns={0:'node_id', 'prediction':'Hetionet_score', 2:'name', 'index_y':'Hetionet_rank'})
    het_not_in_mxr = het_not_in_mxr[["node_id", "name", "Hetionet_score", "Hetionet_rank"]]
    het_not_in_mxr.to_csv(dir+'Hetionet_not_in_MXR.tsv', sep = '\t', header = True, index = False)

    # AIGD = check[check['category'] == 'AIGD']
    # IGD = check[check['category'] == 'IGD']
    # UNKD = check[check['category'] == 'UNKD']

    # AIGD_rate_RWR = len(AIGD)/len(check)
    # IGD_rate_RWR = len(IGD)/len(check)
    # UNKD_rate_RWR = len(UNKD)/len(check)

    # AIGD_article = article_score[article_score['category'] == 'AIGD']
    # IGD_article = article_score[article_score['category'] == 'IGD']
    # UNKD_article = article_score[article_score['category'] == 'UNKD']

    # AIGD_rate_article = len(AIGD_article)/len(article_score)
    # IGD_rate_article = len(IGD_article)/len(article_score)
    # UNKD_rate_article = len(UNKD_article)/len(article_score)

    # # Article :
    # index_x = ['AIGD', 'IGD', 'UNKD']
    # rate = [AIGD_rate_article,IGD_rate_article,UNKD_rate_article]
    # explode = (0.1, 0.0, 0.2) 
    # colors = ("beige", "lightpink", "silver") 
    # wp = { 'linewidth' : 1, 'edgecolor' : "black" } 

    # fig, ax = plt.subplots(figsize = (10, 7)) 
    # wedges, texts, autotexts = ax.pie(rate,
    #                                 autopct = lambda pct: func(pct), 
    #                                 explode = explode,  
    #                                 labels = index_x, 
    #                                 shadow = False, 
    #                                 colors = colors, 
    #                                 startangle = 0, 
    #                                 wedgeprops = wp, 
    #                                 textprops = dict(color ="black"),
    #                                 normalize=False) 


    # plt.setp(autotexts, size = 8, weight ="bold") 
    # ax.set_title('distribution of (anti)-ictogenic drugs in D.S.Himmelstein et al') 
    # plt.savefig(dir+'distribution_article.png', dpi=500, format = 'png')


    # # predicted
    # index_x = ['AIGD', 'IGD', 'UNKD']
    # rate = [AIGD_rate_RWR,IGD_rate_RWR,UNKD_rate_RWR]
    # explode = (0.1, 0.0, 0.2) 
    # colors = ("beige", "lightpink", "silver") 
    # wp = { 'linewidth' : 1, 'edgecolor' : "black" } 

    # fig, ax = plt.subplots(figsize = (10, 7)) 
    # wedges, texts, autotexts = ax.pie(rate,
    #                                 autopct = lambda pct: func(pct), 
    #                                 explode = explode,  
    #                                 labels = index_x, 
    #                                 shadow = False, 
    #                                 colors = colors, 
    #                                 startangle = 0, 
    #                                 wedgeprops = wp, 
    #                                 textprops = dict(color ="black"),
    #                                 normalize=False) 


    # plt.setp(autotexts, size = 8, weight ="bold") 
    # ax.set_title("distribution of (anti)-ictogenic drugs predicted") 
    # plt.savefig(dir+'distribution_predicted.png', dpi=500, format = 'png')
