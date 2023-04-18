import os
import sys
import numpy as np
import pandas as pd
import dill
from sklearn.metrics import r2_score
from sklearn.model_selection import GridSearchCV

from src.exception import CustomException

def save_object(file_path, obj):
    '''
    - this function takes in file_path and object as arguments and saves the object
    in that location;
    - mainly for collecting model and data artifacts and saving them
    in the artifact/
    '''
    try:
        dir_path = os.path.dirname(file_path)
        # check if folder(s) exists, else create
        os.makedirs(dir_path, exist_ok=True)

        # in this folder location, create a dill object for what is passed
        with open(file_path, "wb") as file_obj:
            dill.dump(obj, file_obj)

    except Exception as e:
        raise CustomException(e, sys)

def evaluate_model(X_train, y_train, X_test, y_test, models, params):
    '''
    - this function builds all the specified models using cross validation from the models dictionary;
    - it also does hyperparameter tuning and then picks the best model with the best parameters;
    - hyperparameter dictionary is provided
    - it returns the model name and test evaluation metric of the selected model -- all compiled in a dictionary
    '''
    try:
        report = {}

        for i in range(len(list(models))):
            # select model from list of models
            # select the corresponding dictionary of hyperparameters to try        
            model = list(models.values())[i]
            param = params[list(models.keys())[i]]

            #gridsearch is on cross validated sample with 3 folds - on train data
            gs = GridSearchCV(model,param,cv=3)
            gs.fit(X_train,y_train)

            #selecting best hyperparameters
            model.set_params(**gs.best_params_)
            
            #training on the full set with the best parameters
            model.fit(X_train, y_train)

            #make predictions
            y_train_pred = model.predict(X_train)
            y_test_pred = model.predict(X_test)

            train_model_score = r2_score(y_train, y_train_pred)
            test_model_score = r2_score(y_test, y_test_pred)

            #prepare a dictionary of model name as key and test R2 as value

            report[list(models.keys())[i]] = test_model_score

        return report 


    except Exception as e:
        raise CustomException(e, sys)