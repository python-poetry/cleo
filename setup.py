# -*- coding: utf-8 -*-

import os
from setuptools import setup, find_packages

__version__ = '0.6.1'

here = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(here, 'requirements.txt')) as f:
    requirements = f.readlines()

with open(os.path.join(here, 'requirements.tests.txt')) as f:
    test_requirements = f.readlines()

setup(
    name='cleo',
    license='MIT',
    version=__version__,
    description='Cleo allows you to create beautiful and testable command-line interfaces.',
    long_description=open('README.rst').read(),
    author='Sébastien Eustace',
    author_email='sebastien.eustace@gmail.com',
    url='https://github.com/sdispater/cleo',
    download_url='https://github.com/sdispater/cleo/archive/%s.tar.gz' % __version__,
    packages=find_packages(exclude=["*.tests", "*.tests.*", "tests.*", "tests"]),
    install_requires=requirements,
    tests_require=test_requirements,
    zip_safe=False,
    classifiers=[
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
