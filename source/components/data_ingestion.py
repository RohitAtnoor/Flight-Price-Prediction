# First step is to import the required library.
import os
import sys
from source.logger import logging
from source.exception import CustomException
import pandas as pd
from sklearn.model_selection import train_test_split
from dataclasses import dataclass

from source.components.data_transformation import DataTransformation


# Second step is to initilize the data injection configuration and files.

@dataclass
#dataclass is a function used to directly initilize the variables in a class with out the __init__ process.
#This process is used when we want to only initilize the variables, and there are no functions in the class.

class DataIngestionconfig:
    train_data_path:str=os.path.join('artifacts','train.csv')
    test_data_path:str=os.path.join('artifacts','test.csv')
    raw_data_path:str=os.path.join('artifacts','raw.csv')


# Third Step is to create a class for Data Ingection
class DataIngestion:
    # initilizing the variable.
    def __init__(self):
        self.ingestion_config = DataIngestionconfig()    
    
    # Initiating the Data ingection process.
    def initiate_data_ingestion(self):
        logging.info('Data Ingestion methods Starts') 

        try:
            #data_path = os.path.join("Data","flight_dataset.csv")
            df = pd.read_csv("Notebook/Data/flight_dataset.csv")  # reading the main dataset.
            logging.info('Dataset read as pandas Dataframe') 
            
            logging.info('Conversion of the Date_of_Journey column started')
            df["Date_of_Journey"] = pd.to_datetime(df["Date_of_Journey"],infer_datetime_format=True)
            # Convert the date to 3 columns day, month,and year
            df['Day']=df['Date_of_Journey'].dt.day
            df['Month']=df['Date_of_Journey'].dt.month
            df['Year']=df['Date_of_Journey'].dt.year
            logging.info('Conversion of the Date_of_Journey column Eded')

            # spliting the time to hour and min
            logging.info('Conversion of the Dep_hour column started')
            df["Dep_hour"] = df["Dep_Time"].str.split(":").str[0]
            df["Dep_min"] = df["Dep_Time"].str.split(":").str[1]
            # spliting the time to hour and min
            df["Arrival_Time"] = df["Arrival_Time"].str.split(" ").str[0]
            df["Arival_hour"] = df["Arrival_Time"].str.split(":").str[0]
            df["Arival_min"] = df["Arrival_Time"].str.split(":").str[1]
            logging.info('Conversion of the Dep_hour column Ended')


            # spliting the duration into hours and min saperate columns.
            df["Duration"] = df["Duration"].str.split(" ")
            df["Trveling_hour"] = df["Duration"].str[0].str.split("h").str[0]
            df["Trveling_min"] = df["Duration"].str[1].str.split("m").str[0]

            logging.info('Droping of the unwanted columns and duplicate records started')
            #df.drop_duplicates(inplace=True)
            df.drop(6474,axis=0,inplace=True)
            df.drop(labels=["Date_of_Journey","Route","Dep_Time","Arrival_Time","Duration","Additional_Info"],axis=1,inplace=True)
            logging.info('Droping of the unwanted columns and duplicate records Ended')
        

            # copy of the main data set to another folder artifacts and new file.
            os.makedirs(os.path.dirname(self.ingestion_config.raw_data_path),exist_ok=True)
            df.to_csv(self.ingestion_config.raw_data_path,index=False)   # saving the dataset to another folder.
            logging.info('Train test split')

            # Split the data set to Train and Test data set.
            # train_test_split will return the Train , Test data set. 
            train_set,test_set=train_test_split(df,test_size=0.30,random_state=42) 

            # save the Train data set to new folder and file. 
            # self.ingestion_config.train_data_path is the path to save the trained dataset. 
            train_set.to_csv(self.ingestion_config.train_data_path,index=False,header=True)
            # save the Test data set to new folder and file.
            test_set.to_csv(self.ingestion_config.test_data_path,index=False,header=True)

            logging.info('Ingestion of Data is completed')

            return(

                self.ingestion_config.train_data_path,
                self.ingestion_config.test_data_path
            )
  
            
        except Exception as e:
            logging.info('Exception occured at Data Ingestion stage')
            raise CustomException(e,sys)


""" 

if __name__=="__main__":
    obj=DataIngestion()
    train_data,test_data=obj.initiate_data_ingestion()
    
"""
"""
if __name__=='__main__':
    obj=DataIngestion()
    train_data_path,test_data_path=obj.initiate_data_ingestion()
    data_transformation = DataTransformation()
    train_arr,test_arr,_=data_transformation.initaite_data_transformation(train_data_path,test_data_path)

"""