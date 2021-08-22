import os
from setuptools import setup

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "python-pylontech",
    version = "0.0.2",
    author = "Frank Villaro-Dixon",
    author_email = "frank@villaro-dixon.eu",
    description = ("Interfaces with Pylontech Batteries using RS485 protocol"),
    license = "MIT",
    keywords = "pylontech pylon rs485 lithium battery US2000 US2000C US3000",
    url = "http://github.com/Frankkkkk/python-pylontech",
    packages=['pylontech'],
    long_description=open("README.md", "r").read(),
    long_description_content_type="text/markdown",
    install_requires=['pyserial','construct'],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
        "License :: OSI Approved :: MIT License",
    ],
)
