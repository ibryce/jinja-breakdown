#!/usr/bin/env python

from distutils.core import setup

setup(
    # Metadata
    name='breakdown',
    version='0.9.4',
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
    requires=['jinja2 (>=2.6)'],

    # Program data
    scripts=['scripts/breakdown'],
    data_files=[('share/breakdown/img', ['img/sample.png'])],
)
