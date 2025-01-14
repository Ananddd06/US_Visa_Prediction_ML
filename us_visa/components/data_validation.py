import json
import os
import sys
import pandas as pd
from pandas import DataFrame
from us_visa.logger import logging
from us_visa.exception import Custom_Exception
from us_visa.utils.main_utils import read_yaml_file, write_yaml_file
from us_visa.entity.artifact_entity import DataIngestionArtifact, DataValidationArtifact
from us_visa.entity.config_entity import DataValidationConfig
from us_visa.constants import SCHEMA_FILE_PATH


## defining the class data validation 
class DataValidation:
    def __init__(self, data_ingestion_artifact: DataIngestionArtifact, data_validation_config: DataValidationConfig):
        try:
            self.data_ingestion_artifact = data_ingestion_artifact
            self.data_validation_config = data_validation_config
            self.schema_config = read_yaml_file(file_path=SCHEMA_FILE_PATH)
        except Exception as e:
            raise Custom_Exception(e, sys)

    # To find the no of columns in the dataset
    def validate_no_of_columns(self, dataframe: DataFrame) -> bool:
        try:
            status = len(dataframe.columns) == len(self.schema_config["columns"])
            logging.info(f"Is required column present: {status}")
            return status
        except Exception as e:
            raise Custom_Exception(e, sys)

    # Check if any columns are missing from numerical or categorical features
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

    # Manually detect dataset drift by comparing statistical features of the numerical columns
    def detect_dataset_drift(self, reference_df: DataFrame, current_df: DataFrame) -> bool:
        try:
            drift_status = False

            # Compare means and standard deviations of numerical columns between reference and current datasets
            numerical_columns = self.schema_config["numerical_columns"]

            for column in numerical_columns:
                if column in reference_df.columns and column in current_df.columns:
                    ref_mean = reference_df[column].mean()
                    ref_std = reference_df[column].std()

                    curr_mean = current_df[column].mean()
                    curr_std = current_df[column].std()

                    # Set a threshold for drift (e.g., 10% difference in mean or standard deviation)
                    mean_diff = abs(ref_mean - curr_mean) / ref_mean
                    std_diff = abs(ref_std - curr_std) / ref_std

                    if mean_diff > 0.1 or std_diff > 0.1:  # 10% difference
                        drift_status = True
                        logging.info(f"Drift detected in column: {column}. Mean diff: {mean_diff:.2f}, Std diff: {std_diff:.2f}")
            
            if not drift_status:
                logging.info("No drift detected in numerical columns.")

            return drift_status
        except Exception as e:
            logging.error(f"Error in detect_dataset_drift: {e}")
            raise Custom_Exception(sys, e)

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
                drift_report_file_path=self.data_validation_config.drift_report_file_name
            )
            logging.info(f"Data validation artifact: {data_validation_artifact}")
            return data_validation_artifact
        except Exception as e:
            raise Custom_Exception(e, sys)
