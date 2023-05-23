#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from sklearn.ensemble import RandomForestClassifier, HistGradientBoostingClassifier
from sklearn.linear_model import SGDClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline
from sklearn.model_selection import train_test_split
from sklearn import metrics
import pandas as pd
import scipy as sp
from multiprocessing import Pool
import pickle
import os
import glob
import logging

path = os.path.dirname(os.path.realpath(__file__))
path = path + '/'
os.chdir(path)

factor = 2
classifiers_dir = 'classifiers_f' + str(factor) + '_SVM_GB_RF'
results_sparse_dir = 'results_sparse_f' + str(factor) 

logging.basicConfig(filename='results_f' + str(factor) + '_models_SVM_GB_RF.log', level=logging.INFO)

try : 
    os.mkdir(classifiers_dir)
except OSError : 
    pass

def read_sparse_matrix():
    num = len(glob.glob(results_sparse_dir + '/*.npz'))
    list_sparse = list()
    for i in range(num) :
        temp = sp.sparse.load_npz(results_sparse_dir + '/data_rwr_sparse_' + str(i) + '.npz')
        list_sparse.append(temp)
    data = sp.sparse.vstack([i for i in list_sparse])
    del list_sparse
    return data

def get_classif_metrics(y_test, y_pred):
    accuracy = metrics.accuracy_score(y_test, y_pred)
    balanced_accuracy = metrics.balanced_accuracy_score(y_test, y_pred)
    f1_score = metrics.f1_score(y_test, y_pred)
    tn, fp, fn, tp = metrics.confusion_matrix(y_test, y_pred).ravel()
    m_dict = {"accuracy": accuracy, "balanced_accuracy": balanced_accuracy, "f1_score": f1_score, 
              "tp": tp, "fp": fp, "tn": tn, "fn":fn}
    return m_dict

def save_model(name, model) :
    filename = classifiers_dir + "/" + name + '.sav'
    pickle.dump(model,open(filename,'wb'))

def classifier_training(weight, model, X_train, X_test, y_train, y_test):
    name = str(model) + '_class0_' + str(weight[0]) + '_class1_' + str(weight[1])
    print(name)
    if model == "SVM":
        clf = make_pipeline(StandardScaler(with_mean=False),SGDClassifier(class_weight=weight))
        clf.fit(X_train,y_train)
        y_pred = clf.predict(X_test)
        quality = get_classif_metrics(y_test, y_pred)
    if model == "RF":
        clf = make_pipeline(StandardScaler(with_mean=False),RandomForestClassifier(class_weight=weight))
        clf.fit(X_train,y_train)
        y_pred = clf.predict(X_test)
        quality = get_classif_metrics(y_test, y_pred)
    if model == "GB":
        clf = make_pipeline(StandardScaler(with_mean=False),HistGradientBoostingClassifier(class_weight=weight))
        clf.fit(X_train.toarray(),y_train)
        y_pred = clf.predict(X_test.toarray())
        quality = get_classif_metrics(y_test, y_pred)
    save_model(name, clf)
    logging.info(f'Model saved in file {name}.sav \t Classification metrics: {quality}')
    return(clf, quality)

# Load dataset
X = read_sparse_matrix()
label = pd.read_csv('training_f' + str(factor) + '.tsv', sep = '\t', header = None)
y = label[2]

print(X.shape)

# Training and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.3)

# Class weights to test for training
list_class_weight = list()
for k in range(1,10) :
    dict_weight = {0 : k/10, 1 : (10-k)/10}
    list_class_weight.append(dict_weight)

# Models parallel training
with Pool(processes=2) as pool:
        results = []
        for weights in list_class_weight:
            for model in ["GB", "SVM", "RF"]:
                result = pool.apply_async(classifier_training, args=(weights, model, X_train, X_test, y_train, y_test))
                results.append(result)
        
        # # Wait for all tasks to complete
        for result in results:
            result.get()