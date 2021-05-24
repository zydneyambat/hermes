#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

import hermes

required = [
    "click==8.0.0",
    "pyyaml==5.4.1",
    "halo==0.0.31",
    "pydantic==1.8.2",
    "requests==2.25.1"
]

setup(
    author="Zydney Ambat",
    author_email="zydney.ambat@gmail.com",
    classifiers=[
        "Natural Language :: English",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
    ],
    description="New email notifier on Slack!",
    entry_points={
        "console_scripts": ["hermes=hermes.cli:cli"],
    },
    include_package_data=True,
    install_requires=required,
    name="hermes",
    packages=find_packages(exclude=("tests")),
    project_urls={
        "Source": "https://github.com/zydneyambat/hermes",
        "Tracker": "https://github.com/zydneyambat/hermes/issues",
    },
    python_requires=">=3.9",
    test_suite="tests",
    url="https://github.com/zydneyambat/hermes",
    version=hermes.__version__
)
