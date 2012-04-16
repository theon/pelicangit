#!/usr/bin/env python
from setuptools import setup

requires = ['pelican']

try:
    import argparse
except ImportError:
    requires.append('argparse')

entry_points = {
    'console_scripts': [
        'pelicangit = pelicangit:main'
   ]
}

setup(
    name = "pelicangit",
    version = "0.1",
    url = 'http://theon.github.com/pelicangit',
    author = 'Ian Forsey',
    author_email = 'forsey@gmail.com',
    description = "",
    long_description=open('README.rst').read(),
    packages = ['pelicangit'],
    include_package_data = True,
    install_requires = requires,
    entry_points = entry_points,
    classifiers = ['Development Status :: 4 - Beta',
                   'Environment :: Console',
                   'License :: OSI Approved :: GNU Affero General Public License v3',
                   'Operating System :: OS Independent',
                   'Programming Language :: Python :: 2.6',
                   'Programming Language :: Python :: 2.7',
                   'Topic :: Internet :: WWW/HTTP',
                   'Topic :: Software Development :: Libraries :: Python Modules',
                   ],
    data_files=[('/etc/init', ['upstart/pelicangit.conf'])],
)
