# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

__version__ = '0.2.0'

setup(
    name='cleo',
    license='MIT',
    version=__version__,
    description='Cleo allows you to create beautiful and testable command-line commands.',
    author='Sébastien Eustace',
    author_email='sebastien.eustace@gmail.com',
    url='https://github.com/SDisPater/cleo',
    download_url='https://github.com/SDisPater/cleo/archive/v0.2.0.tar.gz',
    packages=find_packages(),
    install_requires=['nose', 'pylev', 'mock'],
    tests_require=['nose', 'mock'],
    test_suite='nose.collector',
    classifiers=[
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
