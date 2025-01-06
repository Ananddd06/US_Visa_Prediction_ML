from setuptools import find_packages , setup 
from typing import List


HYPEN_E_DOT = '-e .'
def get_requirements(file_path : str)->List[str]:
    requirements = []
    with open(file_path) as file_obj:
        requirements = file_obj.readlines()
        requirements = [req.replace("/n" , "") for req in requirements]

        if HYPEN_E_DOT in requirements:
            requirements.remove(HYPEN_E_DOT)
        
        return requirements

setup(
    name = "us_visa" ,
    version = "1.0.0" ,
    author = 'Anand J',
    author_email = 'anand06.jeyakumar@gmail.com',
    packages = find_packages(),
    install_requires = get_requirements('requirements.txt')
)