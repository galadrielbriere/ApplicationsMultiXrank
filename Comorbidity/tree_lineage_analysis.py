#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA as sklearnPCA
from sklearn.cluster import SpectralClustering
from sklearn.cluster import AgglomerativeClustering
from sklearn.cluster import KMeans
import pandas as pd
import numpy as np
import os
import glob
import seaborn as sns
import matplotlib.pyplot as plt
import scipy.stats as sps
import multiprocessing

path = os.path.dirname(os.path.realpath(__file__))
path = path + '/results/'
os.chdir(path)


# # This was just for checking the Latex formula is ok
# def ranked_with_check(data1, data2) :
#     dist = 0
#     dis1 = list(data1[0])
#     dis2 = list(data2[0])
#     dico_rk1 = dict()
#     dico_dis1 = dict()
#     dico_rk2 = dict()
#     dico_dis2 = dict()
#     for k in range(len(data1)) :
#         dico_rk1[data1[0][k]] = k
#         dico_dis1[data1[0][k]] = data1[1][k]
#     for k in range(len(data2)) :
#         dico_rk2[data2[0][k]] = k
#         dico_dis2[data2[0][k]] = data2[1][k]
#     for k in range(min(len(dis1), len(dis2))) : 
#         if (dis1[k] in dico_rk2.keys()) and (dis2[k] in dico_rk1.keys()) :
#             if (dico_rk1[dis1[k]]!=k):
#                 print(dico_rk1[dis1[k]])
#                 print(k)
#                 break
#             if (dico_rk2[dis2[k]]!=k):
#                 print(dico_rk2[dis2[k]])
#                 print(k)
#                 break
#             if dico_rk1[dis1[k]]!= dico_rk2[dis2[k]]:
#                 print(dico_rk1[dis1[k]])
#                 print(dico_rk2[dis2[k]])
#             if ((dico_rk1[dis1[k]]+dico_rk2[dis2[k]]+1)/2)!=((2*k+1)/2):
#                 print((dico_rk1[dis1[k]]+dico_rk2[dis2[k]]+1)/2)
#                 print((2*k+1)/2)
#                 break
#             dist1 = abs(dico_rk1[dis1[k]] - dico_rk2[dis1[k]])
#             dist2 = abs(dico_rk1[dis2[k]] - dico_rk2[dis2[k]])
#             dist += np.sqrt(dist1**2 + dist2**2)*(1/(((dico_rk1[dis1[k]]+dico_rk2[dis2[k]]+1)/2)**2))
#         elif (dis1[k] not in dico_rk2.keys()) and (dis2[k] in dico_rk1.keys()) :
#             dist1 = 0
#             dist2 = abs(dico_rk1[dis2[k]] - dico_rk2[dis2[k]])
#             dist += np.sqrt(dist1**2 + dist2**2)*(1/(((dico_rk1[dis1[k]]+dico_rk2[dis2[k]]+1)/2)**2))
#         elif (dis1[k] in dico_rk2.keys()) and (dis2[k] not in dico_rk1.keys()) :
#             dist1 = abs(dico_rk1[dis1[k]] - dico_rk2[dis1[k]])
#             dist2 = 0
#             dist += np.sqrt(dist1**2 + dist2**2)*(1/(((dico_rk1[dis1[k]]+dico_rk2[dis2[k]]+1)/2)**2))
#         elif (dis1[k] not in dico_rk2.keys()) and (dis2[k] not in dico_rk1.keys()) :
#             dist1 = 0
#             dist2 = 0
#             dist += 0    
#     return dist

def ranked(data1, data2) :
    dist = 0
    dis1 = list(data1[0])
    dis2 = list(data2[0])
    dico_rk1 = dict()
    dico_dis1 = dict()
    dico_rk2 = dict()
    dico_dis2 = dict()
    for k in range(len(data1)) :
        dico_rk1[data1[0][k]] = k
        dico_dis1[data1[0][k]] = data1[1][k]
    for k in range(len(data2)) :
        dico_rk2[data2[0][k]] = k
        dico_dis2[data2[0][k]] = data2[1][k]
    for k in range(min(len(dis1), len(dis2))) : 
        if (dis1[k] in dico_rk2.keys()) and (dis2[k] in dico_rk1.keys()) :
            dist1 = abs(dico_rk1[dis1[k]] - dico_rk2[dis1[k]])
            dist2 = abs(dico_rk1[dis2[k]] - dico_rk2[dis2[k]])
            dist += np.sqrt(dist1**2 + dist2**2)*(1/(((dico_rk1[dis1[k]]+dico_rk2[dis2[k]]+1)/2)**2))
        elif (dis1[k] not in dico_rk2.keys()) and (dis2[k] in dico_rk1.keys()) :
            dist1 = 0
            dist2 = abs(dico_rk1[dis2[k]] - dico_rk2[dis2[k]])
            dist += np.sqrt(dist1**2 + dist2**2)*(1/(((dico_rk1[dis1[k]]+dico_rk2[dis2[k]]+1)/2)**2))
        elif (dis1[k] in dico_rk2.keys()) and (dis2[k] not in dico_rk1.keys()) :
            dist1 = abs(dico_rk1[dis1[k]] - dico_rk2[dis1[k]])
            dist2 = 0
            dist += np.sqrt(dist1**2 + dist2**2)*(1/(((dico_rk1[dis1[k]]+dico_rk2[dis2[k]]+1)/2)**2))
        elif (dis1[k] not in dico_rk2.keys()) and (dis2[k] not in dico_rk1.keys()) :
            dist1 = 0
            dist2 = 0
            dist += 0    
    return dist

def calculate_heat(i, data, k, full_res):
    res = []
    for j in range(i,disease) :
        res.append(ranked(data[i,k], data[j,k]))
    full_res[str(i)] = res

def tot(heat):
    heat_tot = 0
    for k in range(len(heat)) :
        heat_tot += heat[k]**2
    heat_tot = np.sqrt(heat_tot)
    return heat_tot
        
        
def pca(heat) :
    heat_std = StandardScaler().fit_transform(heat)
    sklearn_pca = sklearnPCA(n_components = len(heat))
    Y_sklearn = np.round(sklearn_pca.fit_transform(heat_std), 3)
    percentage = np.round(sklearn_pca.explained_variance_[0:2]/np.sum(sklearn_pca.explained_variance_),3)
    return Y_sklearn[:,0:2],percentage


def plot_pca(Y_sklearn, name, percentage, index) :
    colors = ['#ff0000ff' if index[i] in ["nB",'nCD4', 'nCD8'] else '#0000ffff' for i in range(len(Y_sklearn))]
    with plt.style.context('seaborn-whitegrid'):
        plt.figure(figsize=(8, 6))
        plt.scatter(Y_sklearn[:,0],Y_sklearn[:,1], c=colors, s=70)
        plt.xlabel('Principal Component 1 : ' + str(round(percentage[0]*100,3)) + '%', fontsize=20)
        plt.ylabel('Principal Component 2 : ' + str(round(percentage[1]*100,3)) + '%', fontsize=20)
        plt.legend(loc='lower center')
        plt.tight_layout()
        for i in range(len(Y_sklearn[:,0])) :
            x = Y_sklearn[i, 0]
            y = Y_sklearn[i, 1]
            text_x = x + 0.2  
            text_y = y + 0.2  
            plt.annotate(index[i], (Y_sklearn[i,0], Y_sklearn[i,1]), c="black", fontsize=20, 
                         xytext=(text_x, text_y), textcoords='offset points')
        plt.savefig(name + '.svg', format='svg', dpi=1200)
        plt.show() 


# def kmeans_cluster(Y_sklearn, n, name, percentage, index) :
#     kmeans = KMeans(n_clusters=n, random_state=0).fit(Y_sklearn)
#     clusters = kmeans.labels_
#     df = pd.DataFrame(dict(x=Y_sklearn[:,0], y=Y_sklearn[:,1], label=clusters))
#     colors = {0:'red', 1:'blue', 2:'green', 3:'orange', 4:'purple', 5:'gold', 6:'grey', 7:'pink',\
#               8:'navy', 9:'springgreen', 10:'salmon', 11:'skyblue', 12:'tan', 13:'sienna',\
#               14:'turquoise', 15:'teal', 16:'chartreuse', 17:'crimson', 18:'fuchsia', 19:'beige',\
#               20:'yellow', 21:'aqua', 22:'olivedrab', 23:'deeppink', 24:'maroon', 25:'mistyrose',\
#               26:'seagreen', 27:'darkorange', 28:'mediumpurple', 29:'khaki'}
#     plt.figure(figsize=(8, 6))
#     fig, ax = plt.subplots()
#     grouped = df.groupby('label')
#     for key, group in grouped:
#         group.plot(ax=ax, kind='scatter', x='x', y='y', label = 'cluster ' + str(key), color=colors[key])
#     plt.legend(prop={'size':8})
#     plt.rc('xtick', labelsize=6) 
#     plt.rc('ytick', labelsize=6) 
#     plt.xlabel('Principal Component 1 : ' + str(round(percentage[0]*100,3)) + '%', fontsize = 10)
#     plt.ylabel('Principal Component 2 : ' + str(round(percentage[1]*100,3)) + '%', fontsize = 10)
#     for i in range(len(Y_sklearn[:,0])) :
#          ax.annotate(index[i], (Y_sklearn[i,0], Y_sklearn[i,1]), fontsize = 6)
#     plt.savefig(name + '.svg', format ='svg', dpi=1200)
#     plt.close()
#     return clusters


# def analysis_disease(heat, n_clus, index, name) :
#     heat_df = pd.DataFrame(heat, columns = index, index = index)
#     cent = (np.min(heat) + np.max(heat))/2
#     sns.set(font_scale=1.4)
#     fig, ax = plt.subplots(figsize=(11, 9))
#     cmap = sns.diverging_palette(230, 20, as_cmap=True)
#     sns.heatmap(heat_df, cmap=cmap, vmin = np.min(heat), vmax = np.max(heat), center = cent, \
#                 square=True, linewidths=.5, cbar_kws={"shrink": .5})
#     fig.savefig(name + "_heatmap_disease.svg", dpi = (600), format = 'svg')
#     sns.set(font_scale=1)
#     Y_sklearn, per = pca(heat)
#     plot_pca(Y_sklearn, name + '_heat_pca_disease', per, index)
#     kmeans_cluster(Y_sklearn, n_clus, name + '_heat_kmeans_disease', per, index)
#     plt.close()
    
    
def analysis_tissue(heat, n_clus, index, name) :
    heat_df = pd.DataFrame(heat, columns = index, index = index)
    cent = (np.min(heat) + np.max(heat))/2
    sns.set(font_scale=1.4)
    fig, ax = plt.subplots(figsize=(11, 9))
    cmap = sns.diverging_palette(230, 20, as_cmap=True)
    sns.heatmap(heat_df, cmap=cmap, vmin = np.min(heat), vmax = np.max(heat), center = cent, \
                square=True, linewidths=.5, cbar_kws={"shrink": .5})
    # fig.savefig(name + "_heatmap_tissue.svg", dpi = (600), format = 'svg')
    sns.set(font_scale=1)
    Y_sklearn, per = pca(heat)
    plot_pca(Y_sklearn, name + '_cells_pca', per, index)
    # kmeans_cluster(Y_sklearn, n_clus, name + '_heat_kmeans_tissue', per, index)
    plt.close()

def calculate_correlation(pair):
    i, j = pair
    list_temp = []
    for k in range(disease):
        temp = sps.pearsonr(list_heat[i][k, :], list_heat[j][k, :])
        list_temp.append(temp[0])
    corr = np.mean(list_temp)
    return i, j, corr

def calculate_correlation2(pair, list_heat):
    i, j = pair
    list_temp = []
    for k in range(len(list_heat)):
        temp = sps.pearsonr(list_heat[k][i, :], list_heat[k][j, :])
        list_temp.append(temp[0])
    corr = np.mean(list_temp)
    return corr


multi = ['tad', 'disease', 'protein', 'fragment']
# Correspondance between multi name and number of multiplex in multilayer network
dict_multi = {multi[0] : 3, multi[1] : 4, multi[2] : 1, multi[3] : 2}

disease = 131
disease_index = [i for i in range(disease)]
tissue = ['Ery', 'Mac0', 'MK', 'Mon', 'nB', 'nCD4', 'nCD8', 'Neu']

list_cors = list()

os.makedirs("integrated_mxr_scores", exist_ok=True)
os.makedirs("plots", exist_ok=True)

for h in range(len(multi)) :
    data = np.zeros((disease, len(tissue)), dtype = object)
    print(multi[h],dict_multi[multi[h]])
    for k in range(disease) :
        for l in range(len(tissue)) :
            name = str(k) + '/' + tissue[l] + '/' + 'multiplex_' + str(dict_multi[multi[h]]) + '.tsv'
            temp = pd.read_csv(name, sep = '\t')
            temp = temp.drop('multiplex', axis=1)
            temp = temp.rename(columns={'node': 0, 'score': 1})
            data[k,l] = temp[[0,1]]
            
    list_heat = list()
    for k in range(len(tissue)) :
        print(tissue[k])
        manager = multiprocessing.Manager()
        full_res = manager.dict()
        jobs = []
        for i in range(disease):
            p = multiprocessing.Process(target=calculate_heat, args=(i, data, k, full_res))
            jobs.append(p)
            p.start()
    
        for proc in jobs:
            proc.join()
        
        results = [full_res[str(j)] for j in range(disease)]
        
        heat = np.zeros((disease, disease))
        for i, row in enumerate(results):
            row_length = len(row)
            heat[i, i:i+row_length] = row
        print(heat)

        heat = heat + heat.T - np.diag(heat.diagonal())

        print(heat)        
        list_heat.append(heat)
        np.save('integrated_mxr_scores/disease_dist_' + multi[h] + '_' + tissue[k], heat)
        
        
    final_heat = tot(list_heat)
    np.save('integrated_mxr_scores/disease_dist_' + multi[h], final_heat)
    # analysis_disease(final_heat, 4, disease_index, multi[h])
    
    corrmatrix = np.zeros((len(tissue), len(tissue)))
    tissue_pairs = [(i, j) for i in range(len(tissue)) for j in range(i, len(tissue))]

    # Use a Pool of worker processes for parallel processing
    with multiprocessing.Pool(20) as pool:  # You can adjust the number of processes as needed
        results = pool.map(calculate_correlation, tissue_pairs)

    # Fill the correlation matrix using the results
    for i, j, corr in results:
        corrmatrix[i, j] = corr
        corrmatrix[j, i] = corr

    np.save('integrated_mxr_scores/cells_corrmatrix_' + multi[h], corrmatrix)
    analysis_tissue(corrmatrix, 4, tissue, "plots/"+multi[h])

    list_cors.append(corrmatrix)

final_corrmatrix = np.zeros((len(tissue),len(tissue)))
tissue_pairs = [(i, j) for i in range(len(tissue)) for j in range(i, len(tissue))]

for pair in tissue_pairs:
    i, j = pair
    corr=calculate_correlation2(pair, list_cors)
    final_corrmatrix[i,j] = corr
    final_corrmatrix[j,i] = final_corrmatrix[i,j]

analysis_tissue(final_corrmatrix, 4, tissue, "plots/all_integrated")
