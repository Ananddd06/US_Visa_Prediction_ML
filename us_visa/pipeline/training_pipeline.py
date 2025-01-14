import sys
from us_visa.exception import Custom_Exception
from us_visa.logger import logging
from us_visa.components.data_ingestion import DataIngestion
from us_visa.components.data_validation import DataValidation
from us_visa.components.data_tranformation import DataTransformation
from us_visa.entity.config_entity import DataIngestionConfig, DataValidationConfig , DataTransformationConfig
from us_visa.entity.artifact_entity import DataIngestionArtifact, DataValidationArtifact , DataTransformationArtifact

class TrainPipeline:
    def __init__(self):
        self.data_ingestion_config = DataIngestionConfig()
        self.data_validation_config = DataValidationConfig()
        self.data_transformation_config = DataTransformationConfig()
    
    def start_data_ingestion(self) -> DataIngestionArtifact:
        try:
            logging.info("Entered the start_data_ingestion of the TrainPipeline Class")
            logging.info("Getting the data from MongoDB")
            data_ingestion = DataIngestion(data_ingestion_config=self.data_ingestion_config)
            data_ingestion_artifact = data_ingestion.initiate_data_ingestion()
            logging.info("Got the train and the test set from MongoDB")
            logging.info("Excited about the Data Ingestion workflow")
            return data_ingestion_artifact
        except Exception as e:
            raise Custom_Exception(e, sys)
    
    def start_data_validation(self, data_ingestion_artifact: DataIngestionArtifact) -> DataValidationArtifact:
        logging.info("Entered the start_data_validation of the TrainPipeline Class")
        try:
            data_validation = DataValidation(
                data_ingestion_artifact=data_ingestion_artifact,
                data_validation_config=self.data_validation_config
            )
            data_validation_artifact = data_validation.initiate_data_validation()
            logging.info("Performed the data validation operation")
            logging.info("Exited the start_data_validation method of TrainPipeline class")
            return data_validation_artifact
        except Exception as e:
            raise Custom_Exception(e, sys)
    
    def start_data_transformation(self , data_ingestion_artifact : DataIngestionArtifact , data_validation_artifact : DataValidationArtifact)->DataTransformationArtifact:
        logging.info("Entered the start_data_transformation of the TrainPipeline Class")
        try:
            data_transformation = DataTransformation(
                data_ingestion_artifact=data_ingestion_artifact,
                data_validation_artifact=data_validation_artifact,
                data_transformation_config=self.data_transformation_config
            )
            data_transformation_artifact = data_transformation.initiate_data_transformation()
            logging.info("Started the data transformation operation")
            logging.info("Exited the start_data_transformation method of TrainPipeline class")
            return data_transformation_artifact
        except Exception as e:
            raise Custom_Exception(e, sys)
    
    def run_pipeline(self) -> None:
        try:
            data_ingestion_artifact = self.start_data_ingestion()
            data_validation_artifact = self.start_data_validation(data_ingestion_artifact = data_ingestion_artifact)
            data_transformation_artifact = self.start_data_transformation(data_ingestion_artifact = data_ingestion_artifact 
                                            , data_validation_artifact = data_validation_artifact)
        except Exception as e:
            raise Custom_Exception(sys, e)
