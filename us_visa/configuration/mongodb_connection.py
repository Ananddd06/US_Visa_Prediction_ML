import os 
import sys 
from us_visa.logger import logging
from us_visa.exception import Custom_Exception
from us_visa.constants import DATABASE_NAME , MONGO_DB_URL

import pymongo
import certifi

ca = certifi.where()

class MongoDBClient:
    client = None

    def __init__(self , database_name = DATABASE_NAME)-> None:
        try:
            if MongoDBClient.client is None:
                mongo_db_url = os.getenv(MONGO_DB_URL)
                if mongo_db_url is None:
                    raise Exception(f"Environment key : {MONGO_DB_URL} is not set")
                MongoDBClient.client = pymongo.MongoClient(mongo_db_url , tlsCAFile = ca)
            self.client = MongoDBClient.client
            self.database = self.client[database_name]
            self.database_name = database_name
            logger.info("Database  connection is succesfull")
        except Exception as e:
            raise Custom_Exception(sys , e)

