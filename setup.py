from __future__ import print_function

import os
import os.path as op
import sys
from glob import glob

from setuptools import setup


def read(fname):
    return open(op.join(op.dirname(__file__), fname)).read()

metadata = {}
exec(read('codesnip_run/__init__.py'), metadata)

setup(
    name=metadata['__project__'],
    version=metadata['__version__'],
    author="Michael Haberler",
    author_email="micviklui@gmail.com",
    description="Extract and run code snippets from latex code.",
    long_description=read('README.md'),
    classifiers=[],
    license="BSD",
    keywords="test, tex",
    url="https://github.com/micviklui/tex-codesnippet-test",
    packages=[
        'codesnip_run'
    ],
    scripts=[],
    package_data={
        '': ['README.md']
    },
    entry_points={
        'console_scripts': [
            'codesnip_run=codesnip_run.runner:main'
        ]
    },
)
