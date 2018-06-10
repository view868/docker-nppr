# -*- coding: utf-8 -*-
import sys

from setuptools import find_packages, setup

setup(
    name='nppr',
    version='0.1.2a',
    description='A nginx/django/postgresql/redis quick deployment tool on docker'
                'Uses docker-compose',
    url='https://github.com/view868/docker-nppr',
    maintainer='view',
    maintainer_email='view868@gmail.com',
    include_package_data=True,
    packages=find_packages(exclude=['tests.py'], include=['nppr']),
    install_requires=[
        'fabric3',
        'PyYAML'
    ],
    platforms=['Any'],
    keywords=['django', 'nginx', 'docker', 'postgresql', 'redis'],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
    ]
)
