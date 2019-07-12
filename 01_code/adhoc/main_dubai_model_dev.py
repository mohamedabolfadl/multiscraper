"""
Purpose
Check the best model for regression
    Input:
        ml_ready_xxx.csv 
    Output:
        model_scores_xxx.csv 
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











#-- Get districts which have ML files
def getMLDistricts():
    outputFiles = os.listdir(proj_dir+"\\02_data\\output")
    r = re.compile("ml_ready_.*")
    inscopeFiles = list(filter(r.match, outputFiles)) 
    districts = [re.sub("(\.csv|ml_ready_)","",x) for x in inscopeFiles]
    return districts


#-- Make sure we are at root of project
os. chdir(proj_dir)


#-- Get districts which have detailed info
districts = getMLDistricts()


#-- Loop through districts
for district in districts:

    print(district)
    #-- Read the detailed offers
    df = pd.read_csv(proj_dir+"\\02_data\\output\\ml_ready_"+district+".csv")
    
    target = 'price'
    predictors = [x for x in list(df.columns) if x!=target and x != "Unnamed: 0"]
    
    y = df.price
    X = df[predictors]


    if DO_HYPERPARAM_SEARCH:
        # build a regressor
        if USE_XGB_MODEL: 
            regr = xgboost.XGBRegressor(objective = 'reg:squarederror')
        else:
            regr = RandomForestRegressor()
        
        # Utility function to report best scores
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
        

        if USE_XGB_MODEL: 
            param_dist =  {  
                            "n_estimators": sp_randint(50, 200),
                            "max_depth": sp_randint(2,5),
                            "learning_rate": st.uniform(0.05, 0.3),
                            "colsample_bytree": st.beta(5, 10)  ,
                            "subsample": st.beta(0.08, 0.099)
#                            "gamma": st.uniform(0, 10),
 #                           'reg_alpha': st.expon(0, 50),
  #                          "min_child_weight": st.expon(0, 50)
                        }
        else:
            
            # specify parameters and distributions to sample from
            param_dist = {"n_estimators":sp_randint(20, 100),
                          #"max_depth": [3, None],
                          #"max_features": sp_randint(1, 11),
                          #"min_samples_split": sp_randint(2, 11),
                          "bootstrap": [True, False]}


        import warnings
        warnings.simplefilter(action='ignore', category=FutureWarning)

        with warnings.catch_warnings():
            warnings.filterwarnings("ignore", category=DeprecationWarning)
            import imp
    
        # run randomized search
        n_iter_search = 1000
        random_search = RandomizedSearchCV(regr, 
                                           param_distributions=param_dist,
                                           n_iter=n_iter_search, 
                                           cv=5,
                                           scoring='r2', #neg_mean_absolute_error
                                           iid=False)
        
        random_search.fit(X, y)
        report(random_search.cv_results_)




    regr = xgboost.XGBRegressor(objective= 'reg:linear')
    

    else:
        ###########################################
        #--      CV using XGboost               --#
        ###########################################
    
        if USE_XGB_CV:
            data_dmatrix = xgboost.DMatrix(data=X,label=y)
        
            params = {"objective":"reg:linear",'colsample_bytree': 0.9,'learning_rate': 0.05,
                        'max_depth': 3, 'nrounds':1000}
        
            cv_results = xgboost.cv(dtrain=data_dmatrix, params=params, nfold=5,
                            num_boost_round=1000,early_stopping_rounds=50,metrics="rmse",
                            as_pandas=True, seed=123)
        
            print((cv_results["test-rmse-mean"]).tail(1))
        
        
            xg_reg = xgboost.train(params=params, dtrain=data_dmatrix, num_boost_round=100)
            xgboost.plot_importance(xg_reg)
            plt.rcParams['figure.figsize'] = [5, 5]
            plt.show()
        
        
            xgboost.plot_tree(xg_reg,num_trees=0)
            plt.rcParams['figure.figsize'] = [50, 10]
            plt.show()
    
        
        
        ###########################################
        #--      CV using sklearn               --#
        ###########################################
        
        else:
            mdl = xgboost.XGBRegressor(colsample_bytree=0.4,
                         gamma=0,                 
                         learning_rate=0.07,
                         max_depth=3,
                         min_child_weight=1.5,
                         n_estimators=100,                                                                    
                         reg_alpha=0.75,
                         reg_lambda=0.45,
                         subsample=0.6,
                         seed=42) 
            
            
            cv = KFold(n_splits=5)
            prediction_cv = cross_val_predict(mdl, X, y, cv=cv)
            
            print("RMSE: %.2f"% math.sqrt(np.mean((prediction_cv - y) ** 2)))
            
            pred_error =   prediction_cv - y
        
            df_basic = pd.read_csv(proj_dir+"\\02_data\\output\\basic_offers_"+district+".csv")
        
            df_basic['pred_error'] = pred_error
            df_basic['price_check'] = y
            df_basic['area_check'] = X.area
        
        
            df_basic.to_csv('modeled_'+district+'.csv')
            





if False:
    Scoring options
    ['accuracy',
 'adjusted_mutual_info_score',
 'adjusted_rand_score',
 'average_precision',
 'balanced_accuracy',
 'brier_score_loss',
 'completeness_score',
 'explained_variance',
 'f1',
 'f1_macro',
 'f1_micro',
 'f1_samples',
 'f1_weighted',
 'fowlkes_mallows_score',
 'homogeneity_score',
 'mutual_info_score',
 'neg_log_loss',
 'neg_mean_absolute_error',
 'neg_mean_squared_error',
 'neg_mean_squared_log_error',
 'neg_median_absolute_error',
 'normalized_mutual_info_score',
 'precision',
 'precision_macro',
 'precision_micro',
 'precision_samples',
 'precision_weighted',
 'r2',
 'recall',
 'recall_macro',
 'recall_micro',
 'recall_samples',
 'recall_weighted',
 'roc_auc',
 'v_measure_score']