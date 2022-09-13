from setuptools import setup


setup(
    name="python-pylontech",
    version="0.2.1",
    author="Frank Villaro-Dixon",
    author_email="frank@villaro-dixon.eu",
    description=("Interfaces with Pylontech Batteries using RS485 protocol"),
    license="MIT",
    keywords="pylontech pylon rs485 lithium battery US2000 US2000C US3000",
    url="http://github.com/Frankkkkk/python-pylontech",
    packages=['pylontech'],
    long_description=open("README.md", "r").read(),
    long_description_content_type="text/markdown",
    install_requires=['pyserial', 'construct'],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
        "License :: OSI Approved :: MIT License",
    ],
)
