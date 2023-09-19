# First step to import the required libraries. 
import sys
from dataclasses import dataclass

import numpy as np 
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OrdinalEncoder,StandardScaler

from source.exception import CustomException
from source.logger import logging
import os
from source.utils import save_object
from sklearn.preprocessing import OneHotEncoder

# Second step to create a pickle file. 
@dataclass
class DataTransformationConfig:
    # We will be creating the preprocessor.pickle file in this path.
    preprocessor_obj_file_path = os.path.join('artifacts','preprocessor.pkl')


# Third step if to create a class with the data transformation pipline
class DataTransformation:

    def __init__(self):
        self.data_transformation_config=DataTransformationConfig()

    # function with data transformation pipeline. 
    def get_data_transformation_object(self):

        try:
            logging.info('Data Transformation initiated')

            # Define which columns should be ordinal-encoded and which should be scaled
            # saperating the numerical and categorical columns into saperate data tables. 
            categorical_cols = ["Airline","Source","Destination","Total_Stops"]
            numerical_cols = ["Day","Month","Year","Dep_hour","Dep_min","Arival_hour","Arival_min","Trveling_hour","Trveling_min"]

            # creating the pipelines
            logging.info('Pipeline Initiated')

            ## Numerical Pipeline
            num_pipeline=Pipeline(
                steps=[
                ('imputer',SimpleImputer(strategy='median')),
                ('scaler',StandardScaler())

                ]

            )

            # Categorigal Pipeline
            cat_pipeline=Pipeline(
                steps=[
                ('imputer',SimpleImputer(strategy='most_frequent')),
                ('ordinalencoder',OneHotEncoder(handle_unknown='ignore')),
                ('scaler',StandardScaler(with_mean=False))
                ]

            )

            preprocessor=ColumnTransformer([
            ('num_pipeline',num_pipeline,numerical_cols),
            ('cat_pipeline',cat_pipeline,categorical_cols)
            ])

            return preprocessor

            logging.info('Pipeline Completed')

        except Exception as e:
            logging.info("Error in Data Trnasformation")
            raise CustomException(e,sys)

    def initaite_data_transformation(self,train_path,test_path):
        try:
            # Reading train and test data
            train_df = pd.read_csv(train_path)
            test_df = pd.read_csv(test_path)

            logging.info('Read train and test data completed')
            logging.info(f'Train Dataframe Head : \n{train_df.head().to_string()}')
            logging.info(f'Test Dataframe Head  : \n{test_df.head().to_string()}')

            logging.info('Obtaining preprocessing object') 

            # output of completely transformed pipeline. 
            preprocessing_obj = self.get_data_transformation_object()

            target_column_name = 'Price'
            drop_columns = [target_column_name]
            
            input_feature_train_df = train_df.drop(columns=drop_columns,axis=1)  # independent columns
            target_feature_train_df=train_df[target_column_name]   # Dependent column or table. 

            input_feature_test_df=test_df.drop(columns=drop_columns,axis=1)
            target_feature_test_df=test_df[target_column_name]

            ## Trnasformating using preprocessor obj
            # fitting the train and test data sets. 
            input_feature_train_arr = preprocessing_obj.fit_transform(input_feature_train_df)
            input_feature_test_arr = preprocessing_obj.transform(input_feature_test_df) 

            logging.info("Applying preprocessing object on training and testing datasets.")
            
            # converting the data into array for easy ritrival process. 
            train_arr = np.c_[input_feature_train_arr, np.array(target_feature_train_df)]
            test_arr = np.c_[input_feature_test_arr, np.array(target_feature_test_df)]

            # importing save object from utilis.py file to save the pickle file. 
            save_object(

                file_path=self.data_transformation_config.preprocessor_obj_file_path,
                obj=preprocessing_obj

            )
            logging.info('Preprocessor pickle file saved')

            return (
                train_arr,
                test_arr,
                self.data_transformation_config.preprocessor_obj_file_path,
            )

        except Exception as e:
            logging.info("Exception occured in the initiate_datatransformation")

            raise CustomException(e,sys)
            