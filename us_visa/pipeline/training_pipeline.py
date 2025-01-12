import sys 
from us_visa.exception import Custom_Exception
from us_visa.logger import logging
from us_visa.components.data_ingestion import DataIngestion
from us_visa.entity.config_entity import DataIngestionConfig
from us_visa.entity.artifact_entity import DataIngestionArtifact

class TrainPipeline:
    def __init__(self):
        self.data_ingestion_config = DataIngestionConfig()
    
    def start_data_ingestion(self)->DataIngestionArtifact:
        try:
            logging.info(f"Entered the start_data_ingestion of the TrainPipeline Class")
            logging.info(f"Getting the data from the mongoDb")
            data_ingestion = DataIngestion(data_ingestion_config = self.data_ingestion_config)
            data_ingestion_artifact = data_ingestion.initiate_data_ingestion()
            logging.info(f"Got the train and the test set from the mongoDb")
            logging.info(f"Excited from the Data Ingestion workflow")
            return data_ingestion_artifact
        except Exception as e:
            raise Custom_Exception(e , sys)
    
    def run_pipeline(self, )-> None:
        try:
            data_ingestion_artifact = self.start_data_ingestion()
        except Exception as e:
            raise Custom_Exception(sys,e)