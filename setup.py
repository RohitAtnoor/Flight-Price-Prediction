from setuptools import find_packages,setup
from typing import List

HYPEN_E_DOT="-e ."

# Function to read the requirements.txt file
def get_requirements(file_path:str)->List[str]:
    requirements=[]
    with open(file_path) as file_obj:
        requirements=file_obj.readlines()
        requirements=[req.replace("\n","") for req in requirements]

        if HYPEN_E_DOT in requirements:
            requirements.remove(HYPEN_E_DOT)

    return requirements

# Below are the comman things to give in setup.py files.

setup(
    name='Flight_Price_Prediction',
    version='0.0.1',
    author='Rohit',
    author_email='my-email-id',
    install_requires=get_requirements('requirements.txt'),
    packages=find_packages()
)