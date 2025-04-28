from setuptools import setup, find_packages


#reading the requirnemtns file
with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="MLOps_Hotel_Reservation",
    version="0.1",
    author="vivek",
    packages=find_packages(), #this will automatically detects the packages i.e utils, src and other folders
    install_requires = requirements
)
