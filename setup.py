#!/usr/bin/env python

from setuptools import setup

setup(
    # Metadata
    name='breakdown',
    version='0.9.6',
    description='Lightweight jinja2 template prototyping server',
    author='Concentric Sky',
    author_email='jbothun@concentricsky.com',
    classifiers=[
        'Environment :: Console',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python',
        'Framework :: Django',
        'Topic :: Text Processing :: Markup :: HTML'
    ],
    install_requires=['jinja2>=2.6', 'PIL'],

    # Program data
    scripts=['scripts/breakdown'],
    packages=['breakdown'],
    package_data={'breakdown': ['img/*']},
)
