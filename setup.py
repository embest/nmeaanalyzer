from setuptools import setup

import imp
_version = imp.load_source("nmeaanalyzer._version", "nmeaanalyzer/_version.py")

setup(
    name='nmeaanalyzer',
    version=_version.__version__,
    author='Wayne Guo',
    author_email='wayne.guo@embest.net',
    license='Apache License 2.0',
    url='https://github.com/embest/nmeaanalyzer',

    description='Python library for the NMEA 0183 analyzer',
    packages=['nmeaanalyzer'],
    keywords='python nmea gps analyzer nmea0183 0183',

    install_requires=[
        'pynmea2',
        'matplotlib'
    ],
    
    entry_points = {
        'console_scripts': ['nmeaparse=nmeaanalyzer.parse:main',
                            'nmeaplot=nmeaanalyzer.plot:main'
        ],
    },
    classifiers=[
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Scientific/Engineering :: GIS',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ]
)
