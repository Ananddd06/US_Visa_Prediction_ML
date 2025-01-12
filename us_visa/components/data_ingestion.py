import os
import sys
import pandas as pd
from pandas import DataFrame
from sklearn.model_selection import train_test_split  # Ensure this is imported

from us_visa.logger import logging
from us_visa.exception import Custom_Exception
from us_visa.data_access.usvisa_data import USvisaData
from us_visa.entity.artifact_entity import DataIngestionArtifact
from us_visa.entity.config_entity import DataIngestionConfig
from us_visa.constants import DATA_INGESTION_INGESTED_DIR  # Ensure constant is imported

class DataIngestion:
    def __init__(self, data_ingestion_config : DataIngestionConfig = DataIngestionConfig()):
        try:
            self.data_ingestion_config = data_ingestion_config
        except Exception as e:
            raise Custom_Exception(sys , e)

    def export_data_into_feature_store(self) -> DataFrame:
        try:
            logging.info("Exporting data into MongoDb")
            usvisa_data = USvisaData()
            dataframe = usvisa_data.export_collection_as_dataframe(collection_name=self.data_ingestion_config.collection_name)
            logging.info(f"Shape of the dataset: {dataframe.shape}")
            feature_store_file_path = self.data_ingestion_config.feature_store_file_path
            dir_path = os.path.dirname(feature_store_file_path)
            os.makedirs(dir_path, exist_ok=True)
            logging.info(f"Saving exported data into feature store file path: {feature_store_file_path}")
            dataframe.to_csv(feature_store_file_path, index=False, header=True)
            return dataframe
        except Exception as e:
            raise Custom_Exception(sys, e)
    
    def split_data_as_train_and_test(self, dataframe: DataFrame) -> None:
        logging.info("Entered split_data_as_train_and_test method of the Data Ingestion class")
        try:
            # Split the dataframe into train and test sets
            train_set, test_set = train_test_split(dataframe, test_size=self.data_ingestion_config.train_test_split_ratio, random_state=42)
            logging.info("Split the data frame successfully")
            
            # Ensure the directories exist and paths are correct under the 'ingested' folder
            os.makedirs(os.path.dirname(self.data_ingestion_config.training_file_path), exist_ok=True)
            os.makedirs(os.path.dirname(self.data_ingestion_config.testing_file_path), exist_ok=True)
            
            logging.info("Exporting the data frame into train and test data frames")
            train_set.to_csv(self.data_ingestion_config.training_file_path, index=False, header=True)
            test_set.to_csv(self.data_ingestion_config.testing_file_path, index=False, header=True)
            logging.info("Exported the data frame into train and test datasets")
        except Exception as e:
            raise Custom_Exception(e, sys)
    
    def initiate_data_ingestion(self) -> DataIngestionArtifact:
        logging.info("Initiating Data Ingestion")
        try:
            # Export data from MongoDB
            dataframe = self.export_data_into_feature_store()
            logging.info("Got the data from MongoDB")
            
            # Perform the train-test split
            self.split_data_as_train_and_test(dataframe)
            logging.info("Executed the train-test split")
            logging.info("Exited initiate_data_ingestion method of DataIngestion class")
            
            # Create DataIngestionArtifact with paths for train and test data
            data_ingestion_artifact = DataIngestionArtifact(
                trained_file_path=self.data_ingestion_config.training_file_path,
                test_file_path=self.data_ingestion_config.testing_file_path
            )
            logging.info(f"Data ingestion artifact: {data_ingestion_artifact}")
            return data_ingestion_artifact
        except Exception as e:
            raise Custom_Exception(e, sys)
