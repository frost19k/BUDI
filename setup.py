#!/usr/bin/env python3

""" __Doc__ File handle class """
from setuptools import find_packages, setup
from src.__version__ import __version__

setup(
    name="BUDI",
    version=__version__,
    url="https://github.com/frost19k/BUDI",
    license="GPLv3",
    description="Refresh a list of docker containers if newer version exists",
    author="Hoodly Twokeys",
    author_email="hoodlytwokeys@gmail.com",
    packages=find_packages(),
    entry_points={
        'console_scripts': ['budi=src.__main__:main']
    },
    install_requires=open('requirements.txt').read().splitlines(),
    include_package_data=False,
    zip_safe=False
)
