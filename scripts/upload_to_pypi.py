""" Python to upload the dist folder to PyPi """
import os
import subprocess
from dotenv import load_dotenv

def upload_to_pypi():
    """ 
    So that we can skip having to run this command (and pass in username and pwd) separately:
    twine upload dist/*
    """
    load_dotenv()
   
    # expect vars to be stored in .env or environment vars
    username = os.getenv('PYPI_USERNAME')
    api_key = os.getenv('PYPI_API_KEY')

    if username is None or api_key is None:
        raise ValueError("PYPI_USERNAME and/or PYPI_PASSWORD are not set in the .env file")

    try:
        subprocess.run(['twine', 'upload', 'dist/*', '-u', username, '-p', api_key], check=True)
    except subprocess.CalledProcessError as e:
        print(f"An error occurred during the upload: {e}")

upload_to_pypi()
