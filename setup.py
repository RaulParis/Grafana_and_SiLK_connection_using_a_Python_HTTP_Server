#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = ['Click>=6.0', ]

setup_requirements = [ ]

test_requirements = [ ]

setup(
    author="Raúl París Murillo",
    author_email='raul.paris.murillo@gmail.com',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    description="This poject contains all the files you need to establish a connection between Grafana and SiLK. The connection uses the Grafana's JSON Data Source and a Python HTTP Server which is shared in the project files.",
    entry_points={
        'console_scripts': [
            'Grafana_and_SiLK_connection_using_a_Python_HTTP_Server=Grafana_and_SiLK_connection_using_a_Python_HTTP_Server.cli:main',
        ],
    },
    install_requires=requirements,
    license="MIT license",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='Grafana_and_SiLK_connection_using_a_Python_HTTP_Server',
    name='Grafana_and_SiLK_connection_using_a_Python_HTTP_Server',
    packages=find_packages(include=['Grafana_and_SiLK_connection_using_a_Python_HTTP_Server']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/RaulParis/Grafana_and_SiLK_connection_using_a_Python_HTTP_Server',
    version='3.6',
    zip_safe=False,
)
