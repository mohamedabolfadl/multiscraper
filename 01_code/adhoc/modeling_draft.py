# -*- coding: utf-8 -*-
"""
Created on Fri Jul 12 20:27:48 2019

@author: Mohamed Ibrahim
"""


#-- Clear variables
from IPython import get_ipython
ipython = get_ipython()
ipython.magic("%reset  -f")




####################################
#--      INPUT PARAMETERS        --#
####################################

proj_dir = "C:\\Users\\Mohamed Ibrahim\\Box Sync\\bot\\multiscraper"
USE_XGB_CV = False
DO_HYPERPARAM_SEARCH = True
USE_XGB_MODEL = True # If false uses RF

####################################
#--      IMPORT LIBRARIES        --#
####################################


import time
import math
import pandas as pd
import re
import statistics as st
import os
import numpy as np
import xgboost
import matplotlib.pyplot as plt

from sklearn.linear_model import LinearRegression
from sklearn import  tree, linear_model
from sklearn.model_selection import cross_val_predict, cross_validate,train_test_split, KFold
from sklearn.metrics import explained_variance_score
from sklearn.preprocessing import StandardScaler



from scipy.stats import randint as sp_randint
import scipy.stats as st

from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import RandomizedSearchCV
from sklearn.datasets import load_digits
from sklearn.ensemble import RandomForestRegressor
#-- Display settings
pd.set_option('display.max_rows', 10)
pd.set_option('display.max_columns', 20)
pd.set_option('display.width', 1000)


district = "downtown"


#-- Read clean data
df = pd.read_csv(proj_dir+"\\02_data\\intermediate\\ml_clean_"+district+".csv")


#-- Isolate predictors and target
target = 'target'
predictors = [x for x in list(df.columns) if x!=target and x != "Unnamed: 0"]
y = df.target
X = df[predictors]



#- Transform to XGboost matrix
data_dmatrix = xgboost.DMatrix(data=X,label=y)


#-- XGboost parameters
params = { "objective" : "reg:squarederror"
         ,"eta":0.10
         ,"gamma":0
         ,"max_depth":4
         ,"min_child_weight":1
         ,"subsample":0.8
         ,"colsample_bytree":0.8
         ,"n_estimators":500}



params = { "objective" : "reg:squarederror"
         ,"eta":0.10
         ,"gamma":0
         ,"max_depth":6
         ,"min_child_weight":1
         ,"subsample":0.8
         ,"colsample_bytree":0.8
         ,"n_estimators":10}
#-- Do CV
cv_results = xgboost.cv(dtrain=data_dmatrix,
                        params=params, 
                        nfold=5,
                        num_boost_round=500,
                        early_stopping_rounds=10,
                        metrics="rmse",
                as_pandas=True,                  
                stratified = True)

print((cv_results["test-rmse-mean"]).tail(1))


xg_reg = xgboost.train(params=params, dtrain=data_dmatrix, num_boost_round=100)
xgboost.plot_importance(xg_reg)




##########################
#-- GBM  grid search   --#
##########################

from sklearn.ensemble import GradientBoostingRegressor

def report(results, n_top=3):
    for i in range(1, n_top + 1):
        candidates = np.flatnonzero(results['rank_test_score'] == i)
        for candidate in candidates:
            print("Model with rank: {0}".format(i))
            print("Mean validation score: {0:.3f} (std: {1:.3f})".format(
                  results['mean_test_score'][candidate],
                  results['std_test_score'][candidate]))
            print("Parameters: {0}".format(results['params'][candidate]))
            print("")

gbm = GradientBoostingRegressor()
loss = ['ls']  # 'ls', 'lad', 'huber'
n_estimators = [100, 200]
max_depth = [3]
min_samples_leaf = [1] 
min_samples_split = [2]
max_features = [None] #'auto', 'sqrt', 'log2', None

# Define the grid of hyperparameters to search
parameters = {
        #'loss': loss,
    #'n_estimators': n_estimators,
    #'max_depth': max_depth,
    #'min_samples_leaf': min_samples_leaf,
    #'min_samples_split': min_samples_split,
    #'max_features': max_features
    }


gbm_grid = RandomizedSearchCV(estimator=gbm,
            param_distributions=parameters,
            cv=5, n_iter=5,
            scoring = 'neg_mean_squared_error',
            verbose = 5, 
            return_train_score = True,
            #n_jobs = 4,
            random_state=42)

gbm_grid.fit(X,
         y)

report(gbm_grid.cv_results_)


#-- Manual k fold
from sklearn.model_selection import KFold
import sklearn
def fitAndPrint(cl, X_train, y_train,X_test,y_test):
    cl.fit(X_train,y_train)
    y_preds = cl.predict(X_test)
    r2 = sklearn.metrics.r2_score(y_test,y_preds)
    rmse =math.sqrt(sklearn.metrics.mean_squared_error(y_test,y_preds)) 
    print(r2)
    print(rmse)
    return r2,rmse

kf = KFold(n_splits=10, random_state=None, shuffle=False)
gbm = GradientBoostingRegressor(n_estimators=200)
r2_all,rmse_all =[],[]

for train_index, test_index in kf.split(X):
    X_train, X_test = X.iloc[train_index,], X.iloc[test_index,]
    y_train, y_test = y.iloc[train_index,], y.iloc[test_index,]
    r2,rmse = fitAndPrint(gbm, X_train, y_train,X_test,y_test)
    r2_all.append(r2)
    rmse_all.append(rmse)


np.mean(rmse_all)
#np.mean(r2_all)


#-- Other variant of manual fitting

from sklearn.model_selection import cross_val_score
print(np.mean(cross_val_score(gbm, X, y, cv=5, scoring ='neg_mean_squared_error')))


##########################
#-- XGB Grid search    --#
##########################

from xgboost.sklearn import XGBRegressor


xgb1 = XGBRegressor()
parameters = {#'nthread':[4], #when use hyperthread, xgboost may become slower
              'objective':['reg:linear'],
              'learning_rate': [.1], #so called `eta` value
              'max_depth': [4],
              'min_child_weight': [1],
              'silent': [1],
              'subsample': [0.8],
              'colsample_bytree': [1],
              'n_estimators': [450]}

xgb_grid = GridSearchCV(xgb1,
                        parameters,
                        cv = 5,
#                        n_jobs = 5,
                        scoring = "neg_mean_squared_error",
                        verbose=False)

xgb_grid.fit(X,
         y)

print(xgb_grid.best_score_)
print(xgb_grid.best_params_)







import sklearn
from sklearn.ensemble import *
from sklearn import linear_model
from sklearn import svm


i = 1

def fitAndPrint(cl, X_train, y_train,X_test,y_test):
    cl.fit(X_train,y_train)
    y_preds = cl.predict(X_test)
    r2 = sklearn.metrics.r2_score(y_test,y_preds)
    rmse =math.sqrt(sklearn.metrics.mean_squared_error(y_test,y_preds)) 
    print(r2)
    print(rmse)
    return r2,rmse

while i<10:
    X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.1, random_state=i)

    print(i)
    clf_xgb = XGBRegressor(#objective='reg:linear',
                  learning_rate=0.1, #so called `eta` value
                  max_depth=4,
                  min_child_weight=1,
                  silent=1,
                  subsample=0.8,
                  colsample_bytree=1,
                  n_estimators=450,
                  seed = 123)
    
    clf_rf = RandomForestRegressor(max_depth=4, random_state=0,n_estimators=1000)
    clf_glm = linear_model.LinearRegression()
    clf_ada = AdaBoostRegressor()
    clf_huber = linear_model.HuberRegressor()
    clf_gbm = GradientBoostingRegressor(n_estimators=900, min_samples_split=6, min_samples_leaf=6, max_features='sqrt', max_depth=15, loss='lad')
    clf_SVM = svm.SVR()
    clf_ridge= linear_model.Ridge(alpha=.5)
    
    print("#------------ GBM-------------------#")
    r2,rmse= fitAndPrint(clf_gbm, X_train, y_train,X_test,y_test)
    print("#------------ XGB -------------------#")
    fitAndPrint(clf_xgb, X_train, y_train,X_test,y_test)
#    print("#------------ RF -------------------#")
#    fitAndPrint(clf_rf, X_train, y_train,X_test,y_test)
    print("#------------ GLM -------------------#")
    fitAndPrint(clf_glm, X_train, y_train,X_test,y_test)
#    print("#------------ ADA -------------------#")
#    fitAndPrint(clf_ada, X_train, y_train,X_test,y_test)
#    print("#------------ HUBER-------------------#")
#    fitAndPrint(clf_huber, X_train, y_train,X_test,y_test)
#    print("#------------ SVM-------------------#")
#    fitAndPrint(clf_SVM, X_train, y_train,X_test,y_test)
    print("#------------ Ridge-------------------#")
    fitAndPrint(clf_ridge, X_train, y_train,X_test,y_test)
    i = i+1






np.corrcoef(y_test,y_preds)

coeff_determination(y_test,y_preds)



def coeff_determination(y_true, y_pred):
    from keras import backend as K
    SS_res =  K.sum(K.square( y_true-y_pred ))
    SS_tot = K.sum(K.square( y_true - K.mean(y_true) ) )
    return ( 1 - SS_res/(SS_tot + K.epsilon()) )

tree.ExtraTreeRegressor
neural_network.MLPRegressor
linear_model.HuberRegressor
ensemble.AdaBoostClassifier([…])	An AdaBoost classifier.
ensemble.AdaBoostRegressor([base_estimator, …])	An AdaBoost regressor.
ensemble.BaggingClassifier([base_estimator, …])	A Bagging classifier.
ensemble.BaggingRegressor([base_estimator, …])	A Bagging regressor.
ensemble.ExtraTreesClassifier([…])	An extra-trees classifier.
ensemble.ExtraTreesRegressor([n_estimators, …])	An extra-trees regressor.
ensemble.GradientBoostingClassifier([loss, …])	Gradient Boosting for classification.
ensemble.GradientBoostingRegressor([loss, …])	Gradient Boosting for regression.
ensemble.IsolationForest([n_estimators, …])	Isolation Forest Algorithm
ensemble.RandomForestClassifier([…])	A random forest classifier.
ensemble.RandomForestRegressor([…])	A random forest regressor.
ensemble.RandomTreesEmbedding([…])	An ensemble of totally random trees.
ensemble.VotingClassifier(estimators[, …])	Soft Voting/Majority Rule classifier for unfitted estimators.
ensemble.VotingRegressor(estimators[, …])	Prediction voting regressor for unfitted estimators.
ensemble.HistGradientBoostingRegressor([…])	Histogram-based Gradient Boosting Regression Tree.
ensemble.HistGradientBoostingClassifier([…])	Histogram-based Gradient Boosting Classification Tree.