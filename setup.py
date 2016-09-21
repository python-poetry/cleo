# -*- coding: utf-8 -*-

import os
from setuptools import setup, find_packages

__version__ = '0.5.0'

here = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(here, 'requirements.txt')) as f:
    requirements = f.readlines()

setup(
    name='cleo',
    license='MIT',
    version=__version__,
    description='Cleo allows you to create beautiful and testable command-line commands.',
    long_description=open('README.rst').read(),
    author='Sébastien Eustace',
    author_email='sebastien.eustace@gmail.com',
    url='https://github.com/sdispater/cleo',
    download_url='https://github.com/sdispater/cleo/archive/%s.tar.gz' % __version__,
    packages=find_packages(exclude=["*.tests", "*.tests.*", "tests.*", "tests"]),
    package_data={'cleo': ['resources/bin/hiddeninput.exe']},
    install_requires=requirements,
    tests_require=['pytest', 'mock'],
    zip_safe=False,
    classifiers=[
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
