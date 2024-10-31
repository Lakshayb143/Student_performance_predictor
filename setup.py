from setuptools import setup, find_packages
from typing import List

HYPEHN_E_DOT = '-e .'

def get_requirements(filename:str) -> List[str]:
    requirements = []
    with open(filename, 'r') as f:
        requirements = f.readlines()
        requirements = [req.replace('\n',"") for req in requirements]

        if HYPEHN_E_DOT in requirements:
            requirements.remove(HYPEHN_E_DOT)

    return requirements



setup(
    name='ML_Project',
    version='1.0.0',
    author='Lakshay Bhatia',
    author_email='lakshaybhatia46@gmail.com',
    packages=find_packages(),
    install_requires=get_requirements('requirements.txt')
)