#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from sklearn.cluster import KMeans
from sklearn.manifold import TSNE
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import os 
import colorcet as cc
from adjustText import adjust_text
from mvlearn.cluster import MultiviewSpectralClustering

path = os.path.dirname(os.path.realpath(__file__))
path = path + '/results/'
os.chdir(path)

def multiview_clustering_tsne(heat_list, n, name) :

    # Multiview Clustering on the 4 node-type specific similarity matrices
    m_spectral = MultiviewSpectralClustering(n_clusters=n,
                                         affinity='nearest_neighbors',
                                         random_state=42)
    clusters = m_spectral.fit_predict(heat_list)

    # tSNE projection on the concatenation of the similarity matrices
    tsne_proj = TSNE(n_components = 2, perplexity=10, random_state=123).fit_transform(np.concatenate(heat_list, axis = 1))

    # Map the multiview clusters to the projection
    index = [i for i in range(len(tsne_proj))]
    df = pd.DataFrame(dict(x=tsne_proj[:,0], y=tsne_proj[:,1], label=clusters))

    # Plot the tSNE projection and use cluster labels as color
    palette = sns.color_palette(sns.color_palette("colorblind"), n_colors=n)
    plt.figure(figsize=(8, 6))
    fig, ax = plt.subplots()
    grouped = df.groupby('label')
    for key, group in grouped:
        group.plot(ax=ax, kind='scatter', x='x', y='y', label = 'Cluster ' + str(key), color=palette[key])
    plt.legend(prop={'size':4})
    plt.rc('xtick', labelsize=6) 
    plt.rc('ytick', labelsize=6) 
    plt.xlabel('Component 1', fontsize = 10)
    plt.ylabel('Component 2', fontsize = 10)
    annotations = [ax.annotate(index[i], (tsne_proj[i,0], tsne_proj[i,1]), fontsize = 7) for i in range(len(tsne_proj[:,0]))]
    adjust_text(annotations)
    plt.savefig(name + '.svg', format ='svg', dpi=1200)
    plt.close()

    return clusters

list_heat = list()

for omic in ['tad', 'fragment', 'protein', 'disease']:
    data = np.load('integrated_mxr_scores/disease_dist_' + omic + '.npy')
    list_heat.append(data)

# Cluster and project
spectral = multiview_clustering_tsne(list_heat, 3, "plots/spectralMultiView_tSNE_clustering_3")

# Save results
seeds = pd.read_csv('../disease_set.tsv', sep = '\t', header = None)
seeds['Spectral'] = spectral
seeds.columns = ["Name", "Id", "SpectralMultiView"]
seeds.to_csv('spectralMultiView_tSNE_clustering_3.tsv', sep  = '\t', header = True, index = False)

