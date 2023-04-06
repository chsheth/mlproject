import sys, os
from dataclasses import dataclass
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

from src.exception import CustomException
from src.logger import logging
from src.utils import save_object


@dataclass
class DataTransformationConfig:
    # these are config parameters for DataTransformation Class
    # this is where we define the paths mainly, to be used later
    preprocessor_obj_file_path = os.path.join('artifacts', 'preprocessor.pkl')

class DataTransformation:
    
    def __init__(self):
        self.data_transformation_config = DataTransformationConfig()
    
    def get_data_transformer_object(self):
        '''
        to do data transformations
        '''
        try:
            # creating  data transformation logic from the notebook 
            # numerical columns will have different preprocessing steps
            # impute; scale
            numerical_columns = ["writing_score", "reading_score"]


            # impute; onehotencode
            categorical_columns = ["gender",
                                   "race_ethnicity",
                                   "parental_level_of_education",
                                   "lunch",
                                   "test_preparation_course"
                                    ]
            num_pipeline = Pipeline(
                steps=[
                ('imputer', SimpleImputer(strategy="median")),
                ('scaler', StandardScaler())
                ]
            )

            cat_pipeline = Pipeline(
                steps=[
                ("imputer", SimpleImputer(strategy='most_frequent')),
                ("one_hot_encoder", OneHotEncoder()),
                ("scaler",StandardScaler(with_mean=False))
                ]
            )
            
            logging.info(f"Numerical columns:{numerical_columns}")
            logging.info(f"Categorical columns:{categorical_columns}")

            preprocessor = ColumnTransformer([
                ("num_pipeline", num_pipeline, numerical_columns),
                ("cat_pipeline",  cat_pipeline, categorical_columns)]
            )

            logging.info("Numerical columns processing completed")
            logging.info("Categorical columns encoding completed")

            return preprocessor


        except Exception as e:
            raise CustomException(e, sys)


    def initiate_data_transformation(self, train_path, test_path):

        try:
            train_df = pd.read_csv(train_path)
            test_df = pd.read_csv(test_path)
            
            logging.info("train, test data read")
            logging.info("obtaining preprocessing object")

            preprocessing_obj = self.get_data_transformer_object()
            
            target_column_name ='math_score'
            numerical_columns = ['writing_score', 'reading_score']

            input_feature_train_df = train_df.drop(columns=[target_column_name], axis=1)
            input_feature_test_df = test_df.drop(columns=[target_column_name], axis=1)

            target_feature_train_df = train_df[target_column_name]
            target_feature_test_df = test_df[target_column_name]

            logging.info("data preprocessing - train and test dataframes")

            input_feature_train_arr = preprocessing_obj.fit_transform(input_feature_train_df)
            input_feature_test_arr = preprocessing_obj.transform(input_feature_test_df)

            train_arr = np.c_[input_feature_train_arr, np.array(target_feature_train_df)
            ]
            test_arr = np.c_[input_feature_test_arr, np.array(target_feature_test_df)
            ]

            save_object(
                file_path = self.data_transformation_config.preprocessor_obj_file_path,
                obj = preprocessing_obj
                )

            return (
                train_arr,
                test_arr,
                self.data_transformation_config.preprocessor_obj_file_path,
            )   
             
        except Exception as e:
            raise CustomException(e, sys)