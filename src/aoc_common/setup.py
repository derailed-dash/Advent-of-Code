""" 
Used to setup the aoc_commons package.
Make sure you have installed twine first.
py -m pip install twine

1.  Delete any existing dist folder from aoc_commons_package.
2.  Before updating, be sure to increment the version number.
3.  Create the package. From the aoc_commons_package folder, run:
    py -m setup sdist
4.  Upload to PyPi:
    twine upload dist/*
5.  Install the package from your venv at the project folder level:
    py -m pip install dazbo-aoc-commons
"""
from setuptools import setup
   
setup(
    name='dazbo-aoc-commons',
    version='0.1.10',
    url='https://github.com/derailed-dash/Advent-of-Code',
    author='derailed-dash',
    description='A set up of helper functions and classes to assist with Advent of Code problems',
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    py_modules=["aoc_commons"],
    package_dir={'': '.'},  # Current directory   
    install_requires=[],
)
