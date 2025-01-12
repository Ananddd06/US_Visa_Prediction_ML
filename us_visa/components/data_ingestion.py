import os 
import sys

from us_visa.logger import logging
from us_visa.exception import Custom_Exception
from us_visa.data_access.usvisa_data import USvisaData
from us_visa.entity.artifact_entity import DataIngestionArtifact
from us_visa.entity.config_entity import DataIngestionConfig

class DataIngestion:
    def __init__(self, data_ingestion_config : DataIngestionConfig = DataIngestion()):
        try:
            self.data_ingestion_config = data_ingestion_config
        except Exception as e:
            raise Custom_Exception(sys , e)