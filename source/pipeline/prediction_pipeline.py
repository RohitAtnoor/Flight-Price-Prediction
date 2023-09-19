import sys
import os
from source.exception import CustomException
from source.logger import logging
from source.utils import load_object
import pandas as pd

# creating the class for predicting the new data. 
class PredictPipeline:
    def __init__(self):
        pass
    
    # function returns the predicted value.
    # features is the input columns details.
    def predict(self,features):
        try:
            # getting the preprocessor and model pickle files path. 
            preprocessor_path=os.path.join('artifacts','preprocessor.pkl')
            model_path=os.path.join('artifacts','model.pkl')

            # opening the preprocessor and model file 
            # load_object is function in utilis to open the files. 
            preprocessor=load_object(preprocessor_path)
            model=load_object(model_path)

            # transforming the new data. 
            data_scaled=preprocessor.transform(features)

            # predicting the price. 
            pred=model.predict(data_scaled)
            return pred
            

        except Exception as e:
            logging.info("Exception occured in prediction")
            raise CustomException(e,sys)

class CustomData:
    def __init__(self,
                 Day:int,
                 Month:int,
                 Airline:str,
                 Source:str,
                 Destination:str,
                 Total_Stops:str,
                 Year:int,
                 Dep_hour:int,
                 Dep_min:int,
                 Arival_hour:int,
                 Arival_min:int,
                 Trveling_hour:int,
                 Trveling_min:int) -> None:
        
        self.Day = Day
        self.Month = Month
        self.Airline = Airline
        self.Source = Source
        self.Destination = Destination
        self.Total_Stops = Total_Stops
        self.Year = Year
        self.Dep_hour = Dep_hour
        self.Dep_min = Dep_min
        self.Arival_hour = Arival_hour
        self.Arival_min = Arival_min
        self.Trveling_hour=Trveling_hour
        self.Trveling_min=Trveling_min

    # storing the variables in the dictionary and converting to Dataframe. 
    def get_data_as_dataframe(self):
        try:
            custom_data_input_dict = {
                'Day':[self.Day],
                'Month':[self.Month],
                'Airline':[self.Airline],
                'Source':[self.Source],
                'Destination':[self.Destination],
                'Total_Stops':[self.Total_Stops],
                'Year':[self.Year],
                'Dep_hour':[self.Dep_hour], 
                'Dep_min':[self.Dep_min],
                'Arival_hour':[self.Arival_hour],
                'Arival_min':[self.Arival_min],
                'Trveling_hour':[self.Trveling_hour],
                'Trveling_min':[self.Trveling_min]
            }
            df = pd.DataFrame(custom_data_input_dict)
            logging.info('Dataframe Gathered')
            return df
        except Exception as e:
            logging.info('Exception Occured in prediction pipeline')
            raise CustomException(e,sys)