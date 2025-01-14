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
    
    def initiate_data_transformation(self ,_ )->DataTransformationArtifact:
        try:
            if self.data_validation_artifact.validation_status:
                logging.info("Started data Transformation")
                preprocessor = self.get_data_transformer_object()
                logging.info("Got the preprocessor object from the class of the datatransformer")
                train_df = DataTransformation.read_data(file_path = self.data_ingestion_artifact.trained_file_path)
                test_df = DataTransformation.read_data(file_path = self.data_ingestion_artifact.test_file_path)
                logging.info("Got the train and the set data set ")
                input_feature_train_df = train_df.drop(columns=[TARGET_COLUMN], axis=1)
                target_feature_train_df = train_df[TARGET_COLUMN]

                logging.info("Got train features and test features of Training dataset")

                input_feature_train_df['company_age'] = CURRENT_YEAR-input_feature_train_df['yr_of_estab']

                logging.info("Added company_age column to the Training dataset")

                drop_cols = self._schema_config['drop_columns']

                logging.info("drop the columns in drop_cols of Training dataset")

                input_feature_train_df = drop_columns(df=input_feature_train_df, cols = drop_cols)
                
                target_feature_train_df = target_feature_train_df.replace(
                    TargetValueMapping()._asdict()
                )


                input_feature_test_df = test_df.drop(columns=[TARGET_COLUMN], axis=1)

                target_feature_test_df = test_df[TARGET_COLUMN]


                input_feature_test_df['company_age'] = CURRENT_YEAR-input_feature_test_df['yr_of_estab']

                logging.info("Added company_age column to the Test dataset")

                input_feature_test_df = drop_columns(df=input_feature_test_df, cols = drop_cols)

                logging.info("drop the columns in drop_cols of Test dataset")

                target_feature_test_df = target_feature_test_df.replace(
                TargetValueMapping()._asdict()
                )

                logging.info("Got train features and test features of Testing dataset")

                logging.info(
                    "Applying preprocessing object on training dataframe and testing dataframe"
                )


                input_feature_test_arr = preprocessor.transform(input_feature_test_df)

                logging.info("Used the preprocessor object to transform the test features")

                logging.info("Applying SMOTEENN on Training dataset")

                smt = SMOTEENN(sampling_strategy="minority")

                input_feature_train_final, target_feature_train_final = smt.fit_resample(
                    input_feature_train_arr, target_feature_train_df
                )

                logging.info("Applied SMOTEENN on training dataset")

                logging.info("Applying SMOTEENN on testing dataset")

                input_feature_test_final, target_feature_test_final = smt.fit_resample(
                    input_feature_test_arr, target_feature_test_df
                )

                logging.info("Applied SMOTEENN on testing dataset")

                logging.info("Created train array and test array")

                train_arr = np.c_[
                    input_feature_train_final, np.array(target_feature_train_final)
                ]

                test_arr = np.c_[
                    input_feature_test_final, np.array(target_feature_test_final)
                ]

                save_object(self.data_transformation_config.transformed_object_file_path, preprocessor)
                save_numpy_array_data(self.data_transformation_config.transformed_train_file_path, array=train_arr)
                save_numpy_array_data(self.data_transformation_config.transformed_test_file_path, array=test_arr)

                logging.info("Saved the preprocessor object")

                logging.info(
                    "Exited initiate_data_transformation method of Data_Transformation class"
                )

                data_transformation_artifact = DataTransformationArtifact(
                    transformed_object_file_path=self.data_transformation_config.transformed_object_file_path,
                    transformed_train_file_path=self.data_transformation_config.transformed_train_file_path,
                    transformed_test_file_path=self.data_transformation_config.transformed_test_file_path
                )

                return data_transformation_artifact
        except Exception as e:
            raise Custom_Exception(e, sys)
