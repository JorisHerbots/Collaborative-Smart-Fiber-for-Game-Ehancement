#!/usr/bin/env python

import io

import re
from setuptools import setup


with io.open('engine/__init__.py', 'rt', encoding='utf8') as f:
    search = re.search(r'__version__ = \"(.*?)\"', f.read())
    version = "Unknown" if (search is None) else search.group(1)

setup(
    name="Engine",
    version=version,
    packages=["engine", "engine.hardware"]
)