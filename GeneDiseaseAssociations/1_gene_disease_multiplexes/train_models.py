#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from sklearn.ensemble import GradientBoostingClassifier, RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn import feature_selection, metrics
import pandas as pd
import numpy as np
import scipy as sp
import pickle
import os
import glob
import logging

path = os.path.dirname(os.path.realpath(__file__))
path = path + '/'
os.chdir(path)

logging.basicConfig(filename='results_models.log', level=logging.INFO)

try : 
    os.mkdir('classifier')
except OSError : 
    pass


def read_sparse_matrix():
    num = len(glob.glob('results_sparse/*.npz'))
    list_sparse = list()
    for i in range(num) :
        temp = sp.sparse.load_npz('results_sparse/data_rwr_sparse_' + str(i) + '.npz')
        list_sparse.append(temp)
    data = sp.sparse.vstack([i for i in list_sparse])
    del list_sparse
    return data


def DecisionTree(X_train, y_train, X_test, y_test, weight, rand_state = 0) :
    clf = DecisionTreeClassifier(random_state = rand_state, class_weight = weight)
    clf.fit(X_train, y_train)
    y_pred = clf.predict(X_test)
    accuracy = metrics.accuracy_score(y_test, y_pred)
    f1_score = metrics.f1_score(y_test, y_pred)
    print("Accuracy:", accuracy)
    print("F1 score:", f1_score)
    return clf, accuracy, f1_score


def RandomForest(X_train, y_train, X_test, y_test, weight, num_est = 100) :
    clf = RandomForestClassifier(n_estimators = num_est, class_weight = weight)
    clf.fit(X_train,y_train)
    y_pred = clf.predict(X_test)
    accuracy = metrics.accuracy_score(y_test, y_pred)
    f1_score = metrics.f1_score(y_test, y_pred)
    print("Accuracy:", accuracy)
    print("F1 score:", f1_score)
    return clf, accuracy, f1_score


def GTB(X_train, y_train, X_test, y_test, rand_state = 0) :
    clf = GradientBoostingClassifier(random_state = rand_state)
    clf.fit(X_train, y_train)
    y_pred = clf.predict(X_test)
    accuracy = metrics.accuracy_score(y_test, y_pred)
    f1_score = metrics.f1_score(y_test, y_pred)
    print("Accuracy:", accuracy)
    print("F1 score:", f1_score)
    return clf, accuracy, f1_score


def save_model(name, model) :
    filename = name + '.sav'
    pickle.dump(model,open(filename,'wb'))
    

def select_from_model_features_selection_RandomForest(X, y, weight, num_est = 100)  :
    rfc = RandomForestClassifier(n_estimators = num_est, class_weight = weight)
    select_model = feature_selection.SelectFromModel(rfc)
    fit = select_model.fit(X, y)
    mask = fit.get_support()
    X_model_features = fit.transform(X)
    return X_model_features, mask 


def select_from_model_features_selection_DecisionTree(X, y, weight, rand_state = 0) :
    dtc = DecisionTreeClassifier(random_state = rand_state, class_weight = weight)
    select_model = feature_selection.SelectFromModel(dtc)
    fit = select_model.fit(X, y)
    mask = fit.get_support()
    X_model_features = fit.transform(X)
    return X_model_features, mask 


def select_from_model_features_selection_GTB(X, y, rand_state = 0) :
    gtb = GradientBoostingClassifier(random_state = rand_state)
    select_model = feature_selection.SelectFromModel(gtb)
    fit = select_model.fit(X, y)
    mask = fit.get_support()
    X_model_features = fit.transform(X)
    return X_model_features, mask 


X = read_sparse_matrix()

label = pd.read_csv('training.tsv', sep = '\t', header = None)
y = label[2]

# RandomForest / No weigth  / 100, 200, 1000 estimators
logging.info(f'####### RandomForest Classifier - No weigth')
list_est = [100, 200, 1000]
for k in range(len(list_est)) :
    logging.info(f'### {list_est[k]} estimators')
    X_new, mask = select_from_model_features_selection_RandomForest(X, y, weight = None, num_est = list_est[k])
    X_train, X_test, y_train, y_test = train_test_split(X_new, y, test_size = 0.3)
    model, accuracy, f1_score = RandomForest(X_train, y_train, X_test, y_test, weight = None, num_est = list_est[k])
    save_file = 'classifier/RandomForest_NoWeigth_' + str(list_est[k]) + 'estimators'
    save_mask = 'classifier/RandomForest_NoWeigth_' + str(list_est[k]) + 'estimators_mask'
    save_model(save_file, model)
    np.save(save_mask, mask)
    logging.info(f'Accuracy: {accuracy}')
    logging.info(f'F1 score: {f1_score}')
    logging.info(f'Model saved in file: classifier/{save_file}.sav')
    logging.info(f'Mask saved in file: classifier/{save_mask}.npy')
    del X_new, X_train, X_test, y_train, y_test, mask, model

# RandomForest / Balanced subsample / 100 estimators
logging.info(f'####### RandomForest Classifier - Balanced Subsample')
X_new, mask = select_from_model_features_selection_RandomForest(X, y, weight = "balanced_subsample", num_est = 100)
X_train, X_test, y_train, y_test = train_test_split(X_new, y, test_size = 0.3)
model, accuracy, f1_score = RandomForest(X_train, y_train, X_test, y_test, weight = "balanced_subsample", num_est = 100)
save_file = 'classifier/RandomForest_BalancedSubsample_100estimators'
save_mask = 'classifier/RandomForest_BalancedSubsample_100estimators_mask'
save_model(save_file, model)
np.save(save_mask, mask)
logging.info(f'Accuracy: {accuracy}')
logging.info(f'F1 score: {f1_score}')
logging.info(f'Model saved in file: classifier/{save_file}.sav')
logging.info(f'Mask saved in file: classifier/{save_mask}.npy')
del X_new, X_train, X_test, y_train, y_test, mask, model

# RandomForest / Balanced / 100 estimators
logging.info(f'####### RandomForest Classifier - Balanced')
X_new, mask = select_from_model_features_selection_RandomForest(X, y, weight = "balanced", num_est = 100)
X_train, X_test, y_train, y_test = train_test_split(X_new, y, test_size = 0.3)
model, accuracy, f1_score = RandomForest(X_train, y_train, X_test, y_test, weight = "balanced", num_est = 100)
save_file = 'classifier/RandomForest_Balanced_100estimators'
save_mask = 'classifier/RandomForest_Balanced_100estimators_mask'
save_model(save_file, model)
np.save(save_mask, mask)
logging.info(f'Accuracy: {accuracy}')
logging.info(f'F1 score: {f1_score}')
logging.info(f'Model saved in file: classifier/{save_file}.sav')
logging.info(f'Mask saved in file: classifier/{save_mask}.npy')
del X_new, X_train, X_test, y_train, y_test, mask, model

# Gradient Boosting / No weight
logging.info(f'####### Gradient Boosting Classifier - No weigth')
X_new, mask = select_from_model_features_selection_GTB(X, y, rand_state = 0) 
X_train, X_test, y_train, y_test = train_test_split(X_new, y, test_size=0.3)
model, accuracy, f1_score = GTB(X_train, y_train, X_test, y_test, rand_state = 0)
save_file = 'classifier/GradientBoosting_100estimators'
save_mask = 'classifier/GradientBoosting_100estimators_mask'
save_model(save_file, model)
np.save(save_mask, mask)
logging.info(f'Accuracy: {accuracy}')
logging.info(f'F1 score: {f1_score}')
logging.info(f'Model saved in file: classifier/{save_file}.sav')
logging.info(f'Mask saved in file: classifier/{save_mask}.npy')
del X_new, X_train, X_test, y_train, y_test, mask, model

# Class weights to use in the following analyses
list_class_weight = list()
for k in range(1,10) :
    dict_weight = {0 : k/10, 1 : (10-k)/10}
    list_class_weight.append(dict_weight)

# RandomForest / Multiple class weights / 100 estimators
logging.info(f'####### RandomForest - 100 estimators')
for k in range(len(list_class_weight)) :
    logging.info(f'### Class Weight: {list_class_weight[k]}')
    X_new, mask = select_from_model_features_selection_RandomForest(X, y, weight = list_class_weight[k], num_est = 100)
    X_train, X_test, y_train, y_test = train_test_split(X_new, y, test_size = 0.3)
    model, accuracy, f1_score = RandomForest(X_train, y_train, X_test, y_test, weight = list_class_weight[k], num_est = 100)
    save_file = 'classifier/RandomForest_' + str(k) + 'classWeights_100estimators'
    save_mask = 'classifier/RandomForest_' + str(k) + 'classWeights_100estimators_mask'
    save_model(save_file, model)
    np.save(save_mask, mask)
    logging.info(f'Accuracy: {accuracy}')
    logging.info(f'F1 score: {f1_score}')
    logging.info(f'Model saved in file: classifier/{save_file}.sav')
    logging.info(f'Mask saved in file: classifier/{save_mask}.npy')
    del X_new, X_train, X_test, y_train, y_test, mask, model

# RandomForest / Multiple class weights / 1000 estimators
logging.info(f'####### RandomForest - 1000 estimators')
for k in range(len(list_class_weight)) :
    logging.info(f'### Class Weight: {list_class_weight[k]}')
    X_new, mask = select_from_model_features_selection_RandomForest(X, y, weight = list_class_weight[k], num_est = 1000)
    X_train, X_test, y_train, y_test = train_test_split(X_new, y, test_size = 0.3)
    model, accuracy, f1_score = RandomForest(X_train, y_train, X_test, y_test, weight = list_class_weight[k], num_est = 1000)
    save_file = 'classifier/RandomForest_' + str(k) + 'classWeights_1000estimators'
    save_mask = 'classifier/RandomForest_' + str(k) + 'classWeights_1000estimators_mask'
    save_model(save_file, model)
    np.save(save_mask, mask)
    logging.info(f'Accuracy: {accuracy}')
    logging.info(f'F1 score: {f1_score}')
    logging.info(f'Model saved in file: classifier/{save_file}.sav')
    logging.info(f'Mask saved in file: classifier/{save_mask}.npy')
    del X_new, X_train, X_test, y_train, y_test, mask, model

# Decision Tree / Multiple class weights 
logging.info(f'####### Decision Tree Classifier')
for k in range(len(list_class_weight)) :
    logging.info(f'### Class Weight: {list_class_weight[k]}')
    X_new, mask = select_from_model_features_selection_DecisionTree(X, y, weight = list_class_weight[k], rand_state = 0)
    X_train, X_test, y_train, y_test = train_test_split(X_new, y, test_size = 0.3)
    model, accuracy, f1_score = DecisionTree(X_train, y_train, X_test, y_test, weight = list_class_weight[k], rand_state = 0)
    save_file = 'classifier/DecisionTree_' + str(k) + 'classWeights'
    save_mask = 'classifier/DecisionTree_' + str(k) + 'classWeights_mask'
    save_model(save_file, model)
    np.save(save_mask, mask)
    logging.info(f'Accuracy: {accuracy}')
    logging.info(f'F1 score: {f1_score}')
    logging.info(f'Model saved in file: classifier/{save_file}.sav')
    logging.info(f'Mask saved in file: classifier/{save_mask}.npy')
    del X_new, X_train, X_test, y_train, y_test, mask, model


