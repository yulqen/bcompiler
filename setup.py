#!/usr/bin/env python

from setuptools import setup, find_packages
import bcompiler
import os


def read(*names):
    values = dict()
    extensions = ['.txt', '.rst']
    for name in names:
        value = ''
        for extension in extensions:
            filename = name + extension
            if os.path.isfile(filename):
                value = open(name + extension).read()
                break
        values[name] = value
    return values

long_description = """
%(README)s

News
====

%(CHANGES)s

""" % read('README', 'CHANGES')

setup(
    name='bcompiler',
    version=bcompiler.__version__,
    description='Program to migrate data for BICC reporting process.',
    long_description=long_description,
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.2",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Topic :: Documentation",
    ],
    keywords='bcomiler help console command line excel',
    author='Matthew Lemon',
    author_email='matt@matthewlemon.com',
    maintainer='Matthew Lemon',
    maintainer_email='matt@matthewlemon.com',
    url='https://bitbucket.org/mrlemon/bicc_excel',
    license='MIT',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'bcompiler = bcompiler.main:main',
        ]
    },
    install_requires=[
                         'openpyxl',
                         'python-dateutil',
                         'colorlog'
                     ],
    test_suite='bcompiler.tests'
)
