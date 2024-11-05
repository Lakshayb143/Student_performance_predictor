import os
import sys
import dill

import numpy as np
import pandas as pd

from sklearn.metrics import r2_score
from sklearn.model_selection import GridSearchCV


from src.exception import CustomException

def save_object(file_path, obj):
    try:
        dir_path = os.path.dirname(file_path)

        os.makedirs(dir_path,exist_ok=True)

        with open(file_path,"wb") as f_obj:
            dill.dump(obj,f_obj)

    except Exception as e:
        raise CustomException(e,sys)


def model_evalutaion(X_train, y_train, X_test, y_test, models :dict, params :dict):
    try:
        report = dict()

        models_list = list(models.values())
        model_name = list(models.keys())

        for i in range(len(model_name)):

            model = models_list[i]
            parameters = params[model_name[i]]

            param_search = GridSearchCV(model, parameters, cv=3)
            param_search.fit(X_train,y_train)

            model.set_params(**param_search.best_params_)
            model.fit(X_train,y_train)

            y_train_pred = model.predict(X_train)

            y_test_pred = model.predict(X_test)

            train_model_score = r2_score(y_train, y_train_pred)
            test_model_score = r2_score(y_test, y_test_pred)

            report[model_name[i]] = test_model_score

        return report


    except Exception as e:
        raise CustomException(e,sys)


def load_object(file):
    try:
        with open(file, 'rb') as f:
            return dill.load(f)
    except Exception as e:
        raise CustomException(e,sys)
