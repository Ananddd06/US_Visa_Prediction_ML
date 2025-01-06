from us_visa.logger import logging
from us_visa.exception import Custom_Exception
import os 
import sys

logging.info("Addition of the 2 numbers ")

try : 
    def add(a : int , b : int):
        return a + b

    num1 = int(input("Enter the number"))
    num2 = int(input("Enter the number"))
    print("The addition of two number " , add(num1 , num2))
except Exception as e:
    raise Custom_Exception(e , sys)

