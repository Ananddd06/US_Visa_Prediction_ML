import json
import sys

import pandas as pd
from evidently.report import Report
from evidently.metric_preset import DataDriftPreset
from pandas import DataFrame

from us_visa.exception import Custom_Exception
from us_visa.logger import logging
from us_visa.utils.main_utils import read_yaml_file, write_yaml_file
from us_visa.entity.artifact_entity import DataIngestionArtifact, DataValidationArtifact
from us_visa.entity.config_entity import DataValidationConfig
from us_visa.constants import SCHEMA_FILE_PATH

class DataValidation:
    def __init__(self, data_ingestion_artifact: DataIngestionArtifact, data_validation_config: DataValidationConfig):
        """
        :param data_ingestion_artifact: Output reference of data ingestion artifact stage
        :param data_validation_config: configuration for data validation
        """
        try:
            self.data_ingestion_artifact = data_ingestion_artifact
            self.data_validation_config = data_validation_config
            self._schema_config = read_yaml_file(file_path=SCHEMA_FILE_PATH)
        except Exception as e:
            raise Custom_Exception(e, sys)

    def validate_number_of_columns(self, dataframe: DataFrame) -> bool:
        """
        Method Name :   validate_number_of_columns
        Description :   This method validates the number of columns
        
        Output      :   Returns bool value based on validation results
        On Failure  :   Write an exception log and then raise an exception
        """
        try:
            status = len(dataframe.columns) == len(self._schema_config["columns"])
            logging.info(f"Is required column present: [{status}]")
            return status
        except Exception as e:
            raise Custom_Exception(e, sys)

    def is_column_exist(self, df: DataFrame) -> bool:
        """
        Method Name :   is_column_exist
        Description :   This method validates the existence of numerical and categorical columns
        
        Output      :   Returns bool value based on validation results
        On Failure  :   Write an exception log and then raise an exception
        """
        try:
            dataframe_columns = df.columns
            missing_numerical_columns = []
            missing_categorical_columns = []

            for column in self._schema_config["numerical_columns"]:
                if column not in dataframe_columns:
                    missing_numerical_columns.append(column)

            if missing_numerical_columns:
                logging.info(f"Missing numerical columns: {missing_numerical_columns}")

            for column in self._schema_config["categorical_columns"]:
                if column not in dataframe_columns:
                    missing_categorical_columns.append(column)

            if missing_categorical_columns:
                logging.info(f"Missing categorical columns: {missing_categorical_columns}")

            return not (missing_numerical_columns or missing_categorical_columns)
        except Exception as e:
            raise Custom_Exception(e, sys) from e

    @staticmethod
    def read_data(file_path) -> DataFrame:
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise Custom_Exception(e, sys)

    def detect_dataset_drift(self, reference_df: DataFrame, current_df: DataFrame) -> bool:
        """
        Method Name :   detect_dataset_drift
        Description :   This method checks if data drift is detected between the reference and current dataframes.

        Output      :   Returns a boolean indicating if drift is detected.
        On Failure  :   Logs an exception and raises a custom exception.
        """
        try:
            logging.info("Starting data drift detection using Evidently.")

            # Initialize the data drift profile
            data_drift_profile = Profile(sections=[DataDriftProfileSection()])

            # Calculate the drift profile using reference and current datasets
            data_drift_profile.calculate(reference_df, current_df)

            # Convert the profile to JSON format
            report = data_drift_profile.json()
            json_report = json.loads(report)

            # Save the report to a YAML file for future reference
            write_yaml_file(file_path=self.data_validation_config.drift_report_file_path, content=json_report)

            # Safely extract metrics from the JSON report
            metrics = json_report.get("data_drift", {}).get("data", {}).get("metrics", {})
            n_features = metrics.get("n_features", 0)
            n_drifted_features = metrics.get("n_drifted_features", 0)
            drift_status = metrics.get("dataset_drift", False)

            logging.info(f"{n_drifted_features}/{n_features} features show drift.")
            logging.info(f"Drift detection status: {'Drift detected' if drift_status else 'No drift detected'}.")

            return drift_status

        except Exception as e:
            logging.error(f"Error during dataset drift detection: {str(e)}")
            raise Custom_Exception(e, sys) from e

    def initiate_data_validation(self) -> DataValidationArtifact:
        """
        Method Name :   initiate_data_validation
        Description :   Initiates the data validation component for the pipeline.

        Output      :   Returns DataValidationArtifact
        On Failure  :   Logs an exception and raises a custom exception
        """
        try:
            validation_error_msg = ""
            logging.info("Starting data validation.")

            train_df = self.read_data(file_path=self.data_ingestion_artifact.trained_file_path)
            test_df = self.read_data(file_path=self.data_ingestion_artifact.test_file_path)

            # Validate columns in training data
            if not self.validate_number_of_columns(dataframe=train_df):
                validation_error_msg += "Missing columns in training data. "

            # Validate columns in testing data
            if not self.validate_number_of_columns(dataframe=test_df):
                validation_error_msg += "Missing columns in testing data. "

            # Check if required columns exist
            if not self.is_column_exist(df=train_df):
                validation_error_msg += "Some columns are missing in training data. "

            if not self.is_column_exist(df=test_df):
                validation_error_msg += "Some columns are missing in testing data. "

            validation_status = len(validation_error_msg) == 0

            if validation_status:
                if self.detect_dataset_drift(train_df, test_df):
                    validation_error_msg += "Data drift detected. "
                    validation_status = False

            data_validation_artisfact = DataValidationArtifact(
                validation_status=validation_status,
                message=validation_error_msg,
                drift_report_file_path=self.data_validation_config.drift_report_file_name
            )

            logging.info(f"Data validation artifact created: {data_validation_artifact}")
            return data_validation_artifact
        except Exception as e:
            raise Custom_Exception(e, sys)
