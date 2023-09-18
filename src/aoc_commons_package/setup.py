""" 
Used to setup the aoc_commons package.
1. Delete any existing dist folder from aoc_commons_package.
2. When updating, be sure to increment the version number.
3. Create the package. From the aoc_commons_package folder, run:
   py -m setup sdist
4. Upload to PyPi:
   twine upload dist/*
5. Install the package from venv at project folder level:
   py -m pip install dazbo-aoc-commons
"""
from setuptools import setup, find_packages

# Read the content of README.md
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()
    
setup(
    name='dazbo-aoc-commons',
    version='0.1.2',
    url='https://github.com/derailed-dash/Advent-of-Code',
    author='derailed-dash',
    description='A set up of helper functions and classes to assist with Advent of Code problems',
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),        
    install_requires=[],
)
