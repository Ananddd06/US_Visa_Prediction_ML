from us_visa.entity.config_entity import ModelEvaluationConfig
from us_visa.entity.artifact_entity import ModelTrainerArtifact, DataIngestionArtifact, ModelEvaluationArtifact
from sklearn.metrics import f1_score
from us_visa.exception import Custom_Exception
from us_visa.constants import TARGET_COLUMN, CURRENT_YEAR
from us_visa.logger import logging
import sys
import pandas as pd
from typing import Optional
from us_visa.entity.estimator import USvisaModel
from us_visa.entity.estimator import TargetValueMapping
from us_visa.utils.main_utils import load_obj  # Assume this utility function loads a serialized model object from the file system
from dataclasses import dataclass

@dataclass
class EvaluateModelResponse:
    trained_model_f1_score: float
    best_model_f1_score: float
    is_model_accepted: bool
    difference: float


class ModelEvaluation:

    def __init__(self, model_eval_config: ModelEvaluationConfig, data_ingestion_artifact: DataIngestionArtifact,
                 model_trainer_artifact: ModelTrainerArtifact):
        try:
            self.model_eval_config = model_eval_config
            self.data_ingestion_artifact = data_ingestion_artifact
            self.model_trainer_artifact = model_trainer_artifact
        except Exception as e:
            raise Custom_Exception(e, sys)

    def get_best_model(self) -> Optional[USvisaModel]:
        """
        Method Name :   get_best_model
        Description :   This function is used to get the best model available locally

        Output      :   Returns model object if available locally
        On Failure  :   Write an exception log and then raise an exception
        """
        try:
            best_model_path = self.model_eval_config.best_model_path
            if best_model_path is not None:
                return load_obj(file_path=best_model_path)
            return None
        except Exception as e:
            raise Custom_Exception(e, sys)

    def evaluate_model(self) -> EvaluateModelResponse:
        """
        Method Name :   evaluate_model
        Description :   This function is used to evaluate the trained model
                        against the best model available locally

        Output      :   Returns an EvaluateModelResponse object
        On Failure  :   Write an exception log and then raise an exception
        """
        try:
            test_df = pd.read_csv(self.data_ingestion_artifact.test_file_path)
            test_df['company_age'] = CURRENT_YEAR - test_df['yr_of_estab']

            x, y = test_df.drop(TARGET_COLUMN, axis=1), test_df[TARGET_COLUMN]
            y = y.replace(
                TargetValueMapping()._asdict()
            )

            # Load the trained model
            trained_model = load_obj(file_path=self.model_trainer_artifact.trained_model_file_path)
            trained_model_f1_score = f1_score(y, trained_model.predict(x))

            best_model_f1_score = None
            best_model = self.get_best_model()
            if best_model is not None:
                y_hat_best_model = best_model.predict(x)
                best_model_f1_score = f1_score(y, y_hat_best_model)

            tmp_best_model_score = 0 if best_model_f1_score is None else best_model_f1_score
            result = EvaluateModelResponse(trained_model_f1_score=trained_model_f1_score,
                                           best_model_f1_score=best_model_f1_score,
                                           is_model_accepted=trained_model_f1_score > tmp_best_model_score,
                                           difference=trained_model_f1_score - tmp_best_model_score
                                           )
            logging.info(f"Result: {result}")
            return result

        except Exception as e:
            raise Custom_Exception(e, sys)

    def initiate_model_evaluation(self) -> ModelEvaluationArtifact:
        """
        Method Name :   initiate_model_evaluation
        Description :   This function is used to initiate all steps of the model evaluation

        Output      :   Returns model evaluation artifact
        On Failure  :   Write an exception log and then raise an exception
        """
        try:
            evaluate_model_response = self.evaluate_model()

            model_evaluation_artifact = ModelEvaluationArtifact(
                is_model_accepted=evaluate_model_response.is_model_accepted,
                best_model_path=self.model_eval_config.best_model_path,
                trained_model_path=self.model_trainer_artifact.trained_model_file_path,
                changed_accuracy=evaluate_model_response.difference)

            logging.info(f"Model evaluation artifact: {model_evaluation_artifact}")
            return model_evaluation_artifact
        except Exception as e:
            raise Custom_Exception(e, sys) 
