import os 
from datetime import date

DATABASE_NAME = "US_VISA"
COLLECTION_NAME = "visa_data"
MONGO_DB_URL = "MONGODB_URL"

PIPELINE_NAME : str = "usvisa"
ARTIFACT_DIR : str = 'artifact'

MODEL_FILE_NAME = "model.pkl"

TRAIN_FILE_NAME: str = "train.csv"
TEST_FILE_NAME: str = "test.csv"

FILE_NAME: str = "usvisa.csv"
MODEL_FILE_NAME = "model.pkl"

TARGET_COLUMN = "case_status"
CURRENT_YEAR = date.today().year
PREPROCSSING_OBJECT_FILE_NAME = "preprocessing.pkl"
SCHEMA_FILE_PATH = os.path.join("config", "schema.yaml")

"""
Data ingestion releated constants start with the DATA_INGESTION var name

"""
DATA_INGESTION_COLLECTION_NAME : str = "visa_data"
DATA_INGESTION_DIR_NAME : str = "data_ingestion"
DATA_INGESTION_FEATURE_STORE_DIR : str = "feature_store"
DATA_INGESTION_INGESTED_DIR : str = "ingested"
DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO : float = 0.2

"""
Data validation releated constants start with the DATA_VALIDATION var name

"""

DATA_VALIDATION_DIR_NAME : str = "data_validation"
DATA_VALIDATION_DRIFT_REPORT_DIR : str = "drift_report"
DATA_VALIDATION_DRIFT_REPORT_FILE_NAME : str = "report.yaml"

"""
Data transformation releated constants start with the DATA_TRANSFORMATION var name

"""
DATA_TRANSFORMATION_DIR_NAME : str = "data_transformation"

