import os
import sys
import numpy as np
import pandas as pd
from sklearn.pipeline import Pipeline
from imblearn.combine import SMOTEENN
from sklearn.preprocessing import StandardScaler, OneHotEncoder, OrdinalEncoder, PowerTransformer
from sklearn.compose import ColumnTransformer
from us_visa.exception import Custom_Exception
from us_visa.logger import logging
from us_visa.entity.config_entity import DataTransformationConfig
from us_visa.utils.main_utils import read_yaml_file, save_obj, drop_columns, save_numpy_array_data
from us_visa.entity.artifact_entity import (
    DataTransformationArtifact,
    DataIngestionArtifact,
    DataValidationArtifact,
)
from us_visa.constants import TARGET_COLUMN, CURRENT_YEAR, SCHEMA_FILE_PATH
from us_visa.entity.estimator import TargetValueMapping

class DataTransformation:
    def __init__(self, data_ingestion_artifact: DataIngestionArtifact,
                 data_validation_artifact: DataValidationArtifact,
                 data_transformation_config: DataTransformationConfig):
        try:
            self.data_ingestion_artifact = data_ingestion_artifact
            self.data_validation_artifact = data_validation_artifact
            self.data_transformation_config = data_transformation_config
            self.schema_config = read_yaml_file(file_path=SCHEMA_FILE_PATH)
        except Exception as e:
            raise Custom_Exception(e, sys)
    
    @staticmethod
    def read_data(file_path) -> pd.DataFrame:
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise Custom_Exception(e, sys)

    def get_data_transformer_object(self) -> Pipeline:
        try:
            logging.info("Entered the data transformer object creation.")
            
            # Initialize transformers
            numeric_transformer = StandardScaler()
            one_hot_transformer = OneHotEncoder()
            ordinal_transformer = OrdinalEncoder()
            power_transformer = PowerTransformer(method="yeo-johnson")

            # Fetch columns from schema configuration
            oh_columns = self.schema_config["oh_columns"]
            or_columns = self.schema_config["or_columns"]
            transform_columns = self.schema_config["transform_columns"]
            num_features = self.schema_config["num_features"]

            logging.info("Setting up ColumnTransformer.")
            preprocessor = ColumnTransformer(
                transformers=[
                    ("OneHotEncoder", one_hot_transformer, oh_columns),
                    ("OrdinalEncoder", ordinal_transformer, or_columns),
                    ("PowerTransformer", power_transformer, transform_columns),
                    ("StandardScaler", numeric_transformer, num_features),
                ]
            )

            logging.info("Preprocessor object created successfully.")
            return preprocessor
        except Exception as e:
            raise Custom_Exception(e, sys)

    def initiate_data_transformation(self) -> DataTransformationArtifact:
        try:
            if not self.data_validation_artifact.validation_status:
                print("Data validation failed. Transformation aborted.")

            logging.info("Starting data transformation.")
            preprocessor = self.get_data_transformer_object()

            train_df = self.read_data(file_path=self.data_ingestion_artifact.trained_file_path)
            test_df = self.read_data(file_path=self.data_ingestion_artifact.test_file_path)

            logging.info("Splitting input and target features for train and test datasets.")
            input_feature_train_df = train_df.drop(columns=[TARGET_COLUMN], axis=1)
            target_feature_train_df = train_df[TARGET_COLUMN]

            input_feature_test_df = test_df.drop(columns=[TARGET_COLUMN], axis=1)
            target_feature_test_df = test_df[TARGET_COLUMN]

            # Compute company age
            input_feature_train_df["company_age"] = CURRENT_YEAR - input_feature_train_df["yr_of_estab"]
            input_feature_test_df["company_age"] = CURRENT_YEAR - input_feature_test_df["yr_of_estab"]

            # Drop specified columns
            drop_cols = self.schema_config["drop_columns"]
            input_feature_train_df = drop_columns(df=input_feature_train_df, cols=drop_cols)
            input_feature_test_df = drop_columns(df=input_feature_test_df, cols=drop_cols)

            # Map target values
            target_feature_train_df = target_feature_train_df.replace(TargetValueMapping()._asdict())
            target_feature_test_df = target_feature_test_df.replace(TargetValueMapping()._asdict())

            # Apply preprocessor
            input_feature_train_arr = preprocessor.fit_transform(input_feature_train_df)
            input_feature_test_arr = preprocessor.transform(input_feature_test_df)

            # Apply SMOTEENN
            smt = SMOTEENN(sampling_strategy="minority")
            input_feature_train_final, target_feature_train_final = smt.fit_resample(
                input_feature_train_arr, target_feature_train_df
            )
            input_feature_test_final, target_feature_test_final = smt.fit_resample(
                input_feature_test_arr, target_feature_test_df
            )

            # Combine features and targets
            train_arr = np.c_[
                input_feature_train_final, np.array(target_feature_train_final)
            ]
            test_arr = np.c_[
                input_feature_test_final, np.array(target_feature_test_final)
            ]

            # Save objects
            save_obj(self.data_transformation_config.transformed_object_file_path, preprocessor)
            save_numpy_array_data(self.data_transformation_config.transformed_train_file_path, array=train_arr)
            save_numpy_array_data(self.data_transformation_config.transformed_test_file_path, array=test_arr)

            logging.info("Data transformation completed successfully.")

            return DataTransformationArtifact(
                transformed_object_file_path=self.data_transformation_config.transformed_object_file_path,
                transformed_train_file_path=self.data_transformation_config.transformed_train_file_path,
                transformed_test_file_path=self.data_transformation_config.transformed_test_file_path,
            )
        except Exception as e:
            raise Custom_Exception(e, sys)
