from distutils.core import setup
from setuptools import setup, find_packages

setup(
    name='Udacity-capstone-python',
    version='0.1',
    author='Joseph Deutsch', 
    author_email='philippdeutsch@icloud.com',
    packages=find_packages(),
    long_description=open('README.md').read()
)