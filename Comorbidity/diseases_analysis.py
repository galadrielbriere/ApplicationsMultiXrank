#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA as sklearnPCA
from sklearn.cluster import SpectralClustering
from sklearn.cluster import AgglomerativeClustering
from sklearn.cluster import KMeans
from sklearn.manifold import TSNE
import umap
import pandas as pd
import glob
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import os 
import colorcet as cc
path = os.path.dirname(os.path.realpath(__file__))
path = path + '/results/'
os.chdir(path)

def tsne(heat) :
    sklearn_tsne = TSNE(n_components = 2, perplexity=10, random_state=123).fit_transform(heat)
    return sklearn_tsne
    
    
def umap_fonc(heat) :
	trans = umap.UMAP(n_components = 2, n_neighbors=10, min_dist=0.15, random_state=123).fit_transform(heat)
	return trans

def kmeans_cluster(sklearn_data, n, name) :
    index = [i for i in range(len(sklearn_data))]
    kmeans = KMeans(n_clusters=n, random_state=0).fit(sklearn_data)
    clusters = kmeans.labels_
    df = pd.DataFrame(dict(x=sklearn_data[:,0], y=sklearn_data[:,1], label=clusters))
    # colors = {0:'red', 1:'blue', 2:'green', 3:'orange', 4:'purple', 5:'gold', 6:'grey', 7:'pink',\
    #           8:'navy', 9:'springgreen', 10:'salmon', 11:'skyblue', 12:'tan', 13:'sienna',\
    #           14:'turquoise', 15:'teal', 16:'chartreuse', 17:'crimson', 18:'fuchsia', 19:'beige',\
    #           20:'yellow', 21:'aqua', 22:'olivedrab', 23:'deeppink', 24:'maroon', 25:'mistyrose',\
    #           26:'seagreen', 27:'darkorange', 28:'mediumpurple', 29:'khaki'}
    palette = sns.color_palette(cc.glasbey, n_colors=30)
    plt.figure(figsize=(8, 6))
    fig, ax = plt.subplots()
    grouped = df.groupby('label')
    for key, group in grouped:
        group.plot(ax=ax, kind='scatter', x='x', y='y', label = 'cluster ' + str(key), color=palette[key])
    plt.legend(prop={'size':4})
    plt.rc('xtick', labelsize=6) 
    plt.rc('ytick', labelsize=6) 
    plt.xlabel('Component 1', fontsize = 10)
    plt.ylabel('Component 2', fontsize = 10)
    for i in range(len(sklearn_data[:,0])) :
         ax.annotate(index[i], (sklearn_data[i,0], sklearn_data[i,1]), fontsize = 5)
    plt.savefig(name + '.svg', format ='svg', dpi=1200)
    plt.close()
    return clusters


def analysis_tsne(heat, n_clus, name) :
    Y_sklearn = tsne(heat)
    kmeans_cluster(Y_sklearn, n_clus, name)


def analysis_umap(heat, n_clus, name) :
    Y_sklearn = umap_fonc(heat)
    kmeans_cluster(Y_sklearn, n_clus, name)
    
    
list_heat = list()

for omic in ['tad', 'fragment', 'protein', 'disease']:
    data = np.load('integrated_mxr_scores/disease_dist_' + omic + '.npy')
    list_heat.append(data)
    analysis_tsne(data, 30, 'plots/'+omic+'_tsne_diseases')
    analysis_umap(data, 30, 'plots/'+omic+'_tsne_diseases')

full_data = np.concatenate(list_heat, axis = 1)
analysis_tsne(full_data, 30, "plots/integrated_tsne_diseases")
analysis_umap(full_data, 30, "plots/integrated_umap_diseases")
