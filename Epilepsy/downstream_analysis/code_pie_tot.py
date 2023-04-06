#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import os
path = os.path.dirname(os.path.realpath(__file__))
path = path + '/'
os.chdir(path)

article = pd.read_csv("Hetionet_prioritization_results/epilepsy_case_study_top100.txt", sep = '\t', header = None)
top100 = pd.read_csv("merged_results_multiXrank_param4_t100/check.tsv", sep = '\t', header = None)
top200 = pd.read_csv("merged_results_multiXrank_param4_t200/check.tsv", sep = '\t', header = None)
top500 = pd.read_csv("merged_results_multiXrank_param4_t500/check.tsv", sep = '\t', header = None)

AIGD_article = article[article[5] == 'AIGD']
IGD_article = article[article[5] == 'IGD']
UNKD_article = article[article[5] == 'UNKD']

AIGD_rate_article = len(AIGD_article)
IGD_rate_article = len(IGD_article)
UNKD_rate_article = len(UNKD_article)


AIGD_100 = top100[top100[6] == 'AIGD']
IGD_100 = top100[top100[6] == 'IGD']
UNKD_100 = top100[top100[6] == 'UNKD']

AIGD_rate_top100 = len(AIGD_100)
IGD_rate_top100 = len(IGD_100)
UNKD_rate_top100 = len(UNKD_100)


AIGD_200 = top200[top200[6] == 'AIGD']
IGD_200 = top200[top200[6] == 'IGD']
UNKD_200 = top200[top200[6] == 'UNKD']

AIGD_rate_top200 = len(AIGD_200) - AIGD_rate_top100
IGD_rate_top200 = len(IGD_200) - IGD_rate_top100
UNKD_rate_top200 = len(UNKD_200) - UNKD_rate_top100


AIGD_500 = top500[top500[6] == 'AIGD']
IGD_500 = top500[top500[6] == 'IGD']
UNKD_500 = top500[top500[6] == 'UNKD']

AIGD_rate_top500 = len(AIGD_500) - len(AIGD_200)
IGD_rate_top500 = len(IGD_500) - len(IGD_200)
UNKD_rate_top500 = len(UNKD_500) - len(UNKD_200)

AIGD_rate_end = len(AIGD_article) -len(AIGD_500)
IGD_rate_end = len(IGD_article) - len(IGD_500)
UNKD_rate_end = len(UNKD_article) -len(UNKD_500)

# Creating autocpt arguments 
def func(pct, allvalues): 
    return "{:.0f}\n".format(pct) 

# Article :
index_x = [str(len(AIGD_article)), str(len(IGD_article)), str(len(UNKD_article))]
rate = [AIGD_rate_article,IGD_rate_article,UNKD_rate_article]
colors = ("#FAF7F3", "#FFB6C1", "#C4C4C4") 

index_y = [str(len(AIGD_100)), str(len(AIGD_200)), str(len(AIGD_500)),'',\
           str(len(IGD_100)), str(len(IGD_200)), str(len(IGD_500)),'',\
           str(len(UNKD_100)), str(len(UNKD_200)), str(len(UNKD_500)),'',]
    
label_y = ['AIGD','AIGD top100', 'AIGD top200' , 'AIGD top500',\
           'IGD','IGD top100', 'IGD top200', 'IGD top500',\
           'UNKD','UNKD top100', 'UNKD top200', 'UNKD top500']
rate_y = [AIGD_rate_top100, AIGD_rate_top200, AIGD_rate_top500, AIGD_rate_end,\
          IGD_rate_top100, IGD_rate_top200, IGD_rate_top500, IGD_rate_end,\
          UNKD_rate_top100, UNKD_rate_top200, UNKD_rate_top500, UNKD_rate_end]

colors_y = ("#FAF0E6", "#f4e1d3", "#f0d7c5", "#f7f7f7",\
         "#ff9ea7", "#ff8492", "#ff6479", "#f7f7f7",\
         "#AFAFAF", "#9E9E9E", "#7E7E7E", "#f7f7f7")



bigger = plt.pie(rate, labels=index_x, colors=colors,
                 startangle=0, frame=True, textprops={'fontsize': 8})
smaller = plt.pie(x = rate_y, labels=index_y,
                  colors=colors_y, radius=0.7,
                  startangle=0, labeldistance=1.1, textprops={'fontsize': 5})
centre_circle = plt.Circle((0, 0), 0.4, color='white', linewidth=0)
fig = plt.gcf()
centre_circle
plt.axis('equal')


color_label = ["#FAF7F3", "#FAF0E6", "#f4e1d3", "#f0d7c5",\
         "#FFB6C1","#ff9ea7", "#ff8492", "#ff6479",\
          "#C4C4C4", "#AFAFAF", "#9E9E9E", "#7E7E7E"]

list_patch = list()
for k in range(len(label_y)) :
    patch = mpatches.Patch(color = color_label[k], label = label_y[k])
    list_patch.append(patch)
    
plt.title('distribution of (anti)-ictogenic drugs : parameters 4', fontsize=10) 
plt.legend(handles=list_patch, loc = 1, fontsize =  'xx-small')
plt.savefig('distribution_article_param4.png', dpi=500, format = 'png')
