"""
MIT License

(C) Copyright [2020-2022] Hewlett Packard Enterprise Development LP

Permission is hereby granted, free of charge, to any person obtaining a
copy of this software and associated documentation files (the "Software"),
to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense,
and/or sell copies of the Software, and to permit persons to whom the
Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included
in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR
OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
OTHER DEALINGS IN THE SOFTWARE.
"""
import subprocess
from os.path import dirname
from os.path import isdir
from os.path import join
from os import devnull
import re

from setuptools import setup
version_re = re.compile('^Version: (.+)$', re.M)

with open('LICENSE') as license_file:
    LICENSE = license_file.read()


def get_version():
    d = dirname(__file__)

    if isdir(join(d, '.git')):
        # Get the version using "git describe".
        cmd = 'git describe --tags --match v[0-9]*'.split()
        try:
            version = subprocess.check_output(cmd).decode().strip()
        except subprocess.CalledProcessError:
            print('Unable to get version number from git tags')
            exit(1)

        # PEP 386 compatibility
        if '-' in version:
            version = '.post'.join(version.split('-')[:2])

        # Don't declare a version "dirty" merely because a time stamp has
        # changed. If it is dirty, append the branch name as a suffix to
        # indicate a development revision after the release.
        with open(devnull, 'w') as fd_devnull:
            subprocess.call(['git', 'status'],
                            stdout=fd_devnull, stderr=fd_devnull)

        cmd = 'git diff-index --name-only HEAD'.split()
        try:
            dirty = subprocess.check_output(cmd).decode().strip()
        except subprocess.CalledProcessError:
            print('Unable to get git index status')
            exit(1)

        if dirty != '':
            version += '.dev1'

    else:
        # Extract the version from the PKG-INFO file.
        with open(join(d, 'PKG-INFO')) as f:
            version = version_re.search(f.read()).group(1)

    return version

setup(
    name='cray',
    author="Hewlett Packard Enterprise LP",
    author_email="eric.lund@hpe.com",
    url="https://cray.com",
    description="Cray management and workflow tool",
    long_description="A tool to help you manage and interact with a cray",
    version=get_version(),
    packages=['cray'],
    license=LICENSE,
    include_package_data=True,
    install_requires=[
        'Click>=7.0,<8.0',
        'boto3>1.20.0,<1.21.0',
        'botocore>1.23.0,<1.24.0'
        'oauthlib==3.0.1',
        'requests-oauthlib==1.3.0',
        'requests-toolbelt==0.9.1',
        'requests>=2.20.0',
        'ruamel.yaml==0.15.89',
        'six>=1.11.0',
        'toml>=0.10.0',
        'websocket-client==0.56.0',
    ],
    extras_require={
        'ci': [
            'nox',
        ],
        'docs': [
            'recommonmark',
            'sphinx',
            'sphinx-click',
            'sphinx-markdown-builder',
        ],
        'lint': [
            'pylint',
        ],
        'test': [
            'mock',
            'names',
            'nox',
            'pytest',
            'pytest-cov',
            'requests-mock',
            'virtualenv',

        ],
    },
    entry_points={
        'console_scripts': [
            'cray=cray.cli:cli',
        ]
    }
)
