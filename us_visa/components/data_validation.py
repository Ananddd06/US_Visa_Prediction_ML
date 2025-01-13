import json
import os
import sys
import pandas as pd
from pandas import DataFrame
from evidently.report import Report
from evidently.metric_preset import DataDriftPreset
from us_visa.logger import logging
from us_visa.exception import Custom_Exception
from us_visa.utils.main_utils import read_yaml_file, write_yaml_file
from us_visa.entity.artifact_entity import DataIngestionArtifact, DataValidationArtifact
from us_visa.entity.config_entity import DataValidationConfig
from us_visa.constants import SCHEMA_FILE_PATH

class DataValidation:
    def __init__(self, data_ingestion_artifact: DataIngestionArtifact, data_validation_config: DataValidationConfig):
        try:
            self.data_ingestion_artifact = data_ingestion_artifact
            self.data_validation_config = data_validation_config
            self.schema_config = read_yaml_file(file_path=SCHEMA_FILE_PATH)
        except Exception as e:
            raise Custom_Exception(e, sys)

    def validate_no_of_columns(self, dataframe: DataFrame) -> bool:
        try:
            status = len(dataframe.columns) == len(self.schema_config["columns"])
            logging.info(f"Is required column present: {status}")
            return status
        except Exception as e:
            raise Custom_Exception(e, sys)

    def is_column_exist(self, df: DataFrame) -> bool:
        try:
            dataframe_columns = df.columns
            missing_numerical_columns = []
            missing_categorical_columns = []

            # Check for missing numerical columns
            for column in self.schema_config["numerical_columns"]:
                if column not in dataframe_columns:
                    missing_numerical_columns.append(column)
            if missing_numerical_columns:
                logging.info(f"Missing numerical columns: {missing_numerical_columns}")

            # Check for missing categorical columns
            for column in self.schema_config["categorical_columns"]:
                if column not in dataframe_columns:
                    missing_categorical_columns.append(column)
            if missing_categorical_columns:
                logging.info(f"Missing categorical columns: {missing_categorical_columns}")

            # If any columns are missing, return False
            return len(missing_numerical_columns) == 0 and len(missing_categorical_columns) == 0
        except Exception as e:
            raise Custom_Exception(e, sys)

    @staticmethod
    def read_data(file_path) -> DataFrame:
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise Custom_Exception(e, sys)

    def detect_dataset_drift(self, reference_df: DataFrame, current_df: DataFrame) -> bool:
        try:
            # Using Report and DataDriftPreset from Evidently
            report = Report(metrics=[DataDriftPreset()])
            report.run(reference_data=reference_df, current_data=current_df)
            report_json = report.json()

            logging.info(f"Drift report JSON: {report_json}")

            # Saving the drift report to YAML
            # Fix: Ensure the report is in a valid format for json.loads()
            try:
                json_report = json.loads(report_json)  # Parse JSON string to a dictionary
            except json.JSONDecodeError as json_err:
                logging.error(f"JSONDecodeError while processing the drift report: {json_err}")
                raise Custom_Exception(f"JSONDecodeError: {json_err}", sys)

            write_yaml_file(file_path=self.data_validation_config.drift_report_file_name, content=json_report)

            # Ensure that 'data_drift' exists in the report before accessing it
            if "data_drift" in json_report:
                # Extracting metrics safely
                data_drift = json_report["data_drift"]
                if "data" in data_drift and "metrics" in data_drift["data"]:
                    metrics = data_drift["data"]["metrics"]
                    n_features = metrics.get("n_features", 0)
                    n_drifted_features = metrics.get("n_drifted_features", 0)
                    logging.info(f"{n_drifted_features}/{n_features} drift detected.")

                    # Return the drift status, with a fallback if it's not available
                    drift_status = metrics.get("dataset_drift", False)
                    return drift_status
                else:
                    logging.error("Metrics missing in the 'data_drift' section of the report.")
                    raise Custom_Exception("Missing 'metrics' in the drift report", sys)
            else:
                logging.error("'data_drift' key not found in the drift report.")
                raise Custom_Exception("'data_drift' key missing in drift report", sys)

        except Exception as e:
            logging.error(f"Error in detect_dataset_drift: {e}")
            raise Custom_Exception(sys,e)

    def initiate_data_validation(self) -> DataValidationArtifact:
        try:
            validation_error_msg = ""
            logging.info("Started the Data Validation flow")

            # Read the data from files
            train_df, test_df = (
                DataValidation.read_data(file_path=self.data_ingestion_artifact.trained_file_path),
                DataValidation.read_data(file_path=self.data_ingestion_artifact.test_file_path)
            )

            # Logging the shapes of the DataFrames to check the data
            logging.info(f"Training DataFrame shape: {train_df.shape}")
            logging.info(f"Testing DataFrame shape: {test_df.shape}")

            # Validate columns in training and testing data
            status = self.validate_no_of_columns(dataframe=train_df)
            logging.info(f"All required columns present in training dataframe: {status}")
            if not status:
                validation_error_msg += f"Columns are missing in training dataframe."

            status = self.validate_no_of_columns(dataframe=test_df)
            logging.info(f"All required columns present in testing dataframe: {status}")
            if not status:
                validation_error_msg += f"Columns are missing in test dataframe."

            status = self.is_column_exist(df=train_df)
            if not status:
                validation_error_msg += f"Columns are missing in training dataframe."
            
            status = self.is_column_exist(df=test_df)
            if not status:
                validation_error_msg += f"Columns are missing in test dataframe."

            validation_status = len(validation_error_msg) == 0

            if validation_status:
                drift_status = self.detect_dataset_drift(train_df, test_df)
                if drift_status:
                    logging.info(f"Drift detected.")
                    validation_error_msg = "Drift detected"
                else:
                    validation_error_msg = "Drift not detected"
            else:
                logging.info(f"Validation_error: {validation_error_msg}")

            # Create and return DataValidationArtifact
            data_validation_artifact = DataValidationArtifact(
                validation_status=validation_status,
                message=validation_error_msg,
                drift_report_file_path=self.data_validation_config.drift_report_file_path
            )
            logging.info(f"Data validation artifact: {data_validation_artifact}")
            return data_validation_artifact
        except Exception as e:
            raise Custom_Exception(e, sys)
