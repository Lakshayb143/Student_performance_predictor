import sys
import os
from dataclasses import dataclass
from multiprocessing.spawn import prepare

import numpy as np
import pandas as pd

from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline

from src.exception import CustomException
from src.logger import logging
from src.utils import save_object


@dataclass
class DataTransformationConfig:
    preprocessor_obj_file_path :str = os.path.join('artifacts','preprocessor.pkl')



class DataTransformation:
    def __init__(self):
        self.data_transformation_config = DataTransformationConfig()


    def get_data_transformer_obj(self):
        try:
            numerical_features = ["writing_score", "reading_score"]
            categorical_features = [
                "gender",
                "race_ethnicity",
                "parental_level_of_education",
                "lunch",
                "test_preparation_course",
            ]

            numerical_pipeline = Pipeline(
                steps=[
                    ('imputer', SimpleImputer(strategy='median')),
                    ('scaler', StandardScaler(with_mean=False))
                ]
            )

            # logging.info('Numerical features scaling completed')
            # logging.info('Categorical features encoding completed')


            categorical_pipeline = Pipeline(
                steps=[
                    ('imputer', SimpleImputer(strategy='most_frequent')),
                    ('one_hot_encoder',OneHotEncoder()),
                    ('scaler', StandardScaler(with_mean=False))
                ]
            )

            logging.info(f"Categorical columns: {categorical_features}")
            logging.info(f"Numerica1 columns: {numerical_features}")

            preprocessor = ColumnTransformer(
                [
                    ('numerical_pipeline', numerical_pipeline, numerical_features),
                    ('categorical_pipeline', categorical_pipeline, categorical_features)
                ]
            )


            return preprocessor


        except Exception as e:
            raise CustomException(e,sys)


    def initiate_data_transformation(self, train_path, test_path):

        try:
            train_df = pd.read_csv(train_path)
            test_df = pd.read_csv(test_path)

            logging.info("Read train and test data completed.")
            logging.info("Obtaining data preprocessor object for data transformation")

            preprocessing_object = self.get_data_transformer_obj()

            target_column_name = "math_score"

            input_feature_train_df = train_df.drop(columns=[target_column_name], axis=1)
            target_feature_train_df = train_df[target_column_name]

            input_feature_test_df = test_df.drop(columns=[target_column_name] , axis=1)
            target_feature_test_df = test_df[target_column_name]

            logging.info("Applying Transformation to Training and Testing Dataframe")

            train_input_feature = preprocessing_object.fit_transform(input_feature_train_df)
            test_input_feature = preprocessing_object.transform(input_feature_test_df)


            train_arr = np.c_[train_input_feature, np.array(target_feature_train_df)]
            test_arr = np.c_[
                test_input_feature, np.array(target_feature_test_df)
            ]


            logging.info("Saved preprocessing object.")

            save_object(
                file_path=self.data_transformation_config.preprocessor_obj_file_path,
                obj=preprocessing_object
            )


            return(
                train_arr,
                test_arr,
                self.data_transformation_config.preprocessor_obj_file_path
            )


        except Exception as e:
            raise CustomException(e,sys)