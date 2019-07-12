"""
Purpose
Scores each offer based on regression model and other rankings
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

    df_basic.loc[df_basic.area_check != df_basic.area,:]
    


    kf = KFold(n_splits=5)
    kf.get_n_splits(df)

    X_train, X_test, y_train, y_test = cross_validation.train_test_split(X, y ,test_size=0.2)
    regr = linear_model.LinearRegression()


    regr.fit(X_train, y_train)

    regr.score(X_test,y_test)
    
    model = xgboost.XGBRegressor(colsample_bytree=0.4,
                 gamma=0,                 
                 learning_rate=0.07,
                 max_depth=3,
                 min_child_weight=1.5,
                 n_estimators=10000,                                                                    
                 reg_alpha=0.75,
                 reg_lambda=0.45,
                 subsample=0.6,
                 seed=42) 
    #########################
    #-- Process amenities --#
    #########################
    
    #-- Number of amenities
    df['n_amenities'] = df.amenities.str.count('\|')
    df['n_amenities'] = df['n_amenities'].fillna(0)
    df['n_amenities'] = df['n_amenities']+1
    df.loc[pd.isnull(df.amenities),'n_amenities'] = 0
    
    
    #-- Split column by separator
    max_amenities = max(df.n_amenities)
    df_amenities= df["amenities"].str.split("|", n = int(max_amenities ), expand = True) 

    #-- Get unique rows per column
    uniqueAmenities = []
    for col in range(len(df_amenities.columns)):
        uniqueAmenities.append( list(df_amenities.iloc[:,col].unique()))


    #-- Flatten and unique list
    # TODO: Flatten list mo module
    uniqueAmenitiesFlat = list(set([item for sublist in uniqueAmenities for item in sublist]))
    
    #-- Exclude NaN, None and replace non character with ""
    # TODO: exclude nan and None
    amenityUniq = [x for x in uniqueAmenitiesFlat if str(x) != 'nan' and  str(x) != 'None']
    amenityCols = [re.sub("\W","",x) for x in uniqueAmenitiesFlat if str(x) != 'nan' and  str(x) != 'None']
    
    #-- Look up of entry and cleaned column name
    amDict = dict(zip(amenityCols,amenityUniq))

    #-- Create columns for each amenity
    for am in amenityCols:
        df[am] = df.amenities.str.contains(amDict[am])
        df.loc[pd.isnull(df[am]),am] = False

    ###########################
    #-- Process furnishment --#
    ###########################

    #-- Look up of furnishment
    uniqFurn = df.furnishment.unique()
    uniqFurnNms = [re.sub("\s+","_",x.lower().strip()) for x in uniqFurn]
    furnDict = dict(zip(uniqFurnNms,uniqFurn))
    
    
    for fur in furnDict.keys():
        df[fur] = df.furnishment.str.contains(furnDict[fur])
        df.loc[pd.isnull(df[fur]),fur] = False

    #-- Base ML cols
    ml_cols = ['price','area','bedrooms','bathrooms','n_amenities']

    #-- Append amenities
    ml_cols.extend(amenityCols)

    #-- Append furnishment
    ml_cols.extend(uniqFurnNms)


    df[ml_cols].to_csv("02_data/output/ml_ready_"+district+".csv")


