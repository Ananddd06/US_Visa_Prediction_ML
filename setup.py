from setuptools import find_packages , setup
import os 
import sys
from us_visa.exception import Custom_Exception 
from us_visa.logger import logging
from typing import List


HYPEN_E_DOT = '-e .'
def get_requirements(file_path : str)->List[str]:
    requirements = []
    try:
        with open(file_path) as file_obj:
            requirements = file_obj.readlines()
            requirements = [req.replace("\n" , "") for req in requirements]

            if HYPEN_E_DOT in requirements:
                requirements.remove(HYPEN_E_DOT)
        
        logging.info("The requirements is Done successfully")
    except Exception as e:
        raise Custom_Exception(e , sys)
    
    return requirements

setup(
    name = "us_visa" ,
    version = "1.0.0" ,
    author = 'Anand J',
    author_email = 'anand06.jeyakumar@gmail.com',
    packages = find_packages(),
    install_requires = get_requirements('requirements.txt')
)