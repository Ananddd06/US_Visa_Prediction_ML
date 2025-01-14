import os 
import sys
import numpy as np 
import pandas as pd
from sklearn.pipeline import Pipeline
from imblearn.combine import SMOTEENN
from sklearn.preprocessing import StandardScaler , OneHotEncoder , OrdinalEncoder , PowerTransFormer
from sklearn.compose import ColumnTransformer 
from us_visa.exception import Custom_Exception
from us_visa.logger import logging
from us_visa.entity.config_entity import DataTransformationConfig
from us_visa.utils.main_utils import read_yaml_file, save_object , drop_columns , save_numpy_array_data
from us_visa.entity.artifact_entity import (DataTransformationArtifact , 
                                            DataIngestionArtifact , 
                                            DataValidationArtifact)
from us_visa.constants import TARGET_COLUMN , CURRENT_YEAR , SCHEMA_FILE_PATH
from us_visa.entity.estimator import TargetValueMapping 

class DataTransformation:
    def __init__(self , data_ingestion_artifact : DataIngestionArtifact ,data_validation_artifact : DataValidationArtifact , data_transformation_config : DataTransformationConfig):
        try:
            self.data_ingestion_artifact = data_ingestion_artifact
            self.data_validation_artifact = data_validation_artifact
            self.data_transformation_config = data_transformation_config
            self.schema_config = read_yaml_file(file_path=SCHEMA_FILE_PATH)
        except Exception as e:
            raise Custom_Exception(e, sys)
    
    @staticmethod
    def read_data(file_path) -> DataFrame:
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise Custom_Exception(e, sys)

    def get_data_transformer_object(self)->Pipeline:
        try:
            logging.info(f"Entered the data transformer object under the DataTransformation class")
            logging.infd("Got the Numerical colms from the schema config file")
            numeric_transfor = StandardScaler()
            oh_transformer = OneHotEncoder()
            ordinal_encoder = OrdinalEncoder()

            logging.info("Initializing the standard Scaler , One hot encoder and the ordinal encoder ")

            oh_columns = self.schema_config['oh_columns']
            or_columns = self.schema_config['or_columns']
            transform_columns = self.schema_config['transform_columns']
            num_features = self.schema_config['num_features']

            logging.info("Initializing the Power Transformer")
            transform_pipe = Pipeline(
                steps=[
                    ('transformer', PowerTransformer(method='yeo-johnson'))
            ])
            logging.info("Initializing the ColumnTransformer")

            preprocessor = ColumnTransformer(
                [
                    ('OneHotEncoder', oh_transformer, oh_columns),
                    ('Ordinal_Encoder', ordinal_encoder, or_columns),
                    ('Transformer', transform_pipe, transform_columns),
                    ('StandardScaler' , numeric_transfor , num_features)
                ]
            )
            logging.info("Created Preprocessor object from the columntransformer")
            logging.info("Excited the transformer_object from the class of the datatransformer")
            return preprocessor
            
        except Exception as e:
            raise Custom_Exception(e, sys)
            