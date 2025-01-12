from us_visa.configuration.mongodb_connection import MongoDBClient
from us_visa.constants import DATABASE_NAME
from us_visa.exception import Custom_Exception
import sys
import pandas as pd
import numpy as np 
from typing import Optional

class USvisaData:
    def __init__(self):
        try:
            self.mongo_client = MongoDBClient(database_name = DATABASE_NAME)
        except Exception as e:
            raise Custom_Exception(sys , e)
    
    def export_collection_as_dataframe(self , collection_name : str , database_name : optional):
        try:
            if database_name is None:
                collection = self.mongo_client.database[collection_name]
            else:
                collection = self.mongo_client.client[database_name][collection_name]
            
            df = pd.DataFrame(list(collection.find()))
            if "_id" in df.columns.to_list():
                df = df.drop(columns = ["_id"], axis = 1)
            df.replace({"na":np.nan} , inplace = True)
            return df
        except Exception as e:
            raise Custom_Exception(sys , e)

        