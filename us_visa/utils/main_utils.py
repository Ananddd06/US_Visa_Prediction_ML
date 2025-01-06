import os
import sys

import numpy as np 
import dill
import yaml
from pandas import Dataframe
from us_visa.logger import logging
from us_visa.exception import Custom_Exception

def read_yaml_file(file_path : str)-> dict:
    try:
        with open(file_path, 'rb') as file:
            return yaml.safe_load(file)
    except Exception as e:
        raise Custom_Exception(e , sys) from e

def write_yaml_file(file_path : str , content : object , replace : bool = False)->None:
    try:
        if replace:
            if os.path.exists(file_path):
                os.remove(file_path)
        os.makedirs(os.path.dirname(file_path) , exists_ok = True)
        with open(file_path, 'wb') as file:
            yaml.dump(content, file)
    except Exception as e:
        raise Custom_Exception(e , sys) from e

def load_obj(file_path : str) -> object:
    logging.info("Entered the load object method of Utils")
    try:
        with open(file_path, 'rb') as file:
            obj =  dill.load(file)
            logging.info("Excited the load object from the method utils")
            return obj
    except Exception as e:
        raise Custom_Exception(e , sys) from e

def save_numpy_array_data(file_path : str , array : np.array):
    try:
      dir_path = os.path.dirname(file_path)
      os.makedirs(dir_path , exists_ok = True)
      with open(file_path , "wb") as file_path:
        np.save(file_path , array)
    except Exception as e:
        raise Custom_Exception(e , sys) from e

def load_numpy_array_data(file_path : str)->np.array:
    try:
        with open(file_path , "rb") as file_path:
            return np.load(file_path)
    except Exception as e:
        raise Custom_Exception(e , sys) from e

def save_obj(file_path : str , obj : object)-> None:
    logging.info("Enter the save method object of the utils")
    try:
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path , exists_ok = True)
        with open(file_path , "wb") as file:
            dill.dump(obj , file)

        logging.info("Exciting the save object from the utils ")

    except Exception as e:
        raise Custom_Exception(e , sys) from e

def drop_colums(df : Dataframe , cols : list)-> Dataframe:
    logging.info("Enterd drop column of the Utils")
    try:
        return df.drop(cols , axis = 1)
        logging.info("Excited the drop columns of the method Utils ")
    except Exception as e:
        raise Custom_Exception(e , sys) from e