# -*- coding: utf-8 -*-
"""
Created on Thu Jul 11 16:48:04 2019

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



from sklearn.model_selection import GridSearchCV
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Dropout
from keras.wrappers.scikit_learn import KerasClassifier
from keras.wrappers.scikit_learn import KerasRegressor
from keras.constraints import maxnorm
import numpy as np
import pandas as pd

def coeff_determination(y_true, y_pred):
    from keras import backend as K
    SS_res =  K.sum(K.square( y_true-y_pred ))
    SS_tot = K.sum(K.square( y_true - K.mean(y_true) ) )
    return ( 1 - SS_res/(SS_tot + K.epsilon()) )



# Function to create model, required for KerasClassifier
def create_model(neurons=1):
	# create model
	model = Sequential()
	model.add(Dense(neurons, input_dim=34, kernel_initializer='uniform', activation='linear', kernel_constraint=maxnorm(4)))
	model.add(Dropout(0.2))
	model.add(Dense(1, activation="linear"))
	model.compile(loss='mean_squared_error', optimizer='adam', metrics = [coeff_determination])

	return model



# fix random seed for reproducibility
seed = 7
np.random.seed(seed)

# load dataset
district = 'downtown'
df = pd.read_csv(proj_dir+"\\02_data\\output\\ml_ready_"+district+".csv")

target = 'price'
predictors = [x for x in list(df.columns) if x!=target and x != "Unnamed: 0"]

y = df.price
X = df[predictors]

from sklearn.preprocessing import StandardScaler
ss = StandardScaler()
X= ss.fit_transform(X)


# create model
model = KerasRegressor(build_fn=create_model, epochs=250, batch_size=10, verbose=0)
# define the grid search parameters
neurons = [5,10,50]
param_grid = dict(neurons=neurons)
#param_grid = {'batch_size': [25,32],
#              'epochs': [5,10],
#              'optimizer': ['adam', 'rmsprop'],
#              'dropout1' : [0.2,0.25,3],
#              'dropout2' : [0.2,0.25,3],
#              }

grid = GridSearchCV(estimator=model, param_grid=param_grid, cv = 5)
grid_result = grid.fit(X, y)




print("Best: %f using %s" % (grid_result.best_score_, grid_result.best_params_))
means = grid_result.cv_results_['mean_test_score']
stds = grid_result.cv_results_['std_test_score']
params = grid_result.cv_results_['params']
for mean, stdev, param in zip(means, stds, params):
    print("%f (%f) with: %r" % (mean, stdev, param))
    

model = Sequential()
model.add(Dense(19, input_dim=34, kernel_initializer='uniform', activation='linear', kernel_constraint=maxnorm(4)))
model.add(Dropout(0.2))
model.add(Dense(1, activation="linear"))
model.compile(loss='mean_squared_error', optimizer='adam')


model.fit(X, y, epochs=150, batch_size=10)

from sklearn.model_selection import KFold
from sklearn.model_selection import cross_val_score


baseline_model = create_model(10)
estimator = KerasRegressor(build_fn=baseline_model, epochs=100, batch_size=5, verbose=0)

kfold = KFold(n_splits=10, random_state=seed)
results = cross_val_score(estimator, X, y, cv=kfold)
print("Results: %.2f (%.2f) MSE" % (results.mean(), results.std()))

kfold = KFold(n_splits=10, random_state=seed)
results = cross_val_score(estimator, X, Y, cv=kfold)
print("Results: %.2f (%.2f) MSE" % (results.mean(), results.std()))


mdl.fit(X,y, epochs=150, batch_size=10)




# define base model
def baseline_model():
	# create model
	model = Sequential()
	model.add(Dense(70, input_dim=34, kernel_initializer='normal', activation='relu'))
	model.add(Dense(20, activation='relu'))
	#model.add(Dense(1, kernel_initializer='normal'))
	model.add(Dense(1))
    
	# Compile model
	model.compile(loss='mean_squared_error', optimizer='adam', metrics = [coeff_determination])
	return model


#-- Estimator
estimator = KerasRegressor(build_fn=baseline_model, epochs=250, batch_size=50, verbose=0)


kfold = KFold(n_splits=3, random_state=seed)
results = cross_val_score(estimator, X, y, cv=kfold)

print("Results: %.2f (%.2f) MSE" % (results.mean(), results.std()))



model.fit(X,y, epochs=250, batch_size=50)




mdl= Sequential()
mdl.add(Dense(70, input_dim=34, kernel_initializer='normal', activation='relu'))
mdl.add(Dense(20, activation='relu'))
mdl.add(Dense(1))
mdl.compile(loss='mean_squared_error', optimizer='adam', metrics = [coeff_determination])

param_grid = dict(epochs=[10,20,30])
model = KerasClassifier(build_fn=baseline_model)
grid = GridSearchCV(estimator=model, param_grid=param_grid)
grid_result = grid.fit(X, y)

param_grid = dict(epochs=[10,20,30])
grid = GridSearchCV(estimator=model, param_grid=param_grid, n_jobs=-1)
grid_result = grid.fit(X, Y)





# summarize results
print("Best: %f using %s" % (grid_result.best_score_, grid_result.best_params_))
means = grid_result.cv_results_['mean_test_score']
stds = grid_result.cv_results_['std_test_score']
params = grid_result.cv_results_['params']
for mean, stdev, param in zip(means, stds, params):
    print("%f (%f) with: %r" % (mean, stdev, param))