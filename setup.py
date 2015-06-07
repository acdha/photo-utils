#!/usr/bin/env python

import os
import platform
import sys
import warnings

from setuptools import setup

setup(
    name="photo-utils",
    version='0.0.1',
    packages=find_packages(),
    author="Chris Adams",
    author_email="chris@improbable.org",
    license="CC0",
    description="Utilities for managing photograph collections",
    classifiers=[
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        ],
    install_requires=[
        'pyexiv2',
        'coloredlogs',
    ]
)
