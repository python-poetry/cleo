# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

__version__ = '0.4.0'

setup(
    name='cleo',
    license='MIT',
    version=__version__,
    description='Cleo allows you to create beautiful and testable command-line commands.',
    long_description=open('README.rst').read(),
    author='Sébastien Eustace',
    author_email='sebastien.eustace@gmail.com',
    url='https://github.com/sdispater/cleo',
    download_url='https://github.com/sdispater/cleo/archive/v%s.tar.gz' % __version__,
    packages=find_packages(exclude=["*.tests", "*.tests.*", "tests.*", "tests"]),
    data_files=[('', ['resources/bin/hiddeninput.exe'])],
    install_requires=['pylev', 'psutil'],
    tests_require=['pytest', 'mock'],
    classifiers=[
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
