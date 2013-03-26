#!/usr/env python

from setuptools import setup

setup(
    name='pyod',
    version='1.0',
    long_description=__doc__,
    packages=['pyod'],
    include_package_data=True,
    zip_safe=False,
    install_requires=['pyquery'],
    scripts=['scripts/pyod.py'],
)

