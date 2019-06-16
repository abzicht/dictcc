import os
import sys
from setuptools import find_packages, setup
from pathlib import Path

CURRENT_PYTHON = sys.version_info[:2]
REQUIRED_PYTHON = (3, 6)
"""
parts of this setup script are proudly copied from DJANGO
"""
# This check and everything above must remain compatible with Python 2.7.
if CURRENT_PYTHON < REQUIRED_PYTHON:
    sys.stderr.write("""
==========================
Unsupported Python version
==========================
Dictcc requires Python {}.{}, but you're trying to
install it on Python {}.{}.
""".format(*(REQUIRED_PYTHON + CURRENT_PYTHON)))
    sys.exit(1)

def read(fname):
    with open(os.path.join(os.path.dirname(__file__), fname)) as f:
        return f.read()


home = str(Path.home())

setup(
    name='dictcc',
    version="1.0.0",
    python_requires='>={}.{}'.format(*REQUIRED_PYTHON),
    author='Abzicht',
    author_email='abzicht@gmail.com',
    description=('Make queries to https://dict.cc on the console'),
    long_description=read('README.md'),
    license='isc',
    include_package_data=True,
    packages=find_packages(),
    entry_points={'console_scripts': [
       'dictcc = dictcc.dictcc:main',
    ]},
    install_requires=['tabulate', 'bs4'],
)
