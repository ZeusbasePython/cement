from setuptools import setup, find_packages
import sys, os

# You probably want to change the name, this is a healthy default for paster
setup(name='helloworld_plugin_sayhi',
    version='0.1',
    description='sayhi plugin for helloworld',
    classifiers=[], 
    keywords='',
    author='',
    author_email='',
    url='',
    license='',
    packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        "ConfigObj",
        "Genshi",
        "Cement >=0.7.1, <0.9",
        "helloworld",
        ],
    setup_requires=[
        ],
    test_suite='nose.collector',
    entry_points="""
    """,
    namespace_packages=[
        'helloworld.bootstrap',
        'helloworld.controllers',
        'helloworld.model',
        'helloworld.helpers',
        'helloworld.templates',
        ],
    )