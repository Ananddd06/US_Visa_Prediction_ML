import json
import os
import sys
from pandas import DataFrame
from evidently.model_profile import Profile
from evidently.model_profile_sections import DataDriftProfileSection
from us_visa.logger import logging 
from us_visa.exception import Custom_Exception
from us_visa.utils.main_utils import read_yaml_file , write_yaml_file
from us_visa.entity.artifact_entity import DataIngestionArtifact , DataValidationArtifact
from us_visa.entity.config_entity import DataValidationConfig
from us_visa.constants import SCHEMA_FILE_PATH

class DataValidation:
    def __init__(self , data_ingestion_artifact : DataIngestionArtifact , data_validation_config : DataValidationConfig):
        try:
            self.data_ingestion_artifact = data_ingestion_artifact
            self.data_validation_config = data_validation_config
            self.schema_config = read_yaml_file(file_path = SCHEMA_FILE_PATH)
        except Exception as e:
            raise Custom_Exception(e, sys)
    
    def validate_no_of_columns(self , dataframe : DataFrame)->bool:
        try:
           status = len(dataframe.colums) == len(self.schema_config["columns"])
           logging.info(f"Is required column is present {status}")
           return status
        except Exception as e:
            raise Custom_Exception(e, sys)
    
    def is_column_exist(self , df : DataFrame)->bool:
        try:
            
            pass
        except Exception as e:
            raise Custom_Exception(e, sys)

