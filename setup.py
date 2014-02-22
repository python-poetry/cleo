# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

__version__ = '0.1.0'

setup(
    name='cleo',
    license='MIT',
    version=__version__,
    description='A Python port of Symfony2 Console Component.',
    author='Sébastien Eustace',
    author_email='sebastien.eustace@gmail.com',
    url='https://github.com/SDisPater/cleo',
    packages=find_packages(),
    install_requires=['nose', 'ordereddict', 'pylev', 'mock'],
    tests_require=['nose', 'mock'],
    test_suite='nose.collector',
    classifiers=[
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
