import sys
from us_visa.exception import Custom_Exception
from us_visa.logger import logging
from us_visa.components.data_ingestion import DataIngestion
from us_visa.components.data_validation import DataValidation
from us_visa.components.data_tranformation import DataTransformation
from us_visa.components.model_trainer import ModelTrainer
from us_visa.components.model_evaluation import ModelEvaluation
from us_visa.entity.config_entity import DataIngestionConfig, DataValidationConfig, DataTransformationConfig, ModelTrainerConfig, ModelEvaluationConfig
from us_visa.entity.artifact_entity import DataIngestionArtifact, DataValidationArtifact, DataTransformationArtifact, ModelTrainerArtifact, ModelEvaluationArtifact

class TrainPipeline:
    def __init__(self):
        self.data_ingestion_config = DataIngestionConfig()
        self.data_validation_config = DataValidationConfig()
        self.data_transformation_config = DataTransformationConfig()
        self.model_trainer_config = ModelTrainerConfig()
        self.model_evaluation_config = ModelEvaluationConfig()

    def start_data_ingestion(self) -> DataIngestionArtifact:
        try:
            logging.info("Starting data ingestion phase of the TrainPipeline.")
            data_ingestion = DataIngestion(data_ingestion_config=self.data_ingestion_config)
            data_ingestion_artifact = data_ingestion.initiate_data_ingestion()
            logging.info("Data ingestion completed successfully.")
            return data_ingestion_artifact
        except Exception as e:
            raise Custom_Exception(e, sys)

    def start_data_validation(self, data_ingestion_artifact: DataIngestionArtifact) -> DataValidationArtifact:
        try:
            logging.info("Starting data validation phase of the TrainPipeline.")
            data_validation = DataValidation(
                data_ingestion_artifact=data_ingestion_artifact,
                data_validation_config=self.data_validation_config
            )
            data_validation_artifact = data_validation.initiate_data_validation()
            logging.info("Data validation completed successfully.")
            return data_validation_artifact
        except Exception as e:
            raise Custom_Exception(e, sys)

    def start_data_transformation(self, data_ingestion_artifact: DataIngestionArtifact, data_validation_artifact: DataValidationArtifact) -> DataTransformationArtifact:
        try:
            logging.info("Starting data transformation phase of the TrainPipeline.")
            data_transformation = DataTransformation(
                data_ingestion_artifact=data_ingestion_artifact,
                data_validation_artifact=data_validation_artifact,
                data_transformation_config=self.data_transformation_config
            )
            data_transformation_artifact = data_transformation.initiate_data_transformation()
            logging.info("Data transformation completed successfully.")
            return data_transformation_artifact
        except Exception as e:
            raise Custom_Exception(e, sys)

    def start_model_trainer(self, data_transformation_artifact: DataTransformationArtifact) -> ModelTrainerArtifact:
        try:
            logging.info("Starting model training phase of the TrainPipeline.")
            model_trainer = ModelTrainer(
                data_transformation_artifact=data_transformation_artifact,
                model_trainer_config=self.model_trainer_config
            )
            model_trainer_artifact = model_trainer.initiate_model_trainer()
            logging.info("Model training completed successfully.")
            return model_trainer_artifact
        except Exception as e:
            raise Custom_Exception(e, sys)

    def start_model_evaluation(self, data_ingestion_artifact: DataIngestionArtifact, model_trainer_artifact: ModelTrainerArtifact) -> ModelEvaluationArtifact:
        try:
            logging.info("Starting model evaluation phase of the TrainPipeline.")
            model_evaluation = ModelEvaluation(
                model_eval_config=self.model_evaluation_config,
                data_ingestion_artifact=data_ingestion_artifact,
                model_trainer_artifact=model_trainer_artifact
            )
            model_evaluation_artifact = model_evaluation.initiate_model_evaluation()
            logging.info("Model evaluation completed successfully.")
            return model_evaluation_artifact
        except Exception as e:
            raise Custom_Exception(e, sys)

    def run_pipeline(self) -> None:
        try:
            logging.info("Starting the training pipeline.")
            data_ingestion_artifact = self.start_data_ingestion()
            data_validation_artifact = self.start_data_validation(data_ingestion_artifact=data_ingestion_artifact)
            data_transformation_artifact = self.start_data_transformation(
                data_ingestion_artifact=data_ingestion_artifact,
                data_validation_artifact=data_validation_artifact
            )
            model_trainer_artifact = self.start_model_trainer(data_transformation_artifact=data_transformation_artifact)
            model_evaluation_artifact = self.start_model_evaluation(
                data_ingestion_artifact=data_ingestion_artifact,
                model_trainer_artifact=model_trainer_artifact
            )
            logging.info("Training pipeline completed successfully.")
        except Exception as e:
            logging.error("Error occurred during the training pipeline.")
            raise Custom_Exception(e, sys)
