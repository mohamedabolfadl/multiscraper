"""
Purpose
Preping data for machine learning
    Input:
        detailed_offers_xxx.csv with amenities, furnishment, desc text, etc
    Output:
        ml_ready_xxx.csv 
"""

#-- Clear variables
from IPython import get_ipython
ipython = get_ipython()
ipython.magic("%reset  -f")




####################################
#--      INPUT PARAMETERS        --#
####################################

proj_dir = "C:\\Users\\Mohamed Ibrahim\\Box Sync\\bot\\multiscraper"


####################################
#--      IMPORT LIBRARIES        --#
####################################


import time
import pandas as pd
import re
import statistics as st
import os
import numpy as np

#-- Display settings
pd.set_option('display.max_rows', 10)
pd.set_option('display.max_columns', 20)
pd.set_option('display.width', 1000)

def flatten(l):
    for el in l:
        if isinstance(el, collections.Iterable) and not isinstance(el, (str, bytes)):
            yield from flatten(el)
        else:
            yield el

#-- Get districts which have detailed files
def getDetailedDistricts():
    outputFiles = os.listdir(proj_dir+"\\02_data\\output")
    r = re.compile("detailed_offers_.*")
    inscopeFiles = list(filter(r.match, outputFiles)) 
    districts = [re.sub("(\.csv|detailed_offers_)","",x) for x in inscopeFiles]
    return districts


#-- Make sure we are at root of project
os. chdir(proj_dir)


#-- Get districts which have detailed info
districts = getDetailedDistricts()


#-- Loop through districts
for district in districts:


    #-- Read the detailed offers
    df = pd.read_csv(proj_dir+"\\02_data\\output\\detailed_offers_"+district+".csv")


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

