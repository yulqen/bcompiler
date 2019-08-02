#!/usr/bin/env python

import os

from setuptools import find_packages, setup

import bcompiler


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
        'bcompiler = bcompiler.main:cli',
        'bcompiler-init = bcompiler.process.bootstrap:main',
    ]},
    setup_requires=['wheel'],
    install_requires=[
        'click',
        'halo',
        'colorama==0.3.9',
        'colorlog',
        'bcompiler-engine @ https://github.com/hammerheadlemon/bcompiler-engine/archive/v0.0.3.zip#egg=bcompiler-engine-0.0.3'

    ],
    test_suite='bcompiler.tests')
