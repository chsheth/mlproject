import os
import sys
from src.logger import logging
from src.exception import CustomException
import pandas as pd

from sklearn.model_selection import train_test_split
from dataclasses import dataclass #to create class variables


## all information that is needed to configure the data ingestion goes in this Class
## typically used for class variables
## here we are using this to provide the path information for where the data will be saved

@dataclass 
class DataIngestionConfig:
    train_data_path:str = os.path.join('artifacts', 'train.csv')
    test_data_path:str = os.path.join('artifacts', 'test.csv')
    raw_data_path:str = os.path.join('artifacts', 'raw.csv')

class DataIngestion:
    
    def __init__(self):
        ## getting all the class variables from the dataclass
        self.ingestion_config = DataIngestionConfig() 
    
    def initiate_data_ingestion(self):
        # log everthing for it to appear in the logger
        logging.info("Entered the data ingestion method")
        # everything in try - except block so that Custom Exception can be applied
        try:
            # can use any way to get the data (json, monngo etc.)    
            df = pd.read_csv('notebook\data\stud.csv')
            logging.info('Read the dataframe')
            # here, we create the artifact folder 
            os.makedirs(os.path.dirname(self.ingestion_config.train_data_path), exist_ok=True)
            # here, we save the entire dataframe as csv
            df.to_csv(self.ingestion_config.raw_data_path, index=False, header=True)

            logging.info('Train test split initiated')
            # here we create train - test dataframes
            train_set, test_set = train_test_split(df, test_size=0.2, random_state=42)
            # here, we save the test and train dataframes separately as csv
            train_set.to_csv(self.ingestion_config.train_data_path, index=False, header=True)
            test_set.to_csv(self.ingestion_config.test_data_path, index=False, header=True)
            logging.info('Ingestion of data is complete')
            # return the path strings for train and test set to call the dataframes
            return(
                self.ingestion_config.train_data_path,
                self.ingestion_config.test_data_path
            )
        except Exception as e:
            raise CustomException(e, sys)

## the following code will test if the data_ingestion.py is working
## this code will create an artifact folder and save all the data - raw, test and train

#if __name__ == "__main__":
#    obj=DataIngestion()
#    obj.initiate_data_ingestion()

