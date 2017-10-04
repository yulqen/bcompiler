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
    description='Program to migrate data for DfT BICC reporting process.',
    long_description=long_description,
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "Intended Audience :: Other Audience",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Topic :: Text Processing",
    ],
    keywords='data console commandline excel',
    author='Matthew Lemon',
    author_email='matt@matthewlemon.com',
    maintainer='Matthew Lemon',
    maintainer_email='matt@matthewlemon.com',
    url='https://bitbucket.org/mrlemon/bcompiler',
    license='MIT',
    packages=find_packages(),
    python_requires='>=3.6',
    entry_points={'console_scripts': [
        'bcompiler = bcompiler.main:main',
        'bcompiler-init = bcompiler.process.bootstrap:main',
    ]},
    install_requires=['openpyxl', 'python-dateutil', 'colorlog'],
    test_suite='bcompiler.tests')
