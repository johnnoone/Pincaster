#!/usr/bin/env python

from setuptools import setup

version = '0.0.1'

setup(
    name='pincaster',
    version=version,
    description='Python client for Pincaster',
    long_description='Python client for Pincaster',
    url='http://github.com/johnnoone/Pincaster',
    download_url='http://cloud.github.com/downloads/johnnoone/Pincaster/pincaster-%s.tar.gz' % version,
    author='Xavier Barbosa',
    author_email='clint.northwood@gmail.com',
    maintainer='Xavier Barbosa',
    maintainer_email='clint.northwood@gmail.com',
    keywords=['Pincaster'],
    license='MIT',
    packages=['pincaster'],
    test_suite='tests.all_tests',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python'
    ]
)
